# Elon Fighter

2026-10-13 · Aman

You are making all the art for Elon Fighter, a 2D pixel-art fighting game in the style of 1990s arcade fighters: 4 caricature fighters, 3 stages and the menu art, 63 files in total. Read the style rules and file specs once, then work through the tables row by row. Start with phase 1 only and wait for approval before making anything else.

## The game in one minute

Two fighters face each other on one screen, side view, and punch, kick and block until one runs out of health. Each fighter also has one special power. The player picks one of three matchups, and each matchup has its own stage.

| Matchup | Stage | The joke behind it |
|---|---|---|
| Elon vs Mark Zuckerberg | Roman Colosseum | The cage fight they talked about in 2023 and never had |
| Elon vs Mukesh Ambani | Mumbai rooftop with telecom towers and satellites | Satellite internet vs mobile towers: who connects India |
| Elon vs Sam Altman | Glowing AI server farm | Co-founders turned rivals |

Elon is in all three fights, so he is built once and used everywhere.

**How your files get used.** You do not need to make sprite sheets or touch any game files.

1. You make one reference image per fighter.
2. You turn that image into short video clips, one clip per move (punch, kick, jump and so on), using an image-to-video tool such as Higgsfield, Kling or Runway.
3. A script on our side cuts each clip into 6 to 12 still frames, removes the green or magenta background, sharpens the pixels and packs them for the game.

So what matters most is that every clip is clean: solid background, locked camera, the same character every time.

## Style rules for every file

Everything should look like it came from one 16-bit console game: original pixel-art caricatures, playful and not mean. These rules apply to every image and every clip.

| Rule | Do | Do not |
|---|---|---|
| Art style | 16-bit pixel art, crisp pixels, limited colour palette, bold dark outlines | Photoreal, 3D render, smooth airbrushed look, anime |
| Proportions | Realistic proportions, exactly as in the finalised references (characters/ in the kit repo). Do not drift toward bigger heads | Grotesque or insulting features, chibi babies, giant heads |
| Camera | Side view, character turned about three-quarters toward camera, full body, camera never moves | Zoom, pan, orbit, shaky cam, close-ups in move clips |
| Facing | Every fighter faces screen LEFT in every image, clip and portrait. The game mirrors them automatically. | Mixing directions between files of one fighter |
| Background | Solid flat chroma green #00FF00 for Elon, Ambani and Zuckerberg clips and the explosion effect. Solid flat magenta #FF00FF for ALL Altman files (his teal glow fringes on green) and for both money effects. Portraits have their own painted background (see the portraits section). | Gradients, floor shadows, scenery, vignettes behind fighters |
| Lighting | Flat, even, front light, the same in every clip | Rim lights that pick up the screen colour, dramatic shadows, colour shifts between clips |
| Props | Only things that stay in every clip (Ambani's watch). Effects like sparks and glow are fine. | Any object that appears in one clip and vanishes in the next (goggles, briefcase, remote) |
| Branding | Generic items only: a plain rocket, made-up banknotes | Any real logo or trademark (Tesla, SpaceX, X, Meta, Facebook, Jio, Reliance, OpenAI, ChatGPT), real currency designs |
| Originality | Our own characters and stages | Copying Street Fighter characters, stages, UI or any other game's art |
| Text | None in the art, except the game logo | Words, names, watermarks or captions baked into images |

**Master style prompt.** Start every image prompt with this line, then add the specific description from the tables below:

```
16-bit SNES-era pixel art fighting game sprite, original caricature character, crisp pixels, limited palette, bold dark outline, full body, side view facing left, flat even lighting, solid flat #00FF00 green background, no shadow, no text, no logos
```

For Altman and the money effects, swap "#00FF00 green" for "#FF00FF magenta" in that line. When a tool will not generate a real person, keep the same description and drop the name. The outfit, hair and colours in the fighter table are enough for the caricature to read.

Do not fight the tool if pixels come out a little soft. Our script sharpens frames back into crisp pixel art, and we judge the look in the game, not in the raw video.

## File specs

Use these exact formats so the files drop straight into our script. Fighter names in file names are always `elon`, `ambani`, `zuckerberg` or `altman`.

| Asset type | Tool | Format | Size | Length / fps | Background | File name example |
|---|---|---|---|---|---|---|
| Style lineup (all 4 together) | Image generator | PNG | 2048 x 1024 | n/a | Solid green #00FF00 | `lineup.png` |
| Fighter reference | Image generator | PNG | 1024 x 1024 or larger, square | n/a | Green, magenta for Altman | `elon_reference.png` |
| Move clip | Image-to-video, started from the reference image (special: from the last frame of the charge clip) | MP4 (H.264), or a folder of transparent PNG frames if your tool removes backgrounds | Any shape, 720p or larger, whole body always in frame | The tool's shortest length is fine (often 5 s). The action happens once in the first 2 to 3 s. 24 fps or more | Green, magenta for Altman | `elon_heavy.mp4` |
| Effect clip (rocket, explosion, money) | Image-to-video | MP4 (H.264) | Any shape, 720p or larger | Shortest length the tool allows, 24 fps or more | Green for rocket and explosion, magenta for money | `fx_rocket.mp4` |
| Portrait | Image generator | PNG | 1254 x 1254 square | n/a | Painted plain background in the fighter's colours | `elon_portrait.png` |
| Stage background | Image generator (upscale if needed) | PNG | 2048 x 768 (8:3, wider than the screen) | n/a | The scene itself, no characters | `stage_colosseum.png` |
| Matchup card | Image generator | PNG | 1330 x 1182 | n/a | Full illustrated card | `card_elon_vs_zuckerberg.png` |
| Mode card | Image generator | PNG | 1330 x 1182 | n/a | Full illustrated card | `mode_1v1.png` |
| Game logo | Image generator | PNG | 1600 x 600 | n/a | Transparent, or solid green | `logo.png` |
| Title screen art | Image generator | PNG | 1920 x 1080 | n/a | Full illustration | `title.png` |

**Rules for every move clip**

- Start every clip from that fighter's approved reference image. The one exception: the special clip starts from the last frame of that fighter's special charge clip, so the glow carries on.
- Everything happens on the spot. Walking is on the spot like a treadmill. Hit reactions, knockdowns and lunges also stay on the spot: the game moves the fighter, so movement inside the clip would double it. Only the jump leaves the ground, and it lands on the same spot.
- Attacks start and end in the fighting stance from the reference image.
- Make the action fill the clip: no long pause before or after the move. The game shows a punch in under half a second, so a slow start means the strike itself gets skipped. Clips marked "ends held" are the only exception.
- If your tool only makes 5 or 10 s clips, trim to the action, or send it untrimmed and write the start and end time of the action in the file's notes.
- Keep the whole body inside the frame for the entire clip, with space above the head, below the feet and in front of the fists.
- Keep the full-quality export. Do not add music, captions or transitions.

## The four fighters

Each fighter needs one reference image that every later clip is made from, so spend time getting it right and send it for approval before animating. Make all four side by side in one lineup image first so they share a scale and style, then make each reference on its own.

| Fighter | Look and outfit | Colours | Stance and personality | Light attack | Heavy attack | Special power |
|---|---|---|---|---|---|---|
| **Elon** (in all 3 fights) | Tall, broad shoulders, short dark hair swept back, big confident grin. Plain black t-shirt, dark jeans, black boots, red wristband | Black, charcoal, red wristband as the one accent | Cocky showman: fists up, bouncing on his feet | Quick straight punch | High front kick | Rocket launch |
| **Mukesh Ambani** | Solid build, grey hair combed back, calm smile. Crisp white shirt, dark navy trousers, polished shoes, gold wristwatch | White, navy, gold | Unbothered and calm: hands loosely raised, barely moves until he strikes | Open-palm strike | Two-handed heavy shove (on the spot) | Throwing money |
| **Mark Zuckerberg** | Lean and athletic, short curly brown hair, focused stare. Plain grey t-shirt, dark fight shorts, MMA gloves, bare feet | Heather grey, dark blue | Disciplined martial artist: low guard, knees bent | Fast jab | High roundhouse kick, no spin (the spin is saved for his special) | Jiu-jitsu spin combo |
| **Sam Altman** | Slim, short brown hair, calm half smile. Plain navy crewneck sweater, jeans, white sneakers | Navy, teal glow accents. Magenta background for all his files | Quiet and calculating: relaxed guard, minimal movement | Quick punch | Front push kick | AI hologram clone |

**Reference image prompt** (one per fighter): master style prompt + this line, with the fighter's look from the table:

```
[fighter look and outfit], standing in a relaxed fighting stance, fists up, weight on back foot, facing left, centred with empty space around the whole body, character fills about 70% of the image height
```

Approval checklist for each reference: full body visible, facing left, flat green background (magenta for Altman), no shadow, outfit and colours match the table, no logos, nothing in the hands.

## Animation shot list (10 clips per fighter)

Every fighter needs the same 10 clips, so 40 in total. There is no crouching in this game, so there are no crouch or low-block clips. Make each clip from the fighter's reference image with the motion prompt in the last column. For the light attack, heavy attack and special, use the move named for that fighter in the fighter table.

| # | Clip | File suffix | Action length | Loops? | What happens | Motion prompt (add to every clip: "locked static camera, character stays on the same spot, solid flat [green or magenta] background, side view facing left, crisp pixel art, no motion blur") |
|---|---|---|---|---|---|---|
| 1 | Idle | `_idle` | 2 to 3 s | Yes, last frame matches first | Fighting stance from the fighter table, gentle breathing bounce | "breathes and bounces lightly in fighting stance, seamless loop" |
| 2 | Walk forward | `_walk` | 2 s | Yes | Steps toward screen left on the spot, guard up. The game plays this backwards for walking back, so no separate clip | "walks forward on the spot like on a treadmill, guard up, seamless loop" |
| 3 | Jump | `_jump` | 1.5 s | No | Bends knees, jumps straight up, tucks legs at the top, lands on the same spot | "jumps straight up, tucks knees at the top, lands back on the same spot" |
| 4 | Block | `_block` | 1 s | No, ends held | Raises both forearms in front of the face and chest | "quickly raises both forearms to guard face and chest and holds" |
| 5 | Hit reaction | `_hit` | 1 s | No | Head snaps back from a hit to the face, recovers to stance, feet stay planted | "gets hit in the face, head snaps back, feet stay planted, recovers to fighting stance" |
| 6 | Light attack | `_light` | 1 s | No | Fast strike toward screen left, back to stance | "throws one fast [light attack] toward the left, returns to stance" |
| 7 | Heavy attack | `_heavy` | 1.5 s | No | Short wind-up, powerful strike toward screen left, back to stance | "winds up and delivers a powerful [heavy attack] toward the left, returns to stance" |
| 8 | Special charge | `_special_charge` | 1 to 1.5 s | No, ends held | Powers up for the special (see the special powers section) | See special powers section |
| 9 | Special | `_special` | 1.5 to 2.5 s | No, ends in stance | The special move itself. Starts from the last frame of the charge clip | See special powers section |
| 10 | Knockdown | `_knockdown` | 2 s | No, ends lying flat | Hit hard, falls flat on the back on the same spot, stays down | "takes a huge hit and falls straight backward onto the ground on the same spot, lies flat, stays down" |

## Special powers

Each special is two fighter clips: the charge, then the move, which starts from the last frame of the charge. Elon and Ambani also need separate effect clips that the game flies across the screen. Altman's hologram is made by the game from his own sprites, so it needs no effect clip. Each special has a different counter, which sets the height the effect travels at.

| Fighter | How the opponent stops it | Special charge clip (`_special_charge`) | Special clip (`_special`) | Effect clips |
|---|---|---|---|---|
| **Elon: Rocket launch** | Jump over it. The rocket flies straight at waist height | Bends his knees, sparks and chunky pixel smoke burst at his feet, holds | Rises and thrusts one arm forward toward the left at waist height, as if firing, then returns to stance | `fx_rocket.mp4`: a small plain white rocket, side view, nose pointing left, orange flame at the back, flame flickering, rocket stays centred. `fx_explosion.mp4`: a chunky pixel-art explosion that bursts and fades. Both on green |
| **Ambani: Throwing money** | Block it. The money flies in a high arc and comes down at chest height | Fans out a glowing gold stack of cash between both hands, holds | Three big overhand throws toward the left, one after another, then returns to stance | `fx_money_bundle.mp4`: a strapped bundle of made-up gold and orange banknotes spinning in place. `fx_money_burst.mp4`: the bundle bursting into fluttering notes. Both on magenta. No green notes |
| **Zuckerberg: Jiu-jitsu spin combo** | Block it. It is a close-range combo | Eyes glow blue, sinks into a wide low stance, holds | A fast spinning combo on the spot: a strike, a sweep and a final spinning kick, then back to stance. The game moves him forward | None |
| **Altman: AI hologram clone** | Block it. A teal copy of him dashes across the screen | Raises one hand, glowing teal lines and particles swirl around him, holds | Thrusts his palm toward the left and holds the pose, then returns to stance | None. The game builds the hologram from his own clips |

Rules for effect art:

- Same 16-bit pixel style and outline as the fighters.
- The object stays centred and the camera does not move. The game handles the flying.
- Banknotes are invented designs in gold and orange: no real currency, faces, emblems or numbers from real notes.
- The rocket is plain, with no logos or text.
- No props in the fighter clips: no goggles, briefcase, remote or anything else that would vanish in the next clip.

## Stages

Each stage is one wide image, 2048 x 768, that scrolls a little as the fighters move. The fighters' feet stand on a line 77% of the way down the image, so the floor must be flat and walkable from about 65% down to the bottom, across the full width. The health bars and portraits cover the top 20% of the screen, so put landmarks (towers, satellites, arches) between 20% and 65% of the height.

| Stage | File | Matchup | What it shows | Time and mood | Stage prompt (after the master style line, but replace "green background" with this scene) |
|---|---|---|---|---|---|
| Roman Colosseum | `stage_colosseum.png` | Elon vs Zuckerberg | Sandy arena floor in front, curved stone arches and tiers of cheering pixel crowd behind, banners in plain colours, torches | Late afternoon, warm golden light | "wide 2D fighting game stage, inside a Roman Colosseum, flat sandy arena floor across the full width at the bottom, stone arches and cheering crowd in the stands behind, torches, golden afternoon light, no characters, no text" |
| Mumbai rooftop | `stage_mumbai.png` | Elon vs Ambani | Concrete rooftop floor with water tanks and a few marigold garlands, Mumbai skyline behind with telecom towers blinking red, sea on one side, several satellites and their streaks crossing the sky | Dusk, orange to purple sky | "wide 2D fighting game stage, Mumbai rooftop at dusk, flat concrete rooftop floor across the full width at the bottom, water tanks, marigold garlands, city skyline with tall telecom towers blinking red lights, satellites streaking across the purple sky, no characters, no text" |
| AI server farm | `stage_server_farm.png` | Elon vs Altman | Polished dark floor with a faint reflection, rows of tall server racks with blinking teal and white lights, thick cables overhead, cooling fans | Night, cool teal and blue light | "wide 2D fighting game stage, inside a huge AI data centre, flat polished dark floor across the full width at the bottom, rows of tall server racks with blinking teal lights, cables overhead, cool blue glow, no characters, no text" |

Rules for stages:

- No people in the foreground and nothing standing on the fight floor (the crowd stays in the stands).
- Keep the middle of the image calm, without bright spots behind where the fighters stand, so they stay easy to read.
- Nothing important in the top 20% (hidden behind the health bars).
- Keep the bottom-left and bottom-right corners plain: on phones, the touch buttons sit there.
- The camera stops at both ends, so the ends do not need to join up.
- If the tool cannot output 2048 x 768, make the widest image it can at the same 8:3 shape and upscale, keeping the pixel look.

## Portraits, cards, logo and title art

These are still images for the menus, the health bar and the special-move flash. Make them from the approved reference images so the faces match the fighters.

| Asset | Files | Size | What it shows | Where it appears |
|---|---|---|---|---|
| Portrait (x4) | `elon_portrait.png`, `ambani_portrait.png`, `zuckerberg_portrait.png`, `altman_portrait.png` | 1254 x 1254 | Head and upper body facing LEFT, face large and in the upper half, slightly more detailed pixel art than the sprites. Plain painted background in the fighter's colours: Elon charcoal with a red glow, Ambani navy with gold, Zuckerberg blue-grey, Altman navy with teal. Poses: Elon grinning, thumb pointing at himself. Ambani arms folded, calm smile. Zuckerberg fists up in a fighting guard. Altman hand raised with a faint teal glow | Health bar, character select and the full-screen flash when a special fires |
| Matchup card (x3) | `card_elon_vs_zuckerberg.png`, `card_elon_vs_ambani.png`, `card_elon_vs_altman.png` | 1330 x 1182 | Elon always on the LEFT facing right, his rival on the right facing left, mid-pose, their stage behind them, a lightning-split down the middle. Use the whole card; the game puts the title underneath | The "pick a matchup" screen |
| Mode card (x2) | `mode_1v1.png`, `mode_vs_cpu.png` | 1330 x 1182 | 1v1: two of the fighters squaring up, two arcade joysticks in the foreground. vs CPU: one fighter facing a glowing pixel robot silhouette | The "choose mode" screen |
| Game logo | `logo.png` | 1600 x 600 | The words ELON FIGHTER in a bold arcade fighting-game style, chunky pixel letters with a fiery red and gold outline. The only file allowed to contain text | Title screen and menus |
| Title screen | `title.png` | 1920 x 1080 | All four fighters in a group action pose, Elon in the centre, a city skyline at dusk behind. Leave the top third clear for the logo, which the game places on top | First screen of the game |

No text goes into any of these images except the logo. All names and titles are added by the game.

## Delivery

There are 63 files. Work in this order and send each phase for approval before starting the next. Phase 1 is a test: we put your files into the game and approve what we see there, so a problem is caught after 4 files, not 60.

1. **Test (stop here):** `lineup.png`, `elon_reference.png`, `elon_idle.mp4`, `elon_heavy.mp4`. Wait while we check them inside the game.
2. **Elon complete:** his other 8 clips, `fx_rocket.mp4`, `fx_explosion.mp4`, `elon_portrait.png`.
3. **Zuckerberg + Colosseum:** reference, 10 clips, portrait, `stage_colosseum.png`.
4. **Ambani + Mumbai:** reference, 10 clips, `fx_money_bundle.mp4`, `fx_money_burst.mp4`, portrait, `stage_mumbai.png`.
5. **Altman + server farm:** reference (magenta), 10 clips (magenta), portrait, `stage_server_farm.png`.
6. **Menus:** 3 matchup cards, 2 mode cards, `logo.png`, `title.png`.

| Asset | Count |
|---|---|
| Style lineup | 1 |
| Fighter references | 4 |
| Move clips (10 x 4 fighters) | 40 |
| Effect clips (rocket, explosion, money bundle, money burst) | 4 |
| Portraits | 4 |
| Stages | 3 |
| Matchup cards | 3 |
| Mode cards | 2 |
| Logo | 1 |
| Title screen | 1 |
| **Total** | **63** |

**Exact file names for each fighter** (swap `elon` for `ambani`, `zuckerberg` or `altman`). Use these names exactly, all lower case:

```
elon_reference.png      elon_portrait.png
elon_idle.mp4           elon_walk.mp4           elon_jump.mp4
elon_block.mp4          elon_hit.mp4            elon_knockdown.mp4
elon_light.mp4          elon_heavy.mp4
elon_special_charge.mp4 elon_special.mp4
```

**Folder layout** (one shared Drive folder, exactly these names):

```
elon-fighter-art/
  _inbox/     the ONE file waiting for approval (you upload here)
  00_style/   lineup.png
  elon/       the 12 files above
  ambani/     the same 12 files for Ambani
  zuckerberg/ the same 12 files for Zuckerberg
  altman/     the same 12 files for Altman
  fx/         fx_rocket.mp4, fx_explosion.mp4, fx_money_bundle.mp4, fx_money_burst.mp4
  stages/     stage_colosseum.png, stage_mumbai.png, stage_server_farm.png
  menus/      card_elon_vs_zuckerberg.png, card_elon_vs_ambani.png, card_elon_vs_altman.png,
              mode_1v1.png, mode_vs_cpu.png, logo.png, title.png
  _rejects/   alternate takes and anything you are unsure about
```

Approved files are moved from `_inbox/` into their final folder by us, not by you.

Only the final take of each file goes in the main folders, under the exact name. Every other take goes in `_rejects/`, never named `v2`, `final` or similar.

## How approval works

Every file is approved on its own before you start the next one. We approve what the file looks like inside the actual game, not the raw video, so each file goes through the same loop.

1. **Make the file** and name it exactly as in the tracker below.
2. **Upload it** to `elon-fighter-art/_inbox/` on the shared Drive. Only one file in the inbox at a time.
3. **Set its Status to "Sent for approval"** in the tracker. If the clip is longer than the action, add a comment on its row with the start and end time of the action.
4. **We run it through the game.** Our script checks it automatically, converts it, and we load it into the game and play it.
5. **You get a verdict on the same row,** usually within 2 working hours:
  - **Approved:** we move it into its final folder. Start the next file in the tracker.
  - **Re-roll:** a comment on the row says exactly what failed (from the reject list) and what to change. Fix it and send it again the same way.

What we check for each kind of file:

| File type | Automatic checks (script) | In-game check (us) |
|---|---|---|
| Fighter reference | Name, size, background is one flat colour, body fully in frame, nothing in the hands | Looks like the lineup, caricature reads, colours match the fighter table |
| Move clip | Name, length, background removes cleanly with no fringes, body stays in frame, no camera zoom, no drift off the spot, same size as the reference, idle and walk loop without a jump | The move plays correctly in a match: timing feels right, the hit lands where it looks like it lands, the character does not slide or pop |
| Effect clip | Name, background removes cleanly, object stays centred | Flies at the right height and looks right when it hits |
| Portrait | Name, size, facing left | Reads clearly in the small health-bar frame and in the full-screen special flash |
| Stage | Name, size 2048 x 768 | Fighters' feet sit on the floor, nothing important hidden under the health bars, fighters stay easy to see |
| Cards, logo, title | Name, size | Look right in the menus at real size |

Phase 1 (the 4 test files) can take a day to review, because it sets the look and the pipeline for everything after it. From phase 2 on, expect a verdict within 2 working hours.

## Master asset tracker

Every one of the 63 files, in the order to make them. Update the Status column as you go by picking a value from the dropdown in each row. A file is only done when it says Approved.

| # | Phase | File | Folder | What it is | Background | Status |
|---|---|---|---|---|---|---|
| 1 | 1 | `lineup.png` | 00_style | All 4 fighters side by side, style test | Green | Not started |
| 2 | 1 | `elon_reference.png` | elon | Elon full-body reference | Green | Not started |
| 3 | 1 | `elon_idle.mp4` | elon | Idle loop | Green | Not started |
| 4 | 1 | `elon_heavy.mp4` | elon | Heavy attack: high front kick | Green | Not started |
| 5 | 2 | `elon_walk.mp4` | elon | Walk forward, on the spot | Green | Not started |
| 6 | 2 | `elon_jump.mp4` | elon | Jump straight up | Green | Not started |
| 7 | 2 | `elon_block.mp4` | elon | Block, ends held | Green | Not started |
| 8 | 2 | `elon_hit.mp4` | elon | Hit reaction | Green | Not started |
| 9 | 2 | `elon_light.mp4` | elon | Light attack: straight punch | Green | Not started |
| 10 | 2 | `elon_special_charge.mp4` | elon | Special charge, ends held | Green | Not started |
| 11 | 2 | `elon_special.mp4` | elon | Special move: rocket launch pose | Green | Not started |
| 12 | 2 | `elon_knockdown.mp4` | elon | Knockdown, ends lying flat | Green | Not started |
| 13 | 2 | `fx_rocket.mp4` | fx | Rocket flying left, looping flame | Green | Not started |
| 14 | 2 | `fx_explosion.mp4` | fx | Pixel explosion | Green | Not started |
| 15 | 2 | `elon_portrait.png` | elon | Portrait, thumb at himself | Painted, charcoal + red | Not started |
| 16 | 3 | `zuckerberg_reference.png` | zuckerberg | Zuckerberg full-body reference | Green | Not started |
| 17 | 3 | `zuckerberg_idle.mp4` | zuckerberg | Idle loop | Green | Not started |
| 18 | 3 | `zuckerberg_walk.mp4` | zuckerberg | Walk forward, on the spot | Green | Not started |
| 19 | 3 | `zuckerberg_jump.mp4` | zuckerberg | Jump straight up | Green | Not started |
| 20 | 3 | `zuckerberg_block.mp4` | zuckerberg | Block, ends held | Green | Not started |
| 21 | 3 | `zuckerberg_hit.mp4` | zuckerberg | Hit reaction | Green | Not started |
| 22 | 3 | `zuckerberg_light.mp4` | zuckerberg | Light attack: fast jab | Green | Not started |
| 23 | 3 | `zuckerberg_heavy.mp4` | zuckerberg | Heavy attack: high roundhouse, no spin | Green | Not started |
| 24 | 3 | `zuckerberg_special_charge.mp4` | zuckerberg | Special charge, ends held | Green | Not started |
| 25 | 3 | `zuckerberg_special.mp4` | zuckerberg | Special move: spin combo on the spot | Green | Not started |
| 26 | 3 | `zuckerberg_knockdown.mp4` | zuckerberg | Knockdown, ends lying flat | Green | Not started |
| 27 | 3 | `zuckerberg_portrait.png` | zuckerberg | Portrait, fists up | Painted, blue-grey | Not started |
| 28 | 3 | `stage_colosseum.png` | stages | Colosseum stage, 2048 x 768 | Scene | Not started |
| 29 | 4 | `ambani_reference.png` | ambani | Ambani full-body reference | Green | Not started |
| 30 | 4 | `ambani_idle.mp4` | ambani | Idle loop | Green | Not started |
| 31 | 4 | `ambani_walk.mp4` | ambani | Walk forward, on the spot | Green | Not started |
| 32 | 4 | `ambani_jump.mp4` | ambani | Jump straight up | Green | Not started |
| 33 | 4 | `ambani_block.mp4` | ambani | Block, ends held | Green | Not started |
| 34 | 4 | `ambani_hit.mp4` | ambani | Hit reaction | Green | Not started |
| 35 | 4 | `ambani_light.mp4` | ambani | Light attack: open-palm strike | Green | Not started |
| 36 | 4 | `ambani_heavy.mp4` | ambani | Heavy attack: two-handed shove | Green | Not started |
| 37 | 4 | `ambani_special_charge.mp4` | ambani | Special charge, ends held | Green | Not started |
| 38 | 4 | `ambani_special.mp4` | ambani | Special move: three money throws | Green | Not started |
| 39 | 4 | `ambani_knockdown.mp4` | ambani | Knockdown, ends lying flat | Green | Not started |
| 40 | 4 | `fx_money_bundle.mp4` | fx | Spinning bundle of gold and orange notes | Magenta | Not started |
| 41 | 4 | `fx_money_burst.mp4` | fx | Bundle bursting into notes | Magenta | Not started |
| 42 | 4 | `ambani_portrait.png` | ambani | Portrait, arms folded | Painted, navy + gold | Not started |
| 43 | 4 | `stage_mumbai.png` | stages | Mumbai rooftop stage, 2048 x 768 | Scene | Not started |
| 44 | 5 | `altman_reference.png` | altman | Altman full-body reference | Magenta | Not started |
| 45 | 5 | `altman_idle.mp4` | altman | Idle loop | Magenta | Not started |
| 46 | 5 | `altman_walk.mp4` | altman | Walk forward, on the spot | Magenta | Not started |
| 47 | 5 | `altman_jump.mp4` | altman | Jump straight up | Magenta | Not started |
| 48 | 5 | `altman_block.mp4` | altman | Block, ends held | Magenta | Not started |
| 49 | 5 | `altman_hit.mp4` | altman | Hit reaction | Magenta | Not started |
| 50 | 5 | `altman_light.mp4` | altman | Light attack: quick punch | Magenta | Not started |
| 51 | 5 | `altman_heavy.mp4` | altman | Heavy attack: front push kick | Magenta | Not started |
| 52 | 5 | `altman_special_charge.mp4` | altman | Special charge, ends held | Magenta | Not started |
| 53 | 5 | `altman_special.mp4` | altman | Special move: palm thrust | Magenta | Not started |
| 54 | 5 | `altman_knockdown.mp4` | altman | Knockdown, ends lying flat | Magenta | Not started |
| 55 | 5 | `altman_portrait.png` | altman | Portrait, hand raised, teal glow | Painted, navy + teal | Not started |
| 56 | 5 | `stage_server_farm.png` | stages | Server farm stage, 2048 x 768 | Scene | Not started |
| 57 | 6 | `card_elon_vs_zuckerberg.png` | menus | Matchup card, Elon on the left | Full illustration | Not started |
| 58 | 6 | `card_elon_vs_ambani.png` | menus | Matchup card, Elon on the left | Full illustration | Not started |
| 59 | 6 | `card_elon_vs_altman.png` | menus | Matchup card, Elon on the left | Full illustration | Not started |
| 60 | 6 | `mode_1v1.png` | menus | Mode card: 1 vs 1 | Full illustration | Not started |
| 61 | 6 | `mode_vs_cpu.png` | menus | Mode card: vs CPU | Full illustration | Not started |
| 62 | 6 | `logo.png` | menus | ELON FIGHTER logo, 1600 x 600 | Transparent or green | Not started |
| 63 | 6 | `title.png` | menus | Title screen, 1920 x 1080 | Full illustration | Not started |

Before marking any clip Sent for approval, check it against the reject list below.

## Reject list

Re-roll any clip that shows one of these problems. They break the game even when the clip looks good as a video.

| Problem | Why it breaks the game | Fix |
|---|---|---|
| Camera zooms, pans or shakes | The character changes size between frames and jitters in game | Add "locked static camera, no zoom" and re-roll |
| Character drifts, staggers back or lunges across the frame | The game already moves the fighter, so it would move twice | Add "stays on the same spot, feet planted"; for walks add "treadmill" |
| Long pause before or after the move | The strike frames get skipped and the attack looks like nothing happened | Re-roll with "fast, immediate" or trim to the action |
| Face, hair or outfit changes during the clip | Looks like a different person mid-move | Re-roll from the reference image; shorten the action |
| A prop appears or disappears | It pops in and out on screen between moves | Re-roll with "empty hands, no objects" |
| Background turns into a gradient, room or floor | The background cannot be removed cleanly | Add "solid flat [green or magenta] background, no floor, no shadow" |
| Screen colour on the character's edges, clothes or glow | Parts of the character turn see-through or get coloured fringes | Add "flat even front lighting"; Altman always on magenta; no green in outfits or money |
| Body, fists or feet cut off by the frame edge | Missing limbs in game | Re-roll with more space around the character |
| Faces the wrong way | Moves look backwards | Re-roll, or tell us and we flip it, as long as the whole fighter set matches |
| Motion blur smears | Frames look muddy when shown one at a time | Add "crisp pixel art, no motion blur" |
| Extra limbs, extra people, morphing hands | Obvious AI glitch on screen | Re-roll |
| Any logo, text or watermark | Shows in the game | Re-roll; remove tool watermarks with a paid export |
