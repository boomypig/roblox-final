---
title: Metadata, thumbnails and icons
type: fundamental
read-when: Writing a title, description, icon, or thumbnail, or before publishing.
last-researched: 2026-10-22
---

# Metadata, thumbnails and icons

## In one line

The thumbnail and title earn the click (play-through rate). The first minute must then match
them, or bounce rate punishes you. Accurate, original metadata is a ranking requirement, not
just style (official, 2026-10). See [discovery](discovery-algorithm.md).

## Asset specs at a glance

| Asset | Where it shows | Spec / limit |
|---|---|---|
| **Title** (root place name) | Everywhere | Max length likely 50 chars (unverified); the longest titles on Charts were exactly 50 (inferred, our Charts API sample 2026-10-22). Text-filtered. No "Roblox"/"Blox" |
| **Icon** | Several Home sorts, search, Continue, detail page | Square, **≥512×512**; shrinks to ~**150×150** in places; 1 per locale; moderated (official) |
| **Thumbnails** (images) | Home recommendations + top of detail page | **16:9, ideally 1920×1080**; .jpg/.gif/.png/.tga/.bmp; up to **10** images/videos on the detail page; Home Page tab and Experience Detail Page tab are configured separately (official) |
| **Personalized Home thumbnails** | RFY tiles | **2–5 active**; each <3 MB and ≤1920×1080 (official) |
| **Video** | First on the detail page; can show on Home | Authentic gameplay only; **3 uploads/month** (rejections count); not shown on Xbox, PlayStation or VR (official). Length and format limits aren't in the thumbnail docs (unverified) |
| **Description** | Detail page; search snippets | **1,000 characters**; the first **~160** show in Google snippets and the collapsed mobile view (official) |
| **Genre + subgenre** | Detail page; genre chart sorts | Changeable **once per 3 months**; Roblox may correct it (official) |
| **Maturity label + descriptors** | Detail page; audience gating | From the Maturity & Compliance questionnaire (official) |
| **Event thumbnails** | Event tiles and pages | Up to 5 per event (official) |
| **Ad creatives** | Sponsored tiles | Up to 10 per campaign, 16:9 (official) |
| **Social links** | Detail page | Visible only to age-checked 16+ users since 2026-06-30 (official) |

A **custom thumbnail is mandatory** for RFY. A default-only game gets zero RFY impressions
(official, 2026-10).

## Title

**Roblox rules (official):**
- Keep the name consistent. Frequent renames make the game harder to find by its old name.
- No word spam ("Obby Madness OBBY OBBY OBBY" can get the game demoted).
- "One or two well-placed emojis isn't harmful". Excessive or in-word emojis confuse players.
- No "Roblox", "Blox" or similar names in titles of games created on or after 2022-06-22.
- No implied monetary reward ("Robux", "free Robux"). Such games are deprioritized.
- No "duplicative" or confusingly similar titles. Community Standards ban metadata that is
  "deceptive, sensational, duplicative, or otherwise misleading".
- Titles and descriptions pass the text filter. Creators report saves failing on filtered
  words or symbols (community).

**What top games do now (inferred, our sample of the top 50 per sort from the Charts API,
2026-10-22):**
- Top Playing Now: 25/50 titles *start* with a bracket tag, 30/50 contain one, ~31/50 contain an
  emoji. Up-and-Coming: 17/50 start with a tag, 22/50 contain an emoji. Median length is 20
  characters in both.
- Patterns: `[🎃] Base Name` (seasonal emoji tag), `[UPD] Base Name`, `[UPDATE!] Base Name`,
  `Base Name 🔦` (permanent brand emoji), `[X50] Base Name | Event`.
- The **base name stays fixed** and only the tag rotates, which fits Roblox's "keep the name
  consistent" rule.
- Roblox has no published rule on bracket tags like "[UPDATE]" (unverified). Its description
  guide shows update tags like "🏴‍☠️ [NEW] Quest Expansion!" inside the description's
  Recent Updates block (official).

**Rules for agents (inferred):**
- Base name: 2–4 words, ≤25 chars. Say what you do or what you get ("Grow a Garden",
  "Fish It!", "Tower Defense" + theme noun). Players and semantic search both read it.
- Optional tag at the front: one emoji or a short word (`[UPD]`, `[🎃]`), ≤8 chars. Change it
  only when real new content ships, and remove it when the event ends so the title doesn't
  mismatch the game.
- Never copy a breakout's exact title structure *and* art. Pick your own noun and twist; see
  [trend lifecycle](trend-lifecycle.md).

## Icon

**Official:** square, ≥512×512, sharp; expresses theme, tone or genre; unique and relevant;
avoid ambiguous corner graphics; use color and contrast to signal mood (bright and saturated
for fantasy, muted for somber, heavy contrast for horror). Preview at small sizes because some
surfaces render ~150×150.

**Practical rules (inferred, plus community reports):**
- One focal subject (a character face or the key object) filling most of the frame. A wide
  scenic shot turns to mush at 150 px.
- Zero to two words of text. Text inside an icon must be legible at 64 px or it is noise.
- Strong value contrast and a clean silhouette against both light and dark Roblox themes.
- Match the thumbnail's art style and colors so the brand reads the same across surfaces.
- No Robux symbols, fake UI badges ("NEW!", "FREE"), or a hit game's mascot silhouette.
- Roblox offers **no icon A/B test**. Only a DevForum feature request exists (unverified as of
  2026-10-22). To test an icon: hold thumbnails fixed, swap the icon, and compare PTR over ≥7
  days each, to cover the Saturday peak and weekly cycle.

## Thumbnails

**Official best practices:**
- 16:9 at 1920×1080. Other ratios get stretched.
- Unique, relevant imagery of what players will actually do. Ambiguous graphics confuse.
- Theme and color signal genre (comedic and bright vs. dark and stormy).
- **Keep essential text and elements off the bottom edge.** Player counts and other metadata
  overlay it.
- Thumbnails used for personalization must all accurately reflect the game.

**Thumbnail personalization (Roblox's A/B tool) (official):**
- Setup: Creator Hub → place → **Thumbnails → Home Page** tab → *Edit active thumbnails* →
  activate **2–5** → Save → Start.
- Each thumbnail is shown to random users. Roblox measures **qualified play-through rate**
  per user group, then gives each group's winner more impressions while keeping minimal traffic
  on the others.
- In testing, average qualified PTR rose **+8.5%** and some games gained **+50%** (official,
  undated).
- The Thumbnail Performance table fills in after a few hours: Impressions, Qualified Plays,
  Average Playtime (per qualified play), Qualified PTR, Winning Segment.
- **Keep several active** instead of picking one winner. Test a new set with each major update,
  then leave it alone until the next.
- 2026-06-15: Roblox said it will test switching personalization from QPTR to PTR (official).
  Open Cloud thumbnail metrics keep only **30 days** of data (official).

**What to test (inferred):**
- Make each variant a *different hook* (the collection, the PvP moment, the base you build, the
  boss) rather than small color tweaks. Personalization picks a winner per audience segment, so
  distinct hooks let different segments find their thumbnail.
- Show a character mid-action doing the core verb, with readable scale and stakes.
- Text: at most 3–4 large words, upper half only.
- Depict real content. A thumbnail that over-promises raises PTR but raises 0–60 s bounce too,
  and bounce is also a top signal.
- Use ad campaigns (10 evenly served creatives) to pre-test concepts with paid traffic before
  adding them to personalization.

## Video

Authentic gameplay video appears first on the detail page and can appear on Home (official).
- **Allowed:** varied camera angles (Studio freecam: **Shift+P** in a solo playtest), minor
  brightness and contrast edits, your logo, highlight-reel cuts of real gameplay, in-game UI
  text, Roblox catalog music (official).
- **Rejected (and counted against the 3/month quota):** mechanics or UI not in the game; a
  wrong theme (horror must show horror); graphics beyond what players see; real-life footage;
  voice-over, narration, voice chat or music with lyrics; promotional text or claims like
  "50% off" or "Free UGC!" (official).
- Overlay text only to explain gameplay context, e.g. "Collect coins to boost jumps" (official).

## Description

Roblox's description guide is labeled *experimental* and aimed at select creators (official),
but its structure is sound:

1. **Hook (≤160 chars):** title, genre, the most unique feature and the main objective, using
   the words players search for. Example: *"X is a fast-paced tower defense game… survive all
   500 levels?"*
2. **Recent updates (optional, short):** one or two lines (`[NEW] …`). Keep it short so it
   doesn't push the main content down.
3. **Main content:** the core loop and selling points as emoji bullets or a short paragraph.
4. **Additional info:** devices, current codes ([codes](../patterns/codes.md)), optional
   Premium perks, a 1–3 question FAQ, and a changelog link.

Rules (official):
- Summarize the game in the first sentence. Include the relevant keywords naturally.
- No keyword stuffing; no lists of other games' names. Spam can demote the game.
- **No tags or hashtags.** They're unused by ranking and waste characters.
- Don't list controls; teach them in-game.
- Keep everything appropriate for all ages.
- No external URLs. Off-platform links are allowed only through Social Links (Community
  Standards).
- Describing a game as a hangout in the title or description gets it **classified as a social
  hangout**, which limits it to 16+ (official, maturity questionnaire).

## Genre

Pick the genre by the **primary loop**, and add a subgenre if one fits. Genres feed the
"Trending in {genre}" charts. A change shows on the detail page at once but can take days to
reach Charts. Roblox reviews genres, may change them, and allows one appeal (official).
Changing genre doesn't change RFY signals (official). Mappings for vault genres (inferred,
using Roblox's official list):

| Vault genre | Roblox genre / subgenre |
|---|---|
| [tycoon](../genres/tycoon.md), [steal-a-x](../genres/steal-a-x.md) | Simulation / Tycoon |
| [simulator](../genres/simulator.md), [plus-one-stat](../genres/plus-one-stat.md), [fishing](../genres/fishing.md) | Simulation / Incremental Simulator |
| [idle-incremental](../genres/idle-incremental.md) | Simulation / Idle |
| [obby-classic](../genres/obby-classic.md) / [obby-tower](../genres/obby-tower.md) | Obby & Platformer / Classic Obby or Tower Obby |
| [obby-escape](../genres/obby-escape.md), escape horror | Survival / Escape |
| [asymmetric-survival](../genres/asymmetric-survival.md), [social-deduction](../genres/social-deduction.md) | Survival / 1 vs All |
| [tower-defense](../genres/tower-defense.md) | Strategy / Tower Defense |
| [battlegrounds](../genres/battlegrounds.md) | Action / Battlegrounds & Fighting |
| [anime-rpg](../genres/anime-rpg.md) | RPG / Action RPG |
| [shooter](../genres/shooter.md) | Shooter / Deathmatch, Battle Royale or PvE |
| [roleplay-life-sim](../genres/roleplay-life-sim.md) | Roleplay & Avatar Sim / Life |
| [fashion-avatar](../genres/fashion-avatar.md) | Roleplay & Avatar Sim / Dress Up |
| [party-minigames](../genres/party-minigames.md) | Party & Casual / Minigame or Childhood Game |
| [story-games](../genres/story-games.md) | Adventure / Story |

Roblox has no "Horror" genre. Chase horror usually sits in Survival (Escape or 1 vs All). The
tracker shows DOORS and Dandy's World as Survival / Escape (data, 2026-10-22).

## Localization of metadata

- Creator Hub → Localization: translate the **name and description** manually, or enable
  automatic translation per language ("Experience Information" = name + description) (official).
- **Icons and thumbnails can also be localized** per language, up to 10 thumbnails per game
  (official).
- Automatic translation quotas count per character per language (official).
- Choose languages from **Analytics → Demographics → Top Languages** (official). Localized names
  also help multilingual semantic search (inferred).

## Maturity & Compliance questionnaire

Creator Hub → **Publish settings → Content rating** (official, 2026-10).

| Outcome | Who can play |
|---|---|
| No questionnaire | Playability restricted for all players |
| Only Q1 answered "No age-restricted content" → **Content May Vary** | Age-checked 16+ only |
| **Minimal / Mild** | Eligible for Roblox Kids (5–8) and Select (9–15), plus everyone above |
| **Moderate** | Select (9–15) and 16+ |
| **Restricted** | Age-verified 18+; unplayable in some countries (e.g. Korea, Saudi Arabia, Türkiye) |

Answer for the **most extreme** content a player can reach (official):
- Any single moment of realistic violence consequence → Moderate or higher.
- A small part with repeated violence or fear → "Repeated".
- Any realistic blood → at least "Light".
- Strong language, romantic themes (including in the **title**), alcohol, or a social hangout
  with private spaces → 18+.
- Social hangouts and **free-form user creation** (freehand drawing, pixel canvases, even
  per-round drawings others can see) → 16+.
- **Paid random items** and **paid item trading** must be disclosed. Respect
  `PolicyService:GetPolicyInfoForPlayerAsync` fields `ArePaidRandomItemsRestricted` and
  `IsPaidItemTradingAllowed`.
- Also asked about: unplayable gambling depictions, sensitive-issue themes, in-game media
  sharing, and generative-AI interaction.
- Retake it whenever an update changes an answer. Inaccurate answers lead to the label being
  replaced or removed, and repeat offenses to account moderation (official).

Design implications (inferred): for under-16 reach, keep blood unrealistic (non-red or
stylized), defeat effects non-graphic, fear "mild", and avoid freehand drawing and "hangout"
wording. Uploaded assets are moderated separately, whatever the label (official).

**Release requirements:** 16+ needs a ≥2-day-old account in good standing plus an age check.
All ages also needs ID verification (18+), 2FA, Plus/Premium for 2 months or a 1,000 Robux
refundable fee, a full questionnaire with Minimal/Mild/Moderate, and an evaluation pass
(250 unique plays by highly engaged age-checked users in 60 days; lowered from 500 on
2026-08-19, official). Max 5 never-released games released per day
(official). Details in [discovery](discovery-algorithm.md#audience-gating-kids-and-select) and
[audience](audience.md).

## What Roblox penalizes or moderates

| Behavior | Consequence |
|---|---|
| Giveaway or "free Robux" metadata | Deprioritized in recommendations (official). Third-party Robux giveaways are banned by Community Standards (official) |
| Thumbnail or title mismatched with gameplay | Not recommended; lower in search (official) |
| Title, art or place file near-identical to an existing game | Not prioritized; lower in search; ads may not spend (official) |
| Keyword or emoji spam | Possible demotion (official) |
| "Roblox"/"Blox" in title | Not permitted (official, since 2022-06-22) |
| Confusingly similar to another creator's work | Community Standards violation (official) |
| Copyright/trademark infringement | Takedown; repeat infringers suspended or terminated (official) |
| External URLs in metadata | Prohibited except Social Links (official) |
| Misleading video (fake gameplay, ad claims, voice-over) | Rejected; counts against quota (official) |
| Inaccurate maturity answers | Label changed or removed; repeat → account moderation (official) |

## Pre-publish checklist

- [ ] Title: stable base name ≤25 chars containing a genre noun or core verb; ≤1 tag; ≤2 emoji;
      no Robux/free/giveaway words; no "Roblox"/"Blox"; not a near-copy of a trending title.
- [ ] Icon: 512×512 original art; readable at 150 px and 64 px; one focal subject; ≤2 words.
- [ ] Home thumbnails: 2–5 distinct hooks, 1920×1080, <3 MB, real gameplay, nothing important
      along the bottom; personalization started.
- [ ] Detail page: 3+ images and one authentic gameplay video (no voice, no claims).
- [ ] Description: ≤160-char hook + updates + loop bullets + devices/codes; no hashtags,
      URLs or control lists; ≤1,000 chars.
- [ ] Genre and subgenre match the primary loop (3-month lock).
- [ ] Full maturity questionnaire answered for the most extreme content; PolicyService checks
      in place if there are paid random items or trading.
- [ ] Name, description and (optionally) icon/thumbnails localized for the top 3–5 languages.
- [ ] Social links set (shown to 16+ only).
- [ ] Look at the tile at phone size next to 10 real Charts tiles: is it distinct and clear?

## Checklist for agents

### Do
- Make metadata a truthful promise the first 60 seconds keep.
- Keep the base title stable; rotate only a short front tag for real updates and events.
- Run thumbnail personalization with 2–5 distinct hooks and refresh the set each major update.
- Write the description hook as genre + unique feature + goal, in the words players type.
- Answer the maturity questionnaire conservatively and redo it after content changes.

### Don't
- Don't use Robux, "free", UGC giveaways, fake UI badges or "#1" claims in any metadata.
- Don't ship the default icon or thumbnail.
- Don't clone a hit's name structure plus art plus template place.
- Don't add hashtags, keyword lists, external links or control instructions to descriptions.
- Don't call the game a "hangout" unless it is one (16+ only).
- Don't upload videos with narration, music with lyrics, or effects beyond real gameplay.

## Related

- [discovery-algorithm.md](discovery-algorithm.md) · [first-time-experience.md](first-time-experience.md)
- [analytics.md](analytics.md) · [trend-lifecycle.md](trend-lifecycle.md) · [audience.md](audience.md)
- [visual-quality.md](visual-quality.md) · [codes](../patterns/codes.md) · the trends report (`private/trends/latest.md`)

## Sources

1. https://create.roblox.com/docs/production/publishing/thumbnails — sizes, formats, 10 slots, video rules, personalization, +8.5%
2. https://create.roblox.com/docs/production/publishing/experience-icons — 512×512, 150×150 preview, icon best practices
3. https://create.roblox.com/docs/production/publishing/descriptions — description structure, 160-char hook, 1,000 chars, no hashtags
4. https://create.roblox.com/docs/production/publishing/publish-games-and-places — naming/emoji/spam rules, release requirements, 5 releases/day
5. https://create.roblox.com/docs/production/publishing/experience-genres — genre list, 3-month change limit, Roblox corrections
6. https://create.roblox.com/docs/production/promotion/content-maturity — labels, questionnaire categories, moderation
7. https://create.roblox.com/docs/production/publishing/kids-and-select — Kids/Select gates, evaluation threshold
8. https://devforum.roblox.com/t/roblox-kids-and-select-global-launch-upcoming-updates-to-eligibility-ads-manager-and-expedited-review/4685717 — 2026-06 launch, social links 16+, 500 HEP figure
9. https://create.roblox.com/docs/discovery — custom thumbnail requirement, penalties
10. https://create.roblox.com/docs/discovery-faq — reusing thumbnails, similarity guidance
11. https://devforum.roblox.com/t/recommended-for-you-algorithm-improvements-that-better-value-long-term-retention/4684575 — personalization to test PTR
12. https://devforum.roblox.com/t/improving-user-experience-by-reducing-exposure-of-low-quality-content/3299107 — clone/giveaway/mismatch enforcement (2024-12)
13. https://en.help.roblox.com/hc/en-us/articles/115001708126 — "Roblox"/"Blox" banned in titles since 2022-06-22
14. https://about.roblox.com/community-standards — misleading/duplicative metadata, off-platform links, Robux giveaways, IP
15. https://create.roblox.com/docs/production/publishing/ip-guidelines — IP takedowns and repeat infringers
16. https://create.roblox.com/docs/production/localization/add-translations — localizing name, description, icon, thumbnails
17. https://create.roblox.com/docs/production/localization/automatic-translations — Experience Information auto-translation, quotas
18. https://create.roblox.com/docs/production/analytics/demographics — top languages
19. https://create.roblox.com/docs/production/promotion/ads-manager — 10 creatives per campaign
20. https://create.roblox.com/docs/production/promotion/experience-events — 5 event thumbnails
21. https://create.roblox.com/docs/cloud/guides/analytics/metrics — thumbnail metrics, 30-day retention
22. https://devforum.roblox.com/t/icon-ab-testing/3274267 — icon A/B testing is only a feature request
23. https://devforum.roblox.com/t/we-need-more-information-on-why-place-name-or-description-is-inappropriate/353001 — text filter blocking title/description saves
24. https://apis.roblox.com/explore-api/v1/get-sorts — title sample (brackets/emoji/length), read 2026-10-22
