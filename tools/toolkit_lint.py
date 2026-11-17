#!/usr/bin/env python3
"""Lint the toolkit itself: duplicated rules, dead paths, stale cards, untested scripts, private data.

    python3 tools/toolkit_lint.py                    # exit 1 on any finding not in the baseline
    python3 tools/toolkit_lint.py --all              # also print the baselined findings
    python3 tools/toolkit_lint.py --write-baseline   # accept today's findings (a human decision)

Run it when editing the toolkit, and in CI. Never during a game build: it reads only this repo.

WHY THIS EXISTS. The toolkit is maintained by sessions that each see part of it. Each check
below is a way it has already decayed:
  dup      the same rule written in two files, which then drift apart (docs/redundancy-map.md
           consolidated a dozen of these by hand);
  path     a path or `file:line` reference to something that moved, shrank or never existed;
  card     an agent card older than the sections it copies (tools/build_cards.py --check);
  untested a script no test or smoke step runs, so nothing notices when it breaks;
  private  a private path, an email, a home folder or a term from private/identity.txt in a
           tracked file (the patterns are tests/test_public_tree.py's; this runs them as a lint).

The baseline (tools/toolkit_lint_baseline.txt) lists findings that existed when the lint was
written, so it fails only on new ones. Shrink it; never grow it to make a change pass.
"""
from __future__ import annotations

import argparse
import importlib.util
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASELINE = ROOT / "tools" / "toolkit_lint_baseline.txt"
SKILLS = ROOT / ".claude" / "skills"
MIN_WORDS = 14
# Files whose job is to quote or log other files: their repeats are not second owners.
DUP_EXEMPT = {"CHANGELOG.md", "docs/decisions.md", "docs/migration.md", "docs/redundancy-map.md",
              "docs/vault-readers.md", "vault/CATALOG.md"}
CHECKED_ROOTS = (".claude/skills/", ".claude/agents/", "tools/", "vault/", "starter/")
# Files whose job is to name old paths and old line numbers: a record, not a reference.
HISTORY = {"CHANGELOG.md", "docs/decisions.md", "docs/migration.md", "docs/redundancy-map.md",
           "docs/vault-readers.md"}


def _load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pt = _load("public_tree", ROOT / "tests" / "test_public_tree.py")
cards = _load("build_cards", ROOT / "tools" / "build_cards.py")


def text_of(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return ""


def rel(p: Path) -> str:
    return p.relative_to(ROOT).as_posix()


def is_generated(text: str) -> bool:
    return text.startswith("---") and "generated-by:" in text.split("---", 2)[1] if text.count("---") >= 2 else False


# ------------------------------------------------------------------ dup

def sentences(text: str) -> list[str]:
    text = re.sub(r"```.*?```", " ", text, flags=re.S)
    text = re.sub(r"^\|.*$", " ", text, flags=re.M)           # tables are indexes, not rules
    text = re.sub(r"^---\n.*?\n---\n", " ", text, flags=re.S)  # frontmatter
    out = []
    for chunk in re.split(r"(?<=[.!?])\s+|\n\s*\n|\n[-*] |\n\d+\. ", text):
        words = re.findall(r"[a-z0-9']+", chunk.lower())
        if len(words) >= MIN_WORDS and "http" not in chunk:  # a shared source citation is not a rule
            out.append(" ".join(words))
    return out


def check_dup(files: list[Path]) -> list[tuple[str, str, str]]:
    seen: dict[str, set[str]] = defaultdict(set)
    for p in files:
        r = rel(p)
        if p.suffix != ".md" or r in DUP_EXEMPT or r.startswith("tests/fixtures/"):
            continue
        t = text_of(p)
        if is_generated(t):
            continue
        for s in set(sentences(t)):
            seen[s].add(r)
    out = []
    for s, where in seen.items():
        if len(where) > 1:
            first = sorted(where)
            out.append(("dup", first[0], f"also in {', '.join(first[1:])}: \"{' '.join(s.split()[:12])} ...\""))
    return out


# ------------------------------------------------------------------ path

TOKEN = re.compile(r"`([^`\s]+)`|\]\(([^)#\s]+)")
LINE_REF = re.compile(r"([\w./-]+\.(?:py|md|lua|luau|json|toml|yml)):(\d+)(?:-(\d+))?")


def owner_skill(p: Path) -> Path | None:
    parts = p.relative_to(ROOT).parts
    if len(parts) > 2 and parts[0] == ".claude" and parts[1] == "skills":
        return SKILLS / parts[2]
    return None


def resolve(token: str, p: Path) -> Path | None | bool:
    """A Path if the token names a toolkit file we can check, True if it exists, None to skip."""
    t = token.strip().rstrip(".,;:")
    if any(c in t for c in "<>*{}$…|") or "..." in t or t.startswith(("http", "#", "mailto:")):
        return None
    for pre in ("~/roblox-final/", "../roblox-final/", "roblox-final/"):
        if t.startswith(pre):
            t = t[len(pre):]
            break
    else:
        if p.parent != ROOT and (p.parent / t).exists():
            return True
    sk = owner_skill(p)
    if t.startswith(("references/", "scripts/", "templates/")) and sk:
        # "roblox-code's `references/security.md`": a skill naming another skill's file.
        if not (sk / t).exists() and list(SKILLS.glob(f"*/{t}")):
            return True
        return sk / t
    if t.startswith(CHECKED_ROOTS):
        return ROOT / t
    m = re.match(r"(roblox-[\w-]+|create-roblox-game|build|pitch|art-brief|toolkit-retro)/(references|scripts)/", t)
    if m and (SKILLS / m.group(1)).is_dir():
        return SKILLS / t
    if re.fullmatch(r"docs/[\w.-]+\.md", t):
        return True if (ROOT / t).exists() or (ROOT / "starter" / t).exists() else ROOT / t
    return None


def find_file(name: str, p: Path) -> Path | None:
    cands = [ROOT / name]
    sk = owner_skill(p)
    if sk:
        cands += [sk / name, sk / "scripts" / name, sk / "references" / name]
    cands += [SKILLS / name]
    for c in cands:
        if c.is_file():
            return c
    hits = [h for h in ROOT.rglob(Path(name).name) if ".git" not in h.parts and "private" not in h.parts]
    return hits[0] if len(hits) == 1 else None


def check_path(files: list[Path]) -> list[tuple[str, str, str]]:
    out = []
    for p in files:
        if p.suffix != ".md" or rel(p).startswith(("tests/fixtures/", "starter/")) or rel(p) in HISTORY:
            continue
        t = text_of(p)
        if is_generated(t):
            continue
        t = re.sub(r"```.*?```", "", t, flags=re.S)
        for n, line in enumerate(t.splitlines(), 1):
            for a, b in TOKEN.findall(line):
                token = a or b
                if LINE_REF.fullmatch(token.rstrip(".,;")):
                    continue
                target = resolve(token, p)
                if isinstance(target, Path) and not target.exists() and not target.with_suffix("").exists():
                    out.append(("path", rel(p), f"names {token}, which does not exist"))
            for name, a, b in LINE_REF.findall(line):
                if "<" in name or name.startswith("http"):
                    continue
                f = find_file(name, p)
                if f is None:
                    continue
                last = int(b or a)
                length = len(text_of(f).splitlines())
                if last > length:
                    out.append(("path", rel(p), f"{name}:{a}{'-' + b if b else ''} is past the end ({length} lines)"))
    return out


# ------------------------------------------------------------------ card, untested, private

def check_card() -> list[tuple[str, str, str]]:
    return [("card", cards.CARDS[n]["path"], msg) for n in cards.CARDS for msg in cards.check(n)]


def check_untested(files: list[Path]) -> list[tuple[str, str, str]]:
    """A script is covered when a test or smoke.py names it, or a covered script does (it runs it)."""
    scripts = [p for p in files if p.suffix == ".py" and p.name != "__init__.py" and "/tests/" not in rel(p)
               and (re.match(r"tools/[^/]+\.py$", rel(p)) or re.match(r"\.claude/skills/[^/]+/scripts/", rel(p)))]
    covered_text = "\n".join(text_of(p) for p in files
                             if (rel(p).startswith("tests/") and p.suffix == ".py") or rel(p) == "tools/smoke.py")
    covered: set[Path] = set()
    while True:
        new = {p for p in scripts if p not in covered
               and (re.search(rf"\b{re.escape(p.name)}\b", covered_text)
                    or re.search(rf"\bimport {re.escape(p.stem)}\b", covered_text))}
        if not new:
            break
        covered |= new
        covered_text += "\n" + "\n".join(text_of(p) for p in new)
    return [("untested", rel(p), "no test or smoke step runs or imports it, directly or through a script")
            for p in scripts if p not in covered and rel(p) != "tools/smoke.py"]


def check_private(files: list[Path]) -> list[tuple[str, str, str]]:
    terms = []
    tf = pt.PRIVATE / "identity.txt"
    if tf.exists():
        terms = [t.strip().lower() for t in tf.read_text(encoding="utf-8").splitlines()
                 if t.strip() and not t.startswith("#")]
    allowed = re.compile(r"github\.com/[\w-]+/roblox-final")
    out = []
    for p in files:
        r = rel(p)
        if r in pt.SELF:
            continue
        for n, line in enumerate(text_of(p).splitlines(), 1):
            why = None
            for m in pt.EMAIL.finditer(line):
                if not pt.EMAIL_OK.search(m.group(0)):
                    why = "an email address"
            for m in pt.HOME.finditer(line):
                if m.group(1) not in pt.HOME_OK:
                    why = f"a machine path ({m.group(0)})"
            m = pt.SPECIFIC_PRIVATE.search(line)
            if m and r not in pt.MOVED_OK:
                why = f"a specific private file ({m.group(0)})"
            low = allowed.sub("", line.lower())
            if any(re.search(r"(?<![a-z0-9])" + re.escape(t) + r"(?![a-z0-9])", low) for t in terms):
                why = "a term from private/identity.txt"
            if why:
                out.append(("private", r, f"line {n}: {why}"))
    return out


def key(f: tuple[str, str, str]) -> str:
    return " | ".join(f)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--all", action="store_true", help="print baselined findings too")
    ap.add_argument("--write-baseline", action="store_true", help="accept every current finding")
    a = ap.parse_args(argv)
    files = pt.tracked()
    findings = check_dup(files) + check_path(files) + check_card() + check_untested(files) + check_private(files)
    findings.sort()
    if a.write_baseline:
        keep = [key(f) for f in findings if f[0] != "private"]  # private data is never accepted
        BASELINE.write_text("# Findings accepted when the lint was written. Shrink this; never grow it.\n"
                            + "\n".join(keep) + "\n", encoding="utf-8")
        print(f"baseline: {len(keep)} finding(s) written to {rel(BASELINE)}")
        return 0
    base = set()
    if BASELINE.exists():
        base = {ln for ln in BASELINE.read_text(encoding="utf-8").splitlines() if ln and not ln.startswith("#")}
    new = [f for f in findings if key(f) not in base or f[0] == "private"]
    old = [f for f in findings if f not in new]
    gone = base - {key(f) for f in findings}
    for f in new:
        print(f"FAIL  {f[0]:8} {f[1]}: {f[2]}")
    if a.all:
        for f in old:
            print(f"base  {f[0]:8} {f[1]}: {f[2]}")
    if gone:
        print(f"note  {len(gone)} baselined finding(s) are fixed: remove them from {rel(BASELINE)}")
    counts = defaultdict(int)
    for f in findings:
        counts[f[0]] += 1
    print(f"{len(new)} new, {len(old)} baselined ("
          + ", ".join(f"{k} {counts[k]}" for k in ("dup", "path", "card", "untested", "private")) + ")")
    return 1 if new else 0


if __name__ == "__main__":
    sys.exit(main())
