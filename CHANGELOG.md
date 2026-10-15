# Changelog

Newest first. After every `git pull`, read the entries since your last pull.

## 2026-10-17: phase 12 approved (all 18 SF2 moves)
- Approved: all 9 Elon and 9 Ambani moves (#123 to #140): crouch, crouch block, low sweep, heavy punch (Elon), light kick, heavy kick (Ambani), throw, thrown, jump kick, get up. Finals are in `approved/elon/` and `approved/ambani/`.
- The self-check flagged the two crouch blocks ("no action detected": the forearms move inside the body outline) and Elon's get up (lying flat is wider than a standing frame). Both were our checker, not your clips; fixed on our side (`git pull` for the updated `selfcheck/`).
- Phase 11: Amit Shah and SRK are no longer needed.
- Nothing open. We will tell you here if anything else is needed.

## 2026-10-16: phase 11, 10 of 16 approved
- Approved: `fx_money_bundle`, `fx_money_burst` (₹500 reads clearly now), `modi_reference`, `modi_run`, `modi_punch`, `salman_reference`, `salman_run`, `salman_punch`, `tower_reference`, `tower_rise` (Jio sign). Finals are in `approved/fx/` and `approved/powers_ambani/`. All passed self-check; Modi ji and Salman are already running in the game.
- Still needed for phase 11: `amitshah_reference`, `amitshah_run`, `amitshah_punch`, `srk_reference`, `srk_run`, `srk_punch` (#115 to #120, prompts in `PART3.md`). They join the Whistle Summon automatically once approved.
- Then phase 12 (SF2 moves): start with `elon_crouch.mp4` and wait.

## 2026-10-16: part 3 (read `PART3.md`)
- **Phase 11, feedback revisions (16 files):** clearer ₹500 notes (fanned, big ₹ and 500), four normal summoned characters instead of the two ghosts (Modi ji, Salman Khan, Amit Shah, Shah Rukh Khan), Jio logo on the telecom tower. The `ghost_*` files are retired once these are approved.
- **Phase 12, Street Fighter II moves (18 files):** crouch, crouch block, low sweep, punch and kick split, throw, thrown, jump kick, get up. Start with `elon_crouch.mp4` and wait.
- Trackers: the brief doc's new tabs "Feedback revisions" and "SF2 moves (part 3)".
- Self-check (`git pull`) now knows every part 3 file name; crouched and mid-air clips are sized from your approved reference.

## 2026-10-15: all 43 part 2 files approved
- Every file in `POWERS.md` (#64 to #106) is approved, including the `elon_special` re-roll (arm at waist height) and the SPACEX rocket and rupee money redos. Finals are in `approved/` (`powers_elon/`, `powers_ambani/`, `fx/`, `elon/`).
- `antilia_fly` and `fx_money_burst` had pink edges from the magenta screen; we fixed that in our converter, no re-roll needed.
- The new `baby_reference` (full-length sleepsuit) is the approved baby.
- Nothing open. We will tell you here if anything else is needed.

## 2026-10-15: self-check knows the new files
- `git pull`, then run `python selfcheck/selfcheck.py <file>` on any part 2 file: glow files on black, object and ghost references, object clips and the power clips are all checked now.
- Run each object's `_reference.png` first (like the fighters) so its clips are checked for size.

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
