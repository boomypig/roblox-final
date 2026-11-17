# Harbor Rush

A test fixture with the shape of a real game made before the toolkit, used by
`tests/test_adopt.py` and `tools/smoke.py` to prove `adopt.py`. It is not a game to play.

Players race around a harbor collecting coins before the round timer runs out.

- Server modules in `src/server/Services`, booted by `Main.server.luau` (`Init`, then `Start`).
- Each service creates its own remotes under `ReplicatedStorage.Remotes`.
- One `src/shared/Config.luau`; pure rules loose in `src/shared`.
- No Wally packages, tools pinned in `rokit.toml`, no tests yet.
- The harbor map was built by hand in Studio from `docs/design/maps/harbor.md`.
