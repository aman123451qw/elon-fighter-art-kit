"""All automatic checks. Every check returns (level, message) with level in
PASS / WARN / FAIL. Thresholds are from PLAN.md section 3.
"""

from __future__ import annotations

import numpy as np
from PIL import Image

from . import spec
from .keying import BLACK_ARR, GREEN_ARR, MAGENTA_ARR, closest_expected_key, color_distance, detect_key_color
from .sprites import alpha_bbox

Check = tuple[str, str]

MIN_SHORT_SIDE = 720
MIN_FPS = 20
BG_DISTANCE_OK = 90.0
BLACK_DISTANCE_OK = 24.0  # a glow adds its background to the scene, so black must be near true black
EDGE_WARN_PCT = 1.0
OBJECT_SIZE_WARN_PCT = 20.0
FRINGE_WARN = 2.0
FRINGE_FAIL = 6.0
ZOOM_FAIL_PCT = 10.0
DRIFT_WARN_PCT = 6.0
DRIFT_FAIL_PCT = 12.0
STANCE_RATIO_WARN_PCT = 15.0
LOOP_SEAM_WARN = 18.0
ACTION_START_WARN_SECONDS = 3.0
FX_CENTRE_WARN_PCT = 10.0
REFERENCE_MIN_SIDE = 1024
REFERENCE_MARGIN = 16
PORTRAIT_SIZE = 1254
STAGE_SIZE = (2048, 768)
STAGE_RATIO = 8 / 3

ZOOM_ACTIONS = {"idle", "walk", "block", "hit", "light", "heavy"}
DRIFT_ACTIONS = {"idle", "walk", "light", "heavy", "block", "hit", "special_charge"}
LOOP_ACTIONS = {"idle", "walk"}


# --------------------------------------------------------------- filename --

def check_filename(stem: str) -> Check:
    asset = spec.identify_asset(stem)
    if asset is not None:
        return ("PASS", f"filename '{stem}' recognised as {asset.kind} asset")
    close = spec.suggest_closest(stem)
    suggestion = f", closest match: {close[0]}" if close else ""
    return ("FAIL", f"filename '{stem}' does not match any expected asset{suggestion}")


# ----------------------------------------------------------------- media --

def check_readable(frame_count: int) -> Check:
    if frame_count <= 0:
        return ("FAIL", "clip could not be read / has no frames")
    return ("PASS", f"clip readable ({frame_count} frames)")


def check_resolution(width: int, height: int) -> Check:
    short = min(width, height)
    if short < MIN_SHORT_SIDE:
        return ("WARN", f"resolution {width}x{height}, short side {short}px is under {MIN_SHORT_SIDE}px")
    return ("PASS", f"resolution {width}x{height}")


def check_fps(fps: float) -> Check:
    if fps <= 0:
        return ("WARN", "fps unknown (PNG folder input)")
    if fps < MIN_FPS:
        return ("WARN", f"fps {fps:.1f} is under {MIN_FPS}")
    return ("PASS", f"fps {fps:.1f}")


def check_background(detected: np.ndarray, expected_bg: str) -> Check:
    if expected_bg not in ("green", "magenta", "black"):
        return ("PASS", "background is scene/painted art, not checked for a flat key colour")
    expected_arr = {"green": GREEN_ARR, "magenta": MAGENTA_ARR, "black": BLACK_ARR}[expected_bg]
    if expected_bg == "black" and color_distance(detected, expected_arr) > BLACK_DISTANCE_OK:
        hexval = "#%02x%02x%02x" % tuple(int(max(0, min(255, c))) for c in detected)
        closer, _ = closest_expected_key(detected)
        if closer != "black":
            return ("FAIL", f"background {hexval} looks like {closer}, expected black")
        return ("FAIL", f"background {hexval} is not pure black; grey or tinted black shows as a haze in the game")
    dist = color_distance(detected, expected_arr)
    hexval = "#%02x%02x%02x" % tuple(int(max(0, min(255, c))) for c in detected)
    if dist <= BG_DISTANCE_OK:
        return ("PASS", f"background {hexval} matches expected {expected_bg} key (distance {dist:.0f})")
    closer, _ = closest_expected_key(detected)
    if closer != expected_bg:
        return ("FAIL", f"background {hexval} looks like {closer}, expected {expected_bg}")
    return ("WARN", f"background {hexval} is {dist:.0f} away from the expected {expected_bg} key")


def check_fringe(pct: float) -> Check:
    if pct > FRINGE_FAIL:
        return ("FAIL", f"key fringe {pct:.1f}% of edge pixels (over {FRINGE_FAIL}%)")
    if pct > FRINGE_WARN:
        return ("WARN", f"key fringe {pct:.1f}% of edge pixels (over {FRINGE_WARN}%)")
    return ("PASS", f"key fringe {pct:.1f}% of edge pixels")


def check_body_edge(frames: list[Image.Image], canvas_w: int, canvas_h: int) -> Check:
    touching: list[int] = []
    for i, frame in enumerate(frames):
        bbox = alpha_bbox(np.array(frame))
        if not bbox:
            continue
        x0, y0, x1, y1 = bbox
        if x0 <= 0 or y0 <= 0 or x1 >= canvas_w or y1 >= canvas_h:
            touching.append(i + 1)
    if touching:
        return ("FAIL", f"body touches the frame edge on frame(s) {touching}")
    return ("PASS", "body stays inside the frame on every frame")


def check_zoom(first_height: int, last_height: int, action: str) -> Check:
    if action not in ZOOM_ACTIONS or first_height <= 0:
        return ("PASS", "stance height check not applicable to this action")
    pct = 100.0 * abs(last_height - first_height) / first_height
    if pct > ZOOM_FAIL_PCT:
        return ("FAIL", f"stance height changed {pct:.1f}% first vs last frame (camera zoom?)")
    return ("PASS", f"stance height stable ({pct:.1f}% first vs last frame)")


def check_drift(first_centre_x: float, last_centre_x: float, frame_w: int, action: str) -> Check:
    if action not in DRIFT_ACTIONS or frame_w <= 0:
        return ("PASS", "feet-drift check not applicable to this action")
    pct = 100.0 * abs(last_centre_x - first_centre_x) / frame_w
    if pct > DRIFT_FAIL_PCT:
        return ("FAIL", f"feet drifted {pct:.1f}% of frame width first vs last frame")
    if pct > DRIFT_WARN_PCT:
        return ("WARN", f"feet drifted {pct:.1f}% of frame width first vs last frame")
    return ("PASS", f"feet stayed put ({pct:.1f}% drift)")


def check_stance_ratio(body_height: int, frame_height: int, reference_ratio: float | None) -> Check:
    if reference_ratio is None:
        return ("PASS", "no reference yet to compare stance size against")
    ratio = body_height / frame_height
    pct = 100.0 * abs(ratio - reference_ratio) / reference_ratio
    if pct > STANCE_RATIO_WARN_PCT:
        return ("WARN", f"stance size {pct:.1f}% different from the reference ({ratio:.3f} vs {reference_ratio:.3f})")
    return ("PASS", f"stance size within {pct:.1f}% of the reference")


def check_action_detected(window: tuple[int, int] | None) -> Check:
    if window is None:
        return ("FAIL", "no action detected (silhouette never differs from frame 1)")
    return ("PASS", f"action window frames {window[0] + 1}-{window[1] + 1}")


def check_loop_seam(diff_value: float | None, action: str) -> Check:
    if action not in LOOP_ACTIONS or diff_value is None:
        return ("PASS", "loop seam check not applicable")
    if diff_value > LOOP_SEAM_WARN:
        return ("WARN", f"loop seam diff {diff_value:.1f} between first and last selected frame")
    return ("PASS", f"loop seam diff {diff_value:.1f}")


def check_action_start(start_index: int | None, fps: float) -> Check:
    if start_index is None or fps <= 0:
        return ("PASS", "action start time not applicable")
    seconds = start_index / fps
    if seconds > ACTION_START_WARN_SECONDS:
        return ("WARN", f"action starts at {seconds:.1f}s (after {ACTION_START_WARN_SECONDS}s)")
    return ("PASS", f"action starts at {seconds:.1f}s")


def check_fx_centre_drift(centres: list[tuple[float, float]], frame_w: int, frame_h: int) -> Check:
    if len(centres) < 2:
        return ("PASS", "fx centre check not applicable")
    diag = max(frame_w, frame_h)
    xs = [c[0] for c in centres]
    ys = [c[1] for c in centres]
    spread = max(max(xs) - min(xs), max(ys) - min(ys))
    pct = 100.0 * spread / diag
    if pct > FX_CENTRE_WARN_PCT:
        return ("WARN", f"fx object centre moves {pct:.1f}% of the frame")
    return ("PASS", f"fx object stays centred ({pct:.1f}% movement)")


# ------------------------------------------------------------- still art --

def check_lineup_size(width: int, height: int) -> Check:
    if min(width, height) < REFERENCE_MIN_SIDE:
        return ("WARN", f"lineup is {width}x{height}, under {REFERENCE_MIN_SIDE}px short side")
    return ("PASS", f"lineup is {width}x{height}")


def check_reference_size(width: int, height: int) -> Check:
    if min(width, height) < REFERENCE_MIN_SIDE:
        return ("WARN", f"reference is {width}x{height}, under {REFERENCE_MIN_SIDE}px short side")
    return ("PASS", f"reference is {width}x{height}")


def check_flat_background(rgb: np.ndarray, expected_bg: str) -> Check:
    detected = detect_key_color(rgb)
    return check_background(detected, expected_bg)


def check_margin(rgba: np.ndarray, margin: int = REFERENCE_MARGIN) -> Check:
    bbox = alpha_bbox(rgba)
    if not bbox:
        return ("FAIL", "nothing detected against the background")
    h, w = rgba.shape[:2]
    x0, y0, x1, y1 = bbox
    if x0 < margin or y0 < margin or x1 > w - margin or y1 > h - margin:
        return ("WARN", f"body is within {margin}px of the frame edge, add margin")
    return ("PASS", "body is fully inside the frame with margin")


def check_portrait_size(width: int, height: int) -> Check:
    if width != height:
        return ("FAIL", f"portrait {width}x{height} is not square")
    if width != PORTRAIT_SIZE:
        return ("WARN", f"portrait is {width}x{width}, expected {PORTRAIT_SIZE}x{PORTRAIT_SIZE}")
    return ("PASS", f"portrait is {PORTRAIT_SIZE}x{PORTRAIT_SIZE}")


def check_portrait_not_flat(rgb: np.ndarray) -> Check:
    h, w = rgb.shape[:2]
    s = max(4, min(h, w) // 20)
    patches = [rgb[:s, :s], rgb[:s, -s:], rgb[-s:, :s], rgb[-s:, -s:]]
    pixels = np.concatenate([p.reshape(-1, 3) for p in patches])
    std = float(np.std(pixels))
    detected = np.median(pixels, axis=0)
    closer, dist = closest_expected_key(detected)
    # Dark painted backgrounds (Elon's charcoal) are fine: only a green or magenta screen fails.
    if std < 6.0 and dist < 40.0 and closer != "black":
        return ("FAIL", f"portrait corners look like a flat {closer} screen, not painted art")
    return ("PASS", "portrait corners are painted, not a flat chroma colour")


def check_stage_size(width: int, height: int) -> Check:
    if (width, height) == STAGE_SIZE:
        return ("PASS", f"stage is {width}x{height}")
    ratio = width / height if height else 0
    if abs(ratio - STAGE_RATIO) < 0.05:
        return ("WARN", f"stage is {width}x{height} (8:3 but not exactly {STAGE_SIZE[0]}x{STAGE_SIZE[1]})")
    return ("FAIL", f"stage is {width}x{height}, not an 8:3 ratio")


MENU_TARGET_SIZES: dict[str, tuple[int, int]] = {
    "logo": (1600, 600),
    "title": (1920, 1080),
}


def check_menu_size(name: str, width: int, height: int) -> Check:
    target = MENU_TARGET_SIZES.get(name, (1330, 1182))
    tw, th = target
    if (width, height) == target:
        return ("PASS", f"{name} is {width}x{height}")
    pct = 100.0 * max(abs(width - tw) / tw, abs(height - th) / th)
    if pct <= 10.0:
        return ("WARN", f"{name} is {width}x{height}, expected {tw}x{th}")
    return ("FAIL", f"{name} is {width}x{height}, expected {tw}x{th}")


# ------------------------------------------------ part 2: glow and objects --

def check_edge_clear(frames_rgba: list[np.ndarray], allowed: tuple[str, ...] = ()) -> Check:
    """Glow and objects must stay inside the frame. Reports the edges the effect
    touches (more than EDGE_WARN_PCT of that edge lit on some frame), ignoring
    edges a beam or trail is allowed to run to.
    """
    touched: set[str] = set()
    for f in frames_rgba:
        vis = f[..., 3] > 32
        edges = {"top": vis[0, :], "bottom": vis[-1, :], "left": vis[:, 0], "right": vis[:, -1]}
        for name, line in edges.items():
            if name not in allowed and 100.0 * line.mean() > EDGE_WARN_PCT:
                touched.add(name)
    if touched:
        return ("WARN", f"effect touches the frame edge ({', '.join(sorted(touched))}); it will look cut off in the game")
    return ("PASS", "effect stays inside the frame")


def check_object_size(fill: tuple[float, float], reference_fill: tuple[float, float] | None, axis: str) -> Check:
    """Clip vs its approved reference: how much of the frame the object fills along
    its main axis. A big change means the tool zoomed or redrew it.
    """
    if reference_fill is None:
        return ("PASS", "no reference yet to compare the object size against")
    i = 0 if axis == "width" else 1
    ref = reference_fill[i]
    if ref <= 0:
        return ("PASS", "object size check not applicable")
    pct = 100.0 * abs(fill[i] - ref) / ref
    if pct > OBJECT_SIZE_WARN_PCT:
        return ("WARN", f"object {axis} fills {fill[i]:.0%} of the frame vs {ref:.0%} in the reference ({pct:.0f}% different)")
    return ("PASS", f"object size within {pct:.0f}% of the reference")
