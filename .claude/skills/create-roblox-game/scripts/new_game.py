#!/usr/bin/env python3
"""The build contract a new game starts from, and an alias for the one new-game command.

    new_game.py "My Game" --dir <games folder>/MyGame     # same as tools/new_game.py

There is one command that makes a game: `tools/new_game.py` in the toolkit. It lays down the
roblox-code scaffold, this contract, the starter docs, the layout map, the session hook and
the handoff. This file still answers to its old name (it forwards there) and owns the part
that is this skill's: the contract every later stage reads.

    design/game.json     THE CONTRACT. Every later stage reads a slice of this.
    design/*.json        one stub spec per stage, pre-filled from game.json
    assets/              where worker output lands
    BUILD.md             the stage checklist, with the exit criterion for each

game.json ships full of TODO markers on purpose. `validate.py` fails while any
remain, so the design stage cannot be skipped by accident - which is the failure
this whole layout is built to prevent, because every downstream skill silently
does something plausible when handed a vague spec. adopt.py writes the same
contract for an existing game.

WHY ONE COMMAND. There were two new_game.py, and a game made with this one had no CLAUDE.md,
docs, session hook or layout map, while the other's output depended on this one's. A game
that got half the setup failed later, far from the cause.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

# The toolkit holds this file at .claude/skills/create-roblox-game/scripts/new_game.py.
TOOLKIT = Path(__file__).resolve().parents[4]
COMMAND = TOOLKIT / "tools" / "new_game.py"

TODO = "TODO"

BUILD_MD = """# {title} - build checklist

One core loop. Every stage has an exit criterion that can be checked, not
eyeballed. A stage is not done because it produced files; it is done because its
criterion passed.

| # | Stage | Exit criterion | Done |
|---|---|---|---|
| 0 | preflight | every REQUIRED row green | [ ] |
| 0b | save the place | `place_state.py` says SAVED. **File > Save to File As, NEVER Ctrl+S** (that publishes) | [ ] |
| 1 | research | a findings file naming the genre, with sources that were opened | [ ] |
| 2 | design | `validate.py` passes: no TODO left, every referenced spec exists | [ ] |
| 3 | code | `roblox-code/scripts/check.py` all four gates green | [ ] |
| 4 | map | the prover returns PASS, not UNVERIFIABLE | [ ] |
| 5 | meshes | manifest lists MEASURED bounds and tri counts, all under budget | [ ] |
| 6 | ui | mockup PNG and .model.json emitted from the same tree | [ ] |
| 7 | animation | verification renders exist AND were looked at | [ ] |
| 8 | vfx | phase-frozen captures for every effect | [ ] |
| 9 | sfx | roles filled == roles requested, zero unfilled | [ ] |
| 10 | assembly | build stamp in Output, no duplicate modules, map + assets placed | [ ] |
| 10b | **wiring** | `verify_wired.py` green on the STATIC and the LIVE pass. Nothing generated is still a placeholder | [ ] |
| 11 | playtest | a human played it and reported back | [ ] |
| 12 | publish | place published and joinable | [ ] |

Re-save the place (File > Save to File) at every stage boundary. An unsaved
place cannot be reopened after a crash, and Studio does crash.

Stages 4 to 9 are the asset block and are mutually independent. They are the only
part of this list that may be fanned out to parallel workers (the default; see the
create-roblox-game skill). Stages 10 to 12 are single-threaded by law: one thread
touches Studio.

## Ledger

Every run is logged from the start, not reconstructed afterwards:

```
python ~/roblox-final/.claude/skills/roblox-build-orchestrator/scripts/run_log.py init --run {slug} --mode fanout
```
"""

GAME = {
    "title": "",
    "slug": "",
    "pitch": TODO + ": one sentence. What the player does, and what is at stake.",
    "core_loop": [TODO + ": step 1", TODO + ": step 2", TODO + ": step 3"],
    "win_condition": TODO,
    "lose_condition": TODO,
    "players": {"min": 1, "max": 4},
    "session_minutes": 8,
    "out_of_scope": [
        "progression",
        "shop",
        "datastore",
        "anything that is not the one core loop",
    ],
    "stages": {
        "map": {"spec": "design/map.json", "status": "todo"},
        "meshes": {"spec": "design/meshes.json", "status": "todo"},
        "ui": {"spec": "design/ui.json", "status": "todo"},
        "animation": {"spec": "design/animations.json", "status": "skip"},
        "vfx": {"spec": "design/vfx.json", "status": "skip"},
        "sfx": {"spec": "design/sfx.json", "status": "todo"},
    },
    "systems": [
        {
            "name": TODO + "Service",
            "side": "server",
            "owns": TODO + ": the one piece of state this service is authoritative for",
        }
    ],
    "config": {TODO + "Tunable": 0},
    "publish": {"universe_id": None, "place_id": None},
}

STUBS = {
    "design/map.json": {
        "name": TODO,
        "theme": TODO,
        "note": "roblox-map spec. Build from a REFERENCE IMAGE, never from imagination.",
    },
    "design/meshes.json": {
        "assets": [
            {"name": TODO, "prompt": TODO + ": a shaded 3D toy render of ...", "tris": 6000}
        ],
        "note": "roblox-3d-model. Colour: PAINT it (paint_texture.py), never project it.",
    },
    "design/ui.json": {
        "screens": [{"name": TODO, "elements": []}],
        "note": "roblox-ui spec. One tree emits the mockup, the .model.json and the Luau.",
    },
    "design/animations.json": {
        "rig": "R15",
        "clips": [{"name": TODO, "reference": TODO}],
        "note": "roblox-animation. Match a reference by ANGLE and fraction-of-reach, not distance.",
    },
    "design/vfx.json": {
        "effects": [{"name": TODO, "from": "a recipe harvested into your own roblox-vfx library"}],
        "note": "roblox-vfx. Harvest effects, never generate them from scratch.",
    },
    "design/sfx.json": {
        "name": TODO,
        "roles": [
            {
                "name": TODO,
                "query": TODO,
                "kind": "SoundEffect",
                "min_len": 0.1,
                "max_len": 5.0,
                "volume": 0.5,
            }
        ],
        "note": "roblox-sfx. One role per thing the game needs a sound FOR.",
    },
}


def slugify(name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", name.title()) or "Game"


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as fh:
        fh.write(json.dumps(data, indent=1) + "\n")


def write_contract(root: Path, title: str, game: dict | None = None, keep: bool = False) -> list[str]:
    """Write game.json, every stage stub, assets/ and BUILD.md. With keep, files that exist are
    left as they are (adopt.py). Returns the paths written, relative to root."""
    slug = slugify(title)
    if game is None:
        game = json.loads(json.dumps(GAME))
        game["title"] = title
        game["slug"] = slug
    files = {"design/game.json": game, **STUBS}
    written = []
    for rel, body in files.items():
        if keep and (root / rel).exists():
            continue
        write_json(root / rel, body)
        written.append(rel)
    (root / "assets").mkdir(parents=True, exist_ok=True)
    if not any((root / "assets").iterdir()):
        (root / "assets" / ".gitkeep").touch()
    if not (keep and (root / "BUILD.md").exists()):
        with open(root / "BUILD.md", "w", encoding="utf-8", newline="") as fh:
            fh.write(BUILD_MD.format(title=title, slug=slug))
        written.append("BUILD.md")
    return written


def main() -> int:
    """The old command: forward to tools/new_game.py, which makes the whole game."""
    if not COMMAND.exists():
        raise SystemExit(f"{COMMAND} not found: this skill runs inside the roblox-final toolkit")
    return subprocess.run([sys.executable, str(COMMAND), *sys.argv[1:]]).returncode


if __name__ == "__main__":
    raise SystemExit(main())
