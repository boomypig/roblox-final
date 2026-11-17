# Contributing

This is a toolkit of Claude Code skills, agents, scripts and design research for building
Roblox games. Changes are welcome when they come with proof.

## Before you open a pull request

```bash
python3 -m unittest discover -s tests -v                    # toolkit tests
python3 tools/vault_lint.py                                 # design library rules
cd tools/trends && python3 -m unittest discover -s tests    # tracker tests (needs requests, PyYAML)
```

All three run in GitHub Actions on every push and pull request.

## Rules for a change

1. **Every change needs proof.** A test that fails before the change and passes after, or, for
   a documentation change that moves or condenses rules, a coverage table showing nothing was
   lost. Say which in the pull request.
2. **One owner per rule.** A rule lives in one file; other files point at it. If you find the
   same rule in two places, keep it where the step that enforces it reads it and replace the
   other with a pointer.
3. **A script says why it exists.** Every script's docstring names the defect it was written
   for. A script that a second game would need belongs in the owning skill's `scripts/` and
   takes paths as arguments.
4. **Lessons go where they will be read.** A lesson about game design goes in `vault/`
   (follow [vault/CONTRIBUTING.md](vault/CONTRIBUTING.md): frontmatter, claim tags, dated
   numbers, a Sources list). A lesson about a tool goes in that skill's traps, written from the
   failure that taught it.
5. **Quality does not drop to save cost.** Do not move a skill or agent to a cheaper model, and
   do not shorten a skill, its description or its references to save space. Cut cost by loading
   things only when a step needs them.
6. **Gates do not loosen quietly.** A change to what a gate accepts is named in the pull
   request and in `CHANGELOG.md`.

## What never goes in

- Anything from `private/`, any `LOCAL.md`, your name, email or home folder path. The tests
  search for email addresses and machine paths; list your own name or handle in
  `private/identity.txt` and they search for those too.
- API keys or tokens. Skills read keys from environment variables (`ROBLOX_API_KEY`,
  `HF_TOKEN`).
- Another game's assets, names or content. Research describes designs; it never copies them.
- Harvested VFX recipes or other Creator Store content. The VFX skill ships no effects.

## Commits

One logical change per commit, with a `type(scope): summary` subject. Types: `feat`, `fix`,
`docs`, `test`, `refactor`, `chore`, `ci`. The scope is the skill, agent or tool touched, for
example `fix(roblox-code): require Packages/ only when wally.toml exists`.

## Licence

This repository has no licence file yet. Until one is added, open an issue before sending a
change you want merged. Notices for fonts, tools and models are in [NOTICE.md](NOTICE.md).
