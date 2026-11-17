#!/usr/bin/env python3
"""Take on an existing game: propose its layout map, design/layout.json and a contract skeleton.

    adopt.py --dir <game>            # read-only: print what it found and what it would write
    adopt.py --dir <game> --write    # write the new files; never touch an existing one

WHY THIS EXISTS. The toolkit assumed every game came from its own scaffold: Knit, a Net.luau of
remotes, Core/ and Config/ folders, Wally packages, tests/. A game made before the toolkit had
none of that (plain modules booted from Main.server.luau, remotes made by each service, one
Config.luau, pure modules loose in src/shared, no packages, no tests, a map built by hand in
Studio), so check.py failed on folders it never had, the reviewer judged code against paths
that did not exist, and section 1 could not close because the game's research and design
stages were never bracketed in a ledger. This reads the game as it is and writes down where
things are, instead of moving the game onto the scaffold.

What --write creates, only where the file does not exist yet:
  design/layout.json          the layout map every reader uses (roblox-code references/layout.md)
  docs/tech/layout.md         the same map for people, with the evidence for each line
  design/game.json + stubs    the contract skeleton, pre-filled from docs/pitch.md, the services
                              and Config; every value it could not find is a TODO marker
  BUILD.md, HANDOFF.md        the stage checklist and an adoption handoff
  the starter's docs, CLAUDE.md, .claude/settings.json (the session hook), the map state template

It never writes under src/ or tests/, never renames or moves a file, and never formats code
(references/adopt.md: never reformat code during adoption).
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLKIT = HERE.parents[3]  # scripts -> create-roblox-game -> skills -> .claude -> toolkit
SKILLS = TOOLKIT / ".claude" / "skills"


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


contract = _load("crg_contract", HERE / "new_game.py")
layout_map = _load("rc_layout", SKILLS / "roblox-code" / "scripts" / "layout.py")
starter = _load("tk_new_game", TOOLKIT / "tools" / "new_game.py")

# A module that touches none of these is pure (inferred): it can run under `lune run test`.
IMPURE = re.compile(r"\bgame\s*[:.]|\bworkspace\b|\bInstance\.new\b|\bscript\b|:WaitForChild\b|"
                    r"\btask\.(wait|spawn|delay)\b|\bwait\s*\(")
REMOTE = re.compile(r'Instance\.new\(\s*"(RemoteEvent|RemoteFunction|UnreliableRemoteEvent)"\s*\)')
FOLDER = re.compile(r'(?:FindFirstChild|WaitForChild)\(\s*"(\w+)"')


def rel(root: Path, p: Path) -> str:
    return p.relative_to(root).as_posix()


def tree_paths(root: Path) -> dict[str, str]:
    """Instance path -> folder, from default.project.json ($path entries)."""
    out: dict[str, str] = {}
    pj = root / "default.project.json"
    if not pj.exists():
        return out

    def walk(node: dict, path: list[str]) -> None:
        for k, v in node.items():
            if k.startswith("$") or not isinstance(v, dict):
                continue
            if "$path" in v:
                out[".".join(path + [k])] = v["$path"]
            walk(v, path + [k])

    walk(json.loads(pj.read_text(encoding="utf-8")).get("tree", {}), [])
    return out


def side_root(paths: dict[str, str], service: str, default: str) -> str:
    for inst, folder in paths.items():
        if inst.startswith(service) and "Packages" not in inst:
            return folder
    return default


def boot_script(root: Path, folder: str, kind: str) -> Path | None:
    d = root / folder
    for name in (f"init.{kind}.luau", f"init.{kind}.lua", f"Main.{kind}.luau", f"Main.{kind}.lua"):
        if (d / name).exists():
            return d / name
    found = sorted(d.glob(f"*.{kind}.lua*")) if d.is_dir() else []
    return found[0] if found else None


def module_dir(root: Path, folder: str, names: tuple[str, ...]) -> str | None:
    for n in names:
        if (root / folder / n).is_dir():
            return f"{folder}/{n}"
    return None


def detect(root: Path) -> tuple[dict, list[str]]:
    """(proposed layout, evidence lines)."""
    ev: list[str] = []
    lay = json.loads(json.dumps(layout_map.DEFAULT))
    lay["adopted"] = True
    notes: list[str] = []
    paths = tree_paths(root)
    server = side_root(paths, "ServerScriptService", "src/server")
    client = side_root(paths, "StarterPlayer", "src/client")
    shared = side_root(paths, "ReplicatedStorage", "src/shared")
    ev.append(f"default.project.json maps server={server}, client={client}, shared={shared}")

    if (root / "rokit.toml").exists():
        lay["toolchain"] = "rokit.toml"
    elif (root / "aftman.toml").exists():
        lay["toolchain"] = "aftman.toml"
    else:
        lay["toolchain"] = None
        notes.append("no rokit.toml or aftman.toml: pin rojo, selene and stylua before running check.py")
    ev.append(f"toolchain: {lay['toolchain'] or 'none found'}")
    lay["packages"] = "wally" if (root / "wally.toml").exists() else "none"
    ev.append(f"packages: {lay['packages']} ({'wally.toml' if lay['packages'] == 'wally' else 'no wally.toml'})")

    sboot, cboot = boot_script(root, server, "server"), boot_script(root, client, "client")
    lay["boot"] = {"server": rel(root, sboot) if sboot else None, "client": rel(root, cboot) if cboot else None}
    boot_text = sboot.read_text(encoding="utf-8") if sboot else ""
    if "Knit" in boot_text:
        lay["framework"] = "knit"
        ev.append(f"framework: knit ({lay['boot']['server']} requires Knit)")
    else:
        lay["framework"] = "modules"
        calls = [c for c in (":Init()", ":Start()") if c in boot_text]
        ev.append(f"framework: modules ({lay['boot']['server']} calls {' and '.join(calls) or 'no Init/Start'})")

    lay["services"] = module_dir(root, server, ("Services", "services", "Systems")) or server
    lay["controllers"] = module_dir(root, client, ("Controllers", "controllers")) or client
    ev.append(f"services: {lay['services']}; controllers: {lay['controllers']}")

    net = sorted(root.glob(f"{shared}/**/Net.lua*"))
    if net:
        lay["remotes"] = {"style": "net-module", "where": rel(root, net[0])}
        ev.append(f"remotes: one module, {rel(root, net[0])}")
    else:
        makers, folders = [], set()
        for f in sorted((root / lay["services"]).rglob("*.lua*")):
            text = f.read_text(encoding="utf-8")
            if REMOTE.search(text):
                makers.append(f.stem)
                folders |= set(FOLDER.findall(text))
        folder = sorted(folders)[0] if folders else "Remotes"
        lay["remotes"] = {"style": "per-service", "where": f"ReplicatedStorage.{folder}"}
        ev.append(f"remotes: created by {', '.join(makers) or 'no service'} under ReplicatedStorage.{folder}")
        if not folders:
            notes.append("(inferred) the remotes folder name was not found in code; check remotes.where")

    if (root / shared / "Config").is_dir():
        lay["config"] = f"{shared}/Config"
    else:
        cfg = sorted((root / shared).glob("Config.lua*")) or sorted((root / shared).rglob("*Config*.lua*"))
        lay["config"] = rel(root, cfg[0]) if cfg else None
        if not cfg:
            notes.append("no Config module found: tunables are inline somewhere; list them in game.json config")
    ev.append(f"config: {lay['config']}")

    if (root / shared / "Core").is_dir():
        lay["pure"] = [f"{shared}/Core"]
        ev.append(f"pure rules: {shared}/Core")
    else:
        pure = []
        for f in sorted((root / shared).glob("*.lua*")):
            p = rel(root, f)
            if p in (lay["config"], lay["remotes"].get("where")):
                continue
            body = re.sub(r"--[^\n]*", "", f.read_text(encoding="utf-8"))
            if not IMPURE.search(body):
                pure.append(p)
                notes.append(f"(inferred) {f.name} is pure: no Instance, service, script or yield")
        lay["pure"] = pure
        ev.append(f"pure rules: {', '.join(pure) or 'none found'} (loose in {shared})")

    specs = sorted((root / "tests").glob("*.spec.luau")) if (root / "tests").is_dir() else []
    lay["tests"] = "tests" if specs else None
    ev.append(f"tests: {len(specs)} spec file(s)" + ("" if specs else ", so check.py skips lune"))
    lay["lint"] = ["src"] if (root / "src").is_dir() else [server]
    lay["format"] = [p for p in ("src", "lune") if (root / p).is_dir()] or [server]

    if (root / "design" / "map.json").exists() and list(root.glob("work/map/report.json")):
        lay["map"] = {"source": "prover", "spec": "design/map.json"}
        ev.append("map: roblox-map prover (design/map.json and work/map/report.json)")
    else:
        briefs = sorted(p for p in (root / "docs" / "design" / "maps").glob("*.md")
                        if not p.name.endswith(".state.md") and not p.name.startswith("_"))
        lay["map"] = {"source": "studio", "brief": rel(root, briefs[0]) if briefs else None}
        ev.append(f"map: built in Studio; brief {lay['map']['brief'] or 'not found'}")
    lay["notes"] = notes
    return lay, ev


def field(text: str, label: str) -> str:
    m = re.search(rf"^\*\*{re.escape(label)}:\*\*[ \t]*(.*)$", text, re.M)
    v = m.group(1).strip() if m else ""
    return "" if v.startswith("<") else v


def bullets_after(text: str, label: str) -> list[str]:
    m = re.search(rf"^\*\*{re.escape(label)}:\*\*\s*\n((?:\s*-[^\n]*\n?)+)", text, re.M)
    if not m:
        return []
    items = [ln.strip()[1:].strip() for ln in m.group(1).splitlines() if ln.strip().startswith("-")]
    return [i for i in items if i and not i.startswith("<")]


def skeleton(root: Path, lay: dict) -> tuple[dict, list[str]]:
    """The contract, pre-filled from the game's own docs and code. (game.json, where each came from)."""
    T = contract.TODO
    game = json.loads(json.dumps(contract.GAME))
    src: list[str] = []
    pj = root / "default.project.json"
    title = json.loads(pj.read_text(encoding="utf-8")).get("name") if pj.exists() else None
    if not title and (root / "README.md").exists():
        m = re.search(r"^# (.+)$", (root / "README.md").read_text(encoding="utf-8"), re.M)
        title = m.group(1).strip() if m else None
    game["title"] = title or root.name
    game["slug"] = contract.slugify(game["title"])
    src.append(f"title: {game['title']} (default.project.json name, else README heading)")

    pitch_md = root / "docs" / "pitch.md"
    if pitch_md.exists():
        text = pitch_md.read_text(encoding="utf-8")
        if field(text, "One line"):
            game["pitch"] = field(text, "One line")
            src.append("pitch: docs/pitch.md 'One line'")
        loop = [s.strip() for s in re.split(r"→|->", field(text, "Core loop")) if s.strip()]
        if len(loop) >= 2:
            game["core_loop"] = loop
            src.append(f"core_loop: docs/pitch.md 'Core loop' ({len(loop)} steps)")
        mins = re.search(r"\d+", field(text, "Session length target"))
        if mins:
            game["session_minutes"] = int(mins.group(0))
            src.append("session_minutes: docs/pitch.md 'Session length target'")
        oos = bullets_after(text, "Out of scope for v1")
        if oos:
            game["out_of_scope"] = oos
            src.append(f"out_of_scope: docs/pitch.md ({len(oos)} items)")

    systems = []
    for folder, side in ((lay["services"], "server"), (lay["controllers"], "client")):
        for f in sorted((root / folder).glob("*.lua*")) if folder and (root / folder).is_dir() else []:
            head = f.read_text(encoding="utf-8").split("\n", 1)[0]
            m = re.search(r"\bowns\s+(.+?)\.?\s*$", head)
            name = f.name.split(".")[0]
            systems.append({"name": name, "side": side,
                            "owns": m.group(1) if m else f"{T}: the one piece of state {name} owns"})
    if systems:
        game["systems"] = systems
        src.append(f"systems: {len(systems)} module(s) in {lay['services']} and {lay['controllers']}, "
                   f"'owns' from each file's first comment")

    cfg = root / lay["config"] if lay.get("config") else None
    if cfg and cfg.is_file():
        values = dict(re.findall(r"^\s*(\w+)\s*=\s*(-?\d+(?:\.\d+)?)\s*,", cfg.read_text(encoding="utf-8"), re.M))
        if values:
            game["config"] = {k: (float(v) if "." in v else int(v)) for k, v in values.items()}
            src.append(f"config: {len(values)} number(s) from {lay['config']}")
    return game, src


def layout_doc(title: str, lay: dict, ev: list[str]) -> str:
    lines = [
        f"# Layout map: {title}",
        "",
        f"Written by `adopt.py` on {date.today().isoformat()}. The machine-readable form is",
        "`design/layout.json` (fields: `roblox-code/references/layout.md` in the toolkit). This game",
        "keeps its own layout; adoption did not move, rename or reformat any code.",
        "",
        "| What | Where |",
        "|---|---|",
        f"| Boot | `{lay['boot']['server']}` (server), `{lay['boot']['client']}` (client); framework `{lay['framework']}` |",
        f"| Services / controllers | `{lay['services']}` / `{lay['controllers']}` |",
        f"| Remotes | {lay['remotes']['style']}: `{lay['remotes']['where']}` |",
        f"| Config | `{lay['config']}` |",
        f"| Pure rules | {', '.join(f'`{p}`' for p in lay['pure']) or 'none found'} |",
        f"| Tests | `{lay['tests']}` |" if lay["tests"] else "| Tests | none yet (check.py skips lune) |",
        f"| Packages, tools | {lay['packages']}; `{lay['toolchain']}` |",
        f"| Map | {lay['map']['source']}: `{lay['map'].get('brief') or lay['map'].get('spec')}` |",
        "",
        "## Evidence",
        "",
        *[f"- {e}" for e in ev],
    ]
    if lay["notes"]:
        lines += ["", "## Check these", "", *[f"- {n}" for n in lay["notes"]]]
    return "\n".join(lines) + "\n"


HANDOFF = """<!-- handoff: start -->
# HANDOFF: {title}, adopted

Adopted on {day} with `adopt.py --write`. The game's code was not changed: no file under
`src/` or `tests/` was written, moved, renamed or formatted.

## Where things are

- `design/layout.json` and `docs/tech/layout.md`: where this game keeps each kind of code.
- `design/game.json`: the contract skeleton. Values found in the docs and code are filled in;
  every other one is a TODO marker for section 1.

## Done

- {written} file(s) written by adopt.py; nothing existing was overwritten.

## Unproven

- Every "(inferred)" line in `docs/tech/layout.md` until someone reads that code.
- The four code gates on this game: `check.py` has not been run since adoption.

## Debts

- None.

## Next: first step

Section 1 for an adopted game (create-roblox-game `references/adopt.md`): start the ledger,
end `market-research` and `design-spec` with `--status adopted`, fill `design/game.json` until
`validate.py` is green, then `section.py handoff 1` and `section.py close 1`.
"""


def write(root: Path, lay: dict, ev: list[str], game: dict, force: bool) -> list[str]:
    written: list[str] = []

    def put(relpath: str, text: str, forceable: bool = True) -> None:
        p = root / relpath
        if p.exists() and not (force and forceable):
            print(f"  kept   {relpath} (exists)")
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8", newline="\n")
        written.append(relpath)
        print(f"  wrote  {relpath}")

    put("design/layout.json", json.dumps(lay, indent=2) + "\n")
    put("docs/tech/layout.md", layout_doc(game["title"], lay, ev))
    for relpath in contract.write_contract(root, game["title"], game, keep=True):
        written.append(relpath)
        print(f"  wrote  {relpath}")
    put("HANDOFF.md", HANDOFF.format(title=game["title"], day=date.today().isoformat(), written="{n}"),
        forceable=False)
    for relpath in starter_files(root, game["title"]):
        written.append(relpath)
        print(f"  wrote  {relpath}")
    hf = root / "HANDOFF.md"
    if "HANDOFF.md" in written:
        hf.write_text(hf.read_text(encoding="utf-8").replace("{n}", str(len(written))), encoding="utf-8")
    return written


def starter_files(root: Path, title: str) -> list[str]:
    """The starter's files that the game lacks, the merged .gitignore, the map state template."""
    out = []
    for src in sorted(starter.STARTER.rglob("*")):
        relpath = src.relative_to(starter.STARTER).as_posix()
        if src.is_dir() or relpath in starter.SKIP or relpath == "HANDOFF.md" or (root / relpath).exists():
            continue
        if relpath.startswith(("src/", "tests/")):
            continue
        dst = root / relpath
        dst.parent.mkdir(parents=True, exist_ok=True)
        text = src.read_text(encoding="utf-8")
        if relpath in starter.FILLED:
            text = text.replace("<Game name>", title)
        dst.write_text(text, encoding="utf-8", newline="\n")
        out.append(relpath)
    starter.merge_gitignore(root)
    state = root / "docs" / "design" / "maps" / "_template.state.md"
    if not state.exists():
        state.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(starter.MAP_STATE, state)
        out.append(rel(root, state))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--dir", default=".", help="the existing game's root (holds default.project.json)")
    ap.add_argument("--write", action="store_true", help="write the new files (default: read-only)")
    ap.add_argument("--force", action="store_true", help="with --write, replace layout.json and layout.md")
    a = ap.parse_args(argv)
    root = Path(a.dir).expanduser().resolve()
    if not (root / "default.project.json").exists():
        print(f"no default.project.json in {root}: adopt.py takes on a Rojo project", file=sys.stderr)
        return 1

    lay, ev = detect(root)
    game, src = skeleton(root, lay)
    todos = len(contract_todos(game))
    print(f"ADOPT {root}\n\nlayout map (design/layout.json):")
    print(json.dumps(lay, indent=2))
    print("\nevidence:")
    for e in ev:
        print(f"  - {e}")
    print("\ncontract skeleton (design/game.json), filled from the game's docs and code:")
    for s in src:
        print(f"  - {s}")
    print(f"  - {todos} value(s) left as TODO markers for section 1 (plan and asset_plan are added there)")
    if not a.write:
        print("\nread-only: nothing was written. Re-run with --write to create the files that do not exist.")
        return 0
    print("\nwriting (existing files are never overwritten; src/ and tests/ are never touched):")
    written = write(root, lay, ev, game, a.force)
    print(f"\n{len(written)} file(s) written. Next: references/adopt.md, step 3 (the ledger).")
    return 0


def contract_todos(obj) -> list[str]:
    if isinstance(obj, dict):
        return [t for k, v in obj.items() for t in contract_todos(k) + contract_todos(v)]
    if isinstance(obj, list):
        return [t for v in obj for t in contract_todos(v)]
    return [obj] if isinstance(obj, str) and obj.startswith(contract.TODO) else []


if __name__ == "__main__":
    sys.exit(main())
