"""Theme tags from themes.yaml (keyword + manual) and Roblox's own genre fields (roblox-genre)."""

from __future__ import annotations

import re
import sqlite3
import unicodedata
from dataclasses import dataclass
from pathlib import Path

import yaml

from . import config, db

# [🎃 HALLOWEEN], (UPDATE 5), {EVENT}, 【NEW】 — update/event labels in game names, not themes.
BRACKET_RE = re.compile(r"[\[\(\{【「]([^\]\)\}】」]{1,40})[\]\)\}】」]")


@dataclass(frozen=True)
class Theme:
    name: str
    patterns: tuple[re.Pattern[str], ...]
    excludes: tuple[re.Pattern[str], ...] = ()
    use_description: bool = False
    name_regexes: tuple[re.Pattern[str], ...] = ()
    include_labels: bool = False  # also match bracketed text, e.g. "Sell Fries! [Anomaly]"


class ThemeFileError(ValueError):
    pass


def normalize(text: str) -> str:
    return unicodedata.normalize("NFKC", text).casefold()


def keyword_pattern(keyword: str) -> re.Pattern[str]:
    """'egg' matches egg/eggs; 'fish*' matches fish, fishing, fisherman; spaces match any whitespace."""
    word = normalize(keyword.strip())
    prefix = word.endswith("*")
    body = r"\s+".join(re.escape(part) for part in word.rstrip("*").split())
    tail = r"[a-z0-9]*" if prefix else r"(?:s|es)?"
    return re.compile(rf"(?<![a-z0-9]){body}{tail}(?![a-z0-9])")


def split_name(name: str) -> tuple[str, list[str]]:
    """('Steal An Egg [🎃 EVENT]') -> ('Steal An Egg', ['🎃 EVENT'])."""
    labels = [m.strip() for m in BRACKET_RE.findall(name) if m.strip()]
    clean = re.sub(r"\s{2,}", " ", BRACKET_RE.sub(" ", name)).strip()
    return clean or name.strip(), labels


def load_themes(path: Path = config.THEMES_FILE) -> tuple[list[Theme], dict[int, list[str]]]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    except (OSError, yaml.YAMLError) as exc:
        raise ThemeFileError(f"{path}: {exc}") from exc
    raw_themes = data.get("themes") or {}
    if not isinstance(raw_themes, dict):
        raise ThemeFileError(f"{path}: 'themes' must be a mapping of theme name -> settings")
    themes = []
    for name, spec in raw_themes.items():
        if isinstance(spec, list):  # shorthand: theme: [kw, kw]
            spec = {"keywords": spec}
        if not isinstance(spec, dict) or not (spec.get("keywords") or spec.get("regex")):
            raise ThemeFileError(f"{path}: theme '{name}' needs a 'keywords' or 'regex' list")
        try:
            regexes = tuple(re.compile(str(r)) for r in spec.get("regex") or [])
        except re.error as exc:
            raise ThemeFileError(f"{path}: theme '{name}' has a bad regex: {exc}") from exc
        themes.append(
            Theme(
                name=str(name),
                patterns=tuple(keyword_pattern(str(k)) for k in spec.get("keywords") or []),
                excludes=tuple(keyword_pattern(str(k)) for k in spec.get("exclude") or []),
                use_description=bool(spec.get("description", False)),
                name_regexes=regexes,
                include_labels=bool(spec.get("include_labels", False)),
            )
        )
    manual: dict[int, list[str]] = {}
    for key, tags in (data.get("manual") or {}).items():
        try:
            manual[int(key)] = [str(t) for t in (tags or [])]
        except (TypeError, ValueError) as exc:
            raise ThemeFileError(f"{path}: manual key '{key}' must be a universeId") from exc
    return themes, manual


def themes_for(name: str, description: str, themes: list[Theme]) -> list[str]:
    clean_name, _ = split_name(name)
    name_text = normalize(clean_name)
    desc_text = normalize((description or "")[: config.DESCRIPTION_CHARS_FOR_THEMES])
    found = []
    raw_name_text = normalize(name)
    for theme in themes:
        texts = [name_text, desc_text] if theme.use_description else [name_text]
        if theme.include_labels:
            texts.append(raw_name_text)
        hit = any(p.search(t) for p in theme.patterns for t in texts) or any(r.search(name_text) for r in theme.name_regexes)
        if hit and not any(x.search(t) for x in theme.excludes for t in texts):
            found.append(theme.name)
    return found


def retag_all(conn: sqlite3.Connection, themes: list[Theme], manual: dict[int, list[str]]) -> int:
    """Recompute keyword, manual and roblox-genre tags for every known game. Returns keyword tag count."""
    rows = conn.execute("SELECT universe_id, name, description, genre_l1, genre_l2 FROM games").fetchall()
    keyword_rows: list[tuple[int, str]] = []
    genre_rows: list[tuple[int, str]] = []
    for r in rows:
        keyword_rows += [(r["universe_id"], t) for t in themes_for(r["name"], r["description"] or "", themes)]
        genre_rows += [(r["universe_id"], g.casefold()) for g in (r["genre_l1"], r["genre_l2"]) if g]
    db.replace_tags(conn, "keyword", keyword_rows)
    db.replace_tags(conn, "roblox-genre", genre_rows)
    db.replace_tags(conn, "manual", [(uid, t) for uid, tags in manual.items() for t in tags])
    return len(keyword_rows)
