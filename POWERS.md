# Elon Fighter: new powers (art brief, part 2)

2026-10-15 · Aman

Read `BRIEF.md` first: everything in it still applies (style, facing left, on the spot, file specs, approval loop, reject list) **except where this file says otherwise**. This file adds 43 new files: new powers for Elon and Ambani, plus glow effects.

## What changed

1. **The game is now Elon vs Ambani only.** Zuckerberg and Altman are no longer being made. Stop any work on them.
2. **Each fighter gets 4 powers** instead of 1. They are listed below.
3. **Powers glow.** Glow, beams, trails, sparks and the two ghosts are made as separate files on a **pure black** background (new rule, see "Black files").
4. **Branding and real people are now allowed where this file asks for them:** SPACEX and Tesla on the rocket, STARLINK on the satellite, Indian ₹500 notes, and the ghosts of Modi ji and Salman Khan. Everything else in `BRIEF.md` about logos and text still applies: no other logos, no other text.

## Black files (new rule)

A see-through glow made on green or magenta leaves a coloured halo when we remove the background. So glows are made on black, and the game adds them on top of the scene with a "light" blend: **black becomes invisible and bright colours glow.**

| Do | Do not |
|---|---|
| Pure solid black `#000000` background, edge to edge | Dark grey, gradients, vignette, stars or smoke on the background |
| Bright, saturated, glowing colours. The brighter a pixel, the more it shows | Dark outlines or dark shading on the effect itself: anything dark turns see-through in the game |
| Effect centred, fully inside the frame with space around it | Effect touching or leaving the frame edge |
| Same 16-bit pixel style, chunky pixels | Smooth photoreal light, lens flares, film grain |
| Loops that loop seamlessly when marked "loop" | A pause or fade at the end of a loop |

The ghosts are made the same way, so they come out see-through and glowing in the game. Draw them as figures made of light, not as solid people.

The self-check tool does not know black files yet. Skip it for black files until we update the kit; we check them on our side.

## File specs for the new files

| Asset type | Format | Size | Length / fps | Background | Example |
|---|---|---|---|---|---|
| Power clip (Elon or Ambani) | MP4 (H.264) | 720p or larger, whole body in frame | Action in the first 2 s, 24 fps | Green `#00FF00` | `elon_cybertruck.mp4` |
| Summoned character or object reference | PNG | 1024 x 1024 or larger, square | n/a | Green, magenta or black (see tracker) | `cybertruck_reference.png` |
| Summoned character or object clip | MP4 (H.264) | 720p or larger, square preferred | See tracker, 24 fps | Same as its reference | `cybertruck_drive.mp4` |
| Glow effect | MP4 (H.264) | 720p or larger, square preferred | See tracker, 24 fps | Black `#000000` | `fx_tower_beam.mp4` |

Rules for every new clip:

- **Power clips start from the last frame of that fighter's approved special charge clip** (`elon_special_charge.mp4` or `ambani_special_charge.mp4`), exactly like the existing special. They end back in the fighting stance.
- **No glow in fighter clips or solid objects.** All glow is in the black files.
- **Summoned characters and objects stay on the spot**, side view, facing LEFT, camera locked. The game moves them across the screen. Make the reference image first, send it for approval, then make its clips from it.
- One summoned character is drawn once (one baby, one Modi ji ghost, one Salman Khan ghost). The game makes the crowd by repeating it.

## The powers

### Elon

| Power | What happens in the game | Counter | Fighter clip | Summoned / object | Glow files (black) |
|---|---|---|---|---|---|
| **1. SpaceX Rocket Barrage** (upgrade of the existing rocket) | Elon fires 3 rockets one after another at waist height | Jump each rocket | `elon_special.mp4` (re-roll still open: arm at waist height) | `fx_rocket.mp4` (REDO): white rocket, **SPACEX** in black letters along the body, red **Tesla "T" logo** on the nose cone | `fx_rocket_trail.mp4` |
| **2. Baby Army** | Elon whistles; a crowd of toddlers runs in and swarms the opponent with tiny punches | Block, or jump the crowd | `elon_babies.mp4` | `baby_reference.png`, `baby_run.mp4`, `baby_punch.mp4` | `fx_baby_hit.mp4` |
| **3. Cybertruck Ram** | Elon clicks a key fob; a Cybertruck speeds in from behind him and rams the opponent | Jump over it | `elon_cybertruck.mp4` | `cybertruck_reference.png`, `cybertruck_drive.mp4` | `fx_cybertruck_lights.mp4`, `fx_cybertruck_crash.mp4` |
| **4. Starlink Strike** | Elon points to the sky; a **STARLINK** satellite appears above the opponent and fires a beam straight down | Walk out from under it | `elon_starlink.mp4` | `starlink_reference.png`, `starlink_sat.mp4` | `fx_starlink_beam.mp4`, `fx_starlink_impact.mp4` |
| Charge glow | Red-orange aura while Elon charges any power | n/a | (existing charge clip) | | `fx_charge_red.mp4` |

The existing `fx_explosion.mp4` (approved) is still used when a rocket hits.

### Ambani

| Power | What happens in the game | Counter | Fighter clip | Summoned / object | Glow files (black) |
|---|---|---|---|---|---|
| **1. Rupee Throw** (existing power, new look) | Same three throws; the bundles are now **Indian ₹500 notes** with a glowing sparkle trail | Block | `ambani_special.mp4` (approved, no change) | `fx_money_bundle.mp4` (REDO), `fx_money_burst.mp4` (REDO) | `fx_money_trail.mp4` (same sparkle as his charge glow) |
| **2. Whistle Summon** | Ambani whistles; the ghosts of **Modi ji** and **Salman Khan** come **running** in from behind him, punch the opponent, then fade | Block | `ambani_whistle.mp4` | `ghost_modi_reference.png`, `ghost_modi_run.mp4`, `ghost_modi_punch.mp4`, `ghost_salman_reference.png`, `ghost_salman_run.mp4`, `ghost_salman_punch.mp4` (all black) | (the ghosts glow themselves) |
| **3. Antilia Throw** | Ambani lifts a mini Antilia and hurls it in an arc onto the opponent | Walk away | `ambani_antilia.mp4` | `antilia_reference.png`, `antilia_fly.mp4` | `fx_antilia_trail.mp4`, `fx_antilia_crash.mp4` |
| **4. Twin Tower Beam** | Two telecom towers rise behind Ambani and both fire a beam at the opponent | Jump over the beams | `ambani_towers.mp4` | `tower_reference.png`, `tower_rise.mp4` | `fx_tower_beam.mp4`, `fx_tower_impact.mp4` |
| Charge glow | Gold aura with rising sparkles while Ambani charges any power | n/a | (existing charge clip) | | `fx_charge_gold.mp4` |

### Shared glow (both fighters)

| File | What it is |
|---|---|
| `fx_hit_glow.mp4` | Glowing impact star for normal hits |
| `fx_block_glow.mp4` | Blue deflect spark for blocked hits |
| `fx_super_flash.mp4` | White-gold burst when any power starts |

## How the new things look

| Thing | Look | Colours | Background |
|---|---|---|---|
| Rocket | Small white rocket, side view, nose pointing left, **SPACEX** in bold black pixel letters along the body (readable), red **Tesla "T"** logo on the nose cone, orange flame at the back | White, black lettering, red logo, orange flame | Green |
| Baby | A toddler (about knee-high to Elon) in a plain light-blue onesie, nappy bump, tiny fists, determined angry face, realistic toddler proportions | Light blue, skin tones. No green | Green |
| Cybertruck | Angular stainless-steel pickup with flat triangular panels, side view, driving toward the left, wheels spinning, headlight bar across the front | Brushed steel grey, black windows. No glow (lights are a separate file) | Green |
| Starlink satellite | Flat rectangular satellite body with one long solar panel wing, **STARLINK** in white pixel letters on the body, seen from below/side, beam emitter facing down | White, dark blue solar cells | Green |
| Ghost of Modi ji | Glowing spirit figure made of light: white hair and full white beard, kurta with a sleeveless Nehru jacket, running with arms pumping | White-blue glow | Black |
| Ghost of Salman Khan | Glowing spirit figure made of light: muscular, short dark hair, stubble, shirtless, blue bracelet on the right wrist, running with fists ready | Warm gold glow, blue bracelet | Black |
| Antilia | Mini version of the tall Mumbai tower: a stack of offset cantilevered floors with terraces and hanging gardens, seen from the side, tumbling slowly as it flies | Bronze, cream, glass, green plants | **Magenta** (it has green plants) |
| Telecom tower | Lattice steel mobile tower, red and white bands, antenna panels and dish at the top, rises out of the ground | Red, white, steel grey | Green |
| ₹500 note bundle | Banded stack of Indian ₹500 notes (stone-grey with the ₹ symbol and 500 visible), spinning in place | Stone grey, brown band | **Magenta** (as before) |

## Master prompts

**Fighter and object clips:** use the master style prompt from `BRIEF.md` (green, or magenta where the tracker says so).

**Black files:** start every black prompt with this line:

```
16-bit SNES-era pixel art game effect, crisp chunky pixels, limited palette, bright glowing saturated colours, no dark outlines, effect centred with empty space around it, pure solid black #000000 background, locked static camera, no characters, no text, no logos, no motion blur
```

For the two ghosts, replace "no characters" with the ghost description.

If a tool will not draw Modi ji or Salman Khan by name, drop the name and keep the description; the look in the table is enough. If a tool garbles the SPACEX or STARLINK lettering, send the cleanest take and say so in the tracker comment: we can stamp the letters on in the game.

## Delivery order

Same approval loop as before: one file in `_inbox/`, verdict on the tracker, then the next file.

1. **Phase 7, test (stop here):** `fx_hit_glow.mp4` (the first black file), `cybertruck_reference.png`, `cybertruck_drive.mp4`. We check that black files and moving objects work in the game before you make the rest.
2. **Phase 8, Elon powers.**
3. **Phase 9, Ambani powers.**
4. **Phase 10, shared glow.**

New folders on the shared Drive, next to the existing ones:

```
elon-fighter-art/
  powers_elon/     elon_* power clips, baby_*, cybertruck_*, starlink_*
  powers_ambani/   ambani_* power clips, ghost_*, antilia_*, tower_*
  fx/              all fx_* files (existing folder)
```

## Tracker (43 files)

| # | Phase | File | Folder | What it is | Background | Length |
|---|---|---|---|---|---|---|
| 64 | 7 | `fx_hit_glow.mp4` | fx | Glowing impact star, one-shot | Black | 0.3 to 0.5 s |
| 65 | 7 | `cybertruck_reference.png` | powers_elon | Cybertruck side view, facing left | Green | n/a |
| 66 | 7 | `cybertruck_drive.mp4` | powers_elon | Driving on the spot, wheels spinning, loop | Green | 0.5 to 1 s loop |
| 67 | 8 | `fx_rocket.mp4` | fx | REDO: SPACEX rocket with Tesla logo, flame flickering, loop | Green | 0.5 s loop |
| 68 | 8 | `fx_rocket_trail.mp4` | fx | Orange flame and smoke trail, loop | Black | 0.5 s loop |
| 69 | 8 | `elon_special.mp4` | elon | RE-ROLL: arm thrust at waist height | Green | 1.5 to 2 s |
| 70 | 8 | `elon_babies.mp4` | powers_elon | Elon whistles and points forward | Green | 1.5 s |
| 71 | 8 | `baby_reference.png` | powers_elon | Toddler in a light-blue onesie, facing left | Green | n/a |
| 72 | 8 | `baby_run.mp4` | powers_elon | Toddler running on the spot, loop | Green | 0.7 s loop |
| 73 | 8 | `baby_punch.mp4` | powers_elon | Toddler punches and kicks forward, back to stance | Green | 0.6 s |
| 74 | 8 | `fx_baby_hit.mp4` | fx | Glowing dust puff with little stars, one-shot | Black | 0.4 s |
| 75 | 8 | `elon_cybertruck.mp4` | powers_elon | Elon holds up a key fob and clicks it | Green | 1.5 s |
| 76 | 8 | `fx_cybertruck_lights.mp4` | fx | Blue headlight beam and speed lines, loop | Black | 0.5 s loop |
| 77 | 8 | `fx_cybertruck_crash.mp4` | fx | Big white-blue crash flash and sparks, one-shot | Black | 0.8 s |
| 78 | 8 | `elon_starlink.mp4` | powers_elon | Elon points to the sky | Green | 1.5 s |
| 79 | 8 | `starlink_reference.png` | powers_elon | STARLINK satellite | Green | n/a |
| 80 | 8 | `starlink_sat.mp4` | powers_elon | Satellite hovering, slight bob, panel glint, loop | Green | 1 s loop |
| 81 | 8 | `fx_starlink_beam.mp4` | fx | Vertical cyan-white beam, top to bottom of frame, loop | Black | 0.5 s loop |
| 82 | 8 | `fx_starlink_impact.mp4` | fx | Glowing ring and sparks where the beam hits the floor, one-shot | Black | 0.8 s |
| 83 | 8 | `fx_charge_red.mp4` | fx | Elon's red-orange charge aura, loop | Black | 1 s loop |
| 84 | 9 | `fx_money_bundle.mp4` | fx | REDO: ₹500 bundle spinning in place, loop | Magenta | 0.5 s loop |
| 85 | 9 | `fx_money_burst.mp4` | fx | REDO: bundle bursting into fluttering ₹500 notes, one-shot | Magenta | 0.6 s |
| 86 | 9 | `fx_money_trail.mp4` | fx | Gold sparkle trail, loop (same sparkles as `fx_charge_gold`) | Black | 0.5 s loop |
| 87 | 9 | `fx_charge_gold.mp4` | fx | Ambani's gold aura with rising sparkles, loop | Black | 1 s loop |
| 88 | 9 | `ambani_whistle.mp4` | powers_ambani | Two fingers in mouth, whistles | Green | 1.5 s |
| 89 | 9 | `ghost_modi_reference.png` | powers_ambani | Ghost of Modi ji, glowing white-blue, facing left | Black | n/a |
| 90 | 9 | `ghost_modi_run.mp4` | powers_ambani | Running on the spot, loop | Black | 0.7 s loop |
| 91 | 9 | `ghost_modi_punch.mp4` | powers_ambani | Punches forward, then fades out | Black | 1 s |
| 92 | 9 | `ghost_salman_reference.png` | powers_ambani | Ghost of Salman Khan, glowing gold, facing left | Black | n/a |
| 93 | 9 | `ghost_salman_run.mp4` | powers_ambani | Running on the spot, loop | Black | 0.7 s loop |
| 94 | 9 | `ghost_salman_punch.mp4` | powers_ambani | Punches forward, then fades out | Black | 1 s |
| 95 | 9 | `ambani_antilia.mp4` | powers_ambani | Lifts something heavy overhead with both hands and hurls it forward | Green | 1.5 s |
| 96 | 9 | `antilia_reference.png` | powers_ambani | Mini Antilia tower | Magenta | n/a |
| 97 | 9 | `antilia_fly.mp4` | powers_ambani | Antilia tumbling slowly in place, loop | Magenta | 1 s loop |
| 98 | 9 | `fx_antilia_trail.mp4` | fx | Gold motion trail, loop | Black | 0.5 s loop |
| 99 | 9 | `fx_antilia_crash.mp4` | fx | Dust, debris and glowing shockwave ring, one-shot | Black | 1 s |
| 100 | 9 | `ambani_towers.mp4` | powers_ambani | Spreads both arms wide, commanding | Green | 1.5 s |
| 101 | 9 | `tower_reference.png` | powers_ambani | Telecom tower, red and white | Green | n/a |
| 102 | 9 | `tower_rise.mp4` | powers_ambani | Tower rises out of the ground, top blinks, ends held | Green | 1 s |
| 103 | 9 | `fx_tower_beam.mp4` | fx | Horizontal cyan signal beam with pulsing rings, loop | Black | 0.5 s loop |
| 104 | 9 | `fx_tower_impact.mp4` | fx | Glowing cyan hit flash, one-shot | Black | 0.6 s |
| 105 | 10 | `fx_block_glow.mp4` | fx | Blue deflect spark, one-shot | Black | 0.3 to 0.5 s |
| 106 | 10 | `fx_super_flash.mp4` | fx | White-gold burst, one-shot | Black | 0.5 s |

## Prompts

Clips: give the tool the image in [brackets] as the start frame and paste the rest as the motion prompt. `[GREEN]` = the master style prompt from `BRIEF.md`; `[MAGENTA]` = the same with magenta; `[BLACK]` = the black master prompt above. Every clip prompt ends with: "locked static camera, stays on the same spot, side view facing left, crisp pixel art, no motion blur".

### Phase 7

`fx_hit_glow.mp4`
```
[BLACK] a small bright impact star bursting outward, white-hot core with yellow and orange spikes, pops and fades out quickly, one-shot
```

`cybertruck_reference.png`
```
[GREEN] an angular futuristic stainless-steel electric pickup truck made of flat triangular panels, side view driving toward the left, black tinted windows, thin light bar across the front (unlit), centred with empty space around it, fills about 60% of the image width
```

`cybertruck_drive.mp4`
```
[start from cybertruck_reference.png] the truck drives toward the left on the spot, wheels spinning fast, body bouncing slightly, seamless loop, locked static camera, stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

### Phase 8 (Elon)

`fx_rocket.mp4`
```
[GREEN] a small white rocket, side view, nose pointing left, the word SPACEX in bold black pixel letters along the body, a red Tesla T logo on the nose cone, orange flame at the back flickering, rocket stays centred, seamless loop
```

`fx_rocket_trail.mp4`
```
[BLACK] a horizontal rocket exhaust trail stretching to the right, bright orange and yellow flame near the left end fading into glowing grey-orange smoke puffs to the right, flickering, seamless loop
```

`elon_special.mp4`
```
[start from the last frame of elon_special_charge.mp4] Elon rises and thrusts one arm straight forward toward the left at WAIST height in a single motion, holds the arm out briefly, returns to fighting stance, no second punch, no sparks, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`elon_babies.mp4`
```
[start from the last frame of elon_special_charge.mp4] Elon puts two fingers in his mouth and whistles, then points forward toward the left with a grin, returns to fighting stance, empty hands, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`baby_reference.png`
```
[GREEN] a toddler about knee high, plain light-blue onesie, tiny clenched fists raised, determined angry little face, realistic toddler proportions, standing in a tiny fighting stance facing left, centred with empty space around the whole body
```

`baby_run.mp4`
```
[start from baby_reference.png] the toddler runs fast toward the left on the spot like on a treadmill, little arms pumping, seamless loop, locked static camera, stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`baby_punch.mp4`
```
[start from baby_reference.png] the toddler throws a quick flurry of tiny punches and a little kick toward the left, then returns to stance, locked static camera, stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`fx_baby_hit.mp4`
```
[BLACK] a small glowing cartoon dust puff with three little spinning yellow stars, pops and fades, one-shot
```

`elon_cybertruck.mp4`
```
[start from the last frame of elon_special_charge.mp4] Elon raises one hand holding a small black key fob and clicks it with a smug grin, then lowers it and returns to fighting stance, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`fx_cybertruck_lights.mp4`
```
[BLACK] a bright electric-blue horizontal headlight beam shining to the left with white-blue speed lines streaking to the right behind it, flickering, seamless loop
```

`fx_cybertruck_crash.mp4`
```
[BLACK] a big crash impact, white-blue flash bursting outward with electric sparks and small glowing metal shards, then fading, one-shot
```

`elon_starlink.mp4`
```
[start from the last frame of elon_special_charge.mp4] Elon points one finger straight up to the sky with a confident grin, holds briefly, returns to fighting stance, empty hands, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`starlink_reference.png`
```
[GREEN] a flat rectangular communications satellite with one long dark-blue solar panel wing, the word STARLINK in white pixel letters on the body, a round beam emitter on the underside pointing down, seen from the side and slightly below, centred with empty space around it
```

`starlink_sat.mp4`
```
[start from starlink_reference.png] the satellite hovers in place, bobbing gently up and down, a glint moving across the solar panel, seamless loop, locked static camera, stays on the same spot, solid flat #00FF00 green background, crisp pixel art, no motion blur
```

`fx_starlink_beam.mp4`
```
[BLACK] a vertical beam of bright cyan-white light from the top edge to the bottom edge of the frame, white-hot core, shimmering cyan edges, pulsing, seamless loop
```

`fx_starlink_impact.mp4`
```
[BLACK] a flat glowing cyan ring spreading outward on the ground seen from the side (a thin ellipse), with sparks shooting up, then fading, one-shot
```

`fx_charge_red.mp4`
```
[BLACK] a body-sized aura of red and orange energy flames rising and pulsing around an empty space in the centre, brighter at the bottom, seamless loop
```

### Phase 9 (Ambani)

`fx_money_bundle.mp4`
```
[MAGENTA] a banded stack of Indian 500 rupee notes, stone-grey notes with the rupee symbol and 500 visible, brown paper band around the middle, spinning in place, seamless loop
```

`fx_money_burst.mp4`
```
[MAGENTA] a banded stack of Indian 500 rupee notes bursting apart, stone-grey notes fluttering outward in all directions and falling, one-shot
```

`fx_money_trail.mp4`
```
[BLACK] a short horizontal trail of golden sparkles and glints stretching to the right, twinkling, seamless loop, same sparkles as a gold charge aura
```

`fx_charge_gold.mp4`
```
[BLACK] a body-sized warm gold aura glowing around an empty space in the centre, small golden sparkles rising upward, seamless loop
```

`ambani_whistle.mp4`
```
[start from the last frame of ambani_special_charge.mp4] Ambani puts two fingers in his mouth and gives a loud whistle, then gestures forward toward the left with a calm smile, returns to fighting stance, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`ghost_modi_reference.png`
```
[BLACK, replace "no characters" with:] the glowing ghost of Narendra Modi made of white-blue light, white hair and full white beard, kurta with a sleeveless Nehru jacket, full body, running pose facing left, see-through spirit with a soft glow, wispy glowing trail at the feet, centred with empty space around the whole body
```

`ghost_modi_run.mp4`
```
[start from ghost_modi_reference.png] the glowing ghost runs fast toward the left on the spot like on a treadmill, arms pumping, wispy trail flowing behind, seamless loop, locked static camera, stays on the same spot, pure solid black #000000 background, side view facing left, crisp pixel art, no motion blur
```

`ghost_modi_punch.mp4`
```
[start from ghost_modi_reference.png] the glowing ghost throws one strong punch toward the left, then fades away into sparkles, locked static camera, stays on the same spot, pure solid black #000000 background, side view facing left, crisp pixel art, no motion blur
```

`ghost_salman_reference.png`
```
[BLACK, replace "no characters" with:] the glowing ghost of Salman Khan made of warm gold light, muscular, short dark hair, stubble, shirtless, blue bracelet on the right wrist, full body, running pose with fists ready facing left, see-through spirit with a soft glow, wispy glowing trail at the feet, centred with empty space around the whole body
```

`ghost_salman_run.mp4`
```
[start from ghost_salman_reference.png] the glowing ghost runs fast toward the left on the spot like on a treadmill, fists ready, wispy trail flowing behind, seamless loop, locked static camera, stays on the same spot, pure solid black #000000 background, side view facing left, crisp pixel art, no motion blur
```

`ghost_salman_punch.mp4`
```
[start from ghost_salman_reference.png] the glowing ghost throws one big hook punch toward the left, then fades away into golden sparkles, locked static camera, stays on the same spot, pure solid black #000000 background, side view facing left, crisp pixel art, no motion blur
```

`ambani_antilia.mp4`
```
[start from the last frame of ambani_special_charge.mp4] Ambani raises both hands overhead as if lifting something huge and heavy, then hurls it forward toward the left in one big throw, returns to fighting stance, empty hands, no objects, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`antilia_reference.png`
```
[MAGENTA] a miniature version of a tall modern Mumbai skyscraper home made of a stack of offset cantilevered floors with terraces and hanging gardens, bronze and cream with glass, seen from the side, centred with empty space around it
```

`antilia_fly.mp4`
```
[start from antilia_reference.png] the tower tumbles slowly end over end in place as if thrown through the air, seamless loop, locked static camera, stays on the same spot, solid flat #FF00FF magenta background, crisp pixel art, no motion blur
```

`fx_antilia_trail.mp4`
```
[BLACK] a glowing gold motion trail of curved speed streaks stretching to the right, shimmering, seamless loop
```

`fx_antilia_crash.mp4`
```
[BLACK] a heavy crash on the ground seen from the side, a glowing orange-gold shockwave ring spreading outward, bright dust and small debris flying up, then fading, one-shot
```

`ambani_towers.mp4`
```
[start from the last frame of ambani_special_charge.mp4] Ambani spreads both arms wide to his sides in a commanding pose, holds briefly, returns to fighting stance, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`tower_reference.png`
```
[GREEN] a lattice steel mobile phone tower with red and white bands, antenna panels and a small dish near the top, red light on the tip, full height, centred with empty space around it
```

`tower_rise.mp4`
```
[start from tower_reference.png] the tower rises straight up out of the ground from the bottom of the frame to full height, the red tip light starts blinking, ends held, locked static camera, stays on the same spot, solid flat #00FF00 green background, crisp pixel art, no motion blur
```

`fx_tower_beam.mp4`
```
[BLACK] a horizontal beam of bright cyan signal light shooting to the left, with glowing rings pulsing along it, seamless loop
```

`fx_tower_impact.mp4`
```
[BLACK] a bright cyan hit flash with signal rings bursting outward, then fading, one-shot
```

### Phase 10 (shared)

`fx_block_glow.mp4`
```
[BLACK] a bright blue deflect spark, white core with blue shards flying outward in a half circle, fades quickly, one-shot
```

`fx_super_flash.mp4`
```
[BLACK] a big white-gold burst of light exploding outward from the centre with radiating rays, then fading, one-shot
```

## Extra reject reasons for the new files

| Problem | Why it breaks the game | Fix |
|---|---|---|
| Black file has a grey, starry or gradient background | The background shows as a haze on top of the fight | Re-roll with "pure solid black #000000 background" |
| Dark outlines or dark parts inside a glow or ghost | They turn see-through and the effect looks hollow | Re-roll with "bright glowing colours, no dark outlines" |
| Glow inside a fighter or object clip | Halo when we remove the background | Re-roll with "no effects, no glow" |
| Summoned object moves across the frame | The game already moves it | Re-roll with "stays on the same spot" |
| SPACEX or STARLINK lettering garbled | Looks broken up close | Send the cleanest take and comment; we can add the letters in the game |
