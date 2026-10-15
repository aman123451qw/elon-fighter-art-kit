#!/usr/bin/env python3
"""
Self-check a file BEFORE uploading it. Runs exactly the automatic checks the
game team runs, prints PASS / WARN / FAIL, and changes nothing in any game.

Usage:
  python selfcheck/selfcheck.py elon_reference.png   # run this first for each fighter
  python selfcheck/selfcheck.py elon_idle.mp4
  python selfcheck/selfcheck.py cybertruck_reference.png   # objects too: run the reference first
  python selfcheck/selfcheck.py fx_hit_glow.mp4            # glow files on black are checked too
  python selfcheck/selfcheck.py some_folder_of_pngs/elon_walk

Checking a fighter's reference image saves its stance size locally, so that
fighter's clips are then also checked for matching size.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import review_core  # noqa: E402  (same checks as the game team's review tool)
from artlib import checks, spec  # noqa: E402


def main() -> None:
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"FAIL: file not found: {path}")
        sys.exit(1)

    stem = path.name if path.is_dir() else path.stem
    results = [checks.check_filename(stem)]
    asset = spec.identify_asset(stem)
    convert = None
    if asset is not None:
        extra, convert = review_core.HANDLERS[asset.kind](asset, path)
        results.extend(extra)

    failed = any(level == "FAIL" for level, _ in results)
    print(f"\n== {stem} ==")
    for level, message in results:
        print(f"{level}: {message}")

    # Only reference images store something (their stance size, locally).
    if asset is not None and asset.kind in ("reference", "object_reference") and not failed and convert is not None:
        convert(results)
        print("(saved this reference's size for checking its clips)")

    print("\nRESULT: " + ("FIX the FAIL lines before uploading" if failed else "OK to upload (mention any WARN in the tracker comment)"))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
