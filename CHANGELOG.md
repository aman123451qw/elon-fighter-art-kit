# Changelog

Newest first. After every `git pull`, read the entries since your last pull.

## 2026-10-15: new powers (read `POWERS.md`)
- The game is now **Elon vs Ambani only**. Stop all Zuckerberg and Altman work.
- Each fighter gets 4 powers. 43 new files, phases 7 to 10, all listed with prompts in `POWERS.md`.
- New rule: glow, beams, trails, sparks and the two ghosts are made on **pure black** `#000000` (the game blends them as light). Fighter clips and objects stay glow-free on green (magenta for money and Antilia).
- Branding is now allowed only where `POWERS.md` asks for it (SPACEX and Tesla on the rocket, STARLINK, ₹500 notes, Modi ji and Salman Khan ghosts).
- Start with phase 7 (3 test files) and wait for approval.

## 2026-10-15: fixes approved
- Approved: `ambani_special_charge`, `ambani_special` (no glow, green background), new `stage_mumbai` (satellites moved down), `elon_walk`, `elon_jump` (trimmed to its first jump).
- Ambani is complete. Elon needs only `elon_special` (arm at waist height). See `approved/README.md`.
- Rule added: no glow, aura or light effects inside fighter clips; the game draws glows itself. (This replaces the earlier "money effects / glows on magenta" advice for fighter clips.)
- Next: phase 3 (Zuckerberg + Colosseum), phase 5 (Altman + server farm), phase 6 (menus).

## 2026-10-14: first approvals
- 27 files approved; finals are in `approved/` (plus `characters/`). See `approved/README.md` for the full status and the re-roll list.
- Re-roll: `elon_special`, `ambani_special_charge`, `ambani_special` (both Ambani specials on magenta). Still never sent: `elon_walk`, `elon_jump`.

## 2026-10-14: Altman reference final
- `characters/altman_reference.png` replaced with your new magenta version. All four references are now final. Start Altman's clips from this one.

## 2026-10-14: characters finalised
- Added `characters/`: the lineup and all 4 references. Start every clip from these.
- Proportions stay realistic as in these images (the brief's "head about 1/5" no longer applies).
- Zuckerberg keeps his gold chain in every clip.
- Altman: you are redoing him. Deliver the new reference on magenta `#FF00FF`. Until then `characters/altman_reference.png` is your green original with the background swapped to magenta.

## 2026-10-14: self-check added
- `selfcheck/` now works: `python selfcheck/selfcheck.py <file>` runs the same checks we run and says PASS / WARN / FAIL. Run it on each fighter's reference first. See `selfcheck/README.md`.

## 2026-10-14: first version
- Brief finalised: 63 files, 10 clips per fighter (no crouch), phase 1 is lineup + Elon reference + idle + heavy.
- Altman files and both money effects on magenta `#FF00FF`; everything else on green `#00FF00`; portraits painted.
- Feet line on stages is 77% down the image (earlier drafts said 82%). Flat floor from about 65% down.
- Altman's hologram clone is made in the game: no hologram clip needed from you.
- Added `PROMPTS.md` (a prompt for every file) and `examples/` (reference art from the original template).
