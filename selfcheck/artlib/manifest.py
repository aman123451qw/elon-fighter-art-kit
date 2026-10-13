"""Read/write src/game/generated/assetManifest.json, and back up / restore
the previous game file + manifest entry for one asset under
public/assets/_previous/<asset>/ so a reject can undo a check.
"""

from __future__ import annotations

import json
import shutil
from datetime import datetime, timezone
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
MANIFEST_PATH = REPO_ROOT / "src" / "game" / "generated" / "assetManifest.json"
PUBLIC_ASSETS = REPO_ROOT / "public" / "assets"
PREVIOUS_DIR = PUBLIC_ASSETS / "_previous"


def empty_manifest() -> dict:
    return {
        "version": 1,
        "updatedAt": datetime.now(timezone.utc).isoformat(),
        "fighters": {},
        "fx": {},
        "stages": {},
        "menus": {},
    }


def load_manifest(path: Path = MANIFEST_PATH) -> dict:
    if path.exists():
        data = json.loads(path.read_text())
        for key in ("fighters", "fx", "stages", "menus"):
            data.setdefault(key, {})
        return data
    return empty_manifest()


def save_manifest(manifest: dict, path: Path = MANIFEST_PATH) -> None:
    manifest["updatedAt"] = datetime.now(timezone.utc).isoformat()
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2))


def get_entry(manifest: dict, key_path: list[str]) -> dict | None:
    node = manifest
    for key in key_path:
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def set_entry(manifest: dict, key_path: list[str], value: dict) -> None:
    node = manifest
    for key in key_path[:-1]:
        node = node.setdefault(key, {})
    node[key_path[-1]] = value


def backup_asset(asset_name: str, game_paths: list[Path], manifest: dict, key_path: list[str]) -> Path | None:
    """Copy the current game file(s) + manifest entry for one asset into
    public/assets/_previous/<asset>/, so `reject` can restore them. Returns
    the backup directory, or None if there was nothing to back up yet.
    """
    existing_paths = [p for p in game_paths if p.exists()]
    old_entry = get_entry(manifest, key_path)
    if not existing_paths and old_entry is None:
        return None

    dest_dir = PREVIOUS_DIR / asset_name
    dest_dir.mkdir(parents=True, exist_ok=True)
    for p in existing_paths:
        shutil.copy2(p, dest_dir / p.name)
    if old_entry is not None:
        (dest_dir / "manifest_entry.json").write_text(json.dumps(old_entry, indent=2))
    (dest_dir / "game_paths.json").write_text(json.dumps([str(p) for p in game_paths], indent=2))
    return dest_dir


def restore_asset(asset_name: str, manifest: dict, key_path: list[str]) -> bool:
    """Restore the game file(s) + manifest entry backed up by `backup_asset`.
    Returns True if a backup existed and was restored.
    """
    dest_dir = PREVIOUS_DIR / asset_name
    if not dest_dir.exists():
        return False

    paths_file = dest_dir / "game_paths.json"
    game_paths = [Path(p) for p in json.loads(paths_file.read_text())] if paths_file.exists() else []
    for p in game_paths:
        backup_file = dest_dir / p.name
        if backup_file.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(backup_file, p)
        elif p.exists():
            p.unlink()  # asset did not exist before this check; undo the delivery

    entry_file = dest_dir / "manifest_entry.json"
    if entry_file.exists():
        set_entry(manifest, key_path, json.loads(entry_file.read_text()))
    else:
        # nothing existed before -> remove the entry this check added
        node = manifest
        for key in key_path[:-1]:
            node = node.get(key, {})
        node.pop(key_path[-1], None)
    return True
