---
title: Story games
type: genre
read-when: Building a chapter-based story game (Break In-like): narrator and NPC dialogue, scripted days and nights, branching choices, multiple endings, replay, chapters as updates.
last-researched: 2026-10-25
---

# Story games

## In one line

A server of players lives through one short scripted story (20–30 min) told by a text
narrator and NPCs: explore, do group tasks, survive a threat, make a choice, reach one of
several endings, collect the badge, queue again for a different ending. Roblox files them as
**Adventure / Story** (data). The archetype is Break In (Cracky4, 2019): five days and nights in
a house, kid and adult roles, four endings (community wiki). Story horror (chase monsters,
darkness) also lives in [horror](horror.md); a linear escape told as a story is an
[escape obby](obby-escape.md).

## Core loop

- **Moment to moment (10–60 s):** read the narrator's line → do the beat it asks for (search
  rooms, answer the door, board windows, cook, find a key) → a scripted event fires.
- **Beat cycle (2–5 min, Break In):** day = explore, gather food and cash, do a group task the
  narrator grades; night = scripted scene, then villains attack rooms; dawn = narrator reports
  who was attacked and who died (community wiki).
- **Run (20–30 min):** 5 day/night cycles end in a boss fight and a final choice; the storyline
  takes about 20–30 minutes (community wiki).
- **Meta (weeks):** endings, badges, side missions (11 in Break In, press Sportskeeda), unlocked
  and paid roles; then the next chapter or sequel.

## Main verbs

Read, explore, search, collect, cook, eat, hide, board up, fight, protect, choose, vote, unlock,
replay.

## Why players come back

- **Endings to collect.** Break In: Good (leave the golden crowbar), Evil (a max-energy player
  takes it; needs 2+ players), Final (finish an NPC's side quest), Easter (a seasonal NPC task)
  (community wiki). "Which ending did you get?" is the replay hook (inferred).
- **Roles change the run.** 16 roles across Break In 1 and 2, each with a starting item; kids
  vs adults works as a difficulty pick (community wiki; press, Sportskeeda).
- **Badges as a checklist.** Break In's stated objective includes "get all of the badges"
  (community wiki).
- **Friends.** A story run is an evening's activity for a group; the narrator names the two
  players who did the most work on a task (community wiki).
- **The next chapter.** Chapter 1 ends on a hook; "favorite to get notified" is in the pitch
  (data, PINKIE PROMISE description 2026-10-25).

## What separates top games from clones

- **A narrator with personality** who reacts to what players did (names who opened the door,
  grades the boarding TERRIBLE/OK/GREAT/PERFECT) (community wiki). Generic quest text feels like
  a tutorial (inferred).
- **Group tasks with visible grades** that change the next beat: bad boarding → more attacks
  (community wiki). Choices have consequences without branching the whole script (inferred).
- **Endings triggered by play, not menus.** Picking up an item, finishing a side quest or
  giving an NPC three objects changes the ending (Break In, community wiki). Break In 2 adds an
  explicit end-of-run choice after a villain's message (community wiki).
- **Short and finishable.** 20–30 min fits a session; long stories lose groups (inferred).
- **Evergreen if it's good:** Break In was last updated 2023-10-09 and still has 2,950 players
  (data, 2026-10-25); Break In 2 (updated 2025-04-04) has 2,433.

## Branching and endings (design rules)

Structure (inferred unless tagged):
- **String of pearls:** a linear main path of 6–10 beats, optional side branches that rejoin,
  and divergence only at the end. Content cost grows by endings, not by paths.
- **3–4 endings for chapter 1:** a default ending, one "secret" gated by a side quest, one
  "dark" ending gated by a player action, one gated by a hidden collectible. Each ending is a
  20–40 s scene on the same map plus a badge.
- **Kinds of ending triggers:**

| Trigger | Example | Rule |
|---|---|---|
| Individual act | Max-energy player takes the boss's item → Evil ending (Break In, community wiki) | Require 2+ players so one troll can't ruin a solo run; show a "Take it?" prompt |
| Side quest | NPC's lost item returned → Final ending (Break In, community wiki) | Hint at it in round 1; put the clue in a place most players pass |
| Collection | 3 villain items found → Secret ending choice (Break In 2, community wiki) | Track per server, show "2/3" after the first find |
| Puzzle | Second wire puzzle → Origin ending (Break In 2, community wiki) | One per chapter; never on the main path |
| Recalled choices | Interrogation answers come back at trial (data, Prove Your Innocence description 2026-10-25) | Store flags, read them in the finale; tell players their choices were remembered |
| Group vote | Final choice by majority | 15 s timer, tie → default ending, show the tally |

- **State:** one server table of story flags (`Chapter`, `Beat`, `BoardGrade`, `ItemTakenBy`,
  `SideQuestDone`…). Publish the current beat as attributes on a `ReplicatedStorage` folder like
  [round-system](../patterns/round-system.md); clients only display. Endings are computed on the
  server from flags at the finale.
- **Badges:** `BadgeService:AwardBadgeAsync` per ending to everyone present (Break In gives the
  Evil badge to all survivors, community wiki). An in-game ending gallery ("2/4 endings")
  saved in [player-data](../patterns/player-data.md).

## NPC dialogue without voice actors

- **Text narrator first.** Break In's narrator is text lines with player names inserted and
  emoji (community wiki transcript). One line ≤ ~90 characters, on screen 3–5 s, typewriter
  effect, a click/tap to advance in solo (inferred).
- **NPC lines:** `TextChatService:DisplayBubble(npcHead, text)` for bubbles over NPCs;
  `TextChannel:DisplaySystemMessage` reaches everyone, including players who can't chat
  (official). Start talks with a `ProximityPrompt` (`ActionText = "Talk"`). The legacy `Dialog` /
  `DialogChoice` objects still exist but give little control over the UI (official API;
  inferred).
- **Cheap portraits:** a `ViewportFrame` with the NPC rig, or an avatar-built NPC from
  `Players:CreateHumanoidModelFromDescriptionAsync` (inferred).
- **Optional voice: `AudioTextToSpeech`.** Text up to **300 characters**; server limit
  1 + 6 × concurrent users requests per minute per experience, client 4 per second per user;
  `AutoLocalize` translates and picks a voice for 11 languages; `Speed` 0.5–2, `Pitch` ±12
  semitones (official, 2026-10). Pre-load each beat's lines during the previous beat (inferred).
- **LLM NPCs: `TextGenerator:GenerateTextAsync`.** Rate starts at 100 requests per minute and
  scales with players; `Temperature` 0.4–1.0; `ContextToken` keeps history; `JsonSchema` forces
  structured output (official, 2026-10). Use it for optional flavor chat only: plot beats must be
  deterministic, testable and translatable (inferred).
- **Translation:** keep all lines in a strings table so Roblox's automatic translation and
  `AutoLocalize` work; avoid text baked into images (see
  [audience](../fundamentals/audience.md#languages-and-automatic-translation)).
- **Animation without an animator:** animations must be owned by the experience owner or
  Roblox to play (community, unverified); use default and Roblox-made emotes, `TweenService`
  for doors and props, and camera moves instead of acted scenes (inferred).
- **Cutscenes:** `Camera.CameraType = Scriptable` with `TweenService` on the camera, started at a
  server-set time, ≤ 8 s, skippable after first view ([obby-escape](obby-escape.md)). No long
  intro: control within 10 s of arrival.

## Session shape

- **First 60 seconds:** lobby → pick a role → step on a queue pad or vehicle; the run starts
  when the pad fills or a 20–30 s timer ends, solo allowed (inferred; Break In players ride a
  moving truck from the lobby, community wiki). First narrator line within 5 s of arrival.
- **First 10 minutes:** two day/night cycles; one scripted scare or twist; one graded group task;
  first death or near-miss (inferred).
- **Day 7:** 2–4 runs, 2+ endings, most badges; waiting for chapter 2 (inferred).
- **Server shape:** the lobby is the root place; each run is a reserved server
  (`TeleportService:ReserveServerAsync` + `TeleportAsync`) so nobody joins mid-story
  (inferred). Break In's lobby holds 45 and Break In 2's 55 (data); the story house has 12 beds
  (data, description).

## Chapters as the update cadence

- **Ship chapter 1, announce chapter 2.** Charted examples put the chapter in the title or the
  pitch: PINKIE PROMISE "Chapter 1 out now", Packed With Care "[CHAPTER ONE]", Clean the House!
  "Play Chapter 1 solo or with a crew of up to 6" (data, descriptions 2026-10-25).
- Piggy's Book 1 has 12 chapters; the count was chosen by a community Discord poll on
  2020-03-11, about six weeks after launch (community wiki). It added a user-map Build Mode on
  2020-06-28 (community wiki). It has 23.2K players today (data, 2026-10-25).
- **Cadence (inferred):** a chapter every 4–6 weeks for a solo dev; in between, a weekly small
  drop (new ending, role, secret or seasonal event) per
  [live-ops](../fundamentals/live-ops-and-updates.md). Use Experience Notifications for the
  chapter launch ([retention](../fundamentals/retention.md#experience-notifications-current-rules-verified-2026-10)).
- **Chapter select:** finished chapters stay playable from the lobby; new players can start at
  chapter 1 or jump to the newest with a recap card (inferred).
- **Reuse:** each chapter reuses the engine (beats, flags, narrator, endings) and swaps the map,
  threat and script; build that engine in chapter 1 (inferred).

## Social hooks

Party queue pads; narrator call-outs by name; group tasks; dead players in a waiting room who
still watch (Break In, community wiki); endings needing 2+ players; private servers for friend
groups ([private-servers](../patterns/private-servers.md)); clip moments at twists and dark
endings ([social](../fundamentals/social-and-virality.md)). Puzzles must work without chat.

## Monetization that works here

Break In's shop (community wiki, prices as listed there):
- **Paid roles:** kid roles 299, adult roles 599 and 1,299 Robux (weapons). They make runs
  easier; fine in co-op, never in PvP (inferred).
- **Perks:** double energy from sleeping 99, keep cash between runs 199 (community wiki).
- **Server-wide help:** "Heal All" 399 heals every player once (community wiki). A purchase
  that helps the group is a good social sale (inferred).
- **Extra life:** "Lucky Respawn" 45 Robux, a respawn plus a wheel of random bonus items
  (community wiki). A wheel bought with Robux is a paid random item: show odds and gate with
  `PolicyService` ([monetization](../fundamentals/monetization.md#paid-random-items-eggs-crates-spins-luck-boosts-pity)).
- Cosmetics fit the theme: role outfits, pets, trails. Don't charge for chapters: paid access
  blocks discovery ([monetization](../fundamentals/monetization.md)).

## Common failure modes

- **One AFK player stalls the story.** Every beat needs a timer and a fallback; teleport
  stragglers (inferred).
- **Long unskippable scenes** and walls of text (inferred; [obby-escape](obby-escape.md)).
- **Content runs out** after one 20 min run with no endings or chapter 2 planned (inferred).
- **Flag bugs:** an ending fires wrongly because state wasn't reset or a leaver held the key
  item. Drop held story items on `PlayerRemoving` (inferred).
- **Too dark for the label:** realistic violence or strong fear moves the game to Moderate or
  higher ([horror](horror.md#maturity-label-what-horror-content-costs-you)).
- **Unlicensed IP:** stories built on film or toy characters invite takedowns; use original
  characters (inferred; hard rule in CLAUDE.md).

## Saturation & opportunity

All (data, 2026-10-25) unless tagged:
- **Adventure / Story: 15 charted games, 66K players.** Adventure overall: 216K, 1.9% share.
- **The leaders are new:** PINKIE PROMISE 13.0K (created 2026-10-06, chapter 1), Something is
  Wrong With My Dog 13.0K (2026-08-26), Clean all the Leaves 7.7K (2026-07-21), Clean the House!
  5.6K (2026-07-28), Motel Maniac 4.8K (2026-08-06), Prove Your Innocence! 3.1K (2026-10-11,
  multiple endings). Older: Rainbow Friends 5.8K (2021), Break In 3.0K (2019), Break In 2 2.4K.
- **Two flavors are working now:** story horror (PINKIE PROMISE and Motel Maniac sit in the
  rising `horror` clone wave) and mundane chores with a twist (leaves, house cleaning).
- **There is no `story` theme in the tracker**; only Roblox's Story subgenre is tracked.
- **Opportunity (inferred):** a Mild, non-horror chapter story with Break In-style group tasks
  and multiple endings (mystery, courtroom, cozy shop, family camping). Few charted games do
  branching endings; the format is cheap in art (one map per chapter) and heavy in writing,
  which suits a CS grad with an AI assistant.

## Scope for a solo dev

**MVP: chapter 1 in 5–6 weeks (inferred).** Lobby with role pick and queue pads; reserved-server
run of 20–25 min with 8 beats over 3 day/night cycles; narrator text; 4–6 NPCs; 2 graded group
tasks; 1 threat with simple AI; 3 endings; 4 roles (2 kid, 2 adult); badges; ending gallery;
skippable cutscenes ≤ 8 s.

| Week | Build |
|---|---|
| 1 | Story engine: beat list as data, flags, timers per beat, attributes, narrator UI with name insertion |
| 2 | Lobby, roles, queue pads, `ReserveServerAsync` teleport; map greybox with 6–8 rooms |
| 3 | Beats 1–5: interactions (`ProximityPrompt`), group task with grade, NPC dialogue |
| 4 | Night threat, waiting room for the dead, beats 6–8, finale and 3 endings |
| 5 | Badges, ending gallery save, cutscene camera, phone UI, strings table |
| 6 | Playtests solo, 4 and 12 players; AFK fallbacks; metadata and maturity questionnaire |

- **Cut:** voice acting, LLM NPCs, more than one map, an open world, combat depth, trading,
  shops beyond 3 passes, a second chapter before launch (write its outline only) (inferred).

## Top examples

- Break In: 5-day house siege, roles, narrator, 4 endings; 2,950 players, last updated
  2023-10-09 (data, 2026-10-25; community wiki).
- Break In 2: training, waves, 4 endings chosen after the boss's message; 2,433 (data; community wiki).
- Prove Your Innocence!: 3 days to a trial, evidence, interrogation choices that return,
  multiple endings; 3,131, 12 per server (data, 2026-10-25).
- PINKIE PROMISE: chapter-based horror story, chapter 1 only; 13.0K (data, 2026-10-25).
- Clean the House!: chores-with-a-twist chapter 1, solo or 6 players, upgrades between runs;
  5,611 (data, 2026-10-25).
- Piggy: 12-chapter Book 1 story horror; 23.2K (data, 2026-10-25). See [horror](horror.md).

## Build checklist for agents

### Do
- Drive the story from a data table of beats with a timer and fallback on each.
- Keep story flags on the server; compute endings from flags; reset state per run.
- Write the narrator as short text lines with player names; filter nothing players typed into it.
- Use `TextChatService:DisplayBubble` and `TextChannel:DisplaySystemMessage` for NPC and
  narrator lines; keep lines in a strings table for translation.
- Give control within 10 s; cap cutscenes at 8 s; make them skippable after first view.
- Ship 3+ endings with badges and an ending gallery; hint at the hidden ones.
- Run each story in a reserved server; drop held story items when a player leaves.
- Let dead players watch from a waiting room and still get the ending badge.
- Announce the next chapter in-game and in the description before launch.

### Don't
- Don't let one player's action ruin a solo run; gate dark endings on 2+ players.
- Don't make plot depend on `TextGenerator` output or on chat.
- Don't sell chapters, or sell weapons in any PvP mode.
- Don't sell an extra-life wheel without odds and `PolicyService` checks.
- Don't use other games' or films' characters, names, maps, villains or narrator lines (no
  Scary Larry, purge plot, pizza scene).

## Sources

1. private/trends/latest.md, `trends lookup` and the tracker DB — Adventure/Story games, players, server sizes, created/updated, descriptions (data, 2026-10-22 and 2026-10-25)
2. https://roblox-break-in.fandom.com/wiki/Break_In — objective, story premise (community wiki, read via API 2026-10-25)
3. https://roblox-break-in.fandom.com/wiki/Endings_(disambiguation) and https://roblox-break-in.fandom.com/wiki/Evil_Ending — ending triggers, 2+ players, badges
4. https://roblox-break-in.fandom.com/wiki/Storyline and https://roblox-break-in.fandom.com/wiki/Narrator — 20–30 min, day/night beats, grading
5. https://roblox-break-in.fandom.com/wiki/Narrator_messages — text transcript with name insertion
6. https://roblox-break-in.fandom.com/wiki/Roles — 16 roles, paid and badge-gated roles
7. https://roblox-break-in.fandom.com/wiki/Robux_Shop and https://roblox-break-in.fandom.com/wiki/Lucky_Respawn — pass and product prices
8. https://roblox-break-in.fandom.com/wiki/Lobby — role pick, moving truck
9. https://www.sportskeeda.com/roblox-news/things-know-playing-roblox-break-in — kid roles as easy mode, 11 side missions (press)
10. https://piggy.fandom.com/wiki/Book_1 — 12 chapters by community poll 2020-03-11, launch date, Build Mode (community wiki)
11. https://create.roblox.com/docs/reference/engine/classes/AudioTextToSpeech.md — 300 chars, rate limits, AutoLocalize languages, ranges
12. https://create.roblox.com/docs/reference/engine/classes/TextGenerator.md — rate limit, Temperature/TopP, ContextToken, JsonSchema
13. https://github.com/MaximumADHD/Roblox-Client-Tracker (API-Dump.json via tools/vault_apicheck.py) — DisplayBubble, DisplaySystemMessage, Dialog/DialogChoice, ReserveServerAsync
