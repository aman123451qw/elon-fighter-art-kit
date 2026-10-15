"""Action window detection, frame selection, stance-based normalisation,
jump feet pinning, frame widening, the pixel pass, sheet packing, preview
GIF and contact sheet.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw

from .spec import FrameTarget

# Sheets are drawn 1:1 on the 1280x720 screen (fighter scale 1.0), so the stance
# height here IS the on-screen height. Old template sheets were 256 px frames
# shown at 1.4x; these are 1.40625x those numbers with no runtime upscaling.
FRAME = 360
COLUMNS = 5
STANCE_HEIGHT = 287
FEET_Y = 326
CANVAS_WIDTHS = (360, 450, 540, 630, 720)  # wide ones are for knockdowns lying flat

ALPHA_OPAQUE = 32  # alpha above this counts as "visible" for bbox/measurement


def alpha_bbox(rgba: np.ndarray, threshold: int = ALPHA_OPAQUE) -> tuple[int, int, int, int] | None:
    """(x0, y0, x1, y1) of opaque pixels, x1/y1 exclusive. None if nothing is opaque."""
    ys, xs = np.nonzero(rgba[..., 3] > threshold)
    if len(xs) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1


# ---------------------------------------------------------------- stance --

@dataclass(frozen=True)
class Stance:
    """Measurements taken from a fighter's standing frame (reference or clip frame 0)."""

    body_height: int
    feet_y: int
    centre_x: float
    image_width: int
    image_height: int

    def to_dict(self) -> dict:
        return {
            "bodyHeight": self.body_height,
            "feetY": self.feet_y,
            "centreX": self.centre_x,
            "imageWidth": self.image_width,
            "imageHeight": self.image_height,
        }

    @staticmethod
    def from_dict(d: dict) -> "Stance":
        return Stance(d["bodyHeight"], d["feetY"], d["centreX"], d["imageWidth"], d["imageHeight"])


def measure_stance(rgba: np.ndarray) -> Stance | None:
    bbox = alpha_bbox(rgba)
    if not bbox:
        return None
    x0, y0, x1, y1 = bbox
    h, w = rgba.shape[:2]
    return Stance(body_height=y1 - y0, feet_y=y1, centre_x=(x0 + x1) / 2.0, image_width=w, image_height=h)


# ------------------------------------------------------ silhouette timing --

def silhouette(rgba: np.ndarray, threshold: int = ALPHA_OPAQUE) -> np.ndarray:
    return rgba[..., 3] > threshold


def diff_fraction(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.count_nonzero(a != b)) / a.size


def action_window(
    frames_rgba: list[np.ndarray], pad: int = 1, diff_thresh: float = 0.015
) -> tuple[int, int] | None:
    """Frames whose silhouette differs from frame 0, plus `pad` frames each side."""
    if not frames_rgba:
        return None
    base = silhouette(frames_rgba[0])
    diffs = [diff_fraction(silhouette(f), base) for f in frames_rgba]
    active = [i for i, d in enumerate(diffs) if d > diff_thresh]
    if not active:
        return None
    start = max(0, min(active) - pad)
    end = min(len(frames_rgba) - 1, max(active) + pad)
    return start, end


def settle_point(frames_rgba: list[np.ndarray], start: int, diff_thresh: float = 0.01) -> int:
    """Index where the clip reaches its final held pose: the start of the run of
    frames, ending at the last frame, that all match the last frame.

    Comparing neighbouring frames instead stops at the first slow moment (a fall
    that starts slowly looked "settled" after 2 frames), so compare to the end pose.
    """
    last = len(frames_rgba) - 1
    end_pose = silhouette(frames_rgba[last])
    settled = last
    for i in range(last - 1, start, -1):
        if diff_fraction(silhouette(frames_rgba[i]), end_pose) > diff_thresh:
            break
        settled = i
    return max(settled, min(start + 1, last))


def evenly_spaced(start: int, end: int, count: int) -> list[int]:
    if count <= 0:
        return []
    if count == 1 or end <= start:
        return [start] * count
    return [round(start + i * (end - start) / (count - 1)) for i in range(count)]


def select_frames(
    frames_rgba: list[np.ndarray], target: FrameTarget, fps: float
) -> tuple[list[int], tuple[int, int] | None]:
    """Pick which source frame indices go into the final sheet.

    Returns (indices, window). window is the (start, end) action window used,
    or None for a loop (there is no "action window" for a loop, and no
    action-detected / action-start check applies).
    """
    n = len(frames_rgba)
    if target.mode == "loop":
        window_fps = fps if fps > 0 else 24.0
        window_frames = max(1, round((target.window_seconds or 1.0) * window_fps))
        end = min(n - 1, window_frames - 1)
        return evenly_spaced(0, end, target.frames), None

    window = action_window(frames_rgba)
    if window is None:
        return [], None
    start, end = window

    if target.mode == "hold":
        end = settle_point(frames_rgba, start)

    return evenly_spaced(start, end, target.frames), (start, end)


# --------------------------------------------------------- normalisation --

def _resize_scale(img: Image.Image, scale: float) -> Image.Image:
    w = max(1, round(img.width * scale))
    h = max(1, round(img.height * scale))
    return img.resize((w, h), Image.LANCZOS)


def normalize_clip(
    frames_rgba: list[np.ndarray],
    stance: Stance,
    pin_feet: bool = False,
    frame_h: int = FRAME,
    target_height: float = STANCE_HEIGHT,
    pin_centre: bool = False,
) -> tuple[list[Image.Image], int, list[str]]:
    """Scale every frame by the stance transform (stance height -> target_height,
    STANCE_HEIGHT x the fighter's height ratio) and place it on a shared canvas
    (centred on the stance centre, feet at FEET_Y).
    One shared horizontal placement for the whole clip; pin_feet (jump) uses a
    per-frame vertical placement instead, and pin_centre (knockdown) centres each
    frame horizontally so a fall that drifts backward lands on the spot (the game
    adds its own knockback). Returns (frames, canvas_width, warnings).
    """
    warnings: list[str] = []
    scale = target_height / max(stance.body_height, 1)
    resized = [_resize_scale(Image.fromarray(f, "RGBA"), scale) for f in frames_rgba]
    stance_centre_resized = stance.centre_x * scale
    stance_feet_resized = stance.feet_y * scale

    bboxes = [alpha_bbox(np.array(img)) for img in resized]

    if pin_centre:
        widest = max((b[2] - b[0] for b in bboxes if b), default=0)
        canvas_w = next((c for c in CANVAS_WIDTHS if c >= widest), CANVAS_WIDTHS[-1])
        if widest > canvas_w:
            warnings.append(f"WARN: motion is wider than {CANVAS_WIDTHS[-1]}px even widened; frames clip horizontally")
        ox_per_frame = [
            round(canvas_w / 2.0 - ((b[0] + b[2]) / 2.0 if b else stance_centre_resized)) for b in bboxes
        ]
    else:
        canvas_w = CANVAS_WIDTHS[-1]
        for candidate in CANVAS_WIDTHS:
            ox = candidate / 2.0 - stance_centre_resized
            fits = True
            for bbox in bboxes:
                if not bbox:
                    continue
                x0, _, x1, _ = bbox
                if x0 + ox < 0 or x1 + ox > candidate:
                    fits = False
                    break
            if fits:
                canvas_w = candidate
                break
        else:
            warnings.append(f"WARN: motion is wider than {CANVAS_WIDTHS[-1]}px even widened; frames clip horizontally")
        ox_per_frame = [round(canvas_w / 2.0 - stance_centre_resized)] * len(resized)

    if pin_feet:
        oy_per_frame = []
        for img in resized:
            bbox = alpha_bbox(np.array(img))
            lowest = bbox[3] if bbox else round(stance_feet_resized)
            oy_per_frame.append(FEET_Y - lowest)
    else:
        oy = round(FEET_Y - stance_feet_resized)
        oy_per_frame = [oy] * len(resized)

    placed: list[Image.Image] = []
    clipped_vertically = False
    for img, ox, oy, bbox in zip(resized, ox_per_frame, oy_per_frame, bboxes):
        canvas = Image.new("RGBA", (canvas_w, frame_h), (0, 0, 0, 0))
        canvas.paste(img, (ox, oy), img)
        placed.append(canvas)
        if bbox:
            x0, y0, x1, y1 = bbox
            if y0 + oy < 0 or y1 + oy > frame_h:
                clipped_vertically = True
    if clipped_vertically:
        warnings.append("WARN: body clips the top/bottom of the frame")

    return placed, canvas_w, warnings


def crop_union(frames_rgba: list[np.ndarray], pad: int = 4) -> tuple[list[Image.Image], tuple[int, int]]:
    """For fx: crop every frame to one shared box (union of all bboxes, padded)
    so the object doesn't jitter or resize between frames. No stance scaling.
    """
    boxes = [b for b in (alpha_bbox(f) for f in frames_rgba) if b]
    if not boxes:
        raise ValueError("every frame was keyed out entirely - nothing to crop")
    x0 = max(0, min(b[0] for b in boxes) - pad)
    y0 = max(0, min(b[1] for b in boxes) - pad)
    x1 = min(frames_rgba[0].shape[1], max(b[2] for b in boxes) + pad)
    y1 = min(frames_rgba[0].shape[0], max(b[3] for b in boxes) + pad)
    out = [Image.fromarray(f[y0:y1, x0:x1], "RGBA") for f in frames_rgba]
    return out, (x1 - x0, y1 - y0)


# --------------------------------------------------------------- pixel pass --

def pixel_pass(frames: list[Image.Image], palette_colors: int = 96) -> list[Image.Image]:
    """One shared no-dither palette across every frame of the clip (so colours
    don't flicker between frames) and binary alpha (>=128). Frames stay at full
    resolution: the source art is already pixel art, and halving it lost faces.
    """
    if not frames:
        return frames
    w, h = frames[0].size

    combo = Image.new("RGB", (w * len(frames), h))
    for i, f in enumerate(frames):
        rgb = Image.new("RGB", f.size, (0, 0, 0))
        rgb.paste(f, (0, 0), f)
        combo.paste(rgb, (i * w, 0))
    pal_source = combo.quantize(colors=palette_colors, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
    shared_palette = pal_source.getpalette()

    out: list[Image.Image] = []
    for f in frames:
        rgb = Image.new("RGB", f.size, (0, 0, 0))
        rgb.paste(f, (0, 0), f)
        alpha = f.split()[3].point(lambda a: 255 if a >= 128 else 0)

        pal_img = Image.new("P", (1, 1))
        pal_img.putpalette(shared_palette)
        quantized = rgb.quantize(palette=pal_img, dither=Image.Dither.NONE).convert("RGB")

        result = Image.new("RGBA", (w, h))
        result.paste(quantized, (0, 0))
        result.putalpha(alpha)
        out.append(result)
    return out


# ------------------------------------------------------------- sheet / gif --

def pack_sheet(frames: list[Image.Image], columns: int = COLUMNS) -> Image.Image:
    if not frames:
        raise ValueError("no frames to pack")
    fw, fh = frames[0].size
    rows = (len(frames) + columns - 1) // columns
    sheet = Image.new("RGBA", (columns * fw, rows * fh), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        sheet.alpha_composite(f, ((i % columns) * fw, (i // columns) * fh))
    return sheet


def unpack_sheet(sheet: Image.Image, frame_w: int, frame_h: int, columns: int = COLUMNS) -> list[Image.Image]:
    """Split a sheet back into frames, reading left-to-right then top-to-bottom,
    stopping as soon as a cell is fully transparent (used by `standins`).
    """
    rows = sheet.height // frame_h
    frames = []
    for r in range(rows):
        for c in range(columns):
            box = (c * frame_w, r * frame_h, (c + 1) * frame_w, (r + 1) * frame_h)
            cell = sheet.crop(box)
            if not np.array(cell)[..., 3].any():
                return frames
            frames.append(cell)
    return frames


def save_preview_gif(frames: list[Image.Image], dest, fps: int, bg=(40, 40, 48, 255)) -> None:
    composited = [Image.alpha_composite(Image.new("RGBA", f.size, bg), f).convert("P") for f in frames]
    duration = max(20, round(1000 / max(fps, 1)))
    composited[0].save(dest, save_all=True, append_images=composited[1:], duration=duration, loop=0)


def save_contact_sheet(all_frames: list[np.ndarray], chosen: list[int], dest, thumb: int = 160) -> None:
    """Every source frame, numbered, with the chosen ones highlighted."""
    cols = 10
    rows = (len(all_frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * thumb, rows * (thumb + 18)), (30, 30, 30))
    draw = ImageDraw.Draw(sheet)
    chosen_set = set(chosen)
    for i, frame in enumerate(all_frames):
        im = Image.fromarray(frame).convert("RGB") if isinstance(frame, np.ndarray) else frame.convert("RGB")
        im = im.copy()
        im.thumbnail((thumb, thumb))
        x, y = (i % cols) * thumb, (i // cols) * (thumb + 18)
        sheet.paste(im, (x, y + 18))
        color = (120, 255, 120) if i in chosen_set else (255, 220, 0)
        draw.text((x + 4, y + 3), str(i + 1), fill=color)
        if i in chosen_set:
            draw.rectangle([x, y + 18, x + im.width - 1, y + 18 + im.height - 1], outline=(120, 255, 120), width=3)
    sheet.save(dest)


def loop_seam_diff(first: Image.Image, last: Image.Image) -> float:
    """Mean abs RGB diff (0-255 scale) between a loop's first and last selected frame."""
    a = np.array(first.convert("RGB"), dtype=np.float32)
    b = np.array(last.convert("RGB"), dtype=np.float32)
    return float(np.mean(np.abs(a - b)))


# ------------------------------------------------- lettering-safe mirroring --

def lettering_box(rgba: np.ndarray, gap: int = 8, min_width: int = 20) -> tuple[int, int, int, int] | None:
    """(x0, y0, x1, y1), inclusive, of the dark lettering painted on a light body
    (e.g. SPACEX on the rocket): the widest run of columns holding dark pixels
    inside the rows where the light body is widest. None if there is none.
    """
    a = rgba[..., 3] > 0
    rgb = rgba[..., :3].astype(int)
    light = a & (rgb.min(axis=2) > 200)
    counts = light.sum(axis=1)
    if counts.max() == 0:
        return None
    body_rows = np.where(counts > 0.3 * counts.max())[0]
    top, bottom = int(body_rows.min()) + 5, int(body_rows.max()) - 5
    if bottom <= top:
        return None
    # Lettering is near-black; seams and rings are mid-grey (77+ on the rocket).
    dark = a & (rgb.max(axis=2) < 60)
    band = dark[top:bottom + 1]
    # Seams and rings run the full height of the body; letters do not.
    lettered = band.any(axis=0) & (band.mean(axis=0) < 0.85)
    cols = np.where(lettered)[0]
    if len(cols) == 0:
        return None
    runs, start, prev = [], cols[0], cols[0]
    for c in cols[1:]:
        if c - prev > gap:
            runs.append((start, prev))
            start = c
        prev = c
    runs.append((start, prev))
    x0, x1 = max(runs, key=lambda r: r[1] - r[0])
    if x1 - x0 + 1 < min_width:
        return None
    # Rows: over the whole body height, so letter tops and bottoms are included.
    body_top, body_bottom = int(body_rows.min()), int(body_rows.max())
    rows = np.where(dark[body_top:body_bottom + 1, x0:x1 + 1].any(axis=1))[0]
    return int(x0), int(body_top + rows.min()), int(x1), int(body_top + rows.max())


def mirror_keep_lettering(frames: list[Image.Image]) -> list[Image.Image]:
    """Mirror frames left-right (an effect flying the other way) but flip the
    lettering back so it still reads correctly. The box comes from frame 0.
    """
    if not frames:
        return frames
    box = lettering_box(np.array(frames[0]))
    out = []
    for f in frames:
        arr = np.array(f)[:, ::-1].copy()
        if box:
            w = arr.shape[1]
            x0, y0, x1, y1 = box
            mx0, mx1 = w - 1 - x1, w - 1 - x0
            arr[y0:y1 + 1, mx0:mx1 + 1] = arr[y0:y1 + 1, mx0:mx1 + 1][:, ::-1]
        out.append(Image.fromarray(arr, "RGBA"))
    return out
