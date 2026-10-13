# Elon Fighter: art kit

Everything you need to make the art for Elon Fighter: the brief, the full list of 63 files, a ready prompt for each one, reference examples, and a self-check tool that tells you whether a file will pass before you upload it.

## Start here
1. Read `BRIEF.md` once, top to bottom.
2. Open `ASSETS.md`: that is the order to work in. Phase 1 is 4 files, then stop and wait for approval.
3. For each file, copy its prompt from `PROMPTS.md`.
4. Before uploading, run the self-check (below).
5. Upload to `elon-fighter-art/_inbox/` on the shared Drive and set the file to "Sent for approval" in the tracker.

If you use Claude (or another AI assistant) with this folder open, it reads `CLAUDE.md` and knows all of this already. Ask it "what's next?".

## Staying up to date
We change this kit when decisions change. Get the latest with:

```
git pull
```

Then read `CHANGELOG.md` for what changed.

## Self-check (optional but saves round trips)
Needs Python 3.10+ and ffmpeg.

```
pip install pillow numpy
python selfcheck/selfcheck.py path/to/elon_idle.mp4
```

It prints PASS / WARN / FAIL for every check we run on our side. Fix every FAIL before uploading.

## What's in here

| Path | What |
|---|---|
| `BRIEF.md` | The full art brief (copy of the shared doc) |
| `ASSETS.md` | All 63 files with phase, folder and background |
| `PROMPTS.md` | A ready prompt for every file |
| `CHANGELOG.md` | What changed and when |
| `CLAUDE.md` | Instructions for an AI assistant working in this folder |
| `examples/` | Reference art from the original game template (format reference only) |
| `selfcheck/` | The self-check tool |
| `scripts/` | Used by us to regenerate the prompt files |
