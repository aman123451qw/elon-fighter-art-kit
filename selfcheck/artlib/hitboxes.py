"""Auto per-frame hitboxes: visual, hit (hurtbox), collision, attack, guard.
All boxes are [x, y, w, h] in frame pixels, origin top-left. These are first
guesses; hand overrides live in public/configs/character-gym.json later.
"""

from __future__ import annotations

import numpy as np

from .sprites import FEET_Y, STANCE_HEIGHT, alpha_bbox

Box = tuple[int, int, int, int]


def visual_box(rgba: np.ndarray) -> Box | None:
    bbox = alpha_bbox(rgba)
    if not bbox:
        return None
    x0, y0, x1, y1 = bbox
    return (x0, y0, x1 - x0, y1 - y0)


def hit_box(visual: Box) -> Box:
    """Hurtbox: visual box inset 6px on each side horizontally."""
    x, y, w, h = visual
    inset = min(6, max(0, w // 2 - 1))
    return (x + inset, y, max(1, w - 2 * inset), h)


def collision_box(frame_w: int, stance_height: int = STANCE_HEIGHT, feet_y: int = FEET_Y) -> Box:
    """48px wide, centred on the frame, bottom at the feet line, 80% of stance height tall."""
    w = 68
    h = round(stance_height * 0.8)
    x = frame_w // 2 - w // 2
    y = feet_y - h
    return (x, y, w, h)


def attack_box(rgba: np.ndarray, stance_left_edge: int, margin: int = 18) -> Box | None:
    """Silhouette that sticks out further toward screen left than
    (stance_left_edge - margin). None if nothing does on this frame.
    """
    threshold = stance_left_edge - margin
    if threshold <= 0:
        return None
    opaque = rgba[..., 3] > 32
    mask = opaque.copy()
    mask[:, threshold:] = False
    ys, xs = np.nonzero(mask)
    if len(xs) == 0:
        return None
    x0, x1 = int(xs.min()), int(xs.max()) + 1
    y0, y1 = int(ys.min()), int(ys.max()) + 1
    return (x0, y0, x1 - x0, y1 - y0)


def guard_box(visual: Box) -> Box:
    """Upper 60% of the visual box, extended 16px toward screen left."""
    x, y, w, h = visual
    gh = round(h * 0.6)
    return (x - 16, y, w + 16, gh)


def frame_boxes(
    rgba: np.ndarray,
    frame_w: int,
    action: str,
    frame_index: int,
    stance_left_edge: int,
) -> dict:
    """All boxes for one frame, per the action's rules. `action` is the
    delivered suffix (e.g. "special_charge"), not the hyphenated game name.
    """
    visual = visual_box(rgba)
    if visual is None:
        visual = (frame_w // 2 - 1, FEET_Y - 1, 2, 2)
    boxes = {
        "visual": list(visual),
        "collision": list(collision_box(frame_w)),
        "hit": list(hit_box(visual)),
        "attack": None,
        "guard": None,
    }
    if action in ("light", "heavy", "special"):
        attack = attack_box(rgba, stance_left_edge)
        boxes["attack"] = list(attack) if attack else None
    if action == "block" and frame_index >= 1:
        boxes["guard"] = list(guard_box(visual))
    return boxes
