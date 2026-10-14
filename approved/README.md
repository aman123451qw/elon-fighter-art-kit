# Approved files

Final, approved deliveries. Do not change these; if one needs redoing we will say so in `CHANGELOG.md`. The lineup and all 4 references are in `characters/`.

## Status (2026-10-14)

| Fighter / group | Approved | Still needed |
|---|---|---|
| Elon | idle, heavy, block, hit, light, special_charge, knockdown, portrait | **walk**, **jump** (never sent), **special** (re-roll) |
| Ambani | idle, walk, jump, block, hit, light, heavy, knockdown, portrait | **special_charge**, **special** (re-roll) |
| Zuckerberg | reference | everything else (phase 3) |
| Altman | reference | everything else (phase 5) |
| Effects | fx_rocket, fx_explosion, fx_money_bundle, fx_money_burst | none |
| Stages | stage_mumbai | stage_colosseum, stage_server_farm |
| Menus | none yet | all (phase 6) |

## Re-rolls: what to change

| File | Problem | Change |
|---|---|---|
| `elon_special.mp4` | Arm fires at shoulder height but the rocket leaves at waist height; extra second punch; sparks at feet. You re-sent `elon_special_charge` 3 times instead (it was already fine). | Start from the last frame of the charge. One arm thrust straight forward at WAIST height, hold briefly, back to stance. No second punch, no sparks. |
| `ambani_special_charge.mp4` | Gold glow turned into a solid light-green disc (glow on green screen cannot be removed); feet slide sideways. | Magenta `#FF00FF` background, gold glow, feet planted. |
| `ambani_special.mp4` | Same green disc; money bundles fly through the air inside the clip (the game throws its own money); chest pushes, not overhand throws. | Magenta `#FF00FF` background, three overhand throws, cash leaves the hand and is gone, no glow, back to stance. |
| `stage_mumbai.png` (optional) | Satellite streaks sit in the top 10%, under the health bars. | Satellites between 20% and 65% of the height. |

Ready prompts for these are in `PROMPTS.md` plus the changes above.

## Please
- Use exact file names. Re-sends arrived as `(1)`, `(2)`, `(3)` and fail the check.
- Make sure a re-send is a new render: 5 of 7 re-sends so far were identical to files already sent.
