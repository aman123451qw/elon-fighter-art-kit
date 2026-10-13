"""Action window detection, frame selection, stance-based normalisation,
jump feet pinning, frame widening, the pixel pass, sheet packing, preview
GIF and contact sheet.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from PIL import Image, ImageDraw

from .spec import FrameTarget

FRAME = 256
COLUMNS = 5
STANCE_HEIGHT = 204
FEET_Y = 232
CANVAS_WIDTHS = (256, 320, 384)

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
    """First index >= start where consecutive-frame silhouette diff goes small (motion stops)."""
    last = len(frames_rgba) - 1
    for i in range(start + 1, len(frames_rgba)):
        d = diff_fraction(silhouette(frames_rgba[i]), silhouette(frames_rgba[i - 1]))
        if d <= diff_thresh:
            return i
    return last


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
    frames_rgba: list[np.ndarray], stance: Stance, pin_feet: bool = False, frame_h: int = FRAME
) -> tuple[list[Image.Image], int, list[str]]:
    """Scale every frame by the stance transform (stance height -> 204px) and
    place it on a shared canvas (centred on the stance centre, feet at y=232).
    One shared horizontal placement for the whole clip; pin_feet (jump) uses a
    per-frame vertical placement instead. Returns (frames, canvas_width, warnings).
    """
    warnings: list[str] = []
    scale = STANCE_HEIGHT / max(stance.body_height, 1)
    resized = [_resize_scale(Image.fromarray(f, "RGBA"), scale) for f in frames_rgba]
    stance_centre_resized = stance.centre_x * scale
    stance_feet_resized = stance.feet_y * scale

    bboxes = [alpha_bbox(np.array(img)) for img in resized]

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
        warnings.append("WARN: motion is wider than 384px even widened; frames clip horizontally")

    ox = round(canvas_w / 2.0 - stance_centre_resized)

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
    for img, oy, bbox in zip(resized, oy_per_frame, bboxes):
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

def pixel_pass(frames: list[Image.Image], palette_colors: int = 48) -> list[Image.Image]:
    """Downscale x2 (box filter), one shared no-dither palette across every
    frame of the clip, upscale x2 nearest-neighbour, binary alpha (>=128).
    """
    if not frames:
        return frames
    w, h = frames[0].size
    down_w, down_h = max(1, w // 2), max(1, h // 2)
    downscaled = [f.resize((down_w, down_h), Image.BOX) for f in frames]

    combo = Image.new("RGB", (down_w * len(downscaled), down_h))
    for i, f in enumerate(downscaled):
        rgb = Image.new("RGB", f.size, (0, 0, 0))
        rgb.paste(f, (0, 0), f)
        combo.paste(rgb, (i * down_w, 0))
    pal_source = combo.quantize(colors=palette_colors, method=Image.MEDIANCUT, dither=Image.Dither.NONE)
    shared_palette = pal_source.getpalette()

    out: list[Image.Image] = []
    for f in downscaled:
        rgb = Image.new("RGB", f.size, (0, 0, 0))
        rgb.paste(f, (0, 0), f)
        alpha = f.split()[3]

        pal_img = Image.new("P", (1, 1))
        pal_img.putpalette(shared_palette)
        quantized = rgb.quantize(palette=pal_img, dither=Image.Dither.NONE).convert("RGB")

        up_rgb = quantized.resize((w, h), Image.NEAREST)
        up_alpha = alpha.resize((w, h), Image.NEAREST).point(lambda a: 255 if a >= 128 else 0)

        result = Image.new("RGBA", (w, h))
        result.paste(up_rgb, (0, 0))
        result.putalpha(up_alpha)
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
