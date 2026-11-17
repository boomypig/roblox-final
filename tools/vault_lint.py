"""Check vault files against vault/CONTRIBUTING.md rules. Stdlib only.

Usage: python3 tools/vault_lint.py [--quiet]
Exit code 1 if any ERROR is found; WARNs don't fail.

The list of files comes from vault/CATALOG.md (vault/INDEX.md is the short form readers load).
Catalog rows may point outside vault/: build references live in the owning skill's references/
folder and are linted here with the same rules, so moving a file never lowers its bar.

Case studies of named games are private notes (private/case-studies/, or
$ROBLOX_FINAL_PRIVATE/case-studies/). When that folder exists they are linted with the same
rules and every `(case study: <slug>)` marker in the vault must name one of them. When it is
missing the markers are counted, not checked, and the lint still passes: a fresh clone of the
toolkit has no private folder.
"""

from __future__ import annotations

import os
import os.path
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
PRIVATE = Path(os.environ.get("ROBLOX_FINAL_PRIVATE") or ROOT / "private").expanduser()
CASE_STUDIES = PRIVATE / "case-studies"
REQUIRED_KEYS = ["title", "type", "read-when", "last-researched"]
TYPES = {"genre", "fundamental", "pattern", "case-study", "trends", "meta"}
FOLDER_TYPES = {"genres": "genre", "fundamentals": "fundamental", "patterns": "pattern", "case-studies": "case-study"}
CLAIM_TAG = re.compile(r"\((?:official|community|press|data|inferred)\b")
LINK = re.compile(r"\]\(([^)#\s]+\.md)(?:#[^)]*)?\)")
CASE_MARKER = re.compile(r"[Cc]ase study: ([a-z0-9][a-z0-9-]*[a-z0-9])\b")
# Deprecated or nonexistent APIs. A line is allowed if it also says why (deprecated, doesn't exist, ...).
BANNED = [
    (re.compile(r"Lighting\.Technology|Technology\s*=\s*(?:Future|ShadowMap|Voxel)"), "Lighting.Technology is deprecated; use LightingStyle"),
    (re.compile(r"\bUIFlexLayout\b"), "UIFlexLayout doesn't exist; use UIListLayout flex + UIFlexItem"),
    (re.compile(r"GetProductInfo\("), "GetProductInfo is deprecated; use GetProductInfoAsync"),
    (re.compile(r"\b(?:TweenSize|TweenPosition)\b"), "GuiObject:TweenSize/TweenPosition are deprecated; use TweenService"),
    (re.compile(r"\[\[[^\]]+\]\]"), "wikilinks aren't allowed; use relative markdown links"),
]
ALLOW_WORDS = re.compile(r"deprecat|doesn't exist|does not exist|not exist|\bno\b|never|don't|instead|replaced|legacy|old ", re.I)
META = {"INDEX.md", "CATALOG.md", "CONTRIBUTING.md", "case-studies/INDEX.md"}


def frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end == -1:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        if ":" in line and not line.startswith(" "):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def index_entries(index: Path, prefix: str = "") -> tuple[set[str], dict[str, str]]:
    """Rows of an index table, as paths relative to the vault ('case-studies/x.md' for private ones)."""
    listed, status = set(), {}
    if not index.exists():
        return listed, status
    for row in index.read_text(encoding="utf-8").splitlines():
        m = re.match(r"\| \[[^\]]+\]\(([^)]+)\) \|.*\| *([a-z][a-z ()-]*?) *\|$", row)
        if m:
            listed.add(prefix + m.group(1))
            status[prefix + m.group(1)] = m.group(2)
    return listed, status


def sources(listed: set[str] | None = None) -> list[tuple[str, Path]]:
    """(name the lint reports, file) for every file to check: the vault, catalog rows that point
    outside it (named as the catalog names them, e.g. '../.claude/skills/x/references/y.md'), and
    the private case studies when present."""
    if listed is None:
        listed, _ = index_entries(VAULT / "CATALOG.md")
    out = [(p.relative_to(VAULT).as_posix(), p) for p in sorted(VAULT.rglob("*.md"))]
    for entry in sorted(e for e in listed if e.startswith("../")):
        p = (VAULT / entry).resolve()
        if p.exists():
            out.append((entry, p))
    if CASE_STUDIES.is_dir():
        out += [("case-studies/" + p.name, p) for p in sorted(CASE_STUDIES.glob("*.md"))]
    return out


def lint() -> tuple[list[str], list[str]]:
    errors, warns = [], []
    listed, status = index_entries(VAULT / "CATALOG.md")
    catalog_only = set(listed)
    have_cases = CASE_STUDIES.is_dir()
    if have_cases:
        more, more_status = index_entries(CASE_STUDIES / "INDEX.md", "case-studies/")
        listed |= more
        status.update(more_status)
    unchecked_markers = 0

    for rel, path in sources(catalog_only):
        text = path.read_text(encoding="utf-8")
        lines = text.count("\n")
        fm = frontmatter(text)
        is_meta = rel in META

        if fm is None:
            errors.append(f"{rel}: missing frontmatter")
            continue
        missing = [k for k in REQUIRED_KEYS if k not in fm]
        if missing:
            errors.append(f"{rel}: frontmatter missing {', '.join(missing)}")
        if fm.get("type") not in TYPES:
            errors.append(f"{rel}: type '{fm.get('type')}' not in {sorted(TYPES)}")
        folder = rel.split("/")[0]
        if not is_meta and folder in FOLDER_TYPES and fm.get("type") != FOLDER_TYPES[folder]:
            errors.append(f"{rel}: type '{fm.get('type')}' should be '{FOLDER_TYPES[folder]}' in {folder}/")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", fm.get("last-researched", "")):
            errors.append(f"{rel}: last-researched must be YYYY-MM-DD")

        if not is_meta:
            if not 100 <= lines <= 400:
                errors.append(f"{rel}: {lines} lines (must be 100-400)")
            srcs = text.split("## Sources", 1)
            if len(srcs) < 2 or "http" not in srcs[1]:
                errors.append(f"{rel}: no '## Sources' section with URLs")
            tags = len(CLAIM_TAG.findall(text))
            if tags < 10:
                warns.append(f"{rel}: only {tags} claim tags")
            if rel not in listed:
                where = "private/case-studies/INDEX.md" if folder == "case-studies" else "CATALOG.md"
                errors.append(f"{rel}: not listed in {where}")
            elif status.get(rel) == "todo":
                warns.append(f"{rel}: on disk but INDEX status is 'todo'")

        for n, line in enumerate(text.splitlines(), 1):
            for pattern, why in BANNED:
                if pattern.search(line) and not ALLOW_WORDS.search(line) and rel != "CONTRIBUTING.md":
                    errors.append(f"{rel}:{n}: {why}")
            for target in LINK.findall(line):
                if target.startswith("http") or rel == "CONTRIBUTING.md":  # its links are examples
                    continue
                resolved = (path.parent / target).resolve()
                if folder != "case-studies" and (PRIVATE in resolved.parents or "private" in Path(target).parts):
                    errors.append(f"{rel}:{n}: link into private/ ({target}); name the path in code "
                                  f"format or use '(case study: <slug>)' so a clone without private/ has no dead link")
                    continue
                if resolved.exists():
                    continue
                if CASE_STUDIES in resolved.parents:
                    key = "case-studies/" + resolved.name
                else:
                    key = os.path.relpath(resolved, VAULT).replace(os.sep, "/")
                if key not in listed:
                    errors.append(f"{rel}:{n}: link to {target} (not on disk, not planned in CATALOG)")
            if rel in META:
                continue
            for slug in CASE_MARKER.findall(line):
                if not have_cases:
                    unchecked_markers += 1
                elif not (CASE_STUDIES / f"{slug}.md").exists():
                    errors.append(f"{rel}:{n}: (case study: {slug}) but private/case-studies/{slug}.md is missing")

    for entry in sorted(listed):
        if not status.get(entry, "").startswith("done"):
            continue
        on_disk = CASE_STUDIES / entry.split("/", 1)[1] if entry.startswith("case-studies/") else VAULT / entry
        if not on_disk.exists():
            errors.append(f"CATALOG.md: {entry} marked done but missing")
    # The short index must name every catalogued file, or a reader loading only INDEX.md misses it.
    short = (VAULT / "INDEX.md").read_text(encoding="utf-8")
    for entry in sorted(catalog_only):
        stem = Path(entry).stem
        if not re.search(r"(?<![\w-])" + re.escape(stem) + r"(?![\w-])", short):
            errors.append(f"INDEX.md: {entry} is in CATALOG.md but not named in the short index")
    if not have_cases:
        warns.append(f"private/case-studies/ is missing: {unchecked_markers} '(case study: <slug>)' "
                     f"markers were not checked (expected on a fresh clone)")
    return errors, warns


def main() -> int:
    errors, warns = lint()
    if "--quiet" not in sys.argv:
        for w in warns:
            print(f"WARN  {w}")
    for e in errors:
        print(f"ERROR {e}")
    print(f"{len(errors)} errors, {len(warns)} warnings")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
