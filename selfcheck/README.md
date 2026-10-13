# Self-check

Runs the same automatic checks we run when you upload a file, and tells you PASS / WARN / FAIL before you upload. It never changes anything.

## Setup (once)
- Python 3.10 or newer
- ffmpeg on your PATH (https://ffmpeg.org)
- `pip install pillow numpy`

## Use
```
python selfcheck/selfcheck.py elon_reference.png    # do this first for each fighter
python selfcheck/selfcheck.py elon_idle.mp4
```

- FAIL: fix it before uploading (the message says what is wrong; the reject list in BRIEF.md says how to fix it).
- WARN: allowed, but mention it in your tracker comment.
- Checking a fighter's reference image first lets the tool also check that the fighter's clips match its size.

What it checks: the file name, size, frame rate, background colour, clean background removal (no coloured fringes), body always inside the frame, no camera zoom, no drifting off the spot, size matching the reference, that the action is found and starts early, and that idle/walk loop smoothly.
