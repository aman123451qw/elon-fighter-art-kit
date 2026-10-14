"""The 63 art assets for the fighting game: name, kind, fighter, action,
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


@dataclass(frozen=True)
class FrameTarget:
    """Target frame count / playback rate / selection strategy for one action."""

    frames: int
    fps: int
    repeat: int  # -1 = loop, 0 = play once (covers both "hold" and "no loop")
    mode: str  # "loop" | "hold" | "window"
    window_seconds: float | None = None  # for mode == "loop": sample within this window
    pin_feet: bool = False


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
    "knockdown": FrameTarget(10, 10, 0, "hold"),
    "fx_rocket": FrameTarget(6, 12, -1, "loop", window_seconds=1.0),
    "fx_money_bundle": FrameTarget(6, 12, -1, "loop", window_seconds=1.0),
    "fx_explosion": FrameTarget(8, 16, 0, "window"),
    "fx_money_burst": FrameTarget(8, 16, 0, "window"),
}


@dataclass(frozen=True)
class Asset:
    name: str  # canonical id == stem of the delivered file/folder name
    kind: str  # lineup | reference | clip | fx | portrait | stage | menu
    phase: int
    folder: str  # Drive subfolder it lives in once approved
    background: str  # green | magenta | painted | scene
    fighter: str | None = None
    action: str | None = None  # suffix form, e.g. "special_charge"
    game_action: str | None = None  # hyphen form, e.g. "special-charge"
    ext: str = ".png"
    accepts_folder: bool = False


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

    return assets


ASSETS: dict[str, Asset] = _build_assets()
ALL_ASSET_NAMES: tuple[str, ...] = tuple(ASSETS.keys())

assert len(ASSETS) == 63, f"expected 63 assets, got {len(ASSETS)}"


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
