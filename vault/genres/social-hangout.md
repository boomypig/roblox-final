---
title: Social hangout
type: genre
read-when: Building a hangout, chill social space, voice or chat game, emote/vibe game, or donation/booth game, or deciding whether a social game will be labeled 16+.
last-researched: 2026-10-24
---

# Social hangout

## In one line

A place whose main activity is being with other people: talking, emoting, sitting, showing off.
On Roblox that is also a **content category**. A game labeled a social hangout reaches only
age-checked 16+ players (18+ age-verified if it has private spaces). So the first design
decision is whether you are building a hangout at all, or a social game with a real verb.

Read with: [audience](../fundamentals/audience.md) (age bands, chat checks, account tiers),
[metadata](../fundamentals/metadata-thumbnails-icons.md) (questionnaire, "hangout" wording),
[social-and-virality](../fundamentals/social-and-virality.md) (voice, invites, clips),
[monetization](../fundamentals/monetization.md), [roleplay-life-sim](roleplay-life-sim.md)
(the roleplay exemption), [private-servers](../patterns/private-servers.md).

## What counts as a hangout (official, content maturity docs 2026-10)

- **Definition:** games "where the primary theme or activity is to talk to or interact with
  other players". Examples: hangouts, vibe games, socializing spaces, and supportive places
  such as "sad rooms".
- **Not a hangout:** games whose primary theme is roleplay, when roleplay is central (taking a
  role and using in-game items to play it). See [roleplay-life-sim](roleplay-life-sim.md).
- **Words decide too.** Mentioning a social hangout in the title or description classifies the
  game as one. Fix a wrong label by changing the text and retaking the questionnaire.
- **Private spaces:** enclosed spaces built for personal, secluded activities (sleeping,
  changing clothes, bathing) *and* for one or very few people (bathroom stall, bedroom, small
  tent).
- **Free-form user creation** (freehand drawing, spray paint, writing, pixel grids, even
  per-round drawings others can see) is also 16+. Building from 3D assets and making outfits
  are excluded.

| Design | Who can play | Tag |
|---|---|---|
| Social hangout, no private spaces | Age-checked 16+ only | official, 2026-10 |
| Social hangout with private spaces | Age-*verified* (ID) 18+ only; Restricted is unplayable in some countries | official, 2026-10 |
| Mainly set in private spaces, or adult venues (bars, clubs) | ID-verified 17+ under the 2025-08-15 policy; romance and alcohol are 18+ in current docs | official |
| Social game whose primary activity is something else (karaoke, rating, trading, donating, emote dance) | Whatever its content earns, often Minimal | official labels, read 2026-10-24 |

**How the rule tightened:**

| Date | Change | Tag |
|---|---|---|
| 2024-11-18 | Hangouts "primarily designed for socializing with users outside of their friends list" and free-form writing/drawing games gated for under-13s | official, newsroom |
| 2025-08-15 | Hangouts that depict private spaces: ID-verified 17+. Roblox auto-removes servers with high volumes of violative behavior | official, newsroom |
| By 2026-10 | Hangouts 16+; with private spaces, age-verified 18+. Older guidelines page still says 13+ | official docs (start date of 16+ unverified) |

## What the label costs in reach

- **Rough math (inferred):** 18+ is 27% of age-checked DAUs and 13–17 is 38% (official,
  2026-06). If 16–17 is about 2/5 of 13–17, then 16+ is about 42% of age-checked DAUs. Only 57%
  of DAUs were age-checked by Q2 2026 (official). So a 16+ hangout can reach roughly a quarter
  of daily players, and none of the Kids or Select accounts.
- **18+ age-verified** is a subset of the 27% that have done ID verification. We found no
  number for it (unverified). Plan for it to be small.
- **Charts barely contain 16+ games.** We read the maturity label of all 880 charted games on
  2026-10-24 (official labels; games from the 2026-10-22 snapshot):
  - 571 Minimal, 233 Mild, 71 Moderate open to all; only **5** have a 16+ minimum (42.6K
    players, 0.6% of charted players); **0** carry a hangout or private-space descriptor; 0
    Restricted (official labels; inferred shares).
  - The biggest 16+ game is Catch the Artist! (20.4K players, free-form creation descriptor)
    (data, 2026-10-22; official label). A 16+ label limits a game; it doesn't kill it.
  - Caveat: the tracker reads charts as an anonymous session. Charts may hide 16+ games from
    that view, so the true count may be higher (unverified).
- **The adult niche is growing:** US 18+ DAUs +32% YoY and US 18–34 +42% (official, Q2 2026).
  A deliberate 16+/18+ hangout aims there.

## Core loop

- **Moment-to-moment (seconds):** walk up to a group → emote or say something → someone reacts
  → sit together, dance, or follow them somewhere.
- **Session (5–20 min):** arrive → see who is here → join a cluster or an activity (a karaoke
  round, an avatar rating, a booth) → watch, react, perform → leave or move servers.
- **Long-term:** regulars and new friends, status (titles, booth decor, avatar), private
  servers for a friend group, scheduled events.

PLS DONATE, the biggest charted Social-genre game, averages 6.8 min per session (community,
Rolimons, read 2026-10-24). Pure hangout sessions are short unless something is happening
(inferred).

## Main verbs

Talk, emote, sit, dance, follow, show off, rate, react, gift, donate, perform. Every verb that
works without chat matters, because many players can't chat with each other (official,
2026-01; see [audience](../fundamentals/audience.md)).

## Why players come back

- **People:** the friends they made, and co-play days, which RFY ranks (official; see
  [social-and-virality](../fundamentals/social-and-virality.md)).
- **A mood:** music, lighting, a view. Golden-hour lighting suits hangouts
  ([visual-quality](../../.claude/skills/roblox-map/references/visual-quality.md)).
- **Status:** a title, a rare emote, a decorated booth, being recognized by regulars (inferred).
- **Something happening at a known time:** a weekly show, a karaoke final, a host's event (see
  [live-ops](../fundamentals/live-ops-and-updates.md)).

## What separates top games from clones

1. **A light structure that makes strangers interact.** Formats with a goal: avatar rating,
   karaoke battles, rap battles, donation booths, emote dance, trading plazas. The charted
   ones are labeled by that activity, not as hangouts: Sing It! Karaoke Battles (voice) and
   Trending Emote Dance are Minimal, Rap Battles (voice) is Mild (official labels, read
   2026-10-24). Describe the activity truthfully; don't dress up a chat room (inferred).
2. **Works without chat.** Emote wheel, reaction buttons, seat invites, "wave" prompts. Roblox
   announced creator Quick Words (preset phrases) at RDC 2026 (press, 2026-09; configuration
   unverified).
3. **Density on purpose.** A small map, seating in clusters of 3–6, and everyone visible from
   spawn. A big empty world reads as a dead game (inferred).
4. **Voice as an option, never a gate.** Voice needs age-checked 13+ users in supported
   countries and servers of ≤100 (official). Proximity is the default; zones need
   `VoiceChatService.UseAudioApi` with `AudioDeviceInput` access lists (official; details in
   [social-and-virality](../fundamentals/social-and-virality.md#voice-and-chat-constraints-2026)).
5. **Moderation tools players can see:** block, mute, report, and "move to another server"
   in one tap (inferred).

## Session shape

Targets (inferred):

- **First 60 seconds:** another player within sight of spawn, a seat or activity one tap away,
  an emote button on screen, music playing.
- **First 10 minutes:** one interaction with a stranger (an emote back, a rating, a booth
  visit), one cosmetic unlocked or earned.
- **Day 7:** knows the event schedule, has friended someone met here, owns a title or emote.

## Social hooks

- Scheduled moments: rounds every 5–10 minutes (rating, karaoke) give a shared focus (inferred).
- Server-wide announcements via `TextChannel:DisplaySystemMessage` reach players who can't
  chat (official).
- Global Chat (cross-server, grouped by age and language) is on by default and can be turned off
  in the Creator Dashboard (official, 2026). Decide on purpose; it can make a small game feel
  full, or flood it (inferred).
- Shareable moments: a winning performance or a top-rated avatar, captured with
  `CaptureService` (see [social-and-virality](../fundamentals/social-and-virality.md)).
- Private servers for friend groups; see [private-servers](../patterns/private-servers.md).

## Monetization that works here

Hangouts sell **status and expression**, not power (inferred).

- **Avatar item commissions:** catalog items sold in-game pay the game owner 40% (official).
  Catalog Avatar Creator had 59K players and was #19 overall (data, 2026-10-22).
- **Robux transfers:** Roblox Plus subscribers send 10–500 Robux to another player in your game;
  your game gets 10%, the recipient 90% (official, 2026-10). Server calls
  `MarketplaceService:PromptRobuxTransferAsync(sender, receiverUserId, amount)` and handles
  `Enum.ReceiptType.RobuxTransferSender` / `RobuxTransferReceiver` with
  `MarketplaceService:BindReceiptHandler` (official). This replaces donation boards that sold
  other games' passes; cross-game pass sales were disabled from 2026-05-30 (official, via
  [monetization](../fundamentals/monetization.md)).
- **Status passes:** chat tag or name color (set through `TextChatService.OnIncomingMessage`
  and `TextChatMessageProperties.PrefixText`), emote packs (`HumanoidDescription:SetEmotes`),
  booth decor, a vehicle or a stage effect (inferred).
- **Example price list:** PLS DONATE sells Boombox Control 49, Donation Sign 99, Disguise Mask
  299, Cloaking Device 399, Golf Cart 499, Booth Painter 699 and a Gigantic Donation Sign at
  100,000 Robux (official listing, read 2026-10-24).
- **Music:** Brookhaven compensated "Music Unlocked" owners with 100+ built-in songs when music
  IDs stopped working (community, Brookhaven wiki). Sell a curated playlist, not "play any ID"
  (inferred).
- **Private servers** for friend groups, with the Plus payout of up to 100 Robux per active
  Plus member (official, 2026-04).
- **Rewarded video ads** fit, since every hangout player is 16+ and ads need 13+ (official
  rules; see [monetization](../fundamentals/monetization.md#rewarded-video-ads)).

## Common failure modes

- **Accidental 16+ label:** the word "hangout" in the description, or a "chill and chat" pitch
  for a game that is really a minigame (official classification rule).
- **Private spaces:** a bedroom, a bathroom stall, a two-person tent or booth pushes it to
  age-verified 18+ (official definition).
- **The cold start.** A hangout with 2 people in it fails the first-minute test, so new players
  bounce, and bounce is a top signal (inferred; see
  [discovery](../fundamentals/discovery-algorithm.md)).
- **The donation crash.** PLS DONATE peaked at 196,819 players on 2025-10-17 (community,
  Rolimons) and had 1,891 on 2026-10-22, last updated 2026-08-16 (data). Cross-game pass sales
  ended 2026-05-30 (official). That rule change likely broke its loop (inferred; we have no
  history in between).
- **Harassment with no tools.** Without block, mute, report and server hop, regulars leave and
  servers get taken down (official takedown policy; inferred effect).
- **Status for sale that shames.** Leaderboards of top donors or "rich only" areas pressure
  young players to spend (inferred reviewer rule; see
  [monetization](../fundamentals/monetization.md#ethics-for-a-young-audience-reviewer-rules)).

## Saturation & opportunity

- **The Social genre is tiny on charts:** 2.8K players across 8 games (data, 2026-10-22).
  PLS DONATE leads with 1,891. The rest are two other donation games, two trading plazas for
  other games' items, a voice rap battle, and two small showcase spaces (data).
- **Hangout behavior lives inside roleplay towns.** Brookhaven won "Best Social / Hangout
  Experience" at the Roblox Innovation Awards 2024 (community, wiki) and is labeled Minimal
  roleplay (official, 2026-10-24). A change.org petition claims chat-blocked players moved to
  Brookhaven and Catalog Avatar Creator to talk (unverified).
- **Opportunity (inferred):**
  - For all ages: a social game *with a verb* (rate, perform, trade, build together) that
    keeps a Minimal or Mild label. This is the realistic path for the user's audience.
  - For 16+/18+: a deliberate adult hangout (music, conversation, voice) for the growing 18–34
    group. It gives up Kids/Select, so judge it against your goals (`private/goals.md`) before
    building.

## Scope for a solo dev

Hangouts need little content but a lot of care: density, moderation and mood. Week counts are
(inferred) for one developer with Rojo and Studio MCP.

**MVP:** one compact map (about 200×200 studs) with seating clusters, lighting and a curated
music zone; emote wheel; one structured activity on a 5-minute round (avatar rating, karaoke,
or a performance stage); name tags with earned titles; block/mute/report and a "new server"
button; 2–3 status passes; private servers.

| Week | Build |
|---|---|
| 1 | Map, lighting preset, seats (`Seat`), music zones, spawn that faces the busiest area |
| 2 | Emote wheel (`Humanoid:PlayEmoteAsync`), reactions, titles via `TextChatService.OnIncomingMessage` |
| 3 | The round activity: queue, timer, voting with server-side tallies, winner announcement |
| 4 | Safety pass (report, block, filtered text), passes with receipts, Robux transfer booths if you want donations |
| 5 | Questionnaire, phone layout, 20-bot server test, launch |

**Cut from v1:** voice-only features, custom chat UI, drawing or writing surfaces, private
rooms, cross-server systems, user-uploaded music IDs.

## Top examples

- Brookhaven (case study: brookhaven): the platform's biggest place to be together,
  labeled as roleplay, not a hangout.
- PLS DONATE (no case study): booth-and-donate format; 196,819 peak (2025-10-17), 1,891 players
  (data, 2026-10-22). A warning about building on a platform rule.
- Sing It! Karaoke Battles (no case study): voice-optional performance rounds; Minimal; 2.8K
  players (data, 2026-10-22).
- Catch the Artist! (no case study): a 16+ drawing party game with 20.4K players (data,
  2026-10-22), proof a 16+ label can still reach an audience.

## Build checklist for agents

### Do

- Decide first: hangout (16+) or social game with a verb (all ages). Write it in the design doc.
- For all-ages, make the verb the primary activity and describe only that activity in the title
  and description.
- Answer the questionnaire honestly; retake it after any update that adds talking spaces,
  drawing or enclosed rooms.
- Route all chat through `TextChatService`; use `TextChannel:DisplaySystemMessage` for round
  starts and winners.
- Filter every player-written string others can see with `TextService:FilterStringAsync` and
  `GetNonChatStringForBroadcastAsync`.
- Make every social action possible without chat: emotes, reactions, seat invites, votes.
- Keep voice optional; use `VoiceChatService.UseAudioApi` and access lists for any zones.
- Give one-tap block, mute, report and server hop.
- Compute votes, ratings and rewards on the server; one vote per player per round.
- Sell status (titles, emotes, decor), never advantages in votes or ratings.
- Use `MarketplaceService:PromptRobuxTransferAsync` for donations, and grant any thank-you perk
  only in the receipt handler.

### Don't

- Don't write "hangout", "chill and chat" or "meet people" in an all-ages game's metadata.
- Don't build bedrooms, bathroom stalls, small tents, private booths or bars and clubs.
- Don't add freehand drawing, spray paint or writable boards unless you accept 16+.
- Don't add dating, romance, "find a partner" or couple features (Community Standards ban).
- Don't let players post links, Discord names or personal info on signs or booths.
- Don't show top-donor leaderboards or let donations buy votes, ratings or visibility.
- Don't sell "play any audio ID" boomboxes.
- Don't copy PLS DONATE, Catalog Avatar Creator or any hangout's map, booth design, name or UI.

## Sources

1. https://create.roblox.com/docs/production/promotion/content-maturity — hangout definition, roleplay exclusion, private spaces, free-form creation, 16+/18+
2. https://about.roblox.com/newsroom/2024/11/major-updates-to-our-safety-systems-and-parental-controls — 2024-11-18 under-13 gate for hangouts and free-form drawing
3. https://about.roblox.com/newsroom/2025/08/extending-roblox-policy-on-romantic-and-sexual-content — 2025-08-15 private-space and adult-venue rules, server takedowns
4. https://about.roblox.com/community-standards — romance and suggestive settings banned, links only via Social Links
5. https://apis.roblox.com/experience-guidelines-api/experience-guidelines/get-age-recommendation — labels of all 880 charted games (read 2026-10-24)
6. https://create.roblox.com/docs/production/monetization/robux-transfers — Robux transfers: Plus senders, 10–500, 10% to the game, BindReceiptHandler
7. https://apis.roblox.com/game-passes/v1/universes/3317679266/game-passes — PLS DONATE pass prices (read 2026-10-24)
8. https://www.rolimons.com/game/8737602449 — PLS DONATE peak 196,819 on 2025-10-17, 6.83 min average playtime (read 2026-10-24)
9. https://www.roblox.com/games/8737602449 — PLS DONATE (tracker snapshot 2026-10-22 in private/trends/latest.md)
10. https://www.roblox.com/games/129928276175025 — Catch the Artist! (tracker snapshot 2026-10-22)
11. https://www.roblox.com/games/7041939546 — Catalog Avatar Creator (tracker snapshot 2026-10-22)
12. https://brookhaven.fandom.com/wiki/Brookhaven_RP — Innovation Award "Best Social Hangout" 2024
13. https://brookhaven.fandom.com/wiki/Brookhaven_RP/Monetization — Music Unlocked compensation
14. https://www.change.org/p/stop-the-roblox-age-check — claim that players moved to Brookhaven and Catalog Avatar Creator to chat (unverified)
15. https://create.roblox.com/docs/reference/engine/classes/Humanoid — PlayEmoteAsync
16. https://www.roblox.com/games/15550215902 — Sing It! Karaoke Battles (tracker snapshot 2026-10-22)
17. https://create.roblox.com/docs/chat/cross-server-chat — Global Chat on by default, can be turned off
18. https://create.roblox.com/docs/chat/voice-chat — voice eligibility, server size, audio API routing
19. https://gamesbeat.com/roblox-is-adding-emojis-custom-quick-words-and-voice-calling-to-its-in-game-chat-rdc-2026/ — Quick Words announced at RDC 2026
20. https://www.sec.gov/Archives/edgar/data/0001315098/000162828026051059/ex991-robloxq22026earnin.htm — Q2 2026 age-checked mix, coverage, US adult growth
