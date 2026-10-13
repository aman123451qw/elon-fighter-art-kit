"""Art-review tooling library for the fighting game.

Modules:
  spec      - the 63 assets, phases, frame/fps targets
  media     - load clips (ffmpeg) / PNG folders / images
  keying    - chroma key detection, removal, fringe metric
  sprites   - frame selection, stance normalisation, pixel pass, sheet packing
  hitboxes  - auto per-frame hit/hurt/collision/attack/guard boxes
  checks    - PASS/WARN/FAIL automatic checks
  manifest  - read/write assetManifest.json, backup/restore
"""
