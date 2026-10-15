# Elon Fighter: part 3 (feedback revisions + Street Fighter II moves)

2026-10-16 · Aman

Read `BRIEF.md`, then `POWERS.md`, then this file. Everything there still applies. This file adds 34 files in two phases. The shared brief doc has the same content in its "Feedback revisions" and "SF2 moves (part 3)" tabs, with Status dropdowns: update those as you go.

- **Phase 11, feedback revisions (16 files, #107 to #122):** clearer rupee notes, four normal summoned characters instead of the two ghosts, Jio branding on the towers.
- **Phase 12, Street Fighter II moves (18 files, #123 to #140):** crouch, crouch block, low sweep, punch and kick split, throw, thrown, jump kick, get up.

## Phase 11: feedback revisions

| Power | Feedback | What is wrong now | Files affected | What to make |
|---|---|---|---|---|
| Ambani: Rupee Throw | Still does not look like rupees | At game size (about 110 px) the grey bundle reads as a plain block; the 500 and ₹ are too small | `fx_money_bundle.mp4`, `fx_money_burst.mp4` | A **fanned** stack of ₹500 notes with a very large ₹ and 500, the Gandhi portrait and the note's real colours. We will also draw it bigger in the game |
| Ambani: Whistle Summon | Ghosts are hard to understand; use normal Modi ji and Salman Khan, and add Amit Shah and SRK | See-through glowing ghosts lose the faces | Replaces all `ghost_*` files | Four **normal, solid** characters on green: Modi ji, Salman Khan, Amit Shah, Shah Rukh Khan. Each needs a reference, a run loop and a punch |
| Ambani: Twin Tower Beam | Right as it is; add Jio branding | Plain red and white tower | `tower_reference.png`, `tower_rise.mp4` | Same tower with a **Jio logo** (red circle, white Jio lettering) on a panel near the top |

### Prompts

`fx_money_bundle.mp4` (redo)
```
16-bit SNES-era pixel art game sprite, crisp pixels, limited palette, bold dark outline, a fanned stack of five Indian 500 rupee notes spread like a hand of cards, each note clearly showing a very large rupee symbol and the number 500 in dark ink, the Mahatma Gandhi portrait on the right of each note, stone grey notes with soft olive and brown tints, a brown paper band across the stack, the fan spins slowly in place and stays centred, seamless loop, locked static camera, flat even lighting, solid flat #FF00FF magenta background, no shadow, crisp pixel art, no motion blur
```

`fx_money_burst.mp4` (redo)
```
16-bit SNES-era pixel art game sprite, crisp pixels, limited palette, bold dark outline, a fanned stack of Indian 500 rupee notes bursting apart from the first frame, about eight large notes flying outward and fluttering down, each note clearly showing a large rupee symbol, the number 500 and the Gandhi portrait, stone grey notes with olive and brown tints, all notes stay inside the frame, one-shot, locked static camera, flat even lighting, solid flat #FF00FF magenta background, no shadow, crisp pixel art, no motion blur
```

References (one per character, green background):
```
16-bit SNES-era pixel art fighting game sprite, original caricature character, crisp pixels, limited palette, bold dark outline, full body, side view facing left, flat even lighting, solid flat #00FF00 green background, no shadow, no text, no logos, [CHARACTER], running pose facing left, realistic proportions, centred with empty space around the whole body, character fills about 70% of the image height, empty hands
```

| File | [CHARACTER] |
|---|---|
| `modi_reference.png` | Narendra Modi: white hair and full white beard, white kurta with a saffron sleeveless Nehru jacket, white pyjama, sandals, determined smile |
| `salman_reference.png` | Salman Khan: muscular, short dark hair, light stubble, shirtless, blue jeans, turquoise bracelet on the right wrist, confident grin |
| `amitshah_reference.png` | Amit Shah: short white hair, neat white beard, glasses, white kurta pyjama with a dark sleeveless jacket, serious expression |
| `srk_reference.png` | Shah Rukh Khan: wavy dark hair, light stubble, black leather jacket over a white t-shirt, dark jeans, charming smile |

Run and punch (same for all four, swap the name):
```
[start from <name>_reference.png] the character runs fast toward the left on the spot like on a treadmill, arms pumping, seamless loop, no effects, no glow, locked static camera, stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```
```
[start from <name>_reference.png] the character plants his feet and throws one big punch toward the left, then returns to the running pose, no effects, no glow, locked static camera, stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```
For `srk_punch.mp4` only: "the character first spreads both arms wide in his famous pose, then throws one big punch toward the left".

`tower_reference.png` (redo)
```
16-bit SNES-era pixel art game sprite, crisp pixels, limited palette, bold dark outline, flat even lighting, solid flat #00FF00 green background, no shadow, a tall lattice steel mobile phone tower with red and white bands, rectangular antenna panels and a small dish near the top, a square sign panel near the top showing the Jio logo (a red circle with the word Jio in white), a small red light on the tip, full height with its base at the bottom of the image, no ground, no cables, centred with empty space on both sides, fills about 85% of the image height
```

`tower_rise.mp4` (redo)
```
[start from tower_reference.png] the tower rises straight up out of the bottom edge of the frame to its full height in one smooth motion, the Jio sign stays readable, then the small red tip light starts blinking, ends held at full height, locked static camera, stays on the same spot, solid flat #00FF00 green background, crisp pixel art, no motion blur
```

If a tool will not draw a real person by name, keep the description and drop the name. If the Jio lettering comes out garbled, send the cleanest take and say so in the tracker comment.

| # | Phase | File | Folder | What it is | Background |
|---|---|---|---|---|---|
| 107 | 11 | `fx_money_bundle.mp4` | fx | REDO: fanned ₹500 notes, big ₹ and 500 | Magenta |
| 108 | 11 | `fx_money_burst.mp4` | fx | REDO: ₹500 notes bursting | Magenta |
| 109 | 11 | `modi_reference.png` | powers_ambani | Modi ji, normal (not a ghost) | Green |
| 110 | 11 | `modi_run.mp4` | powers_ambani | Running on the spot, loop | Green |
| 111 | 11 | `modi_punch.mp4` | powers_ambani | One big punch | Green |
| 112 | 11 | `salman_reference.png` | powers_ambani | Salman Khan, normal | Green |
| 113 | 11 | `salman_run.mp4` | powers_ambani | Running on the spot, loop | Green |
| 114 | 11 | `salman_punch.mp4` | powers_ambani | One big punch | Green |
| 115 | 11 | `amitshah_reference.png` | powers_ambani | Amit Shah, normal | Green |
| 116 | 11 | `amitshah_run.mp4` | powers_ambani | Running on the spot, loop | Green |
| 117 | 11 | `amitshah_punch.mp4` | powers_ambani | One big punch | Green |
| 118 | 11 | `srk_reference.png` | powers_ambani | Shah Rukh Khan, normal | Green |
| 119 | 11 | `srk_run.mp4` | powers_ambani | Running on the spot, loop | Green |
| 120 | 11 | `srk_punch.mp4` | powers_ambani | Arms-wide pose, then one big punch | Green |
| 121 | 11 | `tower_reference.png` | powers_ambani | REDO: tower with Jio logo | Green |
| 122 | 11 | `tower_rise.mp4` | powers_ambani | REDO: rises, Jio sign readable | Green |

## Phase 12: Street Fighter II moves

Start with `elon_crouch.mp4` and wait for approval. Add to every motion prompt: "locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur, no effects, no glow". Clips start from the fighter's approved reference unless the prompt says otherwise.

| # | Clip | File suffix | Action length | Loops? | What happens | Motion prompt |
|---|---|---|---|---|---|---|
| 1 | Crouch | `_crouch` | 0.5 s | No, ends held | Drops into a low crouch, knees bent, guard up | "drops quickly into a low crouch with knees bent and guard up, and holds" |
| 2 | Crouch block | `_crouch_block` | 0.5 s | No, ends held | Stays crouched, raises both forearms | "[start from the last frame of the crouch clip] stays crouched and raises both forearms to guard, and holds" |
| 3 | Low sweep | `_crouch_kick` | 1 s | No, ends crouched | Sweeps one leg along the floor | "[start from the last frame of the crouch clip] sweeps one leg along the floor toward the left in a low spinning sweep, returns to the crouch" |
| 4 | Heavy punch (Elon only) | `_punch_heavy` | 1 s | No | Wind-up and a powerful straight punch | "winds up and throws one powerful straight punch toward the left, returns to stance" |
| 5 | Light kick | `_kick_light` | 0.8 s | No | Fast low front kick | "throws one fast low front kick toward the left, returns to stance" |
| 6 | Heavy kick (Ambani only) | `_kick_heavy` | 1.2 s | No | Wind-up and a powerful side kick | "winds up and delivers a powerful side kick toward the left, returns to stance" |
| 7 | Throw | `_throw` | 1.5 s | No | Grabs and throws over the shoulder | "grabs an invisible opponent in front with both hands and throws them over his shoulder behind him, empty hands, returns to stance" |
| 8 | Thrown | `_thrown` | 1.5 s | No, ends lying flat | Grabbed and slammed onto his back | "is grabbed, lifted and slammed onto his back on the same spot, lies flat, stays down" |
| 9 | Jump kick | `_jump_kick` | 0.6 s | No, ends held | Flying kick in mid-air | "[start from the top frame of the jump clip] in mid-air with knees tucked, extends one leg in a flying kick toward the left and holds it" |
| 10 | Get up | `_getup` | 1 s | No | From lying flat to the stance | "[start from the last frame of the knockdown clip] lying flat on his back, gets up quickly to the fighting stance on the same spot" |

| # | Phase | File | Folder | What it is | Background |
|---|---|---|---|---|---|
| 123 | 12 | `elon_crouch.mp4` | elon | Crouch, ends held (make first, then wait) | Green |
| 124 | 12 | `elon_crouch_block.mp4` | elon | Crouch block, ends held | Green |
| 125 | 12 | `elon_crouch_kick.mp4` | elon | Low sweep | Green |
| 126 | 12 | `elon_punch_heavy.mp4` | elon | Heavy straight punch | Green |
| 127 | 12 | `elon_kick_light.mp4` | elon | Fast low front kick | Green |
| 128 | 12 | `elon_throw.mp4` | elon | Grab and over-the-shoulder throw | Green |
| 129 | 12 | `elon_thrown.mp4` | elon | Thrown, ends lying flat | Green |
| 130 | 12 | `elon_jump_kick.mp4` | elon | Flying kick, ends held | Green |
| 131 | 12 | `elon_getup.mp4` | elon | Gets up from lying flat | Green |
| 132 | 12 | `ambani_crouch.mp4` | ambani | Crouch, ends held | Green |
| 133 | 12 | `ambani_crouch_block.mp4` | ambani | Crouch block, ends held | Green |
| 134 | 12 | `ambani_crouch_kick.mp4` | ambani | Low sweep | Green |
| 135 | 12 | `ambani_kick_light.mp4` | ambani | Fast low front kick | Green |
| 136 | 12 | `ambani_kick_heavy.mp4` | ambani | Powerful side kick | Green |
| 137 | 12 | `ambani_throw.mp4` | ambani | Grab and over-the-shoulder throw | Green |
| 138 | 12 | `ambani_thrown.mp4` | ambani | Thrown, ends lying flat | Green |
| 139 | 12 | `ambani_jump_kick.mp4` | ambani | Flying kick, ends held | Green |
| 140 | 12 | `ambani_getup.mp4` | ambani | Gets up from lying flat | Green |

Elon needs no `_kick_heavy` (his heavy attack is already a kick) and Ambani needs no `_punch_heavy` (his heavy shove already is one).

The self-check tool does not know the phase 11 and 12 file names yet; we will update it before your first upload of each. Skip it for these files until then.
