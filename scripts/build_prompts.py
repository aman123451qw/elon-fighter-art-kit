#!/usr/bin/env python3
"""Regenerate PROMPTS.md and ASSETS.md from the data below.

Edit the data here (never the generated files), then run:
    python scripts/build_prompts.py
"""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STYLE = (
    "16-bit SNES-era pixel art fighting game sprite, original caricature character, crisp pixels, "
    "limited palette, bold dark outline, full body, side view facing left, flat even lighting, "
    "solid flat {bg} background, no shadow, no text, no logos"
)
CLIP_SUFFIX = (
    "locked static camera, character stays on the same spot, solid flat {bg} background, "
    "side view facing left, crisp pixel art, no motion blur"
)
GREEN, MAGENTA = "#00FF00 green", "#FF00FF magenta"

FIGHTERS = {
    "elon": {
        "name": "Elon",
        "bg": GREEN,
        "look": "tall, broad shoulders, short dark hair swept back, big confident grin, plain black t-shirt, "
        "dark jeans, black boots, red wristband",
        "stance": "cocky showman fighting stance, fists up, bouncing on his feet",
        "light": "quick straight punch",
        "heavy": "high front kick",
        "charge": "bends his knees, sparks and chunky pixel smoke burst at his feet, then holds the pose",
        "special": "rises and thrusts one arm forward toward the left at waist height as if firing, "
        "then returns to fighting stance",
        "portrait": "grinning, thumb pointing at himself, plain painted charcoal background with a red glow",
    },
    "zuckerberg": {
        "name": "Mark Zuckerberg",
        "bg": GREEN,
        "look": "lean and athletic, short curly brown hair, focused stare, plain grey t-shirt, dark fight shorts, "
        "MMA gloves, bare feet",
        "stance": "disciplined martial-artist stance, low guard, knees bent",
        "light": "fast jab",
        "heavy": "high roundhouse kick with no spin",
        "charge": "eyes glow blue, sinks into a wide low stance, then holds the pose",
        "special": "fast spinning combo on the spot: a strike, a low sweep and a final spinning kick, "
        "then back to fighting stance",
        "portrait": "fists up in a fighting guard, plain painted blue-grey background",
    },
    "ambani": {
        "name": "Mukesh Ambani",
        "bg": GREEN,
        "look": "solid build, grey hair combed back, calm smile, crisp white shirt, dark navy trousers, "
        "polished shoes, gold wristwatch",
        "stance": "unbothered calm stance, hands loosely raised, barely moving",
        "light": "open-palm strike",
        "heavy": "two-handed heavy shove, feet staying on the same spot",
        "charge": "fans out a glowing gold stack of cash between both hands, then holds the pose",
        "special": "three big overhand throws toward the left, one after another, then returns to fighting stance",
        "portrait": "arms folded, calm smile, plain painted navy background with gold",
    },
    "altman": {
        "name": "Sam Altman",
        "bg": MAGENTA,
        "look": "slim, short brown hair, calm half smile, plain navy crewneck sweater, jeans, white sneakers",
        "stance": "quiet calculating stance, relaxed guard, minimal movement",
        "light": "quick punch",
        "heavy": "front push kick",
        "charge": "raises one hand, glowing teal lines and particles swirl around his body, then holds the pose",
        "special": "thrusts his palm toward the left and holds the pose, then returns to fighting stance",
        "portrait": "hand raised with a faint teal glow, plain painted navy background with teal",
    },
}

CLIPS = [
    ("idle", "Idle loop", "breathes and bounces lightly in his fighting stance, seamless loop"),
    ("walk", "Walk forward", "walks forward on the spot like on a treadmill, guard up, seamless loop"),
    ("jump", "Jump", "jumps straight up, tucks knees at the top, lands back on the same spot"),
    ("block", "Block (ends held)", "quickly raises both forearms to guard face and chest and holds"),
    ("hit", "Hit reaction", "gets hit in the face, head snaps back, feet stay planted, recovers to fighting stance"),
    ("light", "Light attack", "throws one fast {light} toward the left, returns to stance"),
    ("heavy", "Heavy attack", "winds up and delivers a powerful {heavy} toward the left, returns to stance"),
    ("special_charge", "Special charge (ends held)", "{charge}"),
    ("special", "Special move (start from the LAST frame of the charge clip)", "{special}"),
    ("knockdown", "Knockdown (ends lying flat)",
     "takes a huge hit and falls straight backward onto the ground on the same spot, lies flat, stays down"),
]

FX = [
    ("fx_rocket", 2, GREEN, "Rocket in flight (loop)",
     "small plain white rocket, side view, nose pointing left, orange flame at the back, flame flickering, "
     "rocket stays centred, seamless loop"),
    ("fx_explosion", 2, GREEN, "Explosion", "chunky pixel-art explosion bursts and fades"),
    ("fx_money_bundle", 4, MAGENTA, "Money bundle spinning (loop)",
     "strapped bundle of made-up gold and orange banknotes spinning in place, no real currency, seamless loop"),
    ("fx_money_burst", 4, MAGENTA, "Money burst", "bundle of gold and orange banknotes bursts open, notes flutter outward and fall"),
]

STAGES = [
    ("stage_colosseum", 3, "wide 2D fighting game stage, inside a Roman Colosseum, flat sandy arena floor across the full width "
     "at the bottom, stone arches and cheering crowd in the stands behind, torches, golden afternoon light"),
    ("stage_mumbai", 4, "wide 2D fighting game stage, Mumbai rooftop at dusk, flat concrete rooftop floor across the full width "
     "at the bottom, water tanks, marigold garlands, city skyline with tall telecom towers blinking red lights, "
     "satellites streaking across the purple sky"),
    ("stage_server_farm", 5, "wide 2D fighting game stage, inside a huge AI data centre, flat polished dark floor across the full "
     "width at the bottom, rows of tall server racks with blinking teal lights, cables overhead, cool blue glow"),
]
STAGE_TAIL = ("16-bit SNES-era pixel art, no characters, no text, 2048 x 768, feet line 77% down, flat floor from 65% "
              "down, landmarks between 20% and 65% of the height, calm middle, plain bottom corners")

MENUS = [
    ("card_elon_vs_zuckerberg", "Matchup card, 1330 x 1182",
     "Elon on the LEFT facing right, Mark Zuckerberg on the right facing left, both mid fighting pose, Roman Colosseum behind, "
     "a lightning split down the middle, uses the whole card"),
    ("card_elon_vs_ambani", "Matchup card, 1330 x 1182",
     "Elon on the LEFT facing right, Mukesh Ambani on the right facing left, both mid fighting pose, Mumbai rooftop at dusk "
     "behind, a lightning split down the middle, uses the whole card"),
    ("card_elon_vs_altman", "Matchup card, 1330 x 1182",
     "Elon on the LEFT facing right, Sam Altman on the right facing left, both mid fighting pose, glowing AI server farm "
     "behind, a lightning split down the middle, uses the whole card"),
    ("mode_1v1", "Mode card, 1330 x 1182", "two of the fighters squaring up, two arcade joysticks in the foreground"),
    ("mode_vs_cpu", "Mode card, 1330 x 1182", "one fighter facing a glowing pixel robot silhouette"),
    ("logo", "Game logo, 1600 x 600, transparent or green background (the ONLY file with text)",
     "the words ELON FIGHTER in a bold arcade fighting-game style, chunky pixel letters, fiery red and gold outline"),
    ("title", "Title screen, 1920 x 1080",
     "all four fighters in a group action pose, Elon in the centre, a city skyline at dusk behind, top third left clear "
     "for the logo, no text"),
]


def asset_rows():
    """All 63 assets in delivery order: (phase, file, folder, what, background, prompt)."""
    rows = [(1, "lineup.png", "00_style", "All 4 fighters side by side (style test)", "Green",
             STYLE.format(bg=GREEN).replace("full body, side view facing left", "four full-body characters side by side, "
             "same scale, all facing left") + ", " + "; ".join(f"{f['name']}: {f['look']}" for f in FIGHTERS.values()))]

    order = [("elon", 1), ("zuckerberg", 3), ("ambani", 4), ("altman", 5)]
    for fid, phase in order:
        f = FIGHTERS[fid]
        bg_word = "Magenta" if f["bg"] == MAGENTA else "Green"
        ref_prompt = (STYLE.format(bg=f["bg"]) + f", {f['look']}, {f['stance']}, facing left, centred with empty space around "
                      "the whole body, character fills about 70% of the image height, empty hands")
        rows.append((phase, f"{fid}_reference.png", fid, f"{f['name']} full-body reference", bg_word, ref_prompt))
        for suffix, label, motion in CLIPS:
            clip_phase = 1 if fid == "elon" and suffix in ("idle", "heavy") else (2 if fid == "elon" else phase)
            text = motion.format(**f)
            prompt = f"[start from {fid}_reference.png] {f['name']} {text}, " + CLIP_SUFFIX.format(bg=f["bg"])
            if suffix == "special":
                prompt = prompt.replace(f"[start from {fid}_reference.png]", f"[start from the last frame of {fid}_special_charge.mp4]")
            rows.append((clip_phase, f"{fid}_{suffix}.mp4", fid, label, bg_word, prompt))
        portrait_phase = 2 if fid == "elon" else phase
        rows.append((portrait_phase, f"{fid}_portrait.png", fid, "Portrait", "Painted",
                     "16-bit pixel art portrait, slightly more detailed than the sprites, head and upper body facing LEFT, "
                     f"face large and in the upper half, {f['look']}, {f['portrait']}, 1254 x 1254, no text"))

    for name, phase, bg, label, motion in FX:
        rows.append((phase, f"{name}.mp4", "fx", label, "Magenta" if bg == MAGENTA else "Green",
                     f"16-bit pixel art game effect, {motion}, locked static camera, solid flat {bg} background, crisp pixels, no text"))
    for name, phase, scene in STAGES:
        rows.append((phase, f"{name}.png", "stages", "Stage background", "Scene", f"{scene}, {STAGE_TAIL}"))
    for name, label, scene in MENUS:
        rows.append((6, f"{name}.png", "menus", label, "Full art", f"16-bit SNES-era pixel art illustration, {scene}"))

    rows.sort(key=lambda row: row[0])
    return rows


def main() -> None:
    rows = asset_rows()
    assert len(rows) == 63, len(rows)

    prompts = ["# Prompts for all 63 files", "",
               "Generated by `scripts/build_prompts.py`. Copy a prompt, paste it into the tool, then check the result "
               "with `python selfcheck/selfcheck.py <file>` before uploading. Clips: give the tool the image named in "
               "[brackets] as the start frame and paste the rest as the motion prompt.", ""]
    current = None
    for phase, file, folder, what, bg, prompt in rows:
        if phase != current:
            prompts += [f"## Phase {phase}", ""]
            current = phase
        prompts += [f"### `{file}`  ({what}, {bg} background, folder `{folder}/`)", "", "```", prompt, "```", ""]
    (ROOT / "PROMPTS.md").write_text("\n".join(prompts), encoding="utf-8")

    table = ["# All 63 files", "", "Generated by `scripts/build_prompts.py`. Same order as the tracker in the brief.", "",
             "| # | Phase | File | Folder | What it is | Background |", "|---|---|---|---|---|---|"]
    for index, (phase, file, folder, what, bg, _) in enumerate(rows, 1):
        table.append(f"| {index} | {phase} | `{file}` | {folder} | {what} | {bg} |")
    (ROOT / "ASSETS.md").write_text("\n".join(table) + "\n", encoding="utf-8")
    print(f"wrote PROMPTS.md and ASSETS.md ({len(rows)} files)")


if __name__ == "__main__":
    main()
