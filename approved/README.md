# Approved files

Final, approved deliveries. Do not change these; if one needs redoing we will say so in `CHANGELOG.md`. The lineup and all 4 references are in `characters/`.

## Status (2026-10-15)

| Fighter / group | Approved | Still needed |
|---|---|---|
| Elon | idle, walk, jump, heavy, block, hit, light, special_charge, knockdown, portrait | **special** (re-roll: arm thrust at waist height) |
| Ambani | idle, walk, jump, block, hit, light, heavy, special_charge, special, knockdown, portrait | none |
| Zuckerberg | reference | everything else (phase 3) |
| Altman | reference | everything else (phase 5) |
| Effects | fx_rocket, fx_explosion, fx_money_bundle, fx_money_burst | none |
| Stages | stage_mumbai | stage_colosseum (phase 3), stage_server_farm (phase 5) |
| Menus | none yet | all 7 (phase 6) |

Note: `elon_jump.mp4` here is your clip trimmed to its first jump (the original had two jumps back to back). One action per clip, please.

## Re-roll still open

| File | Problem | Change |
|---|---|---|
| `elon_special.mp4` | The arm thrust is at chest height; the rocket must leave at waist height so it can be jumped over. | Start from the last frame of `elon_special_charge`. One arm thrust straight forward at WAIST height, hold briefly, back to stance. No second punch, no sparks, no effects. |

Prompt:

```
[start from the last frame of elon_special_charge.mp4] Elon rises from the crouch and thrusts one arm straight forward toward the left at WAIST height in a single motion, holds the arm out briefly, returns to fighting stance, no second punch, no sparks, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

## Please
- Use exact file names. Re-sends arrived as `(1)`, `(2)`, `(3)` and fail the check.
- Make sure a re-send is a new render.
- One action per clip.
- No glow, aura or light effects inside fighter clips: glows cannot be separated from the green screen. The game draws its own glows.
