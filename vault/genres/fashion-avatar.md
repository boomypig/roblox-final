---
title: Fashion and avatar games
type: genre
read-when: Building a dress-up, fashion-voting, runway, makeup or avatar-creator/catalog game, or any feature that changes avatars with HumanoidDescription or AvatarEditorService.
last-researched: 2026-10-25
---

# Fashion and avatar games

## In one line

Players style an avatar, either for a themed round that strangers rate or simply to try on and
buy catalog items. The outfit is the score, the screenshot and the social currency. Two shapes
chart on Roblox:

| Shape | Loop | Biggest example (data, 2026-10-25) | Content source |
|---|---|---|---|
| **Themed dressing rounds** (Roblox genre *Roleplay & Avatar Sim / Dress Up*) | theme → timed dressing → runway → 1–5 star votes → podium | Dress To Impress (case study: dress-to-impress) 103K, 13 per server | The game's own wardrobe |
| **Avatar creators / catalogs** (*Shopping / Avatar Shopping*) | search the Roblox catalog → try on free → save outfit → buy | Catalog Avatar Creator 85K, 24 per server, 94% likes | The Roblox Marketplace |

A hybrid exists: Catalog Avatar Runway runs DTI-style themed runway rounds with catalog items;
25.0K players, created 2026-05-25 (data, 2026-10-25).

## Core loop

- **Moment to moment (5–30 s):** open a rack or a search → equip → see it on your avatar →
  adjust color, layer or position → compare against the theme.
- **Round (DTI, community wiki 2026-10):** lobby intermission, theme revealed near its end →
  360 s dressing with at most 18 items equipped → runway walk in join order, with poses →
  every player rates every look 1–5 stars → top 3 on a podium → stars and cash paid out.
  DTI launched with 30 s intermission and 3 min dressing (community wiki).
- **Session (20–60 min, inferred):** 3–6 rounds; cash from rounds buys items, poses, walks.
- **Meta (weeks):** lifetime stars raise a rank (DTI: 14 ranks from 0 to 150,000+ stars) that
  unlocks items and harder servers; seasonal updates, quests and a battle pass (community wiki).
- **Catalog games:** search → try on → save to an in-game closet or as a Roblox outfit → buy the
  pieces you love; "50M+ community-created outfits" to browse (data, Catalog Avatar Creator
  description, 2026-10-25).

## Main verbs

Browse, equip, layer, recolor, adjust (move/rotate/scale an accessory), apply makeup and hair,
pose, walk, rate, save, share, buy, gift.

## Why players come back

- **Every round is a new prompt.** DTI had 790+ themes by 2026-07-19 (community wiki), so the
  same wardrobe makes new puzzles. Theme variety is the cheapest content in the genre (inferred).
- **Public judgement and a podium.** Strangers' votes and a top-3 reveal create stakes without
  combat (inferred).
- **Self-expression that leaves the game.** Players screenshot and post looks; DTI's "Pose 28"
  became a TikTok trend in 2024 where people struck the pose in real outfits (community wiki).
- **Collection.** Seasonal and collab items, rank rewards and battle-pass tiers (community wiki).
- **Catalog games:** trying on paid items for free is the hook; anything bought goes to the
  real Roblox inventory and works in every game (data, game descriptions 2026-10-25).

## What separates top games from clones

- **Enough wardrobe for the themes.** A theme you can't dress for is a dead round (inferred). DTI
  ships items every seasonal update and themes that can be answered several ways (community wiki).
- **Layering that tolerates "jank".** Clipping and creative misuse of items is part of the fun;
  RoWatcher lists "item clipping as a creative tool" among DTI's success reasons (press,
  RoWatcher 2026, unverified). DTI later added accessory move/rotate/scale (community wiki).
- **Runway as a show.** Poses, walks and runway effects (players throw hearts or tomatoes) turn
  voting into entertainment (community wiki).
- **Servers sorted by skill.** DTI splits Casual, Regular, Pro (3,000+ stars), Master (10,000+)
  and VIP servers, so new players don't face veterans (community wiki).
- **Moderated themes.** DTI removed themes that players used to mock cultures, and lets players
  report custom themes (community wiki).
- **Catalog games:** speed of search, outfit saving, and a buy button on every item (inferred).

## Avatar plumbing (APIs checked against the engine reference, 2026-10)

| Need | API | Notes |
|---|---|---|
| Read a player's current look | `Humanoid:GetAppliedDescription()` | Returns a copy; doesn't yield (official) |
| Build a look | `HumanoidDescription` properties (`Shirt`, `Pants`, `Face`, `HeightScale`, `BodyTypeScale`…) and `HumanoidDescription:SetAccessories(list, includeRigid)` | Each entry: `AccessoryType`, `AssetId`, `IsLayered`, `Order`, `Puffiness`; prefer it over editing `AccessoryBlob` JSON (official) |
| Apply a look | `Humanoid:ApplyDescriptionAsync()`; `Humanoid:ApplyDescriptionResetAsync()` when anything else also edits the character | The non-`Async` names are deprecated (official API dump). Apply on the server so every client sees the same avatar (inferred) |
| Spawn in a look | `Player:LoadCharacterWithHumanoidDescriptionAsync()` with `Players.CharacterAutoLoads = false` | (official) |
| Load a user or outfit | `Players:GetHumanoidDescriptionFromUserIdAsync()`, `Players:GetHumanoidDescriptionFromOutfitIdAsync()` | (official) |
| Preview on a mannequin | `Players:CreateHumanoidModelFromDescriptionAsync()` | For racks and podium dummies (official) |
| Keep platform rules | `AvatarEditorService:ConformToAvatarRulesAsync()`, `AvatarEditorService:CheckApplyDefaultClothingAsync()` | The second adds default shirt and pants when needed (official) |
| Search the catalog | `AvatarEditorService:SearchCatalogAsync(CatalogSearchParams)` | Throttled with item-detail calls: **100 requests/s per experience across all servers** (official, 2026-10) |
| Read owned items | `AvatarEditorService:PromptAllowInventoryReadAccess()` then `GetInventoryAsync()` / `GetOutfitsAsync()` | Consent lasts one session; ask once per session (official) |
| Save to Roblox | `AvatarEditorService:PromptSaveAvatar()`, `PromptCreateOutfit()` (outfit type Avatar or Makeup) | Non-yielding; read the `...Completed` events. **Unowned items are not granted** (official) |
| Sell catalog items | `MarketplaceService:PlayerOwnsAssetAsync()`, `PromptPurchase()`, `PromptBundlePurchase()`, `PromptBulkPurchase()` | Game owner earns **40%** of in-game avatar item sales ([monetization](../fundamentals/monetization.md)) |
| Let players publish creations | `AvatarCreationService:PromptCreateAvatarAsync()` | Bodies built with `EditableMesh`/`EditableImage`, needs a Robux-bought creation token; items are not listed on the Marketplace and can't be resold or traded (official, 2026-10). Advanced; skip for an MVP |

Layered clothing on a custom rig needs `WrapTarget` on the body and `WrapLayer` on the clothing
with matching cages; R15 with a Humanoid welds automatically (official). Making your own layered
clothing is 3D modeling work with cages; there's no shortcut for a dev without an artist
(inferred).

## Voting and scoring

DTI facts (community wiki, 2026-10): every player rates every look 1–5 stars; no limit on
voters. Its Style Showdown mode gives each voter **3 votes** (2 below 5 players) and deducts
unused votes, and the lowest scorer is eliminated each round until 3 remain. Press on DTI lists
spite-voting and clique voting as standing complaints (press, RoWatcher 2026, unverified).

Rules (inferred unless tagged):
- **Count a vote only if the voter watched the walk** (the model was on stage ≥ 2 s while the
  voter was in the audience). Unrated = no vote, never a hidden 1 star.
- **No self-votes.** Weight votes between friends or party members at 0.5 (`Player:IsFriendsWithAsync`,
  `Player.PartyId`).
- **Neutralize spite voters:** score each look by the voter-normalized mean (each vote minus that
  voter's average this round), or drop the single highest and lowest vote when ≥ 5 voters.
- **Limited ballots beat open star rating** in small servers: "pick your top 2" can't be used to
  bury everyone.
- **Low-effort guard:** an outfit unchanged from the player's own avatar, or with fewer than ~4
  game items, can't reach the podium.
- **NPC judge fallback:** tag every item with styles (`goth`, `beach`, `formal`…) and themes with
  wanted tags. With fewer than 4 players, or as a 20–30% blend, score theme fit from tags. It
  keeps rounds working at low CCU and caps the damage of trolls.
- **Pay participation:** every finisher gets stars and cash; placement adds a bonus, so a bad
  vote never zeroes a round (DTI pays 0–60 cash per round, community wiki).
- All tallies on the server; one rate-limited `CastVote(targetUserId, stars)` remote validated
  per [security](../../.claude/skills/roblox-code/references/security.md) and the phase rules in
  [round-system](../patterns/round-system.md#map-voting).

## Moderation and age rules

- **Content maturity covers what you make, not UGC players bring** (their avatar clothing and
  accessories) (official, 2026-10). See [audience](../fundamentals/audience.md) and the
  questionnaire in [metadata](../fundamentals/metadata-thumbnails-icons.md#maturity--compliance-questionnaire).
- **Outfits built from 3D assets are not free-form creation** (official). **Freehand painting**
  on avatars or surfaces, and pixel grids others can see, **are** free-form creation: 16+ only
  (official). A "paint your own makeup" feature therefore likely makes the game 16+ (inferred).
- **Romantic themes** (even a quick kiss, or in the title) make a game 18+ age-verified
  (official, 2026-10). Keep themes to clothing styles; no "date night" kiss emotes (inferred).
- DTI is rated Minimal (community wiki, 2026-10). Roblox deleted DTI on 2023-12-20 for
  inappropriate content and it reopened a day later with changes (community wiki, unverified).
- Combinations can create problems single items don't: skin-tone bodysuits that read as nudity,
  suggestive pose and item combos. Run `CheckApplyDefaultClothingAsync`, keep a block-list of
  item and pose combos, and give every runway look a report button (inferred).
- **Typed text others see** (custom themes, outfit names) goes through
  `TextService:FilterStringAsync` and `GetNonChatStringForBroadcastAsync`; prefer picking from
  a preset theme list (inferred; DTI's custom themes are reportable, community wiki).
- Chat needs an age check and many players can't chat, so voting, poses and runway effects must
  carry the social layer ([social](../fundamentals/social-and-virality.md#voice-and-chat-constraints-2026)).
- Don't call the game a "hangout": that word classifies it as a social hangout, 16+ (official).

## Session shape

- **First 60 seconds:** spawn into the lobby with a theme countdown visible, or straight into a
  dressing room if a round is under 30 s old; first item equipped by ~20 s (inferred; see
  [first-time experience](../fundamentals/first-time-experience.md)).
- **First 10 minutes:** two rounds with 3–4 min dressing, one runway, first stars, a rank
  progress bar, one cash purchase (inferred). DTI's full 6 min dressing + runway for 13 players
  is about a 10 min cycle (inferred from the community-wiki timings).
- **Day 7:** a few ranks up, a saved outfit, a server tier unlocked, the current seasonal
  quest started (inferred).

## Social hooks

- Duo modes and gifting: DTI sells "gifting props" for every pass at the pass price (community
  wiki).
- Free-play areas with photo spots, poses and walks; DTI's Freeplay mode has no theme or timer
  and loads saved outfits (community wiki).
- Brand and music collabs: DTI's Charli XCX *Brat* collab drew 651K+ concurrent in 2024-08
  (press, NYT 2024-09-15). Not available to a new game; the solo-dev version is seasonal themes
  (inferred).
- Share a look: `CaptureService:PromptShareCapture` exists for captures (official API); test it
  before relying on it (inferred). See [social](../fundamentals/social-and-virality.md).

## Monetization that works here

DTI prices (official game-pass API, read 2026-10-25): VIP Pass 799 (VIP rack, salon, lounge),
x2 Money 399, Custom Makeup 349, Materials+ 299, Run Faster 149, Increased Item Limit 129
(18 → 24 items), item-set passes 279–449. Developer products (community wiki): Theme Prop 75
(choose the theme), +60 seconds 79, monthly VIP 299, accessory adjustment 399 (or free after
30 rounds), cash packs 500 cash for 100 Robux up to 40,500 for 4,500. Battle pass: 30 tiers,
premium track 299, tier skip 199 (community wiki).

- **Cosmetic racks and set passes** are the core: they add expression, not score (inferred).
- **Catalog commissions:** a catalog-based game earns 40% of every avatar item bought in game,
  with no art cost (official). My Avatar! adds a points store rewarding in-game purchases (data,
  description 2026-10-25).
- **Careful with competitive edges.** Extra dressing time and faster running sell, but they buy
  score in a voted contest; RoWatcher reports pay-to-win complaints about VIP items (press,
  unverified). Sell them only for freeplay, or keep timers equal in ranked rounds (inferred).
- Don't put "free UGC" or Robux claims in metadata ([metadata](../fundamentals/metadata-thumbnails-icons.md)).
- Passes and products follow [monetization](../fundamentals/monetization.md) and [shops](../patterns/shops.md).

## Common failure modes

- **Too few items:** every theme looks the same; players leave after two rounds (inferred).
- **Spite and clique voting** ruin the podium (press, RoWatcher, unverified). Fix with the
  scoring rules above.
- **Dead time:** long runways in full servers; 13 walks × 8–10 s is ~2 min of watching
  (inferred). Cap the walk at ~8 s and show two models at once above 10 players.
- **Empty servers:** a vote game at 50 CCU puts 2 players in a room (inferred). Use small
  servers (6–8) and the NPC judge.
- **Event crashes:** DTI's servers crashed during events (press, RoWatcher, unverified); a
  limited code caused crashes at a 2024 launch (press, via Wikipedia).
- **Catalog throttling:** every client searching on every keystroke hits the 100 req/s cap at
  scale (official cap; inferred risk). Debounce search and cache popular queries.
- **Maturity surprise:** freehand makeup painting, romance themes or "hangout" wording quietly
  move the game to 16+ or 18+ (official rules; inferred risk).

## Saturation & opportunity

All (data, 2026-10-25) unless tagged:
- **`fashion-avatar` theme: 25 games, 266K players, 11K per game, median 604**, labeled
  **crowded**; DTI holds 39%; 4 in the top 100; 0 rising. Subgenres: Dress Up 8 games, 153K
  (1.4% of charted players); Avatar Shopping 30 games, 136K (1.2%).
- **Avatar Shopping is a long tail of catalog clones:** after Catalog Avatar Creator (85K) and
  My Avatar! (28.9K), most of the 30 sit under 4K, many under 500.
- **Dress Up is a few big games plus young entries:** Catalog Avatar Runway 25.0K (created
  2026-05-25), Royale High 7.2K (2017), Makeup All Stars 6.8K (created 2026-10-04), Prism Runway
  Show 4.4K (2025-07-14), Dressmaker's Dream 2.7K (2026-09-26, 8 per server). The report's "0
  rising" reflects only 2 snapshots of history; three Dress Up games are under 6 months old.
- **The theme's +51% is mostly time of day and DTI's event:** DTI went 74.8K → 103K between
  snapshots as it added a Halloween quest; the snapshots are Thursday 22:46 vs Saturday 03:24
  UTC.
- **Opportunity (inferred):** (1) the catalog-runway hybrid, which needs no wardrobe art and
  earns commissions (Catalog Avatar Runway proves demand at 25K); (2) a narrower fashion verb
  with NPC clients instead of voters: tailoring, a salon, styling customers for a shop, which
  crosses with the `sell-job` theme ([job-sims](job-sims.md)) and works solo; (3) 6–8 player
  vote servers that fill at low CCU. Head-on DTI clones fight a 3-year wardrobe and a brand.

## Scope for a solo dev

**Recommended MVP (5–6 weeks, inferred): catalog runway.** Lobby with a theme countdown; 3–4 min
dressing with a catalog search panel and 6–8 curated category racks; runway with 2–3 poses;
limited-ballot voting with the NPC judge fallback; podium; stars, ranks and a closet of saved
looks; buy buttons; 8-player servers.

| Week | Build |
|---|---|
| 1 | Round phases ([round-system](../patterns/round-system.md)); server-side `ApplyDescriptionAsync` pipeline; equip/unequip remotes with validation |
| 2 | Catalog search UI with debounce and server cache; curated racks; item → style tags; 60 themes with wanted tags |
| 3 | Runway camera, walk, poses; voting, scoring rules, podium |
| 4 | Stars, ranks, closet saves ([player-data](../patterns/player-data.md)); `PromptPurchase` / `PromptBulkPurchase` with ownership checks |
| 5 | Phone layout of the dressing UI ([ui-ux](../../.claude/skills/roblox-ui/references/ui-ux.md)), report button, theme filter, onboarding |
| 6 | Metadata, maturity questionnaire, playtests at 2, 4 and 8 players |

- **Own-wardrobe variant (8–12 weeks, inferred):** only with an artist or bought-and-licensed
  meshes. Without one, cheap variety comes from color, `Material` and texture swaps on a small
  base set (DTI sells a Materials+ pass and pattern packs, community wiki).
- **Cut:** in-experience creation (`AvatarCreationService`), freehand makeup, trading, duo mode,
  battle pass, freeplay town, minigames, collabs (inferred).

## Top examples

- Dress To Impress (case study: dress-to-impress): themed rounds, star voting, ranks,
  seasonal live-ops; 103K, 13 per server, 91% likes (data, 2026-10-25).
- Catalog Avatar Creator: try-on catalog with community outfits and purchases; 85K, 24 per
  server, 94% likes, created 2021-07-03 (data, 2026-10-25).
- My Avatar!: catalog browsing plus a points store for in-game purchases; 28.9K (data, 2026-10-25).
- Catalog Avatar Runway: runway rounds with catalog items; looks exported to a sister catalog
  game; 25.0K, 15 per server (data, 2026-10-25).
- Royale High: long-running fashion roleplay with seasonal sets; 7.2K, 12 per server (data,
  2026-10-25). See [roleplay-life-sim](roleplay-life-sim.md).

## Build checklist for agents

### Do
- Apply looks on the server with `ApplyDescriptionAsync` (or `ApplyDescriptionResetAsync` if
  other code edits the character); validate every equip against the round's allowed items.
- Use the `Async` API names; the old names are deprecated.
- Enforce an item cap (18 in DTI's standard mode) and run `CheckApplyDefaultClothingAsync` on
  every runway look.
- Tag every item with styles and every theme with wanted tags; ship ≥ 60 themes at launch.
- Score with watched-only votes, no self-votes, friend/party down-weighting and voter
  normalization or limited ballots; keep the NPC judge for small servers.
- Pay every finisher; cap runway walks at ~8 s.
- Debounce catalog search and cache results; stay under 100 requests/s per experience.
- Check ownership with `PlayerOwnsAssetAsync` before `PromptSaveAvatar` / `PromptCreateOutfit`,
  and offer `PromptPurchase` or `PromptSetFavorite` for unowned pieces.
- Ask for inventory access once per session, only when the player opens their own items.
- Filter any player text others see; prefer preset theme lists.
- Add a report button to the runway; keep a block-list of problem item combos.

### Don't
- Don't trust client-side outfit or vote state; don't let the client call apply on others.
- Don't add freehand makeup or body painting unless you accept a 16+ audience.
- Don't use romance themes, kiss emotes or "hangout" wording.
- Don't sell extra dressing time or speed in scored rounds.
- Don't ship voting that needs chat, or a round that can't run with 2 players.
- Don't copy DTI's names (Lana, Baddie Pass, Style Showdown, rank names), themes list, items,
  poses (Pose 28) or runway art.

## Sources

1. private/trends/latest.md, `trends lookup` and the tracker DB — fashion-avatar theme, Dress Up / Avatar Shopping subgenres, per-game players, server sizes, created dates, descriptions (data, 2026-10-22 and 2026-10-25)
2. https://create.roblox.com/docs/reference/engine/classes/HumanoidDescription.md — SetAccessories fields, AccessoryBlob, Async getters
3. https://create.roblox.com/docs/reference/engine/classes/Humanoid.md — ApplyDescriptionAsync, ApplyDescriptionResetAsync, GetAppliedDescription
4. https://create.roblox.com/docs/characters/appearance — HumanoidDescription workflow, LoadCharacterWithHumanoidDescription, WrapTarget/WrapLayer rules
5. https://create.roblox.com/docs/reference/engine/classes/AvatarEditorService.md — prompts, consent, catalog search, 100 req/s throttle
6. https://create.roblox.com/docs/players/avatar-editor — unowned items not granted, PlayerOwnsAsset + PromptPurchase, once-per-session consent
7. https://create.roblox.com/docs/avatar/in-experience-creation — AvatarCreationService bodies, creation tokens, not resellable
8. https://create.roblox.com/docs/production/promotion/content-maturity — UGC exclusion, outfits vs free-form creation, romance 18+, hangout 16+
9. https://github.com/MaximumADHD/Roblox-Client-Tracker (API-Dump.json via tools/vault_apicheck.py) — deprecated vs Async names, Player.PartyId, IsFriendsWithAsync
10. https://dress-to-impress.fandom.com/wiki/Dress_To_Impress/Game_Mode — 360 s, 18/24 items, 1–5 stars, servers and star gates (community wiki, read via API 2026-10-25)
11. https://dress-to-impress.fandom.com/wiki/Style_Showdown — limited votes, eliminations
12. https://dress-to-impress.fandom.com/wiki/Themes — 790+ themes, removed themes
13. https://dress-to-impress.fandom.com/wiki/GamePasses and https://dress-to-impress.fandom.com/wiki/Money — products, gifting, cash packs, cash per round
14. https://apis.roblox.com/game-passes/v1/universes/5203828273/game-passes — DTI pass names and prices (read 2026-10-25)
15. https://en.wikipedia.org/wiki/Dress_to_Impress_(video_game) — collab peak 651K (NYT), event crash
16. https://rowatcher.com/news/dress-to-impress-how-a-teen-developer-s-fashion-game-hit-9-7-billion-visits — success reasons, spite/clique voting, pay-to-win complaints (third-party, unverified)
