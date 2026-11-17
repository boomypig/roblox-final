# Changelog

Notable changes to the toolkit. Dates are YYYY-MM-DD. Changes to what a gate accepts are
marked **Gate change**.

## Unreleased

### Added
- `docs/workflow.md` is now the one path from idea to published game: every step with what runs
  it, what it reads and writes, and the gate that ends it, plus the operating policy every
  skill and agent follows.
- Gates for the design-side steps: `pitch/scripts/check_pitch.py`,
  `art-brief/scripts/check_brief.py`, `build/scripts/check_spec.py`.
- `docs/structure.md` (the five parts of every skill and agent, with a coverage table),
  `docs/redundancy-map.md`, `docs/vault-readers.md`, `docs/migration.md`.
- `tools/migrate_game.py <game dir> [--write]`: rewrites a game repo's references to moved
  toolkit paths.
- `vault/CATALOG.md`: the full read-when line and status of every research file.

### Changed
- `/art-brief`, `/build` and the spec-writer no longer stop to ask. Open points are decided and
  written as `**Assumption:**` lines or judgment calls; the user approves once.
- **Gate change.** `/build` refuses a spec that is not approved or has no checkable acceptance
  criteria (`check_spec.py --require-approved`).
- Seven build references moved from `vault/fundamentals/` to the owning skill's `references/`
  (quality bar, security, UI, game feel, visual quality, performance, Studio MCP). Paths are in
  `docs/migration.md`. `vault/INDEX.md` stays at the same path and is now the short index.
- `tools/vault_lint.py` reads its file list from `vault/CATALOG.md` and lints the moved
  references with the same rules.
- The reviewer reports the output of `validate.py` and `verify_wired.py` instead of repeating
  their checks.

### Fixed
- `roblox-code/scripts/check.py` required `Packages/` in every project; it is required only
  when `wally.toml` exists.
- `check.py` passed a gate when a rokit shim ran for a tool the game had not pinned (the shim
  prints an error and exits 0). That is now a FAIL naming the tool and the line to add to
  `rokit.toml` (or `aftman.toml`).
- **Gate change.** `section.py resume` no longer writes an implied approval into
  `design/sections.json`. It prints `section.py approve N --implied`, which writes the same
  record.
- `validate.py` and `section.py close` rejected any value or HANDOFF line containing "TODO", so
  a game titled "TODO List Tycoon" could not pass. Only values that start with a scaffold
  marker (`TODO`, `TODO:`, `TODO<Name>`) count, and the report shows the first 40 characters.

### Removed
- `starter/docs/workflow.md`: a game points at the toolkit's workflow doc instead of carrying
  a copy. `starter/docs/tech/conventions.md` no longer restates the `roblox-code` rules.

## 0.1.0 - 2026-11-17

First public version.

### Added
- `README.md` for a new reader, `CONTRIBUTING.md`, `NOTICE.md`, this changelog and
  `docs/decisions.md`.
- `goals.template.md`: the template for your own goals file.
- `tests/`: checks that the tracked tree holds no personal names, emails or machine paths, no
  path to a file that moved, and that everything still works when `private/` is absent.
- A GitHub Actions workflow that runs the tests and the vault lint.

### Changed
- Personal material lives in `private/`, which git ignores: the goals file, pitches, generated
  trend reports, the tracker database, cache and log, and the case studies of named games.
  Every skill, agent and script that reads one of them says what it does when the file is
  missing and carries on.
- The trends tracker writes its report to `private/trends/` and keeps its database in
  `private/trends/data/`. `report --out DIR` replaces `report --vault DIR`, which still works.
  `ROBLOX_FINAL_PRIVATE` moves the folder. The client's User-Agent names the tool only; set
  `TRENDS_CONTACT` to add contact details.
- The vault cites case studies as `(case study: <slug>)` instead of linking to them, so a clone
  has no dead links. `tools/vault_lint.py` checks the markers when the case studies are present
  and passes without them.
- `tools/vault_apicheck.py` caches the API dump in `tools/.cache/`.
