---
title: Audience
type: fundamental
read-when: Choosing target players, devices, languages, or pricing.
last-researched: 2026-10-22
---

# Audience

## In one line

Roblox has about 123M daily players. Most play on phones, most live outside the US, and about
73% of age-checked players are under 18. Since 2026, age checks decide who can chat and which games
a player can even see, so the game's content label and social design now limit its reach.

## Size and trend

| Metric | Value | Tag |
|---|---|---|
| Average DAUs, Q2 2026 | 123M, +10% YoY | (official, 2026-07) |
| DAU path | 151.5M (Q3 2025 peak) → 144M (Q4 2025) → 132M (Q1 2026) → 123M (Q2 2026) | (official Q3 2025; press for the rest, 2026-08) |
| Hours engaged, Q2 2026 | 29B, +5% YoY (peak 40B in Q3 2025) | (official / press, 2026-08) |
| Full-year 2025 | 127M avg DAUs in 180+ countries; 123.9B hours; **2.7 h per DAU per day** | (official, 10-K FY2025) |
| Games per player | 24+ unique experiences per user per month in 2025 | (official, Q4 2025 letter) |
| Payers, Q2 2026 | 27M average monthly unique payers, +15% YoY; bookings $1,557M | (official, 2026-07) |
| Bookings per payer | about $19 per payer per month | (inferred: $1,557M ÷ 3 months ÷ 27M) |

- Q3 2026 results were not out as of 2026-10-22. Roblox guided to a *sequential* DAU increase for
  Q3 2026 and bookings down 14–18% YoY (official, 2026-07).
- Roblox said the DAU decline over three quarters is mostly seasonal (press, 2026-08). The
  age-check rollout cost a "mid-single-digit" share of engagement growth, mostly from less-engaged
  users (official, Q4 2025 letter).
- Russia's return in June 2026 added about 3 points to YoY DAU growth (official, 2026-07).
- Players hop between many games (2.7 h per day spread across 24+ games a month). Your game is one
  stop among many. Design for repeat visits, not all-day play (inferred). See
  [retention](retention.md).

## Ages

Roblox switched from self-reported to **age-checked** data in 2026. Age-checked data shows a
younger user base than self-reported data did (official, Q4 2025 letter).

| Age-checked DAUs (global) | Share | Tag |
|---|---|---|
| Under 13 | 35% | (official, 7 days to 2026-06-30) |
| 13–17 | 38% | (official, 2026-06) |
| 18+ | 27% (about one-third in the US) | (official, 2026-06) |

- The same 35/38/27 mix was reported for January 2026 (official, 2026-01).
- Coverage: 57% of global DAUs had age-checked by the end of Q2 2026, with the US and Australia
  above 70%. Among under-18s it was 60% globally and 75% in the US (official, 2026-06).
- Older self-reported data said about two-thirds of DAUs were 13+ (press, Q3 2025 earnings call).
  Don't mix that series with the age-checked one (official caveat).
- Adults are the fastest-growing group: US 18+ DAUs +32% YoY and US ages 18–34 +42% (official,
  Q2 2026). Roblox reaches fewer than 10% of US adults aged 18–34 daily. It is pushing "Novel" games
  (shooters, RPGs, sports and racing) to grow this group (official, Q4 2025 letter).
- **Design default (inferred):** the core audience is 9–17. Make it readable for a 9-year-old,
  but don't look babyish to a 15-year-old. A 16+ / 18+ game is a real, growing niche, but it gives
  up Kids/Select reach.

## Devices

- **2024 average DAUs: 80% mobile, 17% PC, 3% console** (official annual report, via press
  2025-04). The FY2025 10-K shows its device split only as a chart image we couldn't extract, so
  2024 is the latest confirmed split (inferred).
- Clients as of 2025-12-31: iOS, Android, Windows, Mac, Xbox, PlayStation, Chromebook and
  "select" VR (official, 10-K FY2025).
- Revenue: 29% of 2025 revenue came through the Apple App Store and 15% through Google Play
  (official, 10-K FY2025).
- Many players use more than one device. Newzoo: only 24% of players aged 10–65 play *only* on
  mobile (press, 2025). GameAnalytics' 2025 dataset: PC+mobile 48%, PC-only 38%, mobile-only
  7–10%, console about 2% of players (press, 2025). That dataset over-represents PC-heavy games
  (inferred).
- PlayStation is about 3% of platform playtime, 374M hours in Q2 2025 (press, Newzoo).
- VR: no reliable current share found (unverified). Treat it as a rounding error and don't build
  VR-only features (inferred).
- **Design default (inferred):** design and test on a phone first, with PC keyboard/mouse
  second and gamepad third. Save state on the server so players can switch devices mid-week. See
  [performance and devices](performance-and-devices.md).

## Regions

| Region, Q2 2026 | DAUs | YoY DAU growth | Tag |
|---|---|---|---|
| APAC | 41M | +15% | (press for size, 2026-08; official for growth) |
| Rest of world | 34M | +15% | (same) |
| Europe | 26M | +1% | (same) |
| US & Canada | 22M | +6% | (same) |

- Fastest growth: Japan +67% and India +64% DAUs YoY (official, Q2 2026).
- Money is concentrated where players aren't. North America was about $846M of revenue, over half
  of the global total (press, 2026-08). Payers outside the US and Canada grew 23% (official,
  Q2 2026).
- **Design default (inferred):** about 80% of DAUs are outside the US and Canada. Localize UI text
  from day one, avoid US-only cultural references in core mechanics, and let
  [regional pricing](#pricing) handle purchasing power.

## Languages and automatic translation

- **Automatic translation** of game text covers **18 languages**: Arabic, Chinese (Simplified and
  Traditional), English, French, German, Hindi, Indonesian, Italian, Japanese, Korean, Polish,
  Portuguese, Russian, Spanish, Thai, Turkish and Vietnamese (official, 2026-10). The FY2025 10-K
  listed 17 without Hindi, so Hindi looks new for 2026 (inferred).
- How it works: Automatic Text Capture (ATC) collects strings from text objects with
  `AutoLocalize` on, then fills only *blank* entries in your localization table. Manual
  translations win. New strings can take "up to a few days" via ATC (official, 2026-10).
- **Not captured:** text baked into images, `TextBox.Text` (only `PlaceholderText`), player-owned
  item names, and badge/pass names pulled from the platform (official, 2026-10). Strings built in
  scripts need `LocalizationService:GetTranslatorForPlayerAsync` and keyed entries (inferred from
  the docs' "localization scripts" note).
- Translation quota is per character per language: "hello" into 10 languages uses 50 characters
  (official, 2026-10).
- Text chat is auto-translated between 17 languages, and real-time voice chat translation is
  planned (official, Q4 2025 letter).
- **Rules:** never put words in images. Never concatenate translated fragments; use one keyed
  string with parameters. Leave about 30% extra width for longer languages such as German and
  Russian (inferred).

## Safety: age checks, chat and social features (2025–2026)

- **Chat requires an age check**, worldwide since early January 2026. Australia, New Zealand and
  the Netherlands started in early December 2025. Checks are mostly facial age estimation; ID and
  parent-provided age are alternatives (official, 2026-01).
- **Age bands:** under 9, 9–12, 13–15, 16–17, 18–20, 21+. By default, players chat with their own
  band and the bands directly above and below. Chat is off for under-9s unless a parent consents.
  Age-checked 13+ users can add **Trusted Friends** to chat across bands (official, 2026-01).
  Roblox renamed "Connections" back to "Friends" in April 2026 (official, 2026-04).
- **Players who haven't age-checked can't chat.** Messages between players who can't chat are
  hidden from each other. `TextChannel:DisplaySystemMessage` reaches everyone. All player text chat
  must go through `TextChatService` (official, 2026-01).
- Matchmaking includes a Text Chat signal. Custom Matchmaking can raise its weight when chat is
  core to the game (official, 2026-01). Roblox also groups servers by age and skill (official,
  Q4 2025 letter).
- **Global Chat** (cross-server chat inside one game, grouped by age, language and occupancy) is on
  by default and can be turned off in the Creator Dashboard (official docs; launched 2026-05 per
  press). It averaged 30M messages a day in June 2026 (official, 2026-07).
- **Quick Words** preset phrases, with creator-submitted lists reviewed by Roblox, were announced
  at RDC 2026 (press, 2026-09). Configuration details are unverified.
- Overall chat on the platform is still below pre-age-check levels (official, 2026-07).
- Voice chat: age-checked 13+, in 50+ countries (official, 10-K FY2025).
- Social links on game pages, communities and profiles are visible only to age-checked 13+ users,
  from 2026-02-23. Team Create needs an age check from March 2026 (official, 2026-01).
- **APIs:** `Player.AgeChecked` (`Enum.AgeCheckStatus.Unchecked` / `Checked`) and
  `Player:PromptAgeCheck()` exist (official, 2026-10). No API exposes a player's age band;
  developers have asked for one (community, 2026).
- **Moments** clips and the new Home tab are for age-checked 16+ users (official, 2026-07).
- **Design default (inferred):** assume a large share of any server can't talk to each other.
  Social features must work silently: emotes, pings, trades, gifting, co-op goals, and
  system messages for big moments.

## Account tiers and content maturity

| Account | Ages | Can play | Chat default | Tag |
|---|---|---|---|---|
| Roblox Kids | 5–8 | Minimal, Mild (that passed evaluation) | Off; a linked parent can enable it after an age check | (official, 2026-10) |
| Roblox Select | 9–15 | Minimal, Mild, Moderate (that passed evaluation) | Off until age-checked, then phased in | (official, 2026-10) |
| Roblox | 16+ age-checked | All rated games except Restricted | On where available | (official, 2026-10) |
| Restricted access | 18+ age-*verified* (ID) | Restricted | n/a | (official, 2026-10) |

- Kids and Select launched globally on **2026-06-16** after a 2026-05-19 start in NZ, the
  Netherlands, Australia and Indonesia (official, 2026-06). Users who haven't checked their age get
  the most limited catalog and no chat (official, 2026-04).
- The catalog for these accounts was about 30,000 games, up nearly 50% since launch (official,
  2026-07). Roblox says it covers "the vast majority" of playtime (official, 2026-06).
- **Labels:** Minimal and Mild reach Kids and Select. Moderate reaches Select and 16+. "Content May
  Vary" (questionnaire not completed) reaches only age-checked 16+. Restricted reaches only
  age-verified 18+ (official, 2026-10).
- **Unrated games are restricted for all players.** Always complete the Maturity & Compliance
  Questionnaire, and update it whenever content changes (official, 2026-10).
- What the labels allow (official, 2026-10):
  - Minimal: occasional mild violence, light unrealistic blood.
  - Mild: repeated mild violence, heavy unrealistic blood, mild fear, mild crude humor.
  - Moderate: moderate violence, light realistic blood, moderate fear, moderate crude humor,
    *unplayable* gambling.
  - Restricted: strong violence, heavy realistic blood, romance, alcohol, strong language.
  - Playable or simulated gambling is never allowed.
- **Social hangouts are 16+**, or 18+ with private spaces. Free-form user creation (shared drawing
  or writing) is 16+. All three are excluded from Kids and Select by default (official, 2026-10).
  An older Roblox guidelines page still says 13+. The content-maturity page is newer, so follow 16+.
- **Reaching under-16s (Kids/Select) requires all of these** (official, 2026-10):
  creator ID-verified (facial estimation under 18, government ID 18+), 2-Step Verification on,
  questionnaire rating Minimal/Mild/Moderate, a refundable per-game fee or a Plus/Premium
  subscription at least 2 months old, and an evaluation of **250 plays by highly engaged
  age-checked players in 60 days**. The threshold dropped from 500 on 2026-08-19. The bar to *keep*
  eligibility dropped from 100 to 25 on 2026-07-16 (official, 2026-08). The fee was 1,000 Robux at
  launch (official, 2026-06).
- New all-ages games start in a **trial phase visible only to age-checked 16+** until they pass.
  Progress shows on the Audience Reach tab (official, 2026-10).
- Expedited review is a refundable **50,000 Robux** per game per current docs (official, 2026-10);
  it was 100,000 at launch (official, 2026-06).
- Restricted games can't be played in some countries, such as Korea, Saudi Arabia and Türkiye
  (official, 2026-10). Roblox planned to adopt IARC ratings (ESRB, PEGI) "later" in 2026
  (official, 2026-04). We couldn't confirm it is live (unverified).
- **Paid random items** (eggs, crates) are blocked for some players by region or age. Check
  `PolicyService:GetPolicyInfoForPlayerAsync(player).ArePaidRandomItemsRestricted` and offer a
  direct-purchase path instead (official, 2026-10). See
  [rarity tiers and eggs](../patterns/rarity-tiers-and-eggs.md).

## Parental controls and spending

- Parents link to a child's account and manage **all** settings through age 12, and game
  management plus direct chat through 15. They see friends, screen time and spending through 18
  (official, 2026-10).
- **Monthly spending limit:** covers Robux and subscriptions, resets each calendar month, and
  doesn't apply to gift cards (official, 2026-10).
- **Spend alerts** to parents at $100, $250 and $500 in a month, then every 10 transactions (on by
  default) (official, 2026-10).
- **Daily screen-time limits** for all Kids users and Select users aged 9–12. When hit, Roblox is
  unavailable for the rest of the day (official, 2026-10).
- Parents can block games, approve specific games ("Approved Experiences"), and control private
  server access (official, 2026-10).
- Laws in Texas, Utah and Louisiana require parental consent for minors' purchases or for app-store
  in-app purchases (official, 10-K FY2025).
- **Design default (inferred):** a purchase prompt can fail or be blocked for many minors.
  Never lock progress waiting on a purchase. Grant only in `MarketplaceService.ProcessReceipt`, and
  give free players a real path. See [monetization](monetization.md).

## Implications for what we build

### Controls

- Tap-first. Every core action must work with one thumb tap and the default thumbstick (inferred;
  80% of DAUs were on mobile in 2024, official).
- Add keyboard and gamepad bindings for every action. The Input Action System supports all three
  per action (official, 2026-10). Show hints based on `UserInputService.PreferredInput` (official,
  2026-10).
- No precision aiming, multi-touch gestures or hold-and-drag in the first session (inferred).

### Text

- Write for a 9-year-old reader: 3–8 word labels, icons next to words, and numbers over prose
  (inferred).
- Keep all text in `TextLabel`/`TextButton` objects that ATC can capture. Never put words in
  images (official capture rules, 2026-10).
- Never rely on chat for instructions. Many players can't chat (official, 2026-01).

### UI size

- Phone-first layouts using `Scale` sizing with `UISizeConstraint` caps for PC. Keep interactive
  UI inside `ScreenInsets = CoreUISafeInsets`, and keep the bottom corners clear for the default
  controls (official, 2026-10). Exact sizes: [ui-ux](ui-ux.md).

### Pricing

- Regional pricing is **on by default for game passes**. It is opt-in per developer product
  ("Enable Managed Pricing") and fixed on for Robux subscriptions. Regional prices are never above
  your default and never more than 70% below it (official, 2026-10).
- **Never hard-code prices in UI.** Read them with `MarketplaceService:GetProductInfoAsync` or
  `MarketplaceService:GetDeveloperProductsAsync`, and test with the Dynamic Price Check tool
  (official, 2026-10).
- Roblox reported regional pricing on passes raised paying users by 22.4% in Brazil, 44.8% in the
  Philippines and 13.8% in Mexico (official, 2025). Price ladders: [monetization](monetization.md).

### Themes

- For the widest reach, target **Mild** (reaches Kids, Select and 16+). **Moderate** gives up
  ages 5–8. Restricted gives up everyone under 18 and some countries (inferred from the official
  label rules, 2026-10).
- Avoid making "hang out and chat" the main activity unless you accept a 16+ audience (official
  rules, 2026-10).
- Themes that work for 9–17: collecting, building, creatures, light horror (Mild/Moderate fear),
  sports, anime-styled combat without realistic blood (inferred). Check current demand in
  the trends report (`private/trends/latest.md`).

### Session times

- Platform median daily playtime per user *per game* is 16.8 min; p75 is 34.6 min (press,
  GameAnalytics 2025). Players spend 2.7 h a day across Roblox (official, FY2025).
- Build complete loops that fit in 5–15 minutes, aim for a 15–25 min average session, and
  expect abrupt exits from screen-time limits and app switching (inferred). See
  [retention](retention.md) and [first-time experience](first-time-experience.md).

## Checklist for agents

### Do

- Complete the Maturity & Compliance Questionnaire before publishing, and re-answer it when
  content changes.
- Pick the target label on purpose (default Mild) and keep violence, blood and fear within it.
- Plan for the 16+ trial phase. The first players are age-checked 16+, and reaching under-16s needs
  250 highly engaged plays in 60 days.
- Design for phones first, then test keyboard/mouse and gamepad.
- Put all player-facing text in capturable text objects and enable automatic translation.
- Read prices at runtime with `GetProductInfoAsync` / `GetDeveloperProductsAsync`.
- Gate paid random items on `ArePaidRandomItemsRestricted`.
- Route chat through `TextChatService`. Use `TextChannel:DisplaySystemMessage` for key
  announcements.
- Make social play work without chat: emotes, pings, gifting, shared goals.

### Don't

- Don't publish unrated, or with an inaccurate questionnaire.
- Don't build a social hangout, free-draw board or romance content into an all-ages game.
- Don't hard-code Robux prices in UI text or images.
- Don't put text in images or build sentences by joining translated fragments.
- Don't assume players can chat, are over 13, or can complete a purchase.
- Don't design PC-only controls or tiny UI that needs a mouse.
- Don't cite self-reported age splits (pre-2026) as current.

## Related

- [Discovery algorithm](discovery-algorithm.md): who gets recommended your game.
- [First-time experience](first-time-experience.md): mobile-first first minute, 16+ trial.
- [Retention](retention.md): session length and return hooks for this audience.
- [Monetization](monetization.md): pricing, regional prices and receipts.
- [UI/UX](ui-ux.md), [performance and devices](performance-and-devices.md),
  [social and virality](social-and-virality.md).

## Sources

1. https://www.sec.gov/Archives/edgar/data/0001315098/000162828026051059/ex991-robloxq22026earnin.htm: Q2 2026 shareholder letter (DAUs, age-checked mix, Japan/India, Kids/Select, Global Chat, guidance).
2. https://s27.q4cdn.com/984876518/files/doc_financials/2026/q2/Roblox-Q2-2026-Supplemental-Materials.pdf: DAU growth by region, Q2 2026.
3. https://www.pocketgamer.biz/roblox-revenue-rises-36-yy-but-young-north-americans-see-falling-per-hour-monetisation/: regional DAU sizes, DAU path, North America revenue (2026-08).
4. https://www.shacknews.com/article/150208/roblox-daus-grew-10-percent-yoy: DAU path and hours peak.
5. https://s27.q4cdn.com/984876518/files/doc_financials/2025/q4/Q4-2025-Shareholder-Letter.pdf: age-checked data, 18–34 reach, 24+ games per month, chat translation, age-check headwind.
6. https://www.sec.gov/Archives/edgar/data/1315098/000131509826000024/rblx-20251231.htm: FY2025 10-K (127M DAUs, 2.7 h/DAU/day, clients, app-store revenue shares, parental-consent laws, voice chat).
7. https://gamesbeat.com/?p=309290: Q3 2025 151.5M DAUs and 13+ share.
8. https://www.pocketgamer.biz/80-of-roblox-users-are-on-mobile-contributing-46-of-robux-revenue/: 2024 device split 80/17/3.
9. https://gamedevreports.substack.com/p/newzoo-roblox-as-a-platform-in-2025: Newzoo multi-device and PlayStation playtime.
10. https://www.gameanalytics.com/reports/2025-roblox-report: device mix of players, playtime percentiles.
11. https://create.roblox.com/docs/production/localization/automatic-translations.md: 18 languages, ATC rules, quotas.
12. https://about.roblox.com/newsroom/2026/01/roblox-age-checks-required-to-chat: global age checks for chat, age bands.
13. https://devforum.roblox.com/t/age-check-requirement-to-chat-now-live-globally/4226101: creator implications (TextChatService, system messages, matchmaking, social links, Team Create).
14. https://about.roblox.com/newsroom/2026/04/expanding-trusted-friends: Connections renamed back to Friends / Trusted Friends.
15. https://create.roblox.com/docs/reference/engine/enums/AgeCheckStatus.md: Player.AgeChecked and PromptAgeCheck.
16. https://devforum.roblox.com/t/add-a-method-to-fetch-a-players-age-group-with-the-new-age-check-update/4113963: no age-band API (community request).
17. https://create.roblox.com/docs/chat/cross-server-chat: Global/cross-server chat grouping and toggle.
18. https://gamesbeat.com/roblox-is-adding-emojis-custom-quick-words-and-voice-calling-to-its-in-game-chat-rdc-2026/: Quick Words, RDC 2026.
19. https://about.roblox.com/newsroom/2026/07/moments-new-homepage-unlocks-gaming-for-all: Moments 16+, new Home tabs.
20. https://about.roblox.com/newsroom/2026/04/introducing-roblox-kids-and-select-accounts: Kids/Select announcement, IARC plan.
21. https://create.roblox.com/docs/production/publishing/kids-and-select: tiers, publishing requirements, trial phase, expedited review.
22. https://devforum.roblox.com/t/roblox-kids-and-select-global-launch-upcoming-updates-to-eligibility-ads-manager-and-expedited-review/4685717: global launch 2026-06-16, fee, original thresholds.
23. https://devforum.roblox.com/t/highly-engaged-player-threshold-drops-to-250/4820164: 250 threshold, 25 maintenance bar.
24. https://create.roblox.com/docs/production/promotion/content-maturity: labels, descriptors, hangout/free-form ages, regional restrictions.
25. https://create.roblox.com/docs/production/promotion/experience-guidelines.md: older page still listing hangouts as 13+; gambling rules.
26. https://about.roblox.com/parental-controls: parental controls, spending limits, alerts, screen time.
27. https://create.roblox.com/docs/production/monetization/regional-pricing.md: regional pricing defaults, 70% floor, price APIs, Dynamic Price Check.
28. https://devforum.roblox.com/t/introducing-regional-pricing-for-developer-products/3971235: regional pricing results (Brazil, Philippines, Mexico).
29. https://create.roblox.com/docs/reference/engine/classes/PolicyService.md: ArePaidRandomItemsRestricted and other policy fields.
