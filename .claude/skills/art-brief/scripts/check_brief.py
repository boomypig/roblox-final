#!/usr/bin/env python3
"""Gate an /art-brief file: can the map-builder or /build follow it without guessing?

    check_brief.py <brief file>                 # exit 1 on any FAIL
    check_brief.py <brief file> --require-approved

WHY THIS EXISTS. The first game built with this toolkit had no art direction before building:
the map began as grey code-built geometry and got cosmetics late, and the result worked but
felt flat. A brief fixes that only if it carries real values. The failure this gate catches is
the brief that looks finished and is not: a palette row with no RGB, a check view with no
camera position, a template placeholder left in, a reference image that is not on disk (so the
builder, which cannot see the chat, never sees it). Each of those sends the builder back to
guessing, which is the thing the brief exists to prevent.

Checks, by brief kind (art direction, map, UI):
  all   Status line; no template placeholder left; every linked reference image exists;
        a filled "Not this" list; an Assumptions section
  art   lighting preset is one of the four; LightingStyle named; every palette role has an RGB
        value in range; at most 5 hues besides the ground neutrals; materials filled
  map   overall size in studs; at least one zone; gameplay geometry rows carry numbers;
        at least two check views, each with camera coordinates; budgets filled
  ui    at least one screen with its one job; HUD layout rows filled
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

PRESETS = ["bright cartoon day", "golden hour", "night / horror", "night/horror", "stylized neon arena"]
STATUS = re.compile(r"^Status:\s*(draft|approved|built)\b", re.M)
PLACEHOLDER = re.compile(r"<[A-Za-z][^<>\n]{2,}>")
IMAGE = re.compile(r"\]\(([^)\s]+\.(?:png|jpe?g))\)", re.I)
RGB = re.compile(r"(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})")
VEC = re.compile(r"-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?\s*,\s*-?\d+(?:\.\d+)?")
NUM = re.compile(r"\d")


def section(text: str, title: str) -> str | None:
    m = re.search(r"^##+ " + re.escape(title) + r"[^\n]*\n(.*?)(?=^## |\Z)", text, re.M | re.S)
    return m.group(1) if m else None


def table(body: str | None) -> list[list[str]]:
    rows = []
    for ln in (body or "").splitlines():
        if ln.startswith("|") and not re.match(r"^\|[\s:|-]+\|$", ln):
            rows.append([c.strip() for c in ln.strip().strip("|").split("|")])
    return rows[1:]  # drop the header


def bullets(body: str | None) -> list[str]:
    return [b.strip() for b in re.findall(r"^\s*-\s*(.*)$", body or "", re.M) if b.strip()]


def kind_of(text: str) -> str:
    first = text.lstrip().splitlines()[0] if text.strip() else ""
    if first.startswith("# Map"):
        return "map"
    if first.startswith("# UI"):
        return "ui"
    return "art"


def check(text: str, path: Path, require_approved: bool) -> list[str]:
    fails: list[str] = []
    kind = kind_of(text)

    m = STATUS.search(text)
    if not m:
        fails.append("no `Status: draft | approved | built` line")
    elif require_approved and m.group(1) == "draft":
        fails.append("Status is draft; the user approves a brief by setting `Status: approved`")

    for i, ln in enumerate(text.splitlines(), 1):
        ln_wo_comment = re.sub(r"<!--.*?-->", "", ln)
        ph = PLACEHOLDER.search(ln_wo_comment)
        if ph:
            fails.append(f"line {i}: template placeholder left in: {ph.group(0)[:40]}")
        if re.search(r'>\s*"\.\.\."', ln):
            fails.append(f"line {i}: the user's words are still the template's \"...\"")

    for target in IMAGE.findall(text):
        if target.startswith("http"):
            continue
        if not (path.parent / target).resolve().exists():
            fails.append(f"reference image not on disk: {target} (the builder cannot see images pasted in chat)")

    if not bullets(section(text, "Not this")):
        fails.append("`Not this` is empty; it is the best guard against generic output")
    if section(text, "Assumptions") is None:
        fails.append("no `Assumptions` section")

    if kind == "art":
        light = section(text, "Lighting") or ""
        if not any(p in light.lower() for p in PRESETS):
            fails.append("Lighting: no preset named (Bright cartoon day, Golden hour, Night / horror, Stylized neon arena)")
        if not re.search(r"LightingStyle`?\s*=\s*`?(Soft|Realistic)", light):
            fails.append("Lighting: `LightingStyle` = Soft or Realistic is not stated (it is set by hand)")
        rows = table(section(text, "Palette"))
        if len(rows) < 5:
            fails.append(f"Palette: {len(rows)} roles, expected ground light/mid/dark, supports, accent and danger")
        hues = 0
        for r in rows:
            role = r[0] if r else "?"
            rgb = RGB.search(" ".join(r[1:]))
            if not rgb:
                fails.append(f"Palette: `{role}` has no RGB value")
                continue
            if any(int(v) > 255 for v in rgb.groups()):
                fails.append(f"Palette: `{role}` RGB {rgb.group(0)} is out of range")
            if not role.lower().startswith("ground"):
                hues += 1
        if hues > 5:
            fails.append(f"Palette: {hues} hues besides the ground neutrals; the limit is 5")
        for r in table(section(text, "Materials")):
            if len(r) < 2 or not r[1]:
                fails.append(f"Materials: `{r[0] if r else '?'}` has no Enum.Material")

    if kind == "map":
        layout = section(text, "Layout") or ""
        if not re.search(r"\d+\s*[×x]\s*\d+", layout):
            fails.append("Layout: overall size in studs (x × z) is missing")
        zones = [r for r in table(section(text, "Zones")) if len(r) > 1 and r[1]]
        if not zones:
            fails.append("Zones: no zone is described")
        geo = table(section(text, "Gameplay geometry"))
        if not [r for r in geo if r and r[0]]:
            fails.append("Gameplay geometry: no element listed; sizes come from the genre file, not by eye")
        for r in geo:
            if r and r[0] and (len(r) < 2 or not NUM.search(r[1])):
                fails.append(f"Gameplay geometry: `{r[0]}` has no size or spacing in studs")
        views = [r for r in table(section(text, "Check views")) if r and r[0]]
        if len(views) < 2:
            fails.append(f"Check views: {len(views)} listed, expected at least spawn and top-down")
        for r in views:
            if len(r) < 2 or len(VEC.findall(r[1])) < 2:
                fails.append(f"Check views: `{r[0]}` needs a camera position and a look-at position as x, y, z")
        if not NUM.search(section(text, "Budgets") or ""):
            fails.append("Budgets: no numbers; take them from roblox-map references/performance-and-devices.md")

    if kind == "ui":
        screens = [r for r in table(section(text, "Screens")) if r and r[0]]
        if not [r for r in screens if len(r) > 1 and r[1]]:
            fails.append("Screens: no screen has its one job written")
        hud = [r for r in table(section(text, "HUD layout")) if r and r[0]]
        if not hud:
            fails.append("HUD layout: no element placed")
        for r in hud:
            if len(r) < 3 or not r[1] or not r[2]:
                fails.append(f"HUD layout: `{r[0]}` needs a position and a size")
    return fails


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__)
        return 2
    path = Path(args[0])
    if not path.is_file():
        print(f"FAIL  {path}: no such file")
        return 1
    fails = check(path.read_text(encoding="utf-8"), path, "--require-approved" in argv)
    for f in fails[:30]:
        print(f"FAIL  {f}")
    if len(fails) > 30:
        print(f"... and {len(fails) - 30} more")
    print(f"check_brief: {'PASS' if not fails else 'FAIL'} ({len(fails)} problems) {path.name}")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
