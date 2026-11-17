---
title: Vault writing rules
type: meta
read-when: Before writing, editing, or reviewing any vault file.
last-researched: 2026-10-22
---

# Vault writing rules

The vault is read by AI build agents before they work, and by a reviewer agent that checks
their output. Every line should change what an agent builds or decides. Dense and correct
beats long.

## File rules

- Frontmatter on every file, exactly these keys:
  ```yaml
  ---
  title: Tycoon
  type: genre            # genre | fundamental | pattern | case-study | trends (meta: INDEX/CONTRIBUTING only)
  read-when: One line telling an agent when to load this file.
  last-researched: 2026-10-22
  ---
  ```
- 100–400 lines. Split anything bigger into two files and list both in INDEX.md.
- Standard markdown with relative links: `[Tycoon](../genres/tycoon.md)`. No `[[wikilinks]]`.
  Linking to a planned file that INDEX.md lists is fine.
- File names: lowercase-kebab-case, `.md`.
- Every file ends with `## Sources`: a numbered list of URLs, each with a few words on what
  it supports.
- Add every new file to INDEX.md with its read-when line and status.

## Claim tags

Tag every factual claim that isn't common knowledge, at the end of the sentence or bullet:

| Tag | Use for |
|---|---|
| `(official)` | Roblox Creator Docs, Roblox blog/newsroom, Roblox DevForum staff announcements, the engine API reference |
| `(community)` | DevForum posts by experienced developers, dev talks, postmortems, open-source code |
| `(press)` | News coverage: Polygon, Dexerto, PocketGamer, The Verge, Bloomberg, etc. |
| `(data)` | This repo's own tracker output (`private/trends/`). When the report is missing, run the tracker first (tools/trends/README.md); never write a `(data)` number you did not read there |
| `(inferred)` | Our own analysis or reasoning |
| `(unverified)` | Add to any of the above when the source couldn't be confirmed |

- **Date every number:** `~25M concurrent players (press, 2025-10)`. Player counts, prices,
  percentages and rankings go stale fast.
- A number with no source gets `(inferred)` and an explanation, or gets deleted.
- Seed numbers from the task prompt must be checked against a source before they're cited.

## Writing style

- Concrete over vague: numbers, property values, named APIs, real examples.
  - Bad: "Make the lighting look nice."
  - Good: "`Lighting.LightingStyle = Realistic`, `Brightness = 2`, add an `Atmosphere` with
    `Density = 0.3`."
- Rules as checklists and **Do / Don't** lists that an agent can follow and a reviewer can check.
- API names exactly as in the engine reference (`MarketplaceService.ProcessReceipt`,
  `DataStoreService:GetDataStore`, `TweenService:Create`). If you aren't sure an API exists,
  look it up or don't name it.
- Luau snippets are allowed in patterns and craft fundamentals: short, `--!strict`,
  server-authoritative, real APIs only. They're outlines, not drop-in code.
- Write in your own words. Don't copy paid courses, paid vaults, wikis or articles. Quote at
  most one short phrase per source, in quotation marks.
- No filler, no hype, no "In today's fast-paced world". No intro paragraphs that restate the title.
- Describe other games' designs; never copy their assets, names, or content.

## Sources

- Prefer primary sources: create.roblox.com/docs, the Roblox blog and newsroom, DevForum
  posts by staff or experienced developers, the game's own page and update logs.
- Press for numbers and context. Fan wikis are fine for a game's own facts (update dates,
  item lists), not for platform claims.
- Be skeptical of SEO pages ("Top 10 Roblox games", AI-written blogs, code-list sites).
  Don't cite them for anything that matters; if one is the only source, tag `(unverified)`.

## Templates

### Genre (`genres/`)

```markdown
# <Genre>
## In one line
## Core loop
moment-to-moment → session → long-term (meta) loop
## Main verbs
## Why players come back
## What separates top games from clones
## Session shape
typical session length, first 60 seconds, first 10 minutes, day 7
## Social hooks
## Monetization that works here
## Common failure modes
## Saturation & opportunity
cite private/trends/latest.md (data) where possible
## Scope for a solo dev
MVP, build order, what to cut
## Top examples
one line per game; where a private case study exists, add `(case study: <slug>)`, never a link
## Build checklist for agents
### Do
### Don't
## Sources
```

### Fundamental (`fundamentals/`)

```markdown
# <Topic>
## In one line
## <Topic sections: facts, numbers, rules, with tags>
## Checklist for agents
### Do
### Don't
## Related
## Sources
```

### Pattern (`patterns/`)

```markdown
# <Pattern>
## What it is
## Why it works
the player psychology, in plain terms
## Genres that use it
## Design rules
numbers and tuning ranges that are known to work
## Implementation outline (server-authoritative)
data model, services, remotes, named APIs, a short Luau sketch if useful
## Common bugs and exploits
## Checklist for agents
## Sources
```

### Case study (`private/case-studies/`, not in the public tree)

```markdown
# <Game>
## Snapshot
creator, release date, genre, peak and current players (dated), Roblox genre fields
## Core loop
## What makes it stick
## Monetization
## Notable updates and events
## What a small dev can learn
## What NOT to copy
designs that are risky, exploitative, or that only work at their scale; plus never copy assets/names
## Sources
```
