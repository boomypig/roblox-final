#!/usr/bin/env python3
"""Prove the toolkit works end to end: make a game, run every gate, every command, the hooks, adoption.

    python3 tools/smoke.py            # Packages/ is stubbed when wally is not installed
    python3 tools/smoke.py --wally    # run `wally install` for real (CI does; needs the network)
    python3 tools/smoke.py --keep     # leave the temp folder for inspection

WHY THIS EXISTS. Each script had its own unit tests, and the path between them was never run:
a new game whose gates were red before any code was written, a hook that could not find its
script, a section close that refused an adopted game forever. Only running the whole path in
a clean folder catches those. It runs in CI and must pass before a toolkit phase closes.

What it runs, in a temp folder that holds a link to this toolkit so `../roblox-final` resolves
the way it does for a real game:
  1. tools/new_game.py makes a game; every file the starter promises is there; no placeholder
     is left unexplained.
  2. The four code gates (roblox-code check.py) are green with no game code written.
  3. validate.py fails on the fresh contract (TODO markers, on purpose), then passes once the
     contract is filled.
  4. Every section.py command: brief, resume, handoff, close (refused, then passed), approve,
     resume --expect, handoff --light.
  5. The Stop hook, run with the exact command in the game's .claude/settings.json: silent with
     no boundary, blocking at a boundary without a handoff, allowing once it is written, each
     call under 100 ms, and the lessons it appends.
  6. adopt.py on tests/fixtures/adopted-game: read-only writes nothing; --write proposes the
     expected layout and leaves src/ byte for byte; the gates read the layout; section 1 closes
     with its ledger stages ended `adopted` (gate change 2).

The gate tools are found as real binaries (ROBLOX_TOOLS_BIN, then rokit's tool storage, then
PATH), never through a rokit shim, so the game's pins do not decide what runs here.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import statistics
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SK = ROOT / ".claude" / "skills"
CRG = SK / "create-roblox-game" / "scripts"
CHECK = SK / "roblox-code" / "scripts" / "check.py"
LAYOUT = SK / "roblox-code" / "scripts" / "layout.py"
RUN_LOG = SK / "roblox-build-orchestrator" / "scripts" / "run_log.py"
FIXTURE = ROOT / "tests" / "fixtures" / "adopted-game"
GATE_TOOLS = ["rojo", "lune", "selene", "stylua"]
HOOK_BUDGET_MS = 100

sys.path.insert(0, str(CRG))
import validate  # noqa: E402

PY = sys.executable
results: list[tuple[bool, str, str]] = []


def step(ok: bool, name: str, detail: str = "") -> bool:
    results.append((ok, name, detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}" + (f"\n        {detail}" if detail and not ok else ""))
    return ok


def run(cmd: list[str], cwd: Path, env: dict, stdin: str | None = None) -> subprocess.CompletedProcess:
    return subprocess.run([str(c) for c in cmd], cwd=cwd, env=env, input=stdin, capture_output=True,
                          text=True, timeout=600)


def tail(p: subprocess.CompletedProcess, n: int = 12) -> str:
    return "\n        ".join((p.stdout + p.stderr).strip().splitlines()[-n:])


# ------------------------------------------------------------------ tools

def real_tool(name: str) -> Path | None:
    env_dir = os.environ.get("ROBLOX_TOOLS_BIN")
    if env_dir and (Path(env_dir) / name).exists():
        return Path(env_dir) / name
    store = Path.home() / ".rokit" / "tool-storage"
    found = sorted(store.glob(f"*/{name}/*/{name}"), key=lambda p: [int(x) if x.isdigit() else x
                                                                  for x in re.split(r"[.-]", p.parent.name)])
    if found:
        return found[-1]
    on_path = shutil.which(name)
    if on_path and not re.search(r"[\\/]\.(rokit|aftman|foreman)[\\/]bin[\\/]", on_path):
        return Path(on_path)
    return None


def tool_bin(tmp: Path, want_wally: bool) -> tuple[Path, list[str]]:
    b = tmp / "bin"
    b.mkdir()
    missing = []
    for name in GATE_TOOLS + (["wally"] if want_wally else []):
        p = real_tool(name)
        if p:
            (b / name).symlink_to(p)
        else:
            missing.append(name)
    return b, missing


# ------------------------------------------------------------------ helpers

def fill(obj):
    """Replace every scaffold marker the way section 1 would, with a real value."""
    if isinstance(obj, dict):
        return {(re.sub(r"^TODO:?\s*", "Smoke", k) if validate.is_marker(k) else k): fill(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [fill(v) for v in obj]
    if validate.is_marker(obj):
        return "Filled by the smoke test for this toolkit"
    return obj


def fill_contract(root: Path) -> None:
    gp = root / "design" / "game.json"
    game = fill(json.loads(gp.read_text(encoding="utf-8")))
    game["plan"] = {k: {"declined": "smoke test: no design behind this game"} for k in validate.PLAN_SECTIONS}
    game["asset_plan"] = [{"entity": "the world", "needs": [
        {"stage": "map", "name": "SmokeMap", "why": "the loop needs somewhere to happen"}]}]
    gp.write_text(json.dumps(game, indent=1) + "\n", encoding="utf-8")
    for cfg in game["stages"].values():
        sp = root / cfg["spec"]
        if sp.exists():
            sp.write_text(json.dumps(fill(json.loads(sp.read_text(encoding="utf-8"))), indent=1) + "\n",
                          encoding="utf-8")


def fill_handoff(root: Path) -> None:
    hf = root / "HANDOFF.md"
    lines = ["Filled by the smoke test." if validate.TODO_MARKER.match(ln.strip()) else ln
             for ln in hf.read_text(encoding="utf-8").splitlines()]
    hf.write_text("\n".join(lines) + "\n", encoding="utf-8")


def tree_hash(d: Path) -> str:
    h = hashlib.sha256()
    for p in sorted(d.rglob("*")):
        if p.is_file():
            h.update(p.relative_to(d).as_posix().encode() + p.read_bytes())
    return h.hexdigest()


def hook(root: Path, env: dict) -> tuple[str, float]:
    """Run the Stop hook exactly as the game's settings.json declares it. (stdout, ms)."""
    settings = json.loads((root / ".claude" / "settings.json").read_text(encoding="utf-8"))
    cmd = settings["hooks"]["Stop"][0]["hooks"][0]["command"]
    t = time.perf_counter()
    p = subprocess.run(["sh", "-c", cmd], cwd=root, env=env, input='{"stop_hook_active": false}',
                       capture_output=True, text=True, timeout=30)
    ms = (time.perf_counter() - t) * 1000
    if p.returncode != 0:
        raise RuntimeError(f"hook exited {p.returncode}: {p.stderr.strip()[-300:]}")
    return p.stdout.strip(), ms


def placeholders(root: Path) -> list[str]:
    """`<...>` left in a made game's Markdown, outside code, comments and templates, that does not
    say who fills it ("<fill in ...>")."""
    bad = []
    for p in root.rglob("*.md"):
        if p.name.startswith("_template") or ".git" in p.parts:
            continue
        text = re.sub(r"```.*?```", "", p.read_text(encoding="utf-8"), flags=re.S)
        text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        text = re.sub(r"`[^`\n]*`", "", text)
        for m in re.finditer(r"<([^<>\n]+)>", text):
            if not m.group(1).startswith("fill in"):
                bad.append(f"{p.relative_to(root)}: <{m.group(1)}>")
    return bad


# ------------------------------------------------------------------ the run

def new_game_path(base: Path, env: dict) -> Path:
    print("\n1. new game")
    game = base / "smoke-hours"
    p = run([PY, ROOT / "tools" / "new_game.py", "Smoke Hours", "--dir", game], base, env)
    step(p.returncode == 0, "tools/new_game.py makes a game", tail(p))
    expected = ["CLAUDE.md", "HANDOFF.md", ".claude/settings.json", ".mcp.json", "design/game.json",
                "design/layout.json", "BUILD.md", "docs/design/maps/_template.state.md",
                "docs/tech/architecture.md", "default.project.json", "tests/Health.spec.luau"]
    missing = [e for e in expected if not (game / e).exists()]
    step(not missing, "every promised file is there", f"missing: {missing}")
    step("Smoke Hours" in (game / "CLAUDE.md").read_text(encoding="utf-8"), "CLAUDE.md carries the title")
    bad = placeholders(game)
    step(not bad, "no placeholder is left unexplained", "; ".join(bad[:8]))
    p = run([PY, LAYOUT, "check", "--dir", game], game, env)
    step(p.returncode == 0, "design/layout.json names paths that exist", tail(p))
    return game


def gates(game: Path, env: dict, wally: bool, label: str) -> None:
    if (game / "wally.toml").exists() and not (game / "Packages").exists():
        if wally:
            p = run(["wally", "install"], game, env)
            step(p.returncode == 0, f"{label}: wally install", tail(p))
        else:
            (game / "Packages").mkdir()
            print("  note  wally is not used here: Packages/ is an empty stub, so rojo build proves the "
                  "tree, not the packages (CI runs with --wally)")
    p = run([PY, CHECK, "--dir", game], game, env)
    passed = len(re.findall(r"PASS\S*\s+(rojo|lune|selene|stylua)", p.stdout))
    step(p.returncode == 0, f"{label}: check.py all gates green ({passed} ran)", tail(p, 20))


def contract_path(game: Path, env: dict) -> None:
    print("\n3. contract")
    p = run([PY, CRG / "validate.py", "--dir", game], game, env)
    step(p.returncode == 1 and "unfilled TODO" in p.stdout, "validate.py refuses the fresh contract", tail(p))
    fill_contract(game)
    p = run([PY, CRG / "validate.py", "--dir", game], game, env)
    step(p.returncode == 0, "validate.py passes the filled contract", tail(p))


def sections_path(game: Path, env: dict, base: Path) -> None:
    print("\n4. section.py")
    S = CRG / "section.py"
    p = run([PY, S, "brief", "research and plan"], game, env)
    step(p.returncode == 0 and "SECTION 1" in p.stdout, "brief 'research and plan'", tail(p))
    p = run([PY, S, "resume", "--dir", game], game, env)
    step(p.returncode == 0 and "SECTION 1" in p.stdout, "resume on a new game says section 1", tail(p))
    runs = game / "build-runs"
    for cmd in (["init", "--run", "smoke"], ["start", "--stage", "market-research"],
                ["end", "--stage", "market-research"], ["start", "--stage", "design-spec"],
                ["end", "--stage", "design-spec"]):
        p = run([PY, RUN_LOG, cmd[0], "--dir", runs, *cmd[1:]], game, env)
        step(p.returncode == 0, f"run_log.py {' '.join(cmd)}", tail(p))
    p = run([PY, S, "handoff", "1", "--dir", game, "--ledger", runs / "smoke"], game, env)
    step(p.returncode == 0, "handoff 1", tail(p))
    p = run([PY, S, "close", "1", "--dir", game], game, env)
    step(p.returncode == 1 and "TODO" in p.stdout, "close 1 refuses an unfilled handoff", tail(p))
    fill_handoff(game)
    p = run([PY, S, "close", "1", "--dir", game], game, env)
    step(p.returncode == 0 and "SECTION 1 CLOSED" in p.stdout, "close 1 passes", tail(p))
    out, ms = hook(game, env)
    step(out == "", f"Stop hook allows the stop after close ({ms:.0f} ms)", out[:200])
    p = run([PY, S, "resume", "--dir", game], game, env)
    step("approve 1 --implied" in p.stdout, "resume prints approve --implied for an unapproved close", tail(p))
    p = run([PY, S, "approve", "1", "--dir", game], game, env)
    step(p.returncode == 0 and "APPROVED" in p.stdout, "approve 1", tail(p))
    p = run([PY, S, "resume", "--dir", game, "--expect", "2"], game, env)
    step(p.returncode == 0 and "SECTION 2" in p.stdout, "resume --expect 2", tail(p))
    p = run([PY, S, "resume", "--dir", game, "--expect", "3"], game, env)
    step(p.returncode == 1 and "STOP" in p.stdout, "resume --expect 3 refuses out of order", tail(p))
    p = run([PY, S, "handoff", "--light", "map", "--what", "harbor", "--dir", game], game, env)
    archived = list((game / "design" / "handoffs").glob("HANDOFF-section-1.md"))
    step(p.returncode == 0 and archived and "<!-- handoff: map -->" in (game / "HANDOFF.md").read_text(),
         "handoff --light map writes the short form and archives the section handoff", tail(p))


def hook_path(game: Path, env: dict, inbox: Path) -> None:
    print("\n5. Stop hook (outside a section)")
    times = []
    out, ms = hook(game, env)
    times.append(ms)
    step(out == "", f"no boundary: silent ({ms:.0f} ms)", out[:200])
    run([PY, CRG / "session.py", "log", "--gate", "smoke gate", "--note", "a failure for the inbox", "--dir", game],
        game, env)
    time.sleep(1.2)  # the boundary must be measurably newer than the HANDOFF.md new_game.py wrote
    run([PY, CRG / "session.py", "mark", "build", "--what", "coins", "--dir", game], game, env)
    out, ms = hook(game, env)
    times.append(ms)
    blocked = out and json.loads(out).get("decision") == "block"
    step(bool(blocked), f"build boundary, stale handoff: blocks ({ms:.0f} ms)", out[:200])
    run([PY, CRG / "section.py", "handoff", "--light", "build", "--what", "coins", "--dir", game], game, env)
    out, ms = hook(game, env)
    times.append(ms)
    step("unfilled" in out, f"handoff with TODO lines: still blocks ({ms:.0f} ms)", out[:200])
    fill_handoff(game)
    out, ms = hook(game, env)
    times.append(ms)
    step(out == "", f"handoff filled: allows ({ms:.0f} ms)", out[:200])
    text = inbox.read_text(encoding="utf-8") if inbox.exists() else ""
    step("gate failure: smoke gate: a failure for the inbox" in text, "lessons inbox got the gate failure",
         text[-300:])
    for _ in range(3):
        times.append(hook(game, env)[1])
    med = statistics.median(times)
    step(max(times) < HOOK_BUDGET_MS * 2 and med < HOOK_BUDGET_MS,
         f"hook time: median {med:.0f} ms, max {max(times):.0f} ms (budget {HOOK_BUDGET_MS} ms)")


def adopt_path(base: Path, env: dict, wally: bool) -> None:
    print("\n6. adopt.py on the fixture")
    game = base / "harbor-rush"
    shutil.copytree(FIXTURE, game)
    before_all, before_src = tree_hash(game), tree_hash(game / "src")
    A = CRG / "adopt.py"
    p = run([PY, A, "--dir", game], game, env)
    step(p.returncode == 0 and tree_hash(game) == before_all, "read-only by default: nothing written", tail(p))
    p = run([PY, A, "--dir", game, "--write"], game, env)
    step(p.returncode == 0, "--write", tail(p))
    step(tree_hash(game / "src") == before_src, "src/ is byte for byte unchanged (no reformat)")
    lay = json.loads((game / "design" / "layout.json").read_text(encoding="utf-8"))
    want = {"framework": "modules", "remotes": {"style": "per-service", "where": "ReplicatedStorage.Remotes"},
            "config": "src/shared/Config.luau", "pure": ["src/shared/RoundTimer.luau", "src/shared/Scoring.luau"],
            "tests": None, "packages": "none", "toolchain": "rokit.toml",
            "map": {"source": "studio", "brief": "docs/design/maps/harbor.md"},
            "boot": {"server": "src/server/Main.server.luau", "client": "src/client/Main.client.luau"}}
    wrong = {k: lay.get(k) for k, v in want.items() if lay.get(k) != v}
    step(not wrong, "the layout matches the adopted game's shape", f"differs: {wrong}")
    gates(game, env, wally, "adopted game")

    out, _ = hook(game, env)
    step(out == "", "Stop hook is silent in the adopted game with no boundary", out[:200])
    runs = game / "build-runs"
    run([PY, RUN_LOG, "init", "--dir", runs, "--run", "harbor"], game, env)
    for stage in ("market-research", "design-spec"):
        p = run([PY, RUN_LOG, "end", "--dir", runs, "--run", "harbor", "--stage", stage, "--status", "adopted"],
                game, env)
        step(p.returncode == 0, f"run_log.py end --stage {stage} --status adopted (no start)", tail(p))
    fill_contract(game)
    p = run([PY, CRG / "validate.py", "--dir", game], game, env)
    step(p.returncode == 0, "validate.py still has to pass, and does once the contract is filled", tail(p))
    S = CRG / "section.py"
    run([PY, S, "handoff", "1", "--dir", game, "--ledger", runs / "harbor"], game, env)
    fill_handoff(game)
    p = run([PY, S, "close", "1", "--dir", game], game, env)
    step(p.returncode == 0, "close 1 accepts the adopted ledger stages (gate change 2)", tail(p))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--wally", action="store_true", help="run `wally install` (needs wally and the network)")
    ap.add_argument("--keep", action="store_true", help="keep the temp folder")
    a = ap.parse_args(argv)
    tmp = Path(tempfile.mkdtemp(prefix="roblox-final-smoke-"))
    try:
        base = tmp / "games"
        base.mkdir()
        (base / "roblox-final").symlink_to(ROOT, target_is_directory=True)  # ../roblox-final from a game
        bin_dir, missing = tool_bin(tmp, a.wally)
        print(f"smoke: {tmp}")
        if not step(not missing, "gate tools found as real binaries", f"missing: {missing}; install them or "
                    "set ROBLOX_TOOLS_BIN (README, Requirements)"):
            return 1
        inbox = tmp / "private" / "lessons-inbox.md"
        env = {**os.environ, "PATH": f"{bin_dir}{os.pathsep}/usr/bin{os.pathsep}/bin",
               "ROBLOX_FINAL_PRIVATE": str(tmp / "private"), "ROBLOX_GAMES_HOME": str(base)}
        env.pop("CLAUDE_PROJECT_DIR", None)
        game = new_game_path(base, env)
        print("\n2. gates on the empty game")
        gates(game, env, a.wally, "new game")
        contract_path(game, env)
        sections_path(game, env, base)
        other = base / "change-loop"
        run([PY, ROOT / "tools" / "new_game.py", "Change Loop", "--dir", other], base, env)
        hook_path(other, env, inbox)
        adopt_path(base, env, a.wally)
    finally:
        if a.keep:
            print(f"\nkept {tmp}")
        else:
            shutil.rmtree(tmp, ignore_errors=True)
    failed = [r for r in results if not r[0]]
    print(f"\n{len(results) - len(failed)} passed, {len(failed)} failed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
