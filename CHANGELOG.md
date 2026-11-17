# Changelog

Notable changes to the toolkit. Dates are YYYY-MM-DD. Changes to what a gate accepts are
marked **Gate change**.

## Unreleased

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
