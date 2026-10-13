# Elon Fighter art kit: instructions for Claude

You are helping a filmmaker produce all the art for **Elon Fighter**, a 2D pixel-art fighting game, using AI image and image-to-video tools (Higgsfield, Kling, Runway and similar). The game itself lives elsewhere; this repo is everything the art side needs.

## Read these first, in this order
1. `BRIEF.md`: the full art brief. It is the source of truth. If anything here disagrees with it, the brief wins.
2. `CHANGELOG.md`: what changed since the last pull. Read it after every `git pull` and tell the filmmaker about anything that affects files he already made.
3. `ASSETS.md`: all 63 files, in the order to make them.
4. `PROMPTS.md`: a ready prompt for every file.
5. `examples/`: reference art from the game template this project started from. Use it to understand the FORMAT (how a game-ready sheet, stance, portrait, stage and HUD look). Do not copy those characters; ours are new caricatures.

## Hard rules (from the brief)
- Exact file names from `ASSETS.md`, all lower case. Alternate takes go in `_rejects/`, never `v2` or `final`.
- Every fighter faces screen LEFT in every image, clip and portrait.
- Backgrounds: green `#00FF00` for Elon, Zuckerberg, Ambani, the rocket and the explosion. Magenta `#FF00FF` for every Altman file and both money effects. Portraits have a painted background. Stages and menus are full scenes.
- Every clip starts from that fighter's approved reference image. Exception: the special clip starts from the last frame of the special charge clip.
- Everything happens on the spot. No drifting, staggering back or lunging across the frame.
- No props that appear in one clip and vanish in the next. Empty hands in the reference.
- No crouch clips. 10 clips per fighter.
- No text in any image except `logo.png`. No real logos or real banknotes.
- Clips: the action happens once in the first 2 to 3 seconds; a 5 s tool clip is fine.

## The approval loop (one file at a time)
1. Make the file with its prompt from `PROMPTS.md`.
2. Run `python selfcheck/selfcheck.py <file>` (see `selfcheck/README.md`). Fix anything marked FAIL before uploading. WARN is allowed but mention it in the tracker comment.
3. Upload the file to `elon-fighter-art/_inbox/` on the shared Drive. Only one file in the inbox at a time.
4. Set that file's Status to "Sent for approval" in the tracker in the brief doc.
5. Wait for the verdict on the tracker row: Approved (start the next file) or Re-roll (the comment says what to fix).

Do not start the next file until the current one is approved.

## Helping the filmmaker
- When asked "what's next", look at `ASSETS.md` order and the approvals he tells you about, and give him the next file name, its prompt and what to watch for (the reject list in `BRIEF.md`).
- When a file is rejected, read the reason, map it to the reject list in `BRIEF.md`, and rewrite the prompt to fix it.
- Keep prompts short and literal. Tools follow concrete words ("locked static camera", "feet stay planted") better than adjectives.
- After `git pull`, summarise `CHANGELOG.md` entries newer than his last pull.

## Do not edit
`BRIEF.md`, `ASSETS.md`, `PROMPTS.md` and `selfcheck/` are maintained by the game team. If something looks wrong, tell the filmmaker to raise it with Aman instead of changing it.
