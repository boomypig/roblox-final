# Toolkit decisions

Why the toolkit is built the way it is. Newest section last. Each entry: the decision, the
reason, and what was rejected. Game decisions go in the game's own `docs/decisions.md`.

## Private material and the public tree (2026-11-17)

**D1. Personal material lives in `private/`, a gitignored folder that is its own local git repo.**
Goals, pitches, generated trend reports, the tracker database, the case studies of named games,
planning history and maintenance notes are one person's working notes. Keeping them in one
ignored folder means a single `.gitignore` line protects all of them and one test can prove
nothing leaked. Rejected: a separate sibling folder (every reader would need a second path
setting) and per-file ignore rules (one forgotten rule publishes a note).

**D2. `ROBLOX_FINAL_PRIVATE` moves the folder.** Scripts read the variable and fall back to
`<toolkit>/private`. It lets the tests point every reader at an empty folder to prove the
missing-file behaviour, and lets a user keep notes on another drive.

**D3. Every reader of a private file says what to do when it is missing, and never stops.**
The rule is stated where the reader looks: in the skill step, in `vault/INDEX.md` for vault
files, in `CLAUDE.md` for everything else. A goals file is the one thing only the user can
supply, so `/pitch` asks once; everything else continues with a stated assumption.
`tests/test_private_optional.py` is the coverage check.

**D4. What "no private path in a tracked file" means.** A tracked file may name a private
*slot* (`private/goals.md`, `private/trends/latest.md`), because readers need the path. It may
not contain a machine path (a home folder, a Windows user folder), a name or email, or a path
to one *specific* private file (a dated pitch, a note). `tests/test_public_tree.py` enforces
all three. The repository's own address is the single place an owner handle may appear.

**D5. Names to search for are listed in `private/identity.txt`, not in the test.** Writing the
names into a tracked test would publish them; hashing them would not hide a first name from a
dictionary. Generic patterns (any email address, any home folder) run everywhere, including CI;
the literal terms run wherever the private file exists.

**D6. Case studies are cited as `(case study: <slug>)`, not linked.** A link into `private/`
is dead for every visitor. The marker reads as plain text, the lint resolves it when the notes
are present, and the genre file's "Top examples" line still carries the summary. Rejected:
keeping the links pointed at `private/` (72 dead links on GitHub).

**D7. The tracker's data moved with its reports.** "The code is public; the data and reports
are private." The database, cache and scheduled-run log are in `private/trends/data/`, and the
tracker creates the folder on first run, so a fresh clone works with no setup step. The API
dump used by `vault_apicheck.py` is a public file, so it is a cache (`tools/.cache/`), not
private data.

**D8. The tracker's User-Agent names the tool, not a person.** A public tool should not send
its author's address from every user's machine. `TRENDS_CONTACT` adds contact details for
those who want to be reachable.

**D9. `~/roblox-final` is the documented install location, not a machine path.** The skill
docs give script paths from there. Rewriting every path would change the build skills' bodies
for no gain in behaviour; the README says to clone there.

**D10. `NOTICE.md` lists only what someone using the toolkit has to act on.** The fonts the UI
skill ships and their licence, the terms of the tools and models the skills call, how the design
library treats other games, and where the tracker's data stays. Each is a thing a user can get
wrong by not knowing it.

**D11. `starter/.mcp.json` keeps `/mnt/c/Windows/system32/cmd.exe`.** It is the fixed WSL path
to a Windows system binary, the same on every WSL machine, and it is how a WSL session starts
the Studio MCP. It names no user.

**D12. The public history starts from one commit.** The earlier history held the private
files. It is saved as a git bundle inside `private/` and the public branch begins with a single
commit of the cleaned tree; later work is committed on top.

**D13. Public commits carry the repository handle and a GitHub no-reply address.** The machine's
global git identity is a real name and a personal address, and commit metadata is as public as
file contents. The toolkit repo sets a local identity instead; the private repo keeps the global
one. This is a local setting and can be changed before the first push.
