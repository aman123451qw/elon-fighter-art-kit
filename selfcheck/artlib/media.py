"""Load a clip (ffmpeg) or a PNG folder into frames; load still images."""

from __future__ import annotations

import json
import shutil
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image


class ClipLoadError(RuntimeError):
    """A clip or image could not be read."""


def probe_fps(path: Path) -> float:
    """ffprobe the average frame rate of a video file. 0.0 if it can't be read."""
    cmd = [
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=avg_frame_rate", "-of", "json", str(path),
    ]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, check=True).stdout
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return 0.0
    try:
        streams = json.loads(out).get("streams") or []
    except json.JSONDecodeError:
        return 0.0
    if not streams:
        return 0.0
    num, _, den = streams[0].get("avg_frame_rate", "0/0").partition("/")
    den = den or "1"
    try:
        den_f = float(den)
        return float(num) / den_f if den_f else 0.0
    except ValueError:
        return 0.0


def extract_video_frames(path: Path, tmp_dir: Path) -> list[np.ndarray]:
    """Extract every frame of a clip at its native fps as RGB arrays, in order."""
    if shutil.which("ffmpeg") is None:
        raise ClipLoadError("ffmpeg not found on PATH")
    cmd = ["ffmpeg", "-loglevel", "error", "-i", str(path), str(tmp_dir / "f_%05d.png")]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise ClipLoadError(f"ffmpeg could not read {path}: {result.stderr.strip()[:300]}")
    files = sorted(tmp_dir.glob("f_*.png"))
    if not files:
        raise ClipLoadError(f"ffmpeg produced no frames from {path}")
    return [np.array(Image.open(f).convert("RGB")) for f in files]


def load_png_folder(path: Path) -> list[np.ndarray]:
    files = sorted(path.glob("*.png"))
    if not files:
        raise ClipLoadError(f"no PNG files in {path}")
    return [np.array(Image.open(f).convert("RGB")) for f in files]


def load_clip(path: Path) -> tuple[list[np.ndarray], float]:
    """Load a clip (mp4 file, or a folder of PNGs). Returns (frames, fps).

    fps is 0.0 for a PNG folder since there is no timing information.
    """
    if path.is_dir():
        return load_png_folder(path), 0.0
    with tempfile.TemporaryDirectory() as tmp:
        frames = extract_video_frames(path, Path(tmp))
    fps = probe_fps(path)
    return frames, fps


def load_image_rgb(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGB"))


def load_image_rgba(path: Path) -> np.ndarray:
    return np.array(Image.open(path).convert("RGBA"))
