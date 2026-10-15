# Elon Fighter: new powers (art brief, part 2)

2026-10-15 · Aman

Read `BRIEF.md` first: everything in it still applies (style, facing left, on the spot, file specs, approval loop, reject list) **except where this file says otherwise**. This file adds 43 new files: new powers for Elon and Ambani, plus glow effects. Every file has a spec, a checklist and a ready prompt below.

## What changed

1. **The game is now Elon vs Ambani only.** Zuckerberg and Altman are no longer being made. Stop any work on them.
2. **Each fighter gets 4 powers** instead of 1.
3. **Powers glow.** Glow, beams, trails, sparks and the two ghosts are made as separate files on a **pure black** background (see "Black files").
4. **Branding and real people are allowed only where this file asks for them:** SPACEX and the Tesla "T" on the rocket, STARLINK on the satellite, Indian ₹500 notes, and the ghosts of Modi ji and Salman Khan. Everything else in `BRIEF.md` about logos and text still applies.

## How a power plays in the game (read once)

Every power follows the same 4 beats. Knowing this tells you what each file is for.

| Beat | What the player sees | Files used |
|---|---|---|
| 1. Charge | The fighter crouches into the charge pose (existing approved clip) and a coloured aura glows around him; the screen freezes for a moment and his portrait flashes | `*_special_charge.mp4` (have) + `fx_charge_red` / `fx_charge_gold` + `fx_super_flash` |
| 2. Command | The fighter does a short gesture: whistle, key fob click, point to the sky, throw, spread arms | the power clip (`elon_babies.mp4` etc.) |
| 3. Attack | The summoned thing appears and travels across the screen to the opponent. **The game moves it; your file only shows it on the spot** | the object or character clip + its glow trail |
| 4. Impact | On contact: a glow burst, the opponent is knocked back. If the opponent blocks or dodges, the attack fades out | the impact glow file |

What this means for you:

- **Power clips** (beat 2) start from the last frame of the fighter's approved charge clip and end in the normal fighting stance. They contain only the fighter, empty hands, no effects. The game adds everything else.
- **Objects and summoned characters** (beat 3) are drawn alone, side view, facing LEFT, staying in the middle of the frame. A truck "drives" by spinning its wheels on the spot; a baby "runs" like on a treadmill. The game slides them across the screen.
- **Glow files** (beats 1, 3, 4) are separate files on black.

## Size and framing

The game sets the final size, so what matters is that the size stays the same in every frame of a file. Use these as a guide for how big things are next to the fighters.

| Thing | Size next to Elon (Elon = 1 body height) | Fill the frame |
|---|---|---|
| Baby | About one third of Elon's height (knee to hip high) | Baby about 60% of frame height |
| Ghosts | Same height as Elon | Ghost about 70% of frame height |
| Cybertruck | About 1.5 Elon heights long, roof at Elon's shoulder | Truck about 75% of frame width |
| Rocket | About half of Elon's height long | Rocket about 60% of frame width |
| Starlink satellite | About one Elon height wide | Satellite about 70% of frame width |
| Antilia | About one Elon height tall (it is a miniature) | Tower about 70% of frame height |
| Telecom tower | About 1.5 Elon heights tall | Tower about 85% of frame height, base at the bottom edge |
| ₹500 bundle | About the size of Ambani's head | Bundle about 50% of frame width |
| Glow files | Varies | Effect about 60 to 70% of the frame, centred, never touching an edge |

## Black files (new rule)

A see-through glow made on green or magenta leaves a coloured halo when we remove the background. So glows are made on black, and the game adds them on top of the scene with a "light" blend: **black becomes invisible and bright colours glow.**

| Do | Do not |
|---|---|
| Pure solid black `#000000` background, edge to edge | Dark grey, gradients, vignette, stars or smoke on the background |
| Bright, saturated, glowing colours. The brighter a pixel, the more it shows | Dark outlines or dark shading on the effect: anything dark turns see-through in the game |
| Effect centred, fully inside the frame with space around it | Effect touching or leaving the frame edge |
| Same 16-bit pixel style, chunky pixels | Smooth photoreal light, lens flares, film grain |
| Loops that loop seamlessly when marked "loop" | A pause or fade at the end of a loop |

The ghosts are made the same way, so they come out see-through and glowing. Draw them as figures made of light, not as solid people.

The self-check tool does not know black files yet. Skip it for black files until we update the kit; we check them on our side.

## File specs

| Asset type | Format | Size | Length / fps | Background |
|---|---|---|---|---|
| Power clip | MP4 (H.264) | 720p or larger, whole body in frame | Action in the first 2 s, 24 fps | Green `#00FF00` |
| Object or character reference | PNG | 1024 x 1024 or larger, square | n/a | As listed per file |
| Object or character clip | MP4 (H.264) | 720p or larger, square preferred | As listed, 24 fps | Same as its reference |
| Glow effect | MP4 (H.264) | 720p or larger, square preferred | As listed, 24 fps | Black `#000000` |

How to use the prompts: images (`.png`) are made in an image generator with the whole prompt. Clips (`.mp4`) are made in image-to-video: give the tool the image named in [brackets] as the start frame and paste the rest as the motion prompt. Glow clips have no start image: generate an image from the prompt first, then animate it with the same prompt.

---

## Elon

### Power 1: SpaceX Rocket Barrage (upgrade of the existing rocket)

**In the game:** Elon charges, then thrusts his arm forward at waist height three times; a rocket launches from his hand each time, flies straight across the screen at waist height leaving a flame trail, and explodes on the opponent (existing `fx_explosion`). The opponent jumps each rocket to dodge.

| # | File | Spec | Checklist |
|---|---|---|---|
| 69 | `elon_special.mp4` (re-roll, still open) | Starts from the last frame of `elon_special_charge.mp4`. One clean arm thrust straight forward at WAIST height (fist level with his belt), held briefly, back to stance. 1.5 to 2 s | Arm at waist, not chest. One thrust only. No sparks, no smoke, no rocket in his hand |
| 67 | `fx_rocket.mp4` (redo) | One small white rocket, side view, nose pointing LEFT, flying in place. **SPACEX** in bold black capital pixel letters along the body, reading left to right. Red **Tesla "T"** logo on the nose cone. Orange flame at the back flickering. Loop 0.5 s | Letters readable. Rocket does not move or rotate. Flame loops without a jump. No smoke on the background |
| 68 | `fx_rocket_trail.mp4` | Flame and smoke trail on black: brightest at the LEFT end (where it joins the rocket), fading to glowing smoke puffs toward the right. Loop 0.5 s | Pure black background. Trail is horizontal. No rocket in the file |

`elon_special.mp4`
```
[start from the last frame of elon_special_charge.mp4] Elon rises from the crouch and thrusts one arm straight forward toward the left at WAIST height with his fist level with his belt, in a single fast motion, holds the arm out for half a second, then returns to his fighting stance, one thrust only, no second punch, empty hand, no sparks, no smoke, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`fx_rocket.mp4`
```
16-bit SNES-era pixel art game sprite, crisp pixels, limited palette, bold dark outline, a small white rocket seen from the side with its nose pointing left, the word SPACEX in bold black capital pixel letters along the white body reading left to right, a red Tesla T logo on the nose cone, small grey fins at the back, a bright orange and yellow flame at the back flickering, the rocket stays perfectly still in the centre of the frame and only the flame moves, seamless loop, locked static camera, flat even lighting, solid flat #00FF00 green background, no shadow, no smoke, crisp pixel art, no motion blur
```

`fx_rocket_trail.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a horizontal rocket exhaust trail, white-yellow hot flame at the left end turning orange, then breaking into glowing orange-grey smoke puffs that fade toward the right end, flickering and drifting, seamless loop, centred with empty space around it, pure solid black #000000 background, locked static camera, no rocket, no characters, no text, no motion blur
```

### Power 2: Baby Army

**In the game:** Elon whistles and points forward. From behind him, 6 to 8 toddlers run across the floor in a little crowd, reach the opponent and pile on with tiny punches; each hit pops a glowing dust puff with stars. The opponent blocks or jumps over the crowd.

| # | File | Spec | Checklist |
|---|---|---|---|
| 70 | `elon_babies.mp4` | From the last charge frame: Elon rises, puts two fingers in his mouth and whistles (cheeks puffed), then points forward to the left with a big grin, back to stance. 1.5 s | Empty hands. No babies in this clip. No effects |
| 71 | `baby_reference.png` | One toddler, about knee high to Elon, realistic toddler proportions (not chibi, not a big head). Plain light-blue onesie, white nappy bump, bare feet, short tufty hair, tiny clenched fists up, determined angry little face. Tiny fighting stance facing LEFT | Full body, no green in the outfit, facing left, no toys or objects |
| 72 | `baby_run.mp4` | From the reference: the toddler runs fast on the spot like on a treadmill, arms pumping, wobbly toddler run. Loop 0.7 s | Stays centred, does not travel. Loops cleanly |
| 73 | `baby_punch.mp4` | From the reference: a quick flurry of 3 tiny punches and one little kick toward the left, back to stance. 0.6 s | Stays on the spot. Same baby as the reference |
| 74 | `fx_baby_hit.mp4` | Small cartoon impact on black: a glowing white-yellow dust puff that pops, with 3 little yellow stars spinning out. 0.4 s one-shot | Pure black. Small and cute, not violent |

`elon_babies.mp4`
```
[start from the last frame of elon_special_charge.mp4] Elon rises from the crouch, puts two fingers in his mouth and gives a loud whistle with his cheeks puffed, then points forward toward the left with a big confident grin, then returns to his fighting stance, empty hands, no other characters, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`baby_reference.png`
```
16-bit SNES-era pixel art fighting game sprite, original cartoon character, crisp pixels, limited palette, bold dark outline, full body, side view facing left, flat even lighting, solid flat #00FF00 green background, no shadow, no text, no logos, a toddler about one year old with realistic toddler proportions, plain light-blue onesie, white nappy bump, bare feet, short tufty brown hair, tiny clenched fists raised, determined angry little face, standing in a tiny fighting stance, centred with empty space around the whole body, empty hands
```

`baby_run.mp4`
```
[start from baby_reference.png] the toddler runs fast toward the left on the spot like on a treadmill, wobbly toddler steps, little arms pumping, determined face, seamless loop, locked static camera, stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`baby_punch.mp4`
```
[start from baby_reference.png] the toddler throws three quick tiny punches and one little kick toward the left, then returns to its tiny fighting stance, feet stay planted, locked static camera, stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`fx_baby_hit.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a small cartoon impact puff of glowing white and pale yellow dust that pops outward, with three little bright yellow stars spinning out of it, then fades away quickly, one-shot, centred with empty space around it, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

### Power 3: Cybertruck Ram

**In the game:** Elon clicks a key fob. A Cybertruck drives in from behind him with its headlight beam blazing, speeds across the floor and rams the opponent; a white-blue crash flash bursts on impact. The opponent jumps over it.

| # | File | Spec | Checklist |
|---|---|---|---|
| 75 | `elon_cybertruck.mp4` | From the last charge frame: Elon raises one hand holding a small black key fob at shoulder height, clicks it with his thumb, smug grin, lowers it, back to stance. 1.5 s | The fob is the only allowed prop and must be gone by the last frame (hand back in a fist). No truck in this clip |
| 65 | `cybertruck_reference.png` | Angular stainless-steel electric pickup made of flat triangular panels, sharp roof peak, side view, front pointing LEFT, black tinted windows, thin light bar across the front (unlit), big wheels, no driver visible | Facing left. No glow on the lights. No text, no badges |
| 66 | `cybertruck_drive.mp4` | From the reference: the truck drives on the spot, wheels spinning fast, body bouncing slightly on its suspension. Loop 0.5 to 1 s | Truck stays in the middle of the frame. Background never moves (no road, no scenery) |
| 76 | `fx_cybertruck_lights.mp4` | On black: a bright electric-blue headlight beam shining LEFT from a point in the middle, with white-blue speed lines streaking to the right behind it. Loop 0.5 s | No truck in the file. Pure black |
| 77 | `fx_cybertruck_crash.mp4` | On black: a big crash flash, white core bursting outward into blue-white electric sparks and small glowing metal shards, then fading. 0.8 s one-shot | Pure black. Burst stays inside the frame |

`elon_cybertruck.mp4`
```
[start from the last frame of elon_special_charge.mp4] Elon rises from the crouch and raises one hand to shoulder height holding a small black car key fob, clicks it with his thumb with a smug grin, then lowers his hand and closes it into a fist as he returns to his fighting stance, no other objects, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`cybertruck_reference.png`
```
16-bit SNES-era pixel art fighting game sprite, crisp pixels, limited palette, bold dark outline, side view facing left, flat even lighting, solid flat #00FF00 green background, no shadow, no text, no logos, an angular futuristic stainless-steel electric pickup truck made of flat triangular panels with a sharp roof peak, brushed steel grey body, black tinted windows, thin unlit light bar across the front, big dark wheels, the front of the truck points left, no driver visible, centred with empty space around it, the truck fills about 75% of the image width
```

`cybertruck_drive.mp4`
```
[start from cybertruck_reference.png] the truck drives toward the left on the spot, wheels spinning fast, body bouncing slightly on its suspension, the truck stays in the centre of the frame, no road, no scenery, seamless loop, locked static camera, stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`fx_cybertruck_lights.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a bright electric-blue headlight beam shining toward the left from a small white-hot point in the middle of the frame, with white and light-blue speed lines streaking toward the right behind it, flickering, seamless loop, centred with empty space around it, pure solid black #000000 background, locked static camera, no vehicle, no characters, no text, no motion blur
```

`fx_cybertruck_crash.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a big crash impact flash, a white-hot core bursting outward into blue-white electric sparks and small glowing metal shards flying out, then fading out, one-shot, centred with empty space around it, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

### Power 4: Starlink Strike

**In the game:** Elon points to the sky. A STARLINK satellite drops in at the top of the screen right above the opponent, hovers for a moment (a warning), then fires a cyan-white beam straight down; a glowing ring flashes where it hits the floor. The opponent walks out from under it.

| # | File | Spec | Checklist |
|---|---|---|---|
| 78 | `elon_starlink.mp4` | From the last charge frame: Elon rises and points one finger straight up at the sky, confident grin, holds briefly, back to stance. 1.5 s | Arm straight up, fully inside the frame (space above the hand). Empty hand. No effects |
| 79 | `starlink_reference.png` | Flat rectangular satellite body with one long solar panel wing, seen from the side and slightly below. **STARLINK** in white capital pixel letters on the dark body. A round beam emitter on the underside pointing straight DOWN | Letters readable. Emitter faces down. No beam drawn |
| 80 | `starlink_sat.mp4` | From the reference: hovers, bobbing gently up and down, a light glint sliding across the solar panel. Loop 1 s | Stays centred. No beam, no glow |
| 81 | `fx_starlink_beam.mp4` | On black: a vertical beam from the TOP edge to the BOTTOM edge of the frame (the only file allowed to touch edges), white-hot core, shimmering cyan edges, pulsing. Loop 0.5 s | Perfectly vertical. Same width top to bottom |
| 82 | `fx_starlink_impact.mp4` | On black: where the beam hits the floor, a flat glowing cyan ring spreads outward (seen from the side, a thin ellipse), sparks shoot up, then it fades. 0.8 s one-shot | Ring is flat, not a sphere. Pure black |

`elon_starlink.mp4`
```
[start from the last frame of elon_special_charge.mp4] Elon rises from the crouch and points one finger straight up at the sky with his arm fully raised and a confident grin, holds the pose for half a second, then returns to his fighting stance, empty hands, no effects, the raised hand stays inside the frame, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`starlink_reference.png`
```
16-bit SNES-era pixel art game sprite, crisp pixels, limited palette, bold dark outline, flat even lighting, solid flat #00FF00 green background, no shadow, a flat rectangular communications satellite with a dark grey body and one long dark-blue solar panel wing with a grid of cells, the word STARLINK in white capital pixel letters on the body, a round beam emitter on the underside pointing straight down, seen from the side and slightly below, centred with empty space around it, fills about 70% of the image width
```

`starlink_sat.mp4`
```
[start from starlink_reference.png] the satellite hovers in place, bobbing gently up and down, a small light glint slides across the solar panel, no beam, seamless loop, locked static camera, stays on the same spot, solid flat #00FF00 green background, crisp pixel art, no motion blur
```

`fx_starlink_beam.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a perfectly vertical beam of light running from the top edge to the bottom edge of the frame, a white-hot core with shimmering bright cyan edges, the beam pulses and crackles, same width from top to bottom, seamless loop, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

`fx_starlink_impact.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a flat glowing cyan ring spreading outward on the ground seen from the side as a thin wide ellipse, bright white-cyan sparks shooting upward from the centre, then fading out, one-shot, centred with empty space around it, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

### Elon charge glow

| # | File | Spec | Checklist |
|---|---|---|---|
| 83 | `fx_charge_red.mp4` | On black: a body-sized aura of red and orange energy flames rising and pulsing around an EMPTY middle (Elon stands in the middle in the game). Brighter at the bottom. Loop 1 s | Middle stays dark/empty. Pure black. Loops cleanly |

`fx_charge_red.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a tall body-sized aura of red and orange energy flames rising and pulsing in an oval around an empty dark space in the centre where a person would stand, brightest at the bottom, small embers drifting up, seamless loop, centred with empty space around it, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

---

## Ambani

### Power 1: Rupee Throw (existing power, new look)

**In the game:** unchanged: Ambani charges, then throws three bundles overhand (approved `ambani_special.mp4`). Each bundle arcs through the air with a gold sparkle trail and bursts into fluttering ₹500 notes when it hits. The opponent blocks.

| # | File | Spec | Checklist |
|---|---|---|---|
| 84 | `fx_money_bundle.mp4` (redo) | A banded stack of Indian ₹500 notes (stone-grey notes, the ₹ symbol and "500" visible on the top note), brown paper band around the middle, spinning in place. Loop 0.5 s | No green on the notes. Magenta background. Stays centred |
| 85 | `fx_money_burst.mp4` (redo) | The same bundle bursting apart, ₹500 notes fluttering outward in all directions and drifting down. 0.6 s one-shot | Notes stay inside the frame. Magenta background |
| 86 | `fx_money_trail.mp4` | On black: a short horizontal trail of golden sparkles and glints, brightest at the left end. **Same sparkles as `fx_charge_gold`** so the power looks like one set. Loop 0.5 s | Pure black. No money in the file |

`fx_money_bundle.mp4`
```
16-bit SNES-era pixel art game sprite, crisp pixels, limited palette, bold dark outline, a thick banded stack of Indian 500 rupee notes, stone-grey notes with the rupee symbol and the number 500 visible on the top note, a brown paper band around the middle, spinning in place, the stack stays in the centre of the frame, seamless loop, locked static camera, flat even lighting, solid flat #FF00FF magenta background, no shadow, crisp pixel art, no motion blur
```

`fx_money_burst.mp4`
```
16-bit SNES-era pixel art game sprite, crisp pixels, limited palette, bold dark outline, a banded stack of Indian 500 rupee notes bursting apart, the stone-grey notes flying outward in all directions and fluttering down, all notes stay inside the frame, one-shot, locked static camera, flat even lighting, solid flat #FF00FF magenta background, no shadow, crisp pixel art, no motion blur
```

`fx_money_trail.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a short horizontal trail of bright golden sparkles and four-point glints, brightest at the left end and thinning toward the right, twinkling, seamless loop, centred with empty space around it, pure solid black #000000 background, locked static camera, no money, no characters, no text, no motion blur
```

### Power 2: Whistle Summon

**In the game:** Ambani whistles. The glowing ghosts of Modi ji and Salman Khan **come running** in from behind him, one after the other, reach the opponent and each lands one big punch, then fade into sparkles. The opponent blocks.

| # | File | Spec | Checklist |
|---|---|---|---|
| 88 | `ambani_whistle.mp4` | From the last frame of `ambani_special_charge.mp4`: Ambani rises, two fingers in his mouth, gives a loud whistle, then waves forward to the left with a calm smile, back to stance. 1.5 s | Empty hands. No ghosts in this clip. No effects |
| 89 | `ghost_modi_reference.png` | Ghost of Modi ji, full body, made of white-blue light: white hair, full white beard, kurta with a sleeveless Nehru jacket, in a running pose facing LEFT, wispy glowing trail at the feet | On black. Glowing, see-through look, no dark outlines. Same height as a fighter |
| 90 | `ghost_modi_run.mp4` | From the reference: runs fast on the spot like on a treadmill, arms pumping, determined face, wispy trail flowing behind. Loop 0.7 s | Stays centred. Loops cleanly |
| 91 | `ghost_modi_punch.mp4` | From the reference: one strong straight punch toward the left, then dissolves into white-blue sparkles. 1 s | Ends with the frame fully black (faded out) |
| 92 | `ghost_salman_reference.png` | Ghost of Salman Khan, full body, made of warm gold light: muscular, short dark hair, stubble, shirtless, blue bracelet on the right wrist, in a running pose with fists ready, facing LEFT, wispy glowing trail | On black. Glowing, see-through look. Same height as a fighter |
| 93 | `ghost_salman_run.mp4` | From the reference: runs fast on the spot, fists ready, wispy trail flowing behind. Loop 0.7 s | Stays centred. Loops cleanly |
| 94 | `ghost_salman_punch.mp4` | From the reference: one big hook punch toward the left, then dissolves into golden sparkles. 1 s | Ends with the frame fully black |

If a tool refuses to draw Modi ji or Salman Khan by name, drop the name and keep the description.

`ambani_whistle.mp4`
```
[start from the last frame of ambani_special_charge.mp4] Ambani rises from the charge pose, puts two fingers in his mouth and gives a loud whistle, then waves one hand forward toward the left with a calm confident smile, then returns to his fighting stance, empty hands, no other characters, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`ghost_modi_reference.png`
```
16-bit SNES-era pixel art game sprite, crisp chunky pixels, limited palette, the glowing ghost of Narendra Modi made entirely of bright white and pale blue light, white hair and a full white beard, wearing a kurta with a sleeveless Nehru jacket, full body in a running pose with arms pumping, side view facing left, a see-through glowing spirit with a soft outer glow and a wispy glowing trail at the feet, bright colours only, no dark outlines, centred with empty space around the whole body, the figure fills about 70% of the image height, pure solid black #000000 background, no text, no logos
```

`ghost_modi_run.mp4`
```
[start from ghost_modi_reference.png] the glowing ghost runs fast toward the left on the spot like on a treadmill, arms pumping, determined face, the wispy glowing trail flows behind, seamless loop, locked static camera, stays on the same spot, pure solid black #000000 background, side view facing left, crisp pixel art, no motion blur
```

`ghost_modi_punch.mp4`
```
[start from ghost_modi_reference.png] the glowing ghost plants his feet and throws one strong straight punch toward the left, then dissolves into white and blue sparkles until the frame is completely black, locked static camera, stays on the same spot, pure solid black #000000 background, side view facing left, crisp pixel art, no motion blur
```

`ghost_salman_reference.png`
```
16-bit SNES-era pixel art game sprite, crisp chunky pixels, limited palette, the glowing ghost of Salman Khan made entirely of warm gold light, muscular build, short dark hair, stubble, shirtless, a blue bracelet on the right wrist, full body in a running pose with fists ready, side view facing left, a see-through glowing spirit with a soft outer glow and a wispy glowing trail at the feet, bright colours only, no dark outlines, centred with empty space around the whole body, the figure fills about 70% of the image height, pure solid black #000000 background, no text, no logos
```

`ghost_salman_run.mp4`
```
[start from ghost_salman_reference.png] the glowing ghost runs fast toward the left on the spot like on a treadmill, fists ready, the wispy glowing trail flows behind, seamless loop, locked static camera, stays on the same spot, pure solid black #000000 background, side view facing left, crisp pixel art, no motion blur
```

`ghost_salman_punch.mp4`
```
[start from ghost_salman_reference.png] the glowing ghost plants his feet and throws one big hook punch toward the left, then dissolves into golden sparkles until the frame is completely black, locked static camera, stays on the same spot, pure solid black #000000 background, side view facing left, crisp pixel art, no motion blur
```

### Power 3: Antilia Throw

**In the game:** Ambani lifts something huge overhead and hurls it. A mini Antilia tumbles through the air in a high arc with a gold trail and crashes down on the opponent with a dust cloud and a glowing shockwave ring. The opponent walks away from where it lands.

| # | File | Spec | Checklist |
|---|---|---|---|
| 95 | `ambani_antilia.mp4` | From the last charge frame: Ambani raises both hands overhead as if lifting something huge and heavy (strain on his face), then hurls it forward to the left in one big two-handed throw, back to stance. 1.5 s | **Empty hands: do not draw the building** (the game adds it). No effects |
| 96 | `antilia_reference.png` | Miniature of the tall Mumbai skyscraper home: a vertical stack of offset cantilevered floors, some floors jutting out, open terraces with hanging gardens, bronze and cream with glass, seen from the side, upright | **Magenta background** (it has green plants). No ground under it |
| 97 | `antilia_fly.mp4` | From the reference: the building tumbles slowly end over end in place, as if flying through the air. Loop 1 s | Stays centred while rotating. Same size all the way round |
| 98 | `fx_antilia_trail.mp4` | On black: curved glowing gold speed streaks, brightest at the left, fading to the right. Loop 0.5 s | Pure black. No building |
| 99 | `fx_antilia_crash.mp4` | On black: heavy ground crash seen from the side, a glowing orange-gold shockwave ring spreading flat along the ground, bright dust and small debris flying up, then fading. 1 s one-shot | Ring flat on the ground. Stays inside the frame |

`ambani_antilia.mp4`
```
[start from the last frame of ambani_special_charge.mp4] Ambani rises and raises both hands high overhead as if lifting something huge and heavy, straining, then hurls it forward toward the left in one big two-handed throw, then returns to his fighting stance, empty hands, no objects drawn, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`antilia_reference.png`
```
16-bit SNES-era pixel art game sprite, crisp pixels, limited palette, bold dark outline, flat even lighting, solid flat #FF00FF magenta background, no shadow, no text, no logos, a miniature of a tall modern Mumbai skyscraper home, a vertical stack of offset cantilevered floors with some floors jutting out, open terraces with green hanging gardens, bronze and cream walls with glass, seen from the side, standing upright with no ground under it, centred with empty space around it, fills about 70% of the image height
```

`antilia_fly.mp4`
```
[start from antilia_reference.png] the miniature tower tumbles slowly end over end in place as if thrown through the air, staying in the centre of the frame and the same size, seamless loop, locked static camera, stays on the same spot, solid flat #FF00FF magenta background, crisp pixel art, no motion blur
```

`fx_antilia_trail.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a short trail of curved glowing gold speed streaks, brightest at the left end and fading toward the right, shimmering, seamless loop, centred with empty space around it, pure solid black #000000 background, locked static camera, no objects, no characters, no text, no motion blur
```

`fx_antilia_crash.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a heavy crash on the ground seen from the side, a glowing orange and gold shockwave ring spreading flat and wide along the ground, bright glowing dust and small debris chunks flying up, then fading out, one-shot, centred with empty space around it, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

### Power 4: Twin Tower Beam

**In the game:** Ambani spreads his arms. Two telecom towers rise out of the floor behind him, their tip lights blink, and both fire a horizontal cyan signal beam across the screen at the opponent; a cyan flash bursts on the hit. The opponent jumps over the beams.

| # | File | Spec | Checklist |
|---|---|---|---|
| 100 | `ambani_towers.mp4` | From the last charge frame: Ambani spreads both arms wide to his sides in a commanding pose, chin up, holds briefly, back to stance. 1.5 s | Arms fully inside the frame. Empty hands. No towers in this clip |
| 101 | `tower_reference.png` | Lattice steel mobile phone tower, red and white bands, antenna panels and a small dish near the top, red light on the tip, full height, base at the bottom of the image | No ground, no cables to the edges. Unlit tip (no glow) |
| 102 | `tower_rise.mp4` | From the reference: the tower rises straight up out of the bottom edge of the frame to full height, the red tip light starts blinking, ends held at full height. 1 s | Rises straight, no wobble. Ends held. Tip blink is a small red pixel, no glow halo |
| 103 | `fx_tower_beam.mp4` | On black: a horizontal beam of bright cyan signal light shooting to the LEFT, with glowing rings pulsing along it. Loop 0.5 s | Perfectly horizontal. Pure black |
| 104 | `fx_tower_impact.mp4` | On black: a bright cyan hit flash with signal rings bursting outward, then fading. 0.6 s one-shot | Pure black. Inside the frame |

`ambani_towers.mp4`
```
[start from the last frame of ambani_special_charge.mp4] Ambani rises and spreads both arms wide to his sides in a commanding pose with his chin up, holds the pose for half a second, then returns to his fighting stance, empty hands, both arms stay inside the frame, no other objects, no effects, locked static camera, character stays on the same spot, solid flat #00FF00 green background, side view facing left, crisp pixel art, no motion blur
```

`tower_reference.png`
```
16-bit SNES-era pixel art game sprite, crisp pixels, limited palette, bold dark outline, flat even lighting, solid flat #00FF00 green background, no shadow, no text, no logos, a tall lattice steel mobile phone tower with red and white bands, rectangular antenna panels and a small dish near the top, a small red light on the tip, full height with its base at the bottom of the image, no ground, no cables, centred with empty space on both sides, fills about 85% of the image height
```

`tower_rise.mp4`
```
[start from tower_reference.png] the tower rises straight up out of the bottom edge of the frame to its full height in one smooth motion, then the small red tip light starts blinking, ends held at full height, locked static camera, stays on the same spot, solid flat #00FF00 green background, crisp pixel art, no motion blur
```

`fx_tower_beam.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a perfectly horizontal beam of bright cyan signal light shooting toward the left with a white-hot core, glowing cyan rings pulsing along the beam, seamless loop, centred with empty space above and below it, pure solid black #000000 background, locked static camera, no tower, no characters, no text, no motion blur
```

`fx_tower_impact.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a bright cyan hit flash with a white core and glowing signal rings bursting outward, then fading out, one-shot, centred with empty space around it, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

### Ambani charge glow

| # | File | Spec | Checklist |
|---|---|---|---|
| 87 | `fx_charge_gold.mp4` | On black: a body-sized warm gold aura around an EMPTY middle, small golden sparkles rising (the same sparkles as `fx_money_trail`). Loop 1 s | Middle stays empty. Pure black |

`fx_charge_gold.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a tall body-sized warm gold aura glowing in an oval around an empty dark space in the centre where a person would stand, small bright golden sparkles and four-point glints rising upward, seamless loop, centred with empty space around it, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

---

## Shared glow (both fighters)

| # | File | Spec | Checklist |
|---|---|---|---|
| 64 | `fx_hit_glow.mp4` | Small bright impact star for normal punches and kicks: white-hot core, yellow and orange spikes, pops and fades. 0.3 to 0.5 s one-shot | Pure black. Small, fast |
| 105 | `fx_block_glow.mp4` | Blocked-hit spark: white core with blue shards flying out in a half circle, fades fast. 0.3 to 0.5 s one-shot | Pure black |
| 106 | `fx_super_flash.mp4` | When any power starts: big white-gold burst of light with radiating rays exploding from the centre, then fading. 0.5 s one-shot | Pure black. Rays stay inside the frame |

`fx_hit_glow.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a small bright impact star bursting outward with a white-hot core and sharp yellow and orange spikes, pops and fades out quickly, one-shot, centred with empty space around it, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

`fx_block_glow.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a bright deflect spark with a white core and electric-blue shards flying outward in a half circle toward the right, fades out quickly, one-shot, centred with empty space around it, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

`fx_super_flash.mp4`
```
16-bit SNES-era pixel art game effect, crisp chunky pixels, bright glowing saturated colours, no dark outlines, a big burst of white and gold light exploding outward from the centre with sharp radiating rays, then fading out, one-shot, all rays stay inside the frame, pure solid black #000000 background, locked static camera, no characters, no text, no motion blur
```

---

## Delivery

Same approval loop as before: one file in `_inbox/`, verdict on the tracker, then the next file.

1. **Phase 7, test (stop here):** `fx_hit_glow.mp4` (the first black file), `cybertruck_reference.png`, `cybertruck_drive.mp4`. We check that black files and moving objects work in the game before you make the rest.
2. **Phase 8, Elon powers.**
3. **Phase 9, Ambani powers.**
4. **Phase 10, shared glow.**

Make every reference image first and get it approved before animating it.

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
| 65 | 7 | `cybertruck_reference.png` | powers_elon | Cybertruck side view, facing left | Green | image |
| 66 | 7 | `cybertruck_drive.mp4` | powers_elon | Driving on the spot, wheels spinning | Green | 0.5 to 1 s loop |
| 67 | 8 | `fx_rocket.mp4` | fx | REDO: SPACEX rocket with Tesla T on the nose | Green | 0.5 s loop |
| 68 | 8 | `fx_rocket_trail.mp4` | fx | Flame and smoke trail | Black | 0.5 s loop |
| 69 | 8 | `elon_special.mp4` | elon | RE-ROLL: arm thrust at waist height | Green | 1.5 to 2 s |
| 70 | 8 | `elon_babies.mp4` | powers_elon | Whistles and points forward | Green | 1.5 s |
| 71 | 8 | `baby_reference.png` | powers_elon | Toddler in a light-blue onesie | Green | image |
| 72 | 8 | `baby_run.mp4` | powers_elon | Toddler running on the spot | Green | 0.7 s loop |
| 73 | 8 | `baby_punch.mp4` | powers_elon | Toddler punches and kicks | Green | 0.6 s |
| 74 | 8 | `fx_baby_hit.mp4` | fx | Glowing dust puff with stars | Black | 0.4 s |
| 75 | 8 | `elon_cybertruck.mp4` | powers_elon | Clicks a key fob | Green | 1.5 s |
| 76 | 8 | `fx_cybertruck_lights.mp4` | fx | Blue headlight beam and speed lines | Black | 0.5 s loop |
| 77 | 8 | `fx_cybertruck_crash.mp4` | fx | White-blue crash flash | Black | 0.8 s |
| 78 | 8 | `elon_starlink.mp4` | powers_elon | Points to the sky | Green | 1.5 s |
| 79 | 8 | `starlink_reference.png` | powers_elon | STARLINK satellite | Green | image |
| 80 | 8 | `starlink_sat.mp4` | powers_elon | Satellite hovering | Green | 1 s loop |
| 81 | 8 | `fx_starlink_beam.mp4` | fx | Vertical cyan-white beam | Black | 0.5 s loop |
| 82 | 8 | `fx_starlink_impact.mp4` | fx | Glowing floor ring and sparks | Black | 0.8 s |
| 83 | 8 | `fx_charge_red.mp4` | fx | Elon's red-orange charge aura | Black | 1 s loop |
| 84 | 9 | `fx_money_bundle.mp4` | fx | REDO: ₹500 bundle spinning | Magenta | 0.5 s loop |
| 85 | 9 | `fx_money_burst.mp4` | fx | REDO: ₹500 notes bursting | Magenta | 0.6 s |
| 86 | 9 | `fx_money_trail.mp4` | fx | Gold sparkle trail | Black | 0.5 s loop |
| 87 | 9 | `fx_charge_gold.mp4` | fx | Ambani's gold charge aura | Black | 1 s loop |
| 88 | 9 | `ambani_whistle.mp4` | powers_ambani | Whistles with two fingers | Green | 1.5 s |
| 89 | 9 | `ghost_modi_reference.png` | powers_ambani | Ghost of Modi ji, white-blue | Black | image |
| 90 | 9 | `ghost_modi_run.mp4` | powers_ambani | Running on the spot | Black | 0.7 s loop |
| 91 | 9 | `ghost_modi_punch.mp4` | powers_ambani | Punches, then fades | Black | 1 s |
| 92 | 9 | `ghost_salman_reference.png` | powers_ambani | Ghost of Salman Khan, gold | Black | image |
| 93 | 9 | `ghost_salman_run.mp4` | powers_ambani | Running on the spot | Black | 0.7 s loop |
| 94 | 9 | `ghost_salman_punch.mp4` | powers_ambani | Hook punch, then fades | Black | 1 s |
| 95 | 9 | `ambani_antilia.mp4` | powers_ambani | Lifts and hurls (empty hands) | Green | 1.5 s |
| 96 | 9 | `antilia_reference.png` | powers_ambani | Mini Antilia | Magenta | image |
| 97 | 9 | `antilia_fly.mp4` | powers_ambani | Antilia tumbling in place | Magenta | 1 s loop |
| 98 | 9 | `fx_antilia_trail.mp4` | fx | Gold motion trail | Black | 0.5 s loop |
| 99 | 9 | `fx_antilia_crash.mp4` | fx | Dust, debris, shockwave ring | Black | 1 s |
| 100 | 9 | `ambani_towers.mp4` | powers_ambani | Spreads both arms wide | Green | 1.5 s |
| 101 | 9 | `tower_reference.png` | powers_ambani | Red and white telecom tower | Green | image |
| 102 | 9 | `tower_rise.mp4` | powers_ambani | Tower rises, ends held | Green | 1 s |
| 103 | 9 | `fx_tower_beam.mp4` | fx | Horizontal cyan signal beam | Black | 0.5 s loop |
| 104 | 9 | `fx_tower_impact.mp4` | fx | Cyan hit flash | Black | 0.6 s |
| 105 | 10 | `fx_block_glow.mp4` | fx | Blue deflect spark | Black | 0.3 to 0.5 s |
| 106 | 10 | `fx_super_flash.mp4` | fx | White-gold burst | Black | 0.5 s |

## Extra reject reasons for the new files

| Problem | Why it breaks the game | Fix |
|---|---|---|
| Black file has a grey, starry or gradient background | The background shows as a haze on top of the fight | Re-roll with "pure solid black #000000 background" |
| Dark outlines or dark parts inside a glow or ghost | They turn see-through and the effect looks hollow | Re-roll with "bright glowing colours, no dark outlines" |
| Glow inside a fighter or object clip | Halo when we remove the background | Re-roll with "no effects, no glow" |
| Object or summoned character moves across the frame | The game already moves it | Re-roll with "stays in the centre of the frame, on the spot" |
| Fighter holds the summoned thing (building, baby, truck) in his power clip | It would appear twice | Re-roll with "empty hands, no objects drawn" |
| Object changes size or shape while it moves or rotates | It pulses or morphs on screen | Re-roll with "same size all the way through" |
| SPACEX or STARLINK lettering garbled | Looks broken up close | Send the cleanest take and comment; we can add the letters in the game |
| Ghost punch does not end on a fully black frame | The ghost pops off the screen instead of fading | Re-roll with "dissolves until the frame is completely black" |
