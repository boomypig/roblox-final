#!/usr/bin/env python3
"""Session boundaries: refuse to stop at one without an up-to-date HANDOFF.md, and keep lessons.

    session.py stop   [--dir GAME]                  # the Stop hook (reads the hook's JSON on stdin)
    session.py mark   build|map|section --what X [--dir GAME]   # a boundary was reached
    session.py log    --gate NAME --note TEXT [--dir GAME]       # a gate failed (gates call this)
    session.py status [--dir GAME]                  # what the hook would do now, and why

WHY THIS EXISTS. Every session starts cold, so whatever was not written down when the last one
ended is gone. section.py close already refuses to pass without a filled HANDOFF.md, but a map
pass or a /build ended with no handoff at all, and the next session re-toured Studio and
re-derived decisions. A model step that "remembers to write the handoff" is the thing that
failed; a hook does not forget.

A session ends at exactly one of three boundaries:
  - section     `section.py close N` passed (it calls `mark section`);
  - build       one /build passed its gates (its last step runs `mark build`);
  - map         one map-builder run reported: a map's state file has a new Pass log row and an
                empty "Run in progress" (detected from the file, since the agent has no shell).
Inside a section (design/sections.json exists and the game is not finished), only the section
boundary counts: a /build or map pass there is part of the section, and stopping inside a
section is never interrupted. With no boundary, the hook exits at once and prints nothing.

At a boundary, the hook allows the stop only when HANDOFF.md was written after the boundary and
has no unfilled line (the TODO marker validate.py defines). Otherwise it blocks with the command
that writes one. After MAX_BLOCKS refusals it lets the session stop and records a handoff debt,
so a stuck session cannot loop forever.

When a boundary is passed, the lessons since the last one are appended to
private/lessons-inbox.md in the toolkit: gate failures (logged by the gates through `log`),
the ledger's stalls, fallbacks and interventions, failed ledger stages, and the handoff's
"Debts" lines. That is a plain file append, never a model step; /toolkit-retro reads the inbox
when the user asks for it. A missing private/ folder is created (it is gitignored).

Budget: under 100 ms per call (tools/smoke.py measures it). The hook adds no prompt.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
TOOLKIT = HERE.parents[3]  # scripts -> create-roblox-game -> skills -> .claude -> toolkit
MAX_BLOCKS = 3
LEDGER_KINDS = ("fallback", "stall", "intervention")
SKIP_DEBT = re.compile(r"^(none|n/a|-|\(none\))\.?$", re.I)

sys.path.insert(0, str(HERE))
from validate import TODO_MARKER  # noqa: E402  one definition of "unfilled"


# ------------------------------------------------------------------ files

def session_dir(root: Path) -> Path:
    return root / ".claude" / "session"


def read_json(p: Path, default):
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return default


def write_json(p: Path, data) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def is_game(root: Path) -> bool:
    return (root / "design").is_dir() or (root / "HANDOFF.md").exists()


def inbox_path() -> Path:
    private = Path(os.environ.get("ROBLOX_FINAL_PRIVATE") or TOOLKIT / "private").expanduser()
    return private / "lessons-inbox.md"


# ------------------------------------------------------------------ writes from gates and steps

def log_event(root: Path, gate: str, note: str) -> None:
    """Record a gate failure for the next lessons append. Silent outside a game repo."""
    if not is_game(root):
        return
    d = session_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    rec = {"t": time.time(), "kind": "gate-failure", "gate": gate, "note": note[:300]}
    with (d / "log.jsonl").open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")


def mark(root: Path, kind: str, what: str, at: float | None = None) -> dict:
    """A boundary was reached. `at` is the time the handoff must be newer than (default now)."""
    b = {"kind": kind, "what": what, "at": time.time() if at is None else at}
    write_json(session_dir(root) / "boundary.json", b)
    return b


# ------------------------------------------------------------------ reading the game

def in_section(root: Path) -> bool:
    st = read_json(root / "design" / "sections.json", None)
    if not isinstance(st, dict):
        return False
    from section import SECTIONS  # lazy: section.py imports this module
    return str(len(SECTIONS)) not in st.get("closed", {})


def section_text(text: str, heading: str) -> list[str]:
    m = re.search(rf"^## {re.escape(heading)}\s*$(.*?)(?=^## |\Z)", text, re.M | re.S)
    return [ln.strip() for ln in m.group(1).splitlines() if ln.strip()] if m else []


def map_boundary(root: Path, since: float) -> dict | None:
    """The newest map state file that a finished map-builder run updated after `since`."""
    best = None
    for p in (root / "docs" / "design" / "maps").glob("*.state.md"):
        mt = p.stat().st_mtime
        if mt <= since or (best and mt <= best["at"]):
            continue
        text = p.read_text(encoding="utf-8")
        running = [ln for ln in section_text(text, "Run in progress") if ln.startswith("- ")]
        rows = [ln for ln in section_text(text, "Pass log")
                if ln.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", ln) and not ln.startswith("| Date")]
        if rows and running in ([], ["- (none)"]):
            best = {"kind": "map", "what": p.name[: -len(".state.md")], "at": mt}
    return best


def unfilled(text: str) -> list[str]:
    return [ln for ln in text.splitlines() if TODO_MARKER.match(ln.strip().lstrip("-* ").strip())]


def handoff_state(root: Path, at: float) -> str:
    """'' when HANDOFF.md is up to date for a boundary at `at`, else why not."""
    hf = root / "HANDOFF.md"
    if not hf.exists():
        return "there is no HANDOFF.md"
    if hf.stat().st_mtime + 1 < at:
        return "HANDOFF.md is older than the end of this run"
    left = unfilled(hf.read_text(encoding="utf-8"))
    if left:
        return f"HANDOFF.md still has {len(left)} unfilled line(s), first: {left[0].strip()[:60]!r}"
    return ""


def boundary(root: Path, since: float) -> dict | None:
    b = read_json(session_dir(root) / "boundary.json", None)
    sectioned = in_section(root)
    if isinstance(b, dict) and b.get("kind") == "section":
        return b
    if sectioned:
        return None  # a /build or map pass inside a section is part of the section
    if isinstance(b, dict) and b.get("kind") in ("build", "map"):
        return b
    return map_boundary(root, since)


# ------------------------------------------------------------------ lessons

def iso_epoch(s: str) -> float:
    try:
        return datetime.fromisoformat(s).timestamp()
    except (TypeError, ValueError):
        return 0.0


def lessons(root: Path, since: float, b: dict, debt: str | None) -> list[str]:
    out: list[str] = []
    log = session_dir(root) / "log.jsonl"
    if log.exists():
        for line in log.read_text(encoding="utf-8").splitlines():
            e = read_json_line(line)
            if e and e.get("t", 0) > since:
                out.append(f"- gate failure: {e.get('gate')}: {e.get('note')}")
    st = read_json(root / "design" / "sections.json", {})
    ledger = Path(st["ledger"]) / "events.jsonl" if isinstance(st, dict) and st.get("ledger") else None
    if ledger and ledger.exists():
        for line in ledger.read_text(encoding="utf-8").splitlines():
            e = read_json_line(line)
            if not e or iso_epoch(e.get("ts", "")) <= since:
                continue
            if e.get("kind") in LEDGER_KINDS:
                out.append(f"- {e['kind']} ({e.get('stage') or '-'}): {e.get('note')}")
            elif e.get("kind") == "end" and e.get("status") in ("failed", "fell-back"):
                out.append(f"- stage {e.get('stage')} ended {e.get('status')}")
    hf = root / "HANDOFF.md"
    if hf.exists():
        for ln in section_text(hf.read_text(encoding="utf-8"), "Debts"):
            item = ln.lstrip("-* ").strip()
            if item and not SKIP_DEBT.match(item):
                out.append(f"- handoff debt: {item}")
    if debt:
        out.append(f"- handoff debt: {debt}")
    return out


def read_json_line(line: str):
    line = line.strip()
    if not line:
        return None
    try:
        return json.loads(line)
    except ValueError:
        return None


def consume(root: Path, b: dict, debt: str | None = None) -> int:
    """Append this boundary's lessons to the inbox and start a fresh span. Returns lines added."""
    sd = session_dir(root)
    st = read_json(sd / "state.json", {})
    items = lessons(root, float(st.get("consumed", 0)), b, debt)
    if items:
        inbox = inbox_path()
        inbox.parent.mkdir(parents=True, exist_ok=True)
        new = not inbox.exists()
        stamp = datetime.now().astimezone().isoformat(timespec="minutes")
        with inbox.open("a", encoding="utf-8") as fh:
            if new:
                fh.write("# Lessons inbox\n\nAppended by session.py at each session boundary. "
                         "/toolkit-retro turns each entry into one tested edit.\n")
            fh.write(f"\n## {stamp} {root.name}: {b['kind']} {b.get('what') or ''}".rstrip() + "\n\n")
            fh.write("\n".join(items) + "\n")
    write_json(sd / "state.json", {"consumed": time.time(), "blocks": 0})
    (sd / "boundary.json").unlink(missing_ok=True)
    return len(items)


# ------------------------------------------------------------------ commands

def game_root(dir_arg: str | None, payload: dict) -> Path:
    for cand in (dir_arg, os.environ.get("CLAUDE_PROJECT_DIR"), payload.get("cwd")):
        if cand:
            return Path(cand).expanduser().resolve()
    return Path.cwd()


def handoff_command(b: dict) -> str:
    s = "python3 ../roblox-final/.claude/skills/create-roblox-game/scripts/section.py"
    if b["kind"] == "section":
        return f"{s} handoff {b.get('what')} --force --dir ."
    return f"{s} handoff --light {b['kind']} --what \"{b.get('what') or ''}\" --dir ."


def cmd_stop(a) -> int:
    payload = {}
    if not sys.stdin.isatty():
        payload = read_json_line(sys.stdin.read()) or {}
    root = game_root(a.dir, payload)
    if not is_game(root):
        return 0
    sd = session_dir(root)
    st = read_json(sd / "state.json", {})
    b = boundary(root, float(st.get("consumed", 0)))
    if not b:
        return 0
    why = handoff_state(root, float(b["at"]))
    if not why:
        consume(root, b)
        return 0
    blocks = int(st.get("blocks", 0))
    if blocks >= MAX_BLOCKS:
        consume(root, b, debt=f"the session stopped after a {b['kind']} boundary with no up-to-date "
                               f"HANDOFF.md ({why})")
        return 0
    write_json(sd / "state.json", {**st, "blocks": blocks + 1})
    if why.startswith("HANDOFF.md still has"):
        todo = "fill the remaining TODO lines in HANDOFF.md"  # rewriting it would lose what is filled
    else:
        todo = f"run `{handoff_command(b)}` and fill every TODO line"
    reason = (f"Session boundary reached ({b['kind']}: {b.get('what')}), but {why}. Before stopping, "
              f"{todo} with what was done, verified, left unproven and owed, so the next session can "
              f"start from it. Then stop.")
    print(json.dumps({"decision": "block", "reason": reason}))
    return 0


def cmd_mark(a) -> int:
    root = game_root(a.dir, {})
    b = mark(root, a.kind, a.what or "", a.at)
    print(f"boundary: {b['kind']} {b['what']}. Write HANDOFF.md before stopping "
          f"(`{handoff_command(b)}`).")
    return 0


def cmd_log(a) -> int:
    log_event(game_root(a.dir, {}), a.gate, a.note)
    return 0


def cmd_status(a) -> int:
    root = game_root(a.dir, {})
    st = read_json(session_dir(root) / "state.json", {})
    b = boundary(root, float(st.get("consumed", 0))) if is_game(root) else None
    print(f"game:      {root}{'' if is_game(root) else ' (not a game repo: the hook does nothing)'}")
    print(f"section:   {'inside a section' if is_game(root) and in_section(root) else 'no section open'}")
    if not b:
        print("boundary:  none (the hook lets the session stop)")
        return 0
    why = handoff_state(root, float(b["at"]))
    print(f"boundary:  {b['kind']} {b.get('what')}")
    print(f"handoff:   {'up to date' if not why else why}")
    print(f"blocks:    {st.get('blocks', 0)} of {MAX_BLOCKS}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("stop"); p.add_argument("--dir"); p.set_defaults(func=cmd_stop)
    p = sub.add_parser("mark"); p.add_argument("kind", choices=["build", "map", "section"])
    p.add_argument("--what"); p.add_argument("--at", type=float); p.add_argument("--dir")
    p.set_defaults(func=cmd_mark)
    p = sub.add_parser("log"); p.add_argument("--gate", required=True); p.add_argument("--note", required=True)
    p.add_argument("--dir"); p.set_defaults(func=cmd_log)
    p = sub.add_parser("status"); p.add_argument("--dir"); p.set_defaults(func=cmd_status)
    a = ap.parse_args(argv)
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
