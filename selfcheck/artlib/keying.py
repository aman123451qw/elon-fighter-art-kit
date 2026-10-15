"""Chroma key detection and removal (green or magenta screen), with spill
suppression on the feathered edge, plus the fringe quality metric.
"""

from __future__ import annotations

import colorsys

import numpy as np

from .spec import BLACK, GREEN, MAGENTA

GREEN_ARR = np.array(GREEN, dtype=np.float32)
MAGENTA_ARR = np.array(MAGENTA, dtype=np.float32)
BLACK_ARR = np.array(BLACK, dtype=np.float32)

# Glow on black: a pixel brighter than this (max channel) is part of the effect.
BLACK_THRESHOLD = 14


def detect_key_color(rgb: np.ndarray) -> np.ndarray:
    """Median colour of the four corner patches of a frame = the screen colour."""
    h, w = rgb.shape[:2]
    s = max(4, min(h, w) // 20)
    patches = [rgb[:s, :s], rgb[:s, -s:], rgb[-s:, :s], rgb[-s:, -s:]]
    return np.median(np.concatenate([p.reshape(-1, 3) for p in patches]), axis=0)


def color_distance(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a.astype(np.float32) - b.astype(np.float32)))


def closest_expected_key(detected: np.ndarray) -> tuple[str, float]:
    """Which of green/magenta/black the detected colour is nearest to, and the distance."""
    options = [
        ("green", color_distance(detected, GREEN_ARR)),
        ("magenta", color_distance(detected, MAGENTA_ARR)),
        ("black", color_distance(detected, BLACK_ARR)),
    ]
    return min(options, key=lambda o: o[1])


def black_key(rgb: np.ndarray, threshold: int = BLACK_THRESHOLD) -> np.ndarray:
    """RGBA for a glow made on pure black. The game draws these additively, so
    the colour is kept as is (black adds nothing); alpha only marks where the
    effect is, for cropping and frame selection.
    """
    bright = rgb.max(axis=2) > threshold
    alpha = np.where(bright, 255, 0).astype(np.uint8)
    return np.dstack([rgb.astype(np.uint8), alpha])


def key_frame(rgb: np.ndarray, background: str) -> np.ndarray:
    """Key one frame by the asset's background: black glow or a green/magenta screen."""
    if background == "black":
        return black_key(rgb)
    return chroma_key(rgb, detect_key_color(rgb))


SPILL_BAND_PX = 3


def _near_transparent(alpha: np.ndarray, radius: int) -> np.ndarray:
    """True for pixels within `radius` px (4-neighbour steps) of a mostly transparent pixel."""
    near = alpha < 0.5
    grown = near.copy()
    for _ in range(radius):
        step = grown.copy()
        step[1:, :] |= grown[:-1, :]
        step[:-1, :] |= grown[1:, :]
        step[:, 1:] |= grown[:, :-1]
        step[:, :-1] |= grown[:, 1:]
        grown = step
    return grown


def chroma_key(rgb: np.ndarray, key: np.ndarray, tol: float = 70.0, soft: float = 40.0) -> np.ndarray:
    """Return RGBA with the key colour removed and spill suppressed at the edge."""
    rgbf = rgb.astype(np.float32)
    dist = np.linalg.norm(rgbf - key.astype(np.float32), axis=2)
    alpha = np.clip((dist - tol) / max(soft, 1e-3), 0.0, 1.0)

    # Spill lives in a band around the silhouette, not only in soft pixels:
    # video compression bleeds the screen colour into solid outline pixels too.
    # The brief bans the key colour in outfits and props, so the band is safe.
    edge = (alpha < 1) | _near_transparent(alpha, SPILL_BAND_PX)
    r, g, b = rgbf[..., 0], rgbf[..., 1], rgbf[..., 2]
    if key[1] >= max(key[0], key[2]):  # green screen
        rgbf[..., 1] = np.where(edge, np.minimum(g, np.maximum(r, b)), g)
    else:  # magenta screen
        cap = np.maximum(g, np.minimum(r, b) * 0.6)
        rgbf[..., 0] = np.where(edge, np.minimum(r, cap + 30), r)
        rgbf[..., 2] = np.where(edge, np.minimum(b, cap + 30), b)

    out = np.dstack([np.clip(rgbf, 0, 255), alpha * 255]).astype(np.uint8)
    out[..., 3][out[..., 3] < 24] = 0  # drop isolated speckles
    return out


def fringe_percent(rgba: np.ndarray, key: np.ndarray) -> float:
    """% of opaque edge pixels whose hue is within 25deg of the key hue and sat > 0.4."""
    alpha = rgba[..., 3]
    opaque = alpha > 200
    if not opaque.any():
        return 0.0

    up = np.roll(alpha, 1, axis=0); up[0, :] = 255
    down = np.roll(alpha, -1, axis=0); down[-1, :] = 255
    left = np.roll(alpha, 1, axis=1); left[:, 0] = 255
    right = np.roll(alpha, -1, axis=1); right[:, -1] = 255
    touches_transparent = (up <= 24) | (down <= 24) | (left <= 24) | (right <= 24)
    edge = opaque & touches_transparent
    n_edge = int(edge.sum())
    if n_edge == 0:
        return 0.0

    rgb = rgba[..., :3].astype(np.float32) / 255.0
    mx = rgb.max(axis=2)
    mn = rgb.min(axis=2)
    diff = mx - mn
    sat = np.where(mx > 0, diff / np.where(mx == 0, 1, mx), 0.0)

    r, g, b = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    hue = np.zeros_like(mx)
    has_color = diff > 1e-6
    is_r = has_color & (mx == r)
    is_g = has_color & (mx == g) & ~is_r
    is_b = has_color & (mx == b) & ~is_r & ~is_g
    safe = np.where(diff == 0, 1, diff)
    hue[is_r] = ((g[is_r] - b[is_r]) / safe[is_r]) % 6
    hue[is_g] = (b[is_g] - r[is_g]) / safe[is_g] + 2
    hue[is_b] = (r[is_b] - g[is_b]) / safe[is_b] + 4
    hue *= 60.0

    key_h, _, _ = colorsys.rgb_to_hsv(*(key.astype(np.float32) / 255.0))
    key_hue_deg = key_h * 360.0
    hue_diff = np.abs(hue - key_hue_deg)
    hue_diff = np.minimum(hue_diff, 360.0 - hue_diff)

    fringe = edge & (hue_diff <= 25.0) & (sat > 0.4)
    return 100.0 * float(fringe.sum()) / n_edge


def key_tint_fraction(rgba: np.ndarray, key: np.ndarray) -> float:
    """Fraction of opaque pixels whose colour has drifted toward the key colour.

    Effects that fade out in the video fade INTO the screen colour (money notes
    turn pink on magenta), so late frames are mostly key-tinted and must be dropped.
    """
    opaque = rgba[..., 3] > 128
    if not opaque.any():
        return 1.0
    rgb = rgba[..., :3][opaque].astype(np.float32) / 255.0
    mx, mn = rgb.max(axis=1), rgb.min(axis=1)
    diff = mx - mn
    sat = np.where(mx > 0, diff / np.maximum(mx, 1e-6), 0.0)
    r, g, b = rgb[:, 0], rgb[:, 1], rgb[:, 2]
    safe = np.maximum(diff, 1e-6)
    hue = np.where(mx == r, ((g - b) / safe) % 6, np.where(mx == g, (b - r) / safe + 2, (r - g) / safe + 4)) * 60.0
    key_h, _, _ = colorsys.rgb_to_hsv(*(key.astype(np.float32) / 255.0))
    hue_diff = np.abs(hue - key_h * 360.0)
    hue_diff = np.minimum(hue_diff, 360.0 - hue_diff)
    tinted = (hue_diff <= 60.0) & (sat > 0.35) & (diff > 0.08)
    return float(tinted.mean())


def median_hue(rgba: np.ndarray) -> float | None:
    """Hue (degrees) of the median colour of the opaque pixels, or None if empty."""
    opaque = rgba[..., 3] > 128
    if not opaque.any():
        return None
    r, g, b = (np.median(rgba[..., :3][opaque], axis=0) / 255.0).tolist()
    h, _, _ = colorsys.rgb_to_hsv(r, g, b)
    return h * 360.0


def hue_distance(a: float, b: float) -> float:
    d = abs(a - b) % 360.0
    return min(d, 360.0 - d)
