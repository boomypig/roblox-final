# Adopting an existing game

How a game made before the toolkit joins the path in `docs/workflow.md` without being rebuilt.
The script is `scripts/adopt.py`; the layout map it writes is described in
`roblox-code/references/layout.md`.

## The rule that comes first

**Never reformat code during adoption.** No `stylua` over the game, no `check.py --fix`, no
renames, no moving modules into `Core/` or `Config/`, no switching to Knit or `Net.luau`.
Adoption writes down where things are; it does not change them. Why: a formatting pass turns
the first diff into thousands of lines nobody can review, hides any behavior change inside it,
and rewrites code the user wrote and knows. If the format gate fails on adopted code, that is
a debt in `HANDOFF.md` for the user to schedule, not something to fix in passing.

## Steps

1. **Read-only proposal.** `python3 ~/roblox-final/.claude/skills/create-roblox-game/scripts/adopt.py --dir <game>`.
   It prints the proposed `design/layout.json`, the evidence for each line (which file showed
   what), and the contract skeleton with where each value came from. Read every
   `(inferred)` note against the code it names.
2. **Write.** The same command with `--write`. It creates `design/layout.json`,
   `docs/tech/layout.md`, the contract (`design/game.json` and the stage stubs, filled from
   `docs/pitch.md`, the services' first comments and the config module), `BUILD.md`, an
   adoption `HANDOFF.md`, and the starter files the game lacks (CLAUDE.md, docs, the session
   hook in `.claude/settings.json`, the map state template). An existing file is never
   overwritten (`--force` replaces only the two layout files); nothing under `src/` or `tests/`
   is written.
3. **The ledger.** Start it once, then end section 1's stages as adopted, because their work
   was done before the toolkit:
   ```bash
   L=~/roblox-final/.claude/skills/roblox-build-orchestrator/scripts/run_log.py
   python3 $L init --dir <game>/build-runs --run <slug>
   python3 $L end --dir <game>/build-runs --run <slug> --stage market-research --status adopted
   python3 $L end --dir <game>/build-runs --run <slug> --stage design-spec --status adopted
   ```
4. **Fill the contract.** Section 1's design work for a game that exists is reading it, not
   inventing it: replace every TODO in `design/game.json` from the game's docs and code, and
   write `plan` and `asset_plan` (`references/game-plan.md`). `validate.py` must be green;
   adoption does not relax it.
5. **Close section 1.** `section.py handoff 1 --dir <game> --ledger <game>/build-runs/<slug>`,
   fill it, `section.py close 1 --dir <game>`. The close accepts the two stages ended
   `adopted` (gate change 2); every later section needs its stages bracketed as usual.
6. **The gates.** Run `roblox-code/scripts/check.py --dir <game>`. It reads the layout map:
   no `Packages/` is required without `wally.toml`, lune is skipped while `tests` is `null`,
   and selene and stylua check the layout's `lint` and `format` paths. A red gate on adopted
   code goes in `HANDOFF.md` "Debts"; see the first rule.

## What the layout map changes downstream

- `check.py` reads `tests`, `packages`, `toolchain`, `lint` and `format`.
- `/build` puts pure rules in the layout's `pure` paths, tunables in its `config`, and new
  remotes where its `remotes` says (in the creating service, for `per-service`).
- The reviewer checks each roblox-code rule against the layout's paths
  (`roblox-code/references/layout.md`, "How each rule maps").
- A map with `"source": "studio"` has no prover report; the map-builder dresses it from its
  brief and keeps `docs/design/maps/<name>.state.md`. Section 3's `map` stage still needs its
  artifact for `--stage-gate`, or a declared `external_blocker`.

## Traps

- **An "(inferred)" pure module that is not pure.** The check is a text search for Instance,
  service, `script` and yield use. A module that reaches the engine through a required helper
  passes it. Read each one before writing a spec that runs it under Lune.
- **Two folders of remotes.** `adopt.py` names the first folder name it finds in the services.
  If services use different folders, `remotes.where` is wrong for some of them: list them in
  `notes` and fix the layout file by hand.
- **No tool manifest.** Without `rokit.toml` or `aftman.toml`, a rokit shim refuses every tool
  (check.py reports it). Pin the tools the game already uses; don't upgrade them during
  adoption.

## Sources

- The fixture `tests/fixtures/adopted-game/`, built to the shape of a real game made before
  the toolkit, and `tests/test_adopt.py`.
- `tools/smoke.py`, which runs adoption end to end: propose, write, ledger, contract, close 1.
