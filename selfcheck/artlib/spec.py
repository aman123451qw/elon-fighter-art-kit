"""The art assets for the fighting game (63 from the original brief + 39 new
from the kit POWERS.md, part 2): name, kind, fighter, action,
expected background, phase and Drive folder. Also the per-action frame/fps
targets. This is the single source of truth other modules read from.
"""

from __future__ import annotations

import difflib
from dataclasses import dataclass, field

FIGHTERS: tuple[str, ...] = ("elon", "zuckerberg", "ambani", "altman")

# delivered suffix -> game action name (hyphenated)
ACTION_TO_GAME: dict[str, str] = {
    "idle": "idle",
    "walk": "walk",
    "jump": "jump",
    "block": "block",
    "hit": "hit",
    "light": "light",
    "heavy": "heavy",
    "special_charge": "special-charge",
    "special": "special",
    "knockdown": "knockdown",
}
ACTIONS_ORDER: tuple[str, ...] = tuple(ACTION_TO_GAME.keys())
GAME_ACTIONS: tuple[str, ...] = tuple(ACTION_TO_GAME.values())

FX_NAMES: tuple[str, ...] = ("fx_rocket", "fx_explosion", "fx_money_bundle", "fx_money_burst")
STAGE_NAMES: tuple[str, ...] = ("stage_colosseum", "stage_mumbai", "stage_server_farm")
CARD_NAMES: tuple[str, ...] = ("card_elon_vs_zuckerberg", "card_elon_vs_ambani", "card_elon_vs_altman")
MODE_NAMES: tuple[str, ...] = ("mode_1v1", "mode_vs_cpu")
MENU_NAMES: tuple[str, ...] = CARD_NAMES + MODE_NAMES + ("logo", "title")

GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
BLACK = (0, 0, 0)

# ---- part 2 (kit POWERS.md): powers, summoned objects, glow on black ----

# Power clips: fighter clips made from the last frame of the special charge.
POWER_ACTIONS: dict[str, tuple[str, ...]] = {
    "elon": ("babies", "cybertruck", "starlink"),
    "ambani": ("whistle", "antilia", "towers"),
}
POWER_ACTION_NAMES: frozenset[str] = frozenset(a for acts in POWER_ACTIONS.values() for a in acts)

# Summoned objects/characters: reference image background, Drive folder and phase.
OBJECTS: dict[str, tuple[str, str, int]] = {
    "cybertruck": ("green", "powers_elon", 7),
    "baby": ("green", "powers_elon", 8),
    "starlink": ("green", "powers_elon", 8),
    "ghost_modi": ("black", "powers_ambani", 9),
    "ghost_salman": ("black", "powers_ambani", 9),
    "antilia": ("magenta", "powers_ambani", 9),
    "tower": ("green", "powers_ambani", 9),
}

# Object clips -> the object they are made from.
OBJECT_CLIPS: dict[str, str] = {
    "cybertruck_drive": "cybertruck",
    "baby_run": "baby",
    "baby_punch": "baby",
    "starlink_sat": "starlink",
    "ghost_modi_run": "ghost_modi",
    "ghost_modi_punch": "ghost_modi",
    "ghost_salman_run": "ghost_salman",
    "ghost_salman_punch": "ghost_salman",
    "antilia_fly": "antilia",
    "tower_rise": "tower",
}

# Glow effects on pure black, drawn additively by the game. name -> phase.
GLOW_FX: dict[str, int] = {
    "fx_hit_glow": 7,
    "fx_rocket_trail": 8, "fx_baby_hit": 8, "fx_cybertruck_lights": 8, "fx_cybertruck_crash": 8,
    "fx_starlink_beam": 8, "fx_starlink_impact": 8, "fx_charge_red": 8,
    "fx_money_trail": 9, "fx_charge_gold": 9, "fx_antilia_trail": 9, "fx_antilia_crash": 9,
    "fx_tower_beam": 9, "fx_tower_impact": 9,
    "fx_block_glow": 10, "fx_super_flash": 10,
}

# Glow files allowed to touch these frame edges (a beam or trail runs edge to edge).
GLOW_EDGES_ALLOWED: dict[str, tuple[str, ...]] = {
    "fx_starlink_beam": ("top", "bottom"),
    "fx_tower_beam": ("left", "right"),
    "fx_rocket_trail": ("left", "right"),
    "fx_cybertruck_lights": ("left", "right"),
    "fx_money_trail": ("left", "right"),
    "fx_antilia_trail": ("left", "right"),
}


@dataclass(frozen=True)
class FrameTarget:
    """Target frame count / playback rate / selection strategy for one action."""

    frames: int
    fps: int
    repeat: int  # -1 = loop, 0 = play once (covers both "hold" and "no loop")
    mode: str  # "loop" | "hold" | "window"
    window_seconds: float | None = None  # for mode == "loop": sample within this window
    pin_feet: bool = False
    pin_centre: bool = False  # knockdown: centre every frame so a drifting fall lands on the spot


FRAME_TARGETS: dict[str, FrameTarget] = {
    "idle": FrameTarget(12, 8, -1, "loop", window_seconds=2.5),
    "walk": FrameTarget(8, 8, -1, "loop", window_seconds=2.0),
    "jump": FrameTarget(8, 10, 0, "window", pin_feet=True),
    "block": FrameTarget(4, 10, 0, "hold"),
    "hit": FrameTarget(6, 12, 0, "window"),
    "light": FrameTarget(6, 14, 0, "window"),
    "heavy": FrameTarget(10, 12, 0, "window"),
    "special_charge": FrameTarget(5, 14, 0, "hold"),
    "special": FrameTarget(12, 16, 0, "window"),
    "knockdown": FrameTarget(10, 10, 0, "hold", pin_feet=True, pin_centre=True),
    "fx_rocket": FrameTarget(6, 12, -1, "loop", window_seconds=1.0),
    "fx_money_bundle": FrameTarget(6, 12, -1, "loop", window_seconds=1.0),
    "fx_explosion": FrameTarget(8, 16, 0, "window"),
    "fx_money_burst": FrameTarget(8, 16, 0, "window"),
    # power clips (same shape as the special)
    **{a: FrameTarget(12, 16, 0, "window") for acts in POWER_ACTIONS.values() for a in acts},
    # object clips
    "cybertruck_drive": FrameTarget(6, 12, -1, "loop", window_seconds=0.75),
    "baby_run": FrameTarget(8, 12, -1, "loop", window_seconds=0.7),
    "baby_punch": FrameTarget(6, 14, 0, "window"),
    "starlink_sat": FrameTarget(8, 10, -1, "loop", window_seconds=1.0),
    "ghost_modi_run": FrameTarget(8, 12, -1, "loop", window_seconds=0.7),
    "ghost_modi_punch": FrameTarget(10, 12, 0, "window"),
    "ghost_salman_run": FrameTarget(8, 12, -1, "loop", window_seconds=0.7),
    "ghost_salman_punch": FrameTarget(10, 12, 0, "window"),
    "antilia_fly": FrameTarget(8, 10, -1, "loop", window_seconds=1.0),
    "tower_rise": FrameTarget(8, 12, 0, "hold"),
    # glow loops and one-shots
    **{n: FrameTarget(6, 12, -1, "loop", window_seconds=0.5) for n in (
        "fx_rocket_trail", "fx_cybertruck_lights", "fx_starlink_beam", "fx_money_trail",
        "fx_antilia_trail", "fx_tower_beam")},
    "fx_charge_red": FrameTarget(8, 10, -1, "loop", window_seconds=1.0),
    "fx_charge_gold": FrameTarget(8, 10, -1, "loop", window_seconds=1.0),
    **{n: FrameTarget(6, 20, 0, "window") for n in ("fx_hit_glow", "fx_block_glow", "fx_baby_hit")},
    **{n: FrameTarget(8, 16, 0, "window") for n in (
        "fx_cybertruck_crash", "fx_starlink_impact", "fx_antilia_crash", "fx_tower_impact", "fx_super_flash")},
}


@dataclass(frozen=True)
class Asset:
    name: str  # canonical id == stem of the delivered file/folder name
    kind: str  # lineup | reference | clip | fx | portrait | stage | menu | object_reference | object_clip
    phase: int
    folder: str  # Drive subfolder it lives in once approved
    background: str  # green | magenta | black | painted | scene
    fighter: str | None = None
    action: str | None = None  # suffix form, e.g. "special_charge"
    game_action: str | None = None  # hyphen form, e.g. "special-charge"
    ext: str = ".png"
    accepts_folder: bool = False
    obj: str | None = None  # object id for object_reference / object_clip


def _clip_asset(fighter: str, action: str, phase: int) -> Asset:
    bg = "magenta" if fighter == "altman" else "green"
    return Asset(
        name=f"{fighter}_{action}",
        kind="clip",
        phase=phase,
        folder=fighter,
        background=bg,
        fighter=fighter,
        action=action,
        game_action=ACTION_TO_GAME[action],
        ext=".mp4",
        accepts_folder=True,
    )


def _build_assets() -> dict[str, Asset]:
    assets: dict[str, Asset] = {}

    assets["lineup"] = Asset("lineup", "lineup", 1, "00_style", "green")

    # phase assignment per fighter
    fighter_phase = {"elon": None, "zuckerberg": 3, "ambani": 4, "altman": 5}  # elon spans 1 & 2

    for fighter in FIGHTERS:
        bg = "magenta" if fighter == "altman" else "green"
        ref_phase = 1 if fighter == "elon" else fighter_phase[fighter]
        assets[f"{fighter}_reference"] = Asset(
            f"{fighter}_reference", "reference", ref_phase, fighter, bg, fighter=fighter
        )
        portrait_phase = 2 if fighter == "elon" else fighter_phase[fighter]
        assets[f"{fighter}_portrait"] = Asset(
            f"{fighter}_portrait", "portrait", portrait_phase, fighter, "painted", fighter=fighter
        )
        for action in ACTIONS_ORDER:
            if fighter == "elon":
                phase = 1 if action in ("idle", "heavy") else 2
            else:
                phase = fighter_phase[fighter]
            assets[f"{fighter}_{action}"] = Asset(
                f"{fighter}_{action}", "clip", phase, fighter, bg,
                fighter=fighter, action=action, game_action=ACTION_TO_GAME[action],
                ext=".mp4", accepts_folder=True,
            )

    fx_phase = {"fx_rocket": 2, "fx_explosion": 2, "fx_money_bundle": 4, "fx_money_burst": 4}
    for fx in FX_NAMES:
        bg = "magenta" if fx.startswith("fx_money") else "green"
        assets[fx] = Asset(fx, "fx", fx_phase[fx], "fx", bg, ext=".mp4", accepts_folder=True)

    stage_phase = {"stage_colosseum": 3, "stage_mumbai": 4, "stage_server_farm": 5}
    for stage in STAGE_NAMES:
        assets[stage] = Asset(stage, "stage", stage_phase[stage], "stages", "scene")

    for menu in MENU_NAMES:
        assets[menu] = Asset(menu, "menu", 6, "menus", "scene")

    # ---- part 2 ----
    power_phase = {"elon": 8, "ambani": 9}
    for fighter, actions in POWER_ACTIONS.items():
        for action in actions:
            assets[f"{fighter}_{action}"] = Asset(
                f"{fighter}_{action}", "clip", power_phase[fighter], f"powers_{fighter}", "green",
                fighter=fighter, action=action, game_action=action, ext=".mp4", accepts_folder=True,
            )

    for obj, (bg, folder, phase) in OBJECTS.items():
        assets[f"{obj}_reference"] = Asset(f"{obj}_reference", "object_reference", phase, folder, bg, obj=obj)

    for name, obj in OBJECT_CLIPS.items():
        bg, folder, phase = OBJECTS[obj]
        assets[name] = Asset(name, "object_clip", phase, folder, bg, ext=".mp4", accepts_folder=True, obj=obj)

    for name, phase in GLOW_FX.items():
        assets[name] = Asset(name, "fx", phase, "fx", "black", ext=".mp4", accepts_folder=True)

    return assets


ASSETS: dict[str, Asset] = _build_assets()
ALL_ASSET_NAMES: tuple[str, ...] = tuple(ASSETS.keys())

assert len(ASSETS) == 102, f"expected 102 assets (63 + 39 new), got {len(ASSETS)}"
PHASES: tuple[int, ...] = tuple(sorted({a.phase for a in ASSETS.values()}))


def phase_assets(phase: int) -> list[Asset]:
    return [a for a in ASSETS.values() if a.phase == phase]


def identify_asset(path_stem: str) -> Asset | None:
    """Match a delivered file/folder name (without extension) to its Asset."""
    return ASSETS.get(path_stem.lower())


def suggest_closest(path_stem: str, n: int = 3) -> list[str]:
    """Closest expected names for a misnamed delivered file."""
    return difflib.get_close_matches(path_stem.lower(), ALL_ASSET_NAMES, n=n, cutoff=0.0)


def expected_delivered_filename(asset: Asset) -> str:
    return f"{asset.name}{asset.ext}"


# Relative on-screen height per fighter (Elon tallest), baked into every sheet so
# all fighters draw 1:1. From the finalised references: Ambani 776, Elon 772,
# Altman 728, Zuckerberg 712 px; Elon is kept tallest by design.
HEIGHT_RATIO = {"elon": 1.0, "ambani": 0.98, "altman": 0.95, "zuckerberg": 0.93}


# On-screen size (longest side, px) each effect is resized to; the game draws
# effects 1:1. Clips arrive at video size (a 1080p rocket is ~960 px long).
FX_DISPLAY_SIZE = {
    "fx_rocket": 200, "fx_explosion": 260, "fx_money_bundle": 110, "fx_money_burst": 240,
    # glow (fighters stand ~287 px tall on screen)
    "fx_hit_glow": 120, "fx_block_glow": 120, "fx_baby_hit": 90, "fx_super_flash": 420,
    "fx_rocket_trail": 220, "fx_cybertruck_lights": 320, "fx_cybertruck_crash": 320,
    "fx_starlink_beam": 560, "fx_starlink_impact": 260, "fx_charge_red": 380, "fx_charge_gold": 380,
    "fx_money_trail": 140, "fx_antilia_trail": 260, "fx_antilia_crash": 380,
    "fx_tower_beam": 600, "fx_tower_impact": 200,
}

# On-screen size of summoned objects: (axis, px, basis). That axis of the object,
# measured on the basis frame(s), is scaled to px; every frame gets the same scale.
# basis: "first" (clip starts from the reference pose), "max" (grows into view),
# "median" (moving or turning).
OBJECT_DISPLAY: dict[str, tuple[str, int, str]] = {
    "cybertruck": ("width", 430, "median"),
    "baby": ("height", 100, "first"),
    "starlink": ("width", 290, "median"),
    "ghost_modi": ("height", 290, "median"),
    "ghost_salman": ("height", 290, "median"),
    "antilia": ("height", 280, "first"),
    "tower": ("height", 430, "max"),
}
