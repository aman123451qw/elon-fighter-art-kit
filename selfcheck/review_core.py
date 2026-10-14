#!/usr/bin/env python3
"""
Art review CLI for the fighting game's 63 delivered assets (see
plans/01-artwork/PLAN.md). Runs the automatic checks on a delivered file,
converts it into game assets when it's clean, and tracks approve/reject
state. Also rebuilds the manifest from whatever stand-in art already lives
in public/assets/.

Usage:
  python tools/review.py check "G:/My Drive/elon-fighter-art/_inbox/elon_idle.mp4"
  python tools/review.py approve elon_idle
  python tools/review.py reject  elon_idle "drifts left 40px, keep feet planted"
  python tools/review.py status
  python tools/review.py standins
"""

from __future__ import annotations

import argparse
import json
import math
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

from artlib import checks, hitboxes, keying, manifest, media, spec, sprites

TOOLS_DIR = Path(__file__).resolve().parent
PUBLIC_ASSETS = manifest.PUBLIC_ASSETS
REVIEW_OUT_DIR = TOOLS_DIR / "review_out"
REFERENCES_DIR = REVIEW_OUT_DIR / "references"
REVIEW_STATE_PATH = TOOLS_DIR / "review_state.json"
REVIEW_CONFIG_PATH = TOOLS_DIR / "review_config.json"
REVIEW_URL_HINT = "http://127.0.0.1:5180/?review"


# --------------------------------------------------------------- plumbing --

def load_config() -> dict:
    if REVIEW_CONFIG_PATH.exists():
        return json.loads(REVIEW_CONFIG_PATH.read_text())
    return {"drive_root": ""}


def load_state() -> dict:
    if REVIEW_STATE_PATH.exists():
        return json.loads(REVIEW_STATE_PATH.read_text())
    return {}


def save_state(state: dict) -> None:
    REVIEW_STATE_PATH.write_text(json.dumps(state, indent=2))


def set_state(asset_name: str, **fields) -> None:
    state = load_state()
    entry = state.get(asset_name, {})
    entry.update(fields)
    entry["updatedAt"] = datetime.now(timezone.utc).isoformat()
    state[asset_name] = entry
    save_state(state)


def resolve_input(raw: str) -> tuple[str, Path | None]:
    """A bare asset name, a filename, or a real path -> (stem, path-or-None)."""
    path = Path(raw)
    if path.exists():
        stem = path.name if path.is_dir() else path.stem
        return stem, path
    name = Path(raw).name
    stem = Path(name).stem if "." in name else name
    return stem, None


def key_path_for(asset: spec.Asset) -> list[str]:
    if asset.kind == "clip":
        return ["fighters", asset.fighter, "actions", asset.game_action]
    if asset.kind == "portrait":
        return ["fighters", asset.fighter, "portrait"]
    if asset.kind == "fx":
        return ["fx", asset.name]
    if asset.kind == "stage":
        return ["stages", asset.name]
    if asset.kind == "menu":
        return ["menus", asset.name]
    return []  # lineup / reference have no game-side manifest entry


def game_paths_for(asset: spec.Asset) -> list[Path]:
    if asset.kind == "clip":
        return [PUBLIC_ASSETS / "fighters" / asset.fighter / f"{asset.game_action}.png"]
    if asset.kind == "portrait":
        return [PUBLIC_ASSETS / "fighters" / asset.fighter / "portrait.png"]
    if asset.kind == "fx":
        return [PUBLIC_ASSETS / "fx" / f"{asset.name}.png"]
    if asset.kind == "stage":
        return [PUBLIC_ASSETS / "stages" / f"{asset.name}.png"]
    if asset.kind == "menu":
        return [PUBLIC_ASSETS / "menus" / f"{asset.name}.png"]
    return []


def format_report(results: list[tuple[str, str]]) -> str:
    lines = [f"{level}: {msg}" for level, msg in results]
    has_fail = any(level == "FAIL" for level, _ in results)
    lines.append("VERDICT: " + ("FIX BEFORE LOOK" if has_fail else "READY FOR IN-GAME LOOK"))
    return "\n".join(lines)


def write_review_out(
    asset_name: str,
    full_results: list[tuple[str, str]],
    frames=None,
    chosen=None,
    placed=None,
    fps: float | None = None,
) -> None:
    out_dir = REVIEW_OUT_DIR / asset_name
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "report.txt").write_text(format_report(full_results) + "\n")
    if placed and fps:
        sprites.save_preview_gif(placed, out_dir / "preview.gif", fps)
    if frames is not None and chosen is not None:
        sprites.save_contact_sheet(list(frames), chosen, out_dir / "contact.jpg")


# ----------------------------------------------------------- kind handlers --
# Each handler returns (results, convert_fn). convert_fn(full_results) is only
# called when there is no FAIL among the full results (filename check included).

def handle_lineup(asset: spec.Asset, path: Path):
    rgb = media.load_image_rgb(path)
    h, w = rgb.shape[:2]
    results = [checks.check_lineup_size(w, h), checks.check_flat_background(rgb, asset.background)]
    return results, None  # look only, no game files, no measurements


def handle_reference(asset: spec.Asset, path: Path):
    rgb = media.load_image_rgb(path)
    h, w = rgb.shape[:2]
    results = [checks.check_reference_size(w, h), checks.check_flat_background(rgb, asset.background)]
    key = keying.detect_key_color(rgb)
    rgba = keying.chroma_key(rgb, key)
    results.append(checks.check_margin(rgba))

    def convert(_full_results):
        stance = sprites.measure_stance(rgba)
        if stance is None:
            return
        REFERENCES_DIR.mkdir(parents=True, exist_ok=True)
        (REFERENCES_DIR / f"{asset.fighter}.json").write_text(json.dumps(stance.to_dict(), indent=2))

    return results, convert  # measurements only, no game files


def handle_portrait(asset: spec.Asset, path: Path):
    rgb = media.load_image_rgb(path)
    h, w = rgb.shape[:2]
    results = [checks.check_portrait_size(w, h), checks.check_portrait_not_flat(rgb)]

    def convert(full_results):
        game_path = game_paths_for(asset)[0]
        man = manifest.load_manifest()
        kp = key_path_for(asset)
        manifest.backup_asset(asset.name, [game_path], man, kp)
        game_path.parent.mkdir(parents=True, exist_ok=True)
        Image.open(path).convert("RGB").save(game_path)
        manifest.set_entry(man, kp, {
            "url": f"/assets/fighters/{asset.fighter}/portrait.png",
            "width": w, "height": h, "source": "delivered",
        })
        manifest.save_manifest(man)
        write_review_out(asset.name, full_results)

    return results, convert


def handle_stage(asset: spec.Asset, path: Path):
    rgb = media.load_image_rgb(path)
    h, w = rgb.shape[:2]
    results = [checks.check_stage_size(w, h)]

    def convert(full_results):
        game_path = game_paths_for(asset)[0]
        man = manifest.load_manifest()
        kp = key_path_for(asset)
        manifest.backup_asset(asset.name, [game_path], man, kp)
        game_path.parent.mkdir(parents=True, exist_ok=True)
        Image.open(path).convert("RGB").save(game_path)
        manifest.set_entry(man, kp, {"url": f"/assets/stages/{asset.name}.png", "width": w, "height": h, "source": "delivered"})
        manifest.save_manifest(man)
        write_review_out(asset.name, full_results)

    return results, convert


def handle_menu(asset: spec.Asset, path: Path):
    img = Image.open(path)
    rgb = np.array(img.convert("RGB"))
    h, w = rgb.shape[:2]
    results = [checks.check_menu_size(asset.name, w, h)]

    def convert(full_results):
        game_path = game_paths_for(asset)[0]
        man = manifest.load_manifest()
        kp = key_path_for(asset)
        manifest.backup_asset(asset.name, [game_path], man, kp)
        game_path.parent.mkdir(parents=True, exist_ok=True)
        has_alpha = img.mode in ("RGBA", "LA") or "transparency" in img.info
        (img.convert("RGBA") if has_alpha else img.convert("RGB")).save(game_path)
        manifest.set_entry(man, kp, {"url": f"/assets/menus/{asset.name}.png", "width": w, "height": h, "source": "delivered"})
        manifest.save_manifest(man)
        write_review_out(asset.name, full_results)

    return results, convert


def handle_fx(asset: spec.Asset, path: Path):
    try:
        frames, fps = media.load_clip(path)
    except media.ClipLoadError as exc:
        return [("FAIL", str(exc))], None

    results = [checks.check_readable(len(frames))]
    if not frames:
        return results, None
    h, w = frames[0].shape[:2]
    results.append(checks.check_resolution(w, h))
    results.append(checks.check_fps(fps))
    key = keying.detect_key_color(frames[0])
    results.append(checks.check_background(key, asset.background))

    keyed = [keying.chroma_key(f, key) for f in frames]
    fringe_values = [keying.fringe_percent(f, key) for f in keyed]
    results.append(checks.check_fringe(sum(fringe_values) / len(fringe_values)))

    target = spec.FRAME_TARGETS[asset.name]
    chosen, window = sprites.select_frames(keyed, target, fps)
    if target.mode != "loop":
        results.append(checks.check_action_detected(window))
    if not chosen:
        return results, None

    try:
        cropped, (fw, fh) = sprites.crop_union([keyed[i] for i in chosen])
    except ValueError as exc:
        results.append(("FAIL", str(exc)))
        return results, None

    centres = []
    for img in cropped:
        bbox = sprites.alpha_bbox(np.array(img))
        if bbox:
            x0, y0, x1, y1 = bbox
            centres.append(((x0 + x1) / 2, (y0 + y1) / 2))
    results.append(checks.check_fx_centre_drift(centres, fw, fh))

    pixelated = sprites.pixel_pass(cropped)

    def convert(full_results):
        sheet = sprites.pack_sheet(pixelated)
        game_path = game_paths_for(asset)[0]
        man = manifest.load_manifest()
        kp = key_path_for(asset)
        manifest.backup_asset(asset.name, [game_path], man, kp)
        game_path.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(game_path)
        manifest.set_entry(man, kp, {
            "url": f"/assets/fx/{asset.name}.png",
            "frames": len(pixelated), "frameRate": target.fps, "repeat": target.repeat,
            "frameWidth": fw, "frameHeight": fh, "source": "delivered",
        })
        manifest.save_manifest(man)
        write_review_out(asset.name, full_results, frames=frames, chosen=chosen, placed=pixelated, fps=target.fps)

    return results, convert


def handle_clip(asset: spec.Asset, path: Path):
    try:
        frames, fps = media.load_clip(path)
    except media.ClipLoadError as exc:
        return [("FAIL", str(exc))], None

    results = [checks.check_readable(len(frames))]
    if not frames:
        return results, None
    h, w = frames[0].shape[:2]
    results.append(checks.check_resolution(w, h))
    results.append(checks.check_fps(fps))
    key = keying.detect_key_color(frames[0])
    results.append(checks.check_background(key, asset.background))

    keyed = [keying.chroma_key(f, key) for f in frames]
    fringe_values = [keying.fringe_percent(f, key) for f in keyed]
    results.append(checks.check_fringe(sum(fringe_values) / len(fringe_values)))

    stance = sprites.measure_stance(keyed[0])
    if stance is None:
        results.append(("FAIL", "could not measure the fighting stance on frame 1 (nothing survived the key)"))
        return results, None

    ref_path = REFERENCES_DIR / f"{asset.fighter}.json"
    reference_ratio = None
    if ref_path.exists():
        ref = sprites.Stance.from_dict(json.loads(ref_path.read_text()))
        reference_ratio = ref.body_height / ref.image_height
    results.append(checks.check_stance_ratio(stance.body_height, stance.image_height, reference_ratio))

    target = spec.FRAME_TARGETS[asset.action]
    chosen, window = sprites.select_frames(keyed, target, fps)
    if target.mode != "loop":
        results.append(checks.check_action_detected(window))
        results.append(checks.check_action_start(window[0] if window else None, fps))
    if not chosen:
        return results, None

    selected = [keyed[i] for i in chosen]
    target_height = sprites.STANCE_HEIGHT * spec.HEIGHT_RATIO.get(asset.fighter, 1.0)
    placed, canvas_w, norm_warnings = sprites.normalize_clip(
        selected, stance, pin_feet=target.pin_feet, target_height=target_height
    )
    results.extend(("WARN", w) for w in norm_warnings)

    results.append(checks.check_body_edge(placed, canvas_w, sprites.FRAME))

    first_stance = sprites.measure_stance(np.array(placed[0]))
    last_stance = sprites.measure_stance(np.array(placed[-1]))
    if first_stance and last_stance:
        results.append(checks.check_zoom(first_stance.body_height, last_stance.body_height, asset.action))
        results.append(checks.check_drift(first_stance.centre_x, last_stance.centre_x, canvas_w, asset.action))

    if asset.action in checks.LOOP_ACTIONS:
        seam = sprites.loop_seam_diff(placed[0], placed[-1])
        results.append(checks.check_loop_seam(seam, asset.action))

    pixelated = sprites.pixel_pass(placed)

    def convert(full_results):
        stance_box = sprites.alpha_bbox(np.array(pixelated[0]))
        left_edge = stance_box[0] if stance_box else canvas_w // 2
        frame_boxes = [
            hitboxes.frame_boxes(np.array(f), canvas_w, asset.action, i, left_edge)
            for i, f in enumerate(pixelated)
        ]
        sheet = sprites.pack_sheet(pixelated)
        game_path = game_paths_for(asset)[0]
        man = manifest.load_manifest()
        kp = key_path_for(asset)
        manifest.backup_asset(asset.name, [game_path], man, kp)
        game_path.parent.mkdir(parents=True, exist_ok=True)
        sheet.save(game_path)
        manifest.set_entry(man, kp, {
            "url": f"/assets/fighters/{asset.fighter}/{asset.game_action}.png",
            "frames": len(pixelated), "frameRate": target.fps, "repeat": target.repeat,
            "frameWidth": canvas_w, "frameHeight": sprites.FRAME,
            "source": "delivered", "boxes": frame_boxes,
        })
        manifest.save_manifest(man)
        write_review_out(asset.name, full_results, frames=frames, chosen=chosen, placed=pixelated, fps=target.fps)

    return results, convert


HANDLERS = {
    "lineup": handle_lineup,
    "reference": handle_reference,
    "clip": handle_clip,
    "fx": handle_fx,
    "portrait": handle_portrait,
    "stage": handle_stage,
    "menu": handle_menu,
}


# --------------------------------------------------------------- commands --

def cmd_check(path_arg: str) -> None:
    path = Path(path_arg)
    if not path.exists():
        print(f"FAIL: path not found: {path}")
        sys.exit(1)

    stem = path.name if path.is_dir() else path.stem
    fn_level, fn_msg = checks.check_filename(stem)
    results: list[tuple[str, str]] = [(fn_level, fn_msg)]

    asset = spec.identify_asset(stem)
    convert_fn = None
    if asset is not None:
        extra, convert_fn = HANDLERS[asset.kind](asset, path)
        results.extend(extra)

    has_fail = any(level == "FAIL" for level, _ in results)
    verdict = "FIX BEFORE LOOK" if has_fail else "READY FOR IN-GAME LOOK"

    print(f"\n== {stem} ==")
    for level, msg in results:
        print(f"{level}: {msg}")
    print(f"VERDICT: {verdict}")

    if not has_fail and convert_fn is not None:
        convert_fn(results)

    if asset is not None:
        set_state(asset.name, state="checked", verdict=verdict, file=str(path))

    print(f"\n{REVIEW_URL_HINT}")


def cmd_approve(raw: str) -> None:
    stem, path = resolve_input(raw)
    asset = spec.identify_asset(stem)
    if asset is None:
        print(f"FAIL: '{raw}' is not a recognised asset name")
        sys.exit(1)

    cfg = load_config()
    drive_root = cfg.get("drive_root") or ""
    state = load_state()
    entry = state.get(asset.name, {})

    moved_to = None
    if drive_root:
        inbox = Path(drive_root) / "_inbox"
        src = path or (Path(entry["file"]) if entry.get("file") else None)
        if src and src.exists():
            try:
                in_inbox = inbox.resolve() in src.resolve().parents
            except OSError:
                in_inbox = False
            if in_inbox:
                dest_dir = Path(drive_root) / asset.folder
                dest_dir.mkdir(parents=True, exist_ok=True)
                moved_to = dest_dir / src.name
                shutil.move(str(src), str(moved_to))

    entry["state"] = "approved"
    entry["approvedAt"] = datetime.now(timezone.utc).isoformat()
    state[asset.name] = entry
    save_state(state)

    if moved_to:
        print(f"approved {asset.name}; moved {src.name} -> {moved_to}")
    elif drive_root:
        print(f"approved {asset.name} (file not found under {drive_root}/_inbox, nothing moved)")
    else:
        print(f"approved {asset.name} (drive_root not set in tools/review_config.json, nothing moved)")


def cmd_reject(raw: str, reason: str) -> None:
    stem, path = resolve_input(raw)
    asset = spec.identify_asset(stem)
    if asset is None:
        print(f"FAIL: '{raw}' is not a recognised asset name")
        sys.exit(1)

    kp = key_path_for(asset)
    restored = False
    if kp:
        man = manifest.load_manifest()
        restored = manifest.restore_asset(asset.name, man, kp)
        manifest.save_manifest(man)

    cfg = load_config()
    drive_root = cfg.get("drive_root") or ""
    state = load_state()
    entry = state.get(asset.name, {})

    moved_to = None
    if drive_root:
        inbox = Path(drive_root) / "_inbox"
        src = path or (Path(entry["file"]) if entry.get("file") else None)
        if src and src.exists():
            try:
                in_inbox = inbox.resolve() in src.resolve().parents
            except OSError:
                in_inbox = False
            if in_inbox:
                dest_dir = Path(drive_root) / "_rejects"
                dest_dir.mkdir(parents=True, exist_ok=True)
                moved_to = dest_dir / src.name
                shutil.move(str(src), str(moved_to))

    entry["state"] = "rejected"
    entry["reason"] = reason
    entry["rejectedAt"] = datetime.now(timezone.utc).isoformat()
    state[asset.name] = entry
    save_state(state)

    parts = [f"rejected {asset.name}: {reason}"]
    parts.append("restored previous game asset" if restored else "nothing to restore (no previous version)")
    if moved_to:
        parts.append(f"moved file -> {moved_to}")
    print(" | ".join(parts))


def _asset_state_label(asset: spec.Asset, man: dict, state_store: dict) -> str:
    entry = state_store.get(asset.name)
    if entry:
        if entry.get("state") == "approved":
            return "approved"
        if entry.get("state") == "rejected":
            return f"rejected ({entry.get('reason', '')})"
    kp = key_path_for(asset)
    node = manifest.get_entry(man, kp) if kp else None
    if node and node.get("source") == "delivered":
        return "checked (delivered)"
    if entry and entry.get("state") == "checked":
        return f"checked ({entry.get('verdict', '')})"
    return "not received"


def cmd_status() -> None:
    man = manifest.load_manifest()
    state_store = load_state()
    for phase in range(1, 7):
        assets = sorted(spec.phase_assets(phase), key=lambda a: a.name)
        print(f"\n=== Phase {phase} ({len(assets)} files) ===")
        for asset in assets:
            print(f"  {asset.name:<28} {_asset_state_label(asset, man, state_store)}")


# ------------------------------------------------------------- standins --

def _pixel_font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def make_logo() -> Image.Image:
    """1600x600, transparent, big pixel-style 'ELON FIGHTER' via nearest-neighbour upscale."""
    scale = 8
    small_w, small_h = 1600 // scale, 600 // scale
    small = Image.new("RGBA", (small_w, small_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(small)
    text = "ELON FIGHTER"
    bbox = draw.textbbox((0, 0), text)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((small_w - tw) / 2 - bbox[0], (small_h - th) / 2 - bbox[1]), text, fill=(255, 210, 40, 255))
    return small.resize((small_w * scale, small_h * scale), Image.NEAREST)


def make_title() -> Image.Image:
    """1920x1080, the colosseum stage stretched/cropped + a STAND-IN label."""
    stage_path = PUBLIC_ASSETS / "stages" / "stage_colosseum.png"
    if stage_path.exists():
        img = Image.open(stage_path).convert("RGB").resize((1920, 1080), Image.LANCZOS)
    else:
        img = Image.new("RGB", (1920, 1080), (20, 20, 30))
    draw = ImageDraw.Draw(img)
    font = _pixel_font(96)
    text = "STAND-IN"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((1920 - tw) / 2, (1080 - th) / 2), text, fill=(255, 255, 255), font=font, stroke_width=4, stroke_fill=(0, 0, 0))
    return img


def make_card(portrait_a: Path, portrait_b: Path, size: tuple[int, int] = (1330, 1182)) -> Image.Image:
    """1330x1182, dark background, both fighters' portraits side by side + STAND-IN label."""
    w, h = size
    img = Image.new("RGB", (w, h), (16, 16, 22))
    draw = ImageDraw.Draw(img)
    half = w // 2
    slot_h = h - 180
    for i, portrait_path in enumerate((portrait_a, portrait_b)):
        if not portrait_path.exists():
            continue
        portrait = Image.open(portrait_path).convert("RGB")
        portrait.thumbnail((half - 60, slot_h))
        x = i * half + (half - portrait.width) // 2
        y = 40 + (slot_h - portrait.height) // 2
        img.paste(portrait, (x, y))
    draw.line([(half, 20), (half, h - 20)], fill=(70, 70, 80), width=3)
    font = _pixel_font(48)
    text = "STAND-IN"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text(((w - tw) / 2, h - th - 30), text, fill=(255, 220, 0), font=font)
    return img


def make_fx_rocket() -> list[Image.Image]:
    """6 frames, 128x64: white capsule facing left, flickering orange flame on the right."""
    frames = []
    w, h = 128, 64
    for i in range(6):
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        cy = h // 2
        body_left, body_right = 34, 92
        draw.rounded_rectangle([body_left, cy - 12, body_right, cy + 12], radius=12, fill=(235, 235, 240, 255))
        draw.polygon([(body_left, cy - 12), (body_left - 18, cy), (body_left, cy + 12)], fill=(235, 235, 240, 255))
        flick = 12 + (i % 3) * 6
        draw.polygon([(body_right, cy - 9), (body_right + flick, cy), (body_right, cy + 9)], fill=(255, 140, 0, 255))
        draw.polygon([(body_right, cy - 4), (body_right + flick * 0.6, cy), (body_right, cy + 4)], fill=(255, 225, 90, 255))
        frames.append(img)
    return frames


def make_fx_explosion() -> list[Image.Image]:
    """8 frames, 128x128: expanding orange/yellow circles fading out."""
    frames = []
    w, h = 128, 128
    cx, cy = w // 2, h // 2
    for i in range(8):
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        t = i / 7
        r = 10 + t * 50
        alpha = max(0, int(255 * (1 - t)))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(255, 150, 0, alpha))
        r2 = r * 0.6
        draw.ellipse([cx - r2, cy - r2, cx + r2, cy + r2], fill=(255, 230, 80, alpha))
        frames.append(img)
    return frames


def make_fx_money_bundle() -> list[Image.Image]:
    """6 frames, 96x64: gold/orange bundle with a band, squash-rotating in a loop."""
    frames = []
    w, h = 96, 64
    for i in range(6):
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        squash = abs(((i % 6) - 3) / 3)
        bw, bh = 60 * (1 - 0.3 * squash), 36 * (1 + 0.3 * squash)
        x0, y0 = (w - bw) / 2, (h - bh) / 2
        draw.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(210, 160, 30, 255), outline=(140, 100, 10, 255), width=2)
        draw.rectangle([x0, y0 + bh * 0.4, x0 + bw, y0 + bh * 0.6], fill=(160, 40, 40, 255))
        frames.append(img)
    return frames


def make_fx_money_burst() -> list[Image.Image]:
    """8 frames, 128x128: small gold/orange rectangles flying outward."""
    frames = []
    w, h = 128, 128
    cx, cy = w // 2, h // 2
    n_bills = 6
    for i in range(8):
        img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        t = i / 7
        for b in range(n_bills):
            ang = (2 * math.pi * b / n_bills) + 0.3
            dist = 10 + t * 45
            x, y = cx + math.cos(ang) * dist, cy + math.sin(ang) * dist
            bw, bh = 16, 10
            alpha = max(0, int(255 * (1 - 0.6 * t)))
            draw.rectangle([x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2], fill=(210, 170, 40, alpha), outline=(140, 100, 10, alpha))
        frames.append(img)
    return frames


FX_GENERATORS = {
    "fx_rocket": make_fx_rocket,
    "fx_explosion": make_fx_explosion,
    "fx_money_bundle": make_fx_money_bundle,
    "fx_money_burst": make_fx_money_burst,
}

CARD_OPPONENTS = {
    "card_elon_vs_zuckerberg": ("elon", "zuckerberg"),
    "card_elon_vs_ambani": ("elon", "ambani"),
    "card_elon_vs_altman": ("elon", "altman"),
}


def _load_standin_cells(sheet_path: Path) -> list[Image.Image]:
    """Stand-in sheet frames at the current FRAME size. Old template sheets use
    256 px frames: they are upscaled (nearest) and the file rewritten once, so
    stand-ins and delivered sheets draw at the same 1:1 scale in the game.
    """
    sheet = Image.open(sheet_path).convert("RGBA")
    if sheet.width == sprites.FRAME * sprites.COLUMNS or sheet.width % 256 != 0:
        return sprites.unpack_sheet(sheet, sprites.FRAME, sprites.FRAME)

    cells = sprites.unpack_sheet(sheet, 256, 256)
    upscaled = [cell.resize((sprites.FRAME, sprites.FRAME), Image.NEAREST) for cell in cells]
    if upscaled:
        sprites.pack_sheet(upscaled).save(sheet_path)
    return upscaled


def cmd_standins() -> None:
    man = manifest.load_manifest()

    for fighter in spec.FIGHTERS:
        fighter_dir = PUBLIC_ASSETS / "fighters" / fighter
        idle_path = fighter_dir / "idle.png"
        idle_frames = []
        if idle_path.exists():
            idle_frames = _load_standin_cells(idle_path)
        stance_left_edge = 0
        if idle_frames:
            vb = hitboxes.visual_box(np.array(idle_frames[0]))
            stance_left_edge = vb[0] if vb else 0

        for action in spec.ACTIONS_ORDER:
            game_action = spec.ACTION_TO_GAME[action]
            kp = ["fighters", fighter, "actions", game_action]
            existing = manifest.get_entry(man, kp)
            if existing and existing.get("source") == "delivered":
                continue
            sheet_path = fighter_dir / f"{game_action}.png"
            if not sheet_path.exists():
                print(f"warn: no stand-in sheet for {fighter}/{game_action}, skipping")
                continue
            cells = _load_standin_cells(sheet_path)
            if not cells:
                print(f"warn: {sheet_path} has no non-empty frames, skipping")
                continue
            target = spec.FRAME_TARGETS[action]
            boxes = [
                hitboxes.frame_boxes(np.array(f), sprites.FRAME, action, i, stance_left_edge)
                for i, f in enumerate(cells)
            ]
            manifest.set_entry(man, kp, {
                "url": f"/assets/fighters/{fighter}/{game_action}.png",
                "frames": len(cells), "frameRate": target.fps, "repeat": target.repeat,
                "frameWidth": sprites.FRAME, "frameHeight": sprites.FRAME, "source": "standin", "boxes": boxes,
            })

        portrait_kp = ["fighters", fighter, "portrait"]
        existing_p = manifest.get_entry(man, portrait_kp)
        if not (existing_p and existing_p.get("source") == "delivered"):
            portrait_path = fighter_dir / "portrait.png"
            if portrait_path.exists():
                pw, ph = Image.open(portrait_path).size
                manifest.set_entry(man, portrait_kp, {
                    "url": f"/assets/fighters/{fighter}/portrait.png",
                    "width": pw, "height": ph, "source": "standin",
                })

    for stage in spec.STAGE_NAMES:
        kp = ["stages", stage]
        existing = manifest.get_entry(man, kp)
        if existing and existing.get("source") == "delivered":
            continue
        stage_path = PUBLIC_ASSETS / "stages" / f"{stage}.png"
        if stage_path.exists():
            sw, sh = Image.open(stage_path).size
            manifest.set_entry(man, kp, {"url": f"/assets/stages/{stage}.png", "width": sw, "height": sh, "source": "standin"})

    menus_dir = PUBLIC_ASSETS / "menus"
    menus_dir.mkdir(parents=True, exist_ok=True)

    for mode in spec.MODE_NAMES:
        kp = ["menus", mode]
        existing = manifest.get_entry(man, kp)
        if existing and existing.get("source") == "delivered":
            continue
        mode_path = menus_dir / f"{mode}.png"
        if mode_path.exists():
            mw, mh = Image.open(mode_path).size
            manifest.set_entry(man, kp, {"url": f"/assets/menus/{mode}.png", "width": mw, "height": mh, "source": "standin"})

    for card, (a, b) in CARD_OPPONENTS.items():
        kp = ["menus", card]
        existing = manifest.get_entry(man, kp)
        if existing and existing.get("source") == "delivered":
            continue
        img = make_card(PUBLIC_ASSETS / "fighters" / a / "portrait.png", PUBLIC_ASSETS / "fighters" / b / "portrait.png")
        img.save(menus_dir / f"{card}.png")
        manifest.set_entry(man, kp, {"url": f"/assets/menus/{card}.png", "width": img.width, "height": img.height, "source": "standin"})

    for name, maker in (("logo", make_logo), ("title", make_title)):
        kp = ["menus", name]
        existing = manifest.get_entry(man, kp)
        if existing and existing.get("source") == "delivered":
            continue
        img = maker()
        img.save(menus_dir / f"{name}.png")
        manifest.set_entry(man, kp, {"url": f"/assets/menus/{name}.png", "width": img.width, "height": img.height, "source": "standin"})

    fx_dir = PUBLIC_ASSETS / "fx"
    fx_dir.mkdir(parents=True, exist_ok=True)
    for fx_name, maker in FX_GENERATORS.items():
        kp = ["fx", fx_name]
        existing = manifest.get_entry(man, kp)
        if existing and existing.get("source") == "delivered":
            continue
        frames = maker()
        target = spec.FRAME_TARGETS[fx_name]
        sheet = sprites.pack_sheet(frames)
        sheet.save(fx_dir / f"{fx_name}.png")
        fw, fh = frames[0].size
        manifest.set_entry(man, kp, {
            "url": f"/assets/fx/{fx_name}.png", "frames": len(frames), "frameRate": target.fps,
            "repeat": target.repeat, "frameWidth": fw, "frameHeight": fh, "source": "standin",
        })

    manifest.save_manifest(man)
    print(f"manifest written -> {manifest.MANIFEST_PATH}")


# ------------------------------------------------------------------- main --

def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="command", required=True)

    p_check = sub.add_parser("check", help="run checks on a delivered file/folder; convert it if clean")
    p_check.add_argument("path")

    p_approve = sub.add_parser("approve", help="mark an asset approved; move it out of _inbox if drive_root is set")
    p_approve.add_argument("name")

    p_reject = sub.add_parser("reject", help="restore the previous asset and mark it rejected")
    p_reject.add_argument("name")
    p_reject.add_argument("reason")

    sub.add_parser("status", help="show every asset's state, grouped by phase")
    sub.add_parser("standins", help="(re)build the manifest from the current stand-in art")

    args = ap.parse_args()
    if args.command == "check":
        cmd_check(args.path)
    elif args.command == "approve":
        cmd_approve(args.name)
    elif args.command == "reject":
        cmd_reject(args.name, args.reason)
    elif args.command == "status":
        cmd_status()
    elif args.command == "standins":
        cmd_standins()


if __name__ == "__main__":
    main()
