"""Check Roblox API names in vault files against the public API dump. Stdlib only.

Checks every file the vault lint covers: vault/, the build references vault/CATALOG.md lists
in skills' references/ folders, and, when it exists, private/case-studies/.
Finds `Class.Member`, `Class:Method`, `Enum.Type.Item` (plus common variables like
`player:`/`workspace.`) and reports members that don't exist or are deprecated.

Usage: python3 tools/vault_apicheck.py [--refresh] [--deprecated]
The dump is cached at tools/.cache/api-dump.json (gitignored).
Source: MaximumADHD/Roblox-Client-Tracker (a public mirror of Roblox's own API dump).
"""

from __future__ import annotations

import json
import os
import re
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VAULT = ROOT / "vault"
CASE_STUDIES = Path(os.environ.get("ROBLOX_FINAL_PRIVATE") or ROOT / "private").expanduser() / "case-studies"
CACHE = ROOT / "tools" / ".cache" / "api-dump.json"
DUMP_URL = "https://raw.githubusercontent.com/MaximumADHD/Roblox-Client-Tracker/roblox/API-Dump.json"

# Lowercase names that are almost always instances of a known class in vault code and prose.
ALIASES = {
    "game": "DataModel", "workspace": "Workspace", "player": "Player", "humanoid": "Humanoid",
    "camera": "Camera", "char": "Model", "character": "Model", "plr": "Player", "hum": "Humanoid",
}
# Names that look like classes but are datatypes, libraries or Roblox Lua globals.
SKIP = {"Vector3", "Vector2", "CFrame", "Color3", "UDim", "UDim2", "TweenInfo", "Random", "DateTime",
        "NumberRange", "NumberSequence", "ColorSequence", "Ray", "RaycastParams", "OverlapParams",
        "Region3", "Rect", "Font", "Content", "PhysicalProperties", "BrickColor", "Instance",
        "RBXScriptSignal", "RBXScriptConnection", "SharedTable", "Axes", "Faces", "Path2DControlPoint",
        "ProfileStore", "ProfileService", "DataStore2", "Trove", "Maid", "FastCast", "OpenCloud",
        "PlayerData", "Catalog", "Inventory", "Config", "CFG", "State", "Palette", "Stats"}
TOKEN = re.compile(r"(?<![\w./-])([A-Za-z_][A-Za-z0-9_]*)([.:])([A-Za-z_][A-Za-z0-9_]*)(?:\.([A-Za-z_][A-Za-z0-9_]*))?")


def load_dump(refresh: bool) -> dict:
    if refresh or not CACHE.exists():
        CACHE.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(DUMP_URL, timeout=60) as resp:
            CACHE.write_bytes(resp.read())
    return json.loads(CACHE.read_text(encoding="utf-8"))


def index(dump: dict) -> tuple[dict, dict, dict]:
    classes = {c["Name"]: c for c in dump["Classes"]}
    enums = {e["Name"]: {i["Name"]: i for i in e["Items"]} for e in dump["Enums"]}

    members: dict[str, dict[str, dict]] = {}
    for name in classes:
        found: dict[str, dict] = {}
        cur = name
        while cur and cur in classes:
            for m in classes[cur]["Members"]:
                found.setdefault(m["Name"], m)
            cur = classes[cur].get("Superclass")
        members[name] = found
    return classes, enums, members


def deprecated(entry: dict) -> bool:
    return "Deprecated" in (entry.get("Tags") or [])


def check(show_deprecated: bool, refresh: bool) -> int:
    classes, enums, members = index(load_dump(refresh))
    unknown, old = [], []
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from vault_lint import sources  # one definition of "the files the vault rules cover"
    for rel, path in sources():
        for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for head, sep, member, sub in TOKEN.findall(line):
                if head == "Enum":
                    if member in enums and sub:
                        if sub not in enums[member]:
                            unknown.append(f"{rel}:{n}: Enum.{member}.{sub} not in enum")
                        elif deprecated(enums[member][sub]):
                            old.append(f"{rel}:{n}: Enum.{member}.{sub} is deprecated")
                    elif member not in enums and member[:1].isupper():
                        unknown.append(f"{rel}:{n}: Enum.{member} not an enum")
                    continue
                cls = ALIASES.get(head, head)
                if cls in SKIP or cls not in classes:
                    continue
                entry = members[cls].get(member)
                if entry is None:
                    # Child instances (workspace.Map, ReplicatedStorage.Remotes) are fine with ".".
                    if sep == ":" or (member[:1].islower() and cls not in ALIASES.values()):
                        unknown.append(f"{rel}:{n}: {head}{sep}{member} not a member of {cls}")
                    continue
                if sep == ":" and entry["MemberType"] not in ("Function", "Callback"):
                    unknown.append(f"{rel}:{n}: {head}:{member} is a {entry['MemberType']}, not a method")
                if deprecated(entry):
                    old.append(f"{rel}:{n}: {head}{sep}{member} is deprecated")
    for u in unknown:
        print(f"UNKNOWN    {u}")
    if show_deprecated:
        for d in old:
            print(f"DEPRECATED {d}")
    print(f"{len(unknown)} unknown, {len(old)} deprecated mentions (deprecated mentions are fine when the text says so)")
    return 1 if unknown else 0


if __name__ == "__main__":
    sys.exit(check("--deprecated" in sys.argv, "--refresh" in sys.argv))
