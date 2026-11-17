---
title: Social and virality
type: fundamental
read-when: Designing co-play, invites, private servers, or clip-worthy moments.
last-researched: 2026-10-22
---

# Social and virality

## In one line

Give players a reason to come back *with friends*, make bringing them a one-tap action that
rewards both sides, and build moments worth clipping. Do it all with Roblox's own invite,
party, share and capture APIs, inside its age and link rules.

## Why co-play matters (numbers)

- **It's a ranking signal.** "Intentional co-play days per user" is in the *important* tier
  of Recommended for You. It counts unique days users come back to play with friends through
  joins, invites or private servers (official, 2026-10). See
  [discovery](discovery-algorithm.md).
- **Friend sessions run longer.** Play sessions with friends averaged 1.9× the length of solo
  sessions (official, Roblox newsroom, data as of 2024-06-30).
- **Friend arrivals count differently.** Players who arrive through friends, ads, search or
  social media don't count toward RFY *ranking* signals. They do speed up a game's
  consideration for recommendations (official). Friends are the launch fuel; RFY is the engine.
- **Outside links pay.** Audience Expansion pays 35% of a new or returning user's first $100
  of platform spend when they arrive by your Share Link, direct link, or a search for your
  name (official, 2026-10; see [monetization](monetization.md)).
- **The biggest peaks were social events.** The 2025-08-23 "admin war" between Grow a Garden
  and Steal a Brainrot was hyped for a week on TikTok, X and Discord (press, Tubefilter
  2025-08-25). Roblox hit a record 47.4M concurrent users that day (press, PocketGamer.biz
  2025-10-07). Peak dates and sizes: [trend lifecycle](trend-lifecycle.md).

## Social plumbing (APIs verified against the engine reference, 2026-10)

| Need | API / feature | Notes |
|---|---|---|
| Invite friends | `SocialService:CanSendGameInviteAsync(player, recipientId?)`, then `SocialService:PromptGameInvite(player, options)` | Wrap the check in `pcall`; availability varies by platform and player (official). |
| Customize invite | `ExperienceInviteOptions`: `PromptMessage`, `InviteUser`, `InviteMessageId`, `LaunchData` | `InviteMessageId` is a notification string from Creator Dashboard > Engagement > Notifications, and must include `{experienceName}`. `LaunchData` is ≤200 characters (official). |
| Know who came from an invite | `Player:GetJoinData().ReferredByPlayerId` and `.LaunchData` | Fills in automatically for every invite type. Launch data can take a few seconds to arrive, so retry a few times (official). |
| Count invites sent | Not possible | `GameInvitePromptClosed`'s `recipientIds` is always empty now (official). Reward joins, not prompts. |
| Referral reward banner | Creator Dashboard > Engagement > Referral Rewards | One published banner at a time, and it must describe your real reward. The game must be live ≥1 day. Invites can go to non-friends, and the link never expires (official). |
| Off-platform links | Share Links (Creator Dashboard); `SocialService:PromptLinkSharingAsync(player, options)` (server only) | Per-channel campaign links with optional LaunchData and Acquisition analytics. Prompt links default to `ExpirationSeconds` 86,400 (official). |
| Parties | `Player.PartyId`, `SocialService:GetPlayersByPartyId(partyId)`, `SocialService:GetPartyAsync(partyId)` | Party: up to 6 friends join the same server and spawn together (official, 2024-12). `GetPartyAsync` returns each member's `UserId`, `PlaceId`, `JobId`, `PrivateServerId` and `ReservedServerAccessCode`, across servers (official). Test with Studio's Party Simulator. |
| Friends in game | `Player.FollowUserId`, `Player:GetFriendsOnlineAsync()`, `Player:IsFriendsWithAsync(userId)`, `TeleportService:GetPlayerPlaceInstanceAsync(userId)` | `IsFriendsWith` (no Async) is deprecated (official API). |
| Calls | `SocialService:CanSendCallInviteAsync`, `SocialService:PromptPhoneBook(player, tag)`, `SocialService.OnCallInviteInvoked` | The callback must return `PlaceId` plus a `ReservedServerAccessCode` from `TeleportService:ReserveServerAsync` (official). |
| Community | `GroupService:PromptJoinAsync(groupId)`, `Player:IsInGroupAsync(groupId)` | `Player:IsInGroup` is deprecated (official API). Groups are called "Communities" in the player UI (official, DevForum). |
| Clips and screenshots | `CaptureService:TakeScreenshotCaptureAsync`, `StartVideoCaptureAsync` / `StopVideoCapture`, `PromptShareCapture`, `PromptSaveCapturesToGallery` | Client-only. Video stops at 30 s, with voices muted. The share sheet attaches an invite link with launch data where the device supports it (official). |
| Voice | `VoiceChatService` (`EnableDefaultVoice`, `UseAudioApi`), `AudioDeviceInput`, `VoiceChatService:IsVoiceEnabledForUserIdAsync` | Details below. |
| Feedback | `SocialService:PromptFeedbackSubmissionAsync(options)` | Feedback lands in Creator Dashboard > Audience > Feedback. One submission per player per day, age-limited (official). |

Before showing any share or capture prompt, check `PolicyService` `IsContentSharingAllowed`
(official).

## Designing for co-play

**Give friends a reason to play together** (inferred unless tagged):
- Shared progress: a co-owned base or plot, a co-op boss that's hard solo, roles that need two
  people (driver/gunner, builder/defender).
- Friend-aware systems: put party members on the same team, and spawn invitees next to the
  inviter. Read `ReferredByPlayerId` and teleport near them if they're on another server
  (official example pattern).
- A small, visible friend bonus, such as +10% currency while a friend is in the server. Keep it
  modest so solo players aren't punished.
- Trading, gifting and showing off: these need an audience, so give players a shared space
  (hub, plaza, trading area). See [trading](../patterns/trading.md).
- Private servers count toward co-play days (official). Keep them cheap or free. Roblox Plus
  members get paid ones free, and Roblox pays you up to 100 Robux per active Plus member
  (official, 2026-04). See [private servers](../patterns/private-servers.md).

**When to show the invite prompt** (inferred):
- Right after a shared win or a rare drop, when a co-op feature unlocks, or after a solo
  player fails a co-op challenge.
- Never at spawn, never on a timer, and never more than once per session unless the player
  opens it.

**Invite rewards** (officially supported through the referral system):
- Reward **both** sides, and only when the invitee actually joins (check
  `ReferredByPlayerId ~= 0`). Give the invitee a one-time welcome reward.
- Store a per-invitee "already counted" flag in the inviter's save. Cap rewards per inviter
  (Roblox's example cap is 3). Add a cooldown, and watch for alt-account farming (official
  recommendations).
- Reward with cosmetics, a badge, or soft currency, never Robux. The reward should be
  meaningful but not progression-defining (inferred).

## Voice and chat constraints (2026)

- **Chat needs an age check worldwide** since 2026-01. Users are sorted into six age bands
  (<9, 9–12, 13–15, 16–17, 18–20, 21+) and by default chat only with the adjacent bands.
  Chat is off by default for under-9s, and age-checked 13+ users can add "Trusted Connections"
  (official newsroom, 2026-01).
- **Kids accounts (5–8)** have chat off by default. **Select accounts (9–15)** that haven't
  been age-checked have chat off (official, 2026-10).
- **Design consequence:** many players in any server can't talk to each other. Co-op must
  work through pings, emotes, quick-chat wheels and readable body language (inferred). Use
  `TextChatService:CanUsersChatAsync` before building chat-dependent features (official API).
- **Voice requirements:** voice is for age-verified 13+ users in supported countries. It
  needs servers of ≤100 players, and it's on by default for new games (official, 2026-10).
- **Voice routing:** voice is proximity-based by default. For team-only voice, set
  `VoiceChatService.UseAudioApi` to Enabled and use `AudioDeviceInput` access lists
  (official). Never require voice to play (inferred).
- **Party voice:** reportedly launched for phone-verified 18+ users in some countries on
  2025-03-11, with 13+ planned later (unverified; fan wiki only).

## Clip-able moments (TikTok, YouTube Shorts, Roblox Moments)

Steal a Brainrot's rise was credited to stealing and raiding producing shareable conflict
(press, via [trend lifecycle](trend-lifecycle.md)). Roblox launched **Moments**, an in-app feed
of ≤30 s gameplay clips for 13+ users, as a beta in 2025-09 (press, TechCrunch 2025-09-05). It
also promised creator APIs (official, newsroom 2025-09). A clip is now a discovery surface
inside Roblox too.

**Design rules for clip-worthy moments** (inferred, drawn from the 2025–26 hits):
1. **Readable in 2 seconds without sound.** Big shapes, big numbers, one obvious event. Assume
   a vertical 9:16 crop of a phone screen, so keep the key action centered.
2. **Visible rarity reveals.**
   - A slow build-up (shake, glow, color by tier), then a burst.
   - Show it to the whole server: a chat broadcast or banner such as "X hatched a SECRET
     (0.01%)".
   - Show the odds number on screen. It makes the clip legible, and paid items need the odds
     shown anyway ([monetization](monetization.md)).
3. **Social conflict with a comeback:** steal and chase, betray and revenge, a last-second
   save. The victim must be able to respond, or the clip turns into a complaint.
4. **Absurd scale and escalation:** numbers climbing past a million, giant pets, a base
   packed with items.
5. **Name tags and titles over heads,** so viewers can tell who did what.
6. **A "share this" moment:** after a rare event, offer a one-tap screenshot share with
   `CaptureService:TakeScreenshotCaptureAsync` and `PromptShareCapture`, which carries an
   invite link. Don't auto-record video.

**YouTuber and streamer appeal** (inferred):
- Video makers need variety per episode, challenges ("noob to max in one video"), rare finds,
  trolling friends, and spectacle on demand.
- Private servers for recording, admin-style events, and creator codes (see
  [codes](../patterns/codes.md)) make your game easier to film.
- Roblox's Video Stars program is invite-only and based on channel size, for example 100K
  subscribers for long-form (official help center, unverified current thresholds). Don't plan
  around it.

## Admin abuse and live events as social draws

- **The format:** the developer spawns rare items, weather or chaos for a fixed weekend window.
  Only players online during the window get the limited items (press, Tubefilter 2025-08-25).
- **The effect:** both games usually averaged about 1M concurrent players. Before the
  2025-08-23 "war", each had reached about 15M during admin events (press, Tubefilter).
- **The peaks:**
  - Tubefilter reports 21.1M for Grow a Garden that day (below its June 21.6M) and 20M for
    Steal a Brainrot.
  - Other outlets report 22.3M for Grow a Garden. Sources conflict, and
    [trend lifecycle](trend-lifecycle.md) uses 22.3M.
- **Why it works** (inferred): synchronized attendance fills servers, which means co-play,
  witnesses for rare drops, and clips. A known weekly slot becomes an appointment friends
  plan around.
- **Rules for a small game** (inferred; build details in
  [admin abuse](../patterns/server-events-admin-abuse.md)):
  - Fixed slot, announced with a countdown and the time in the player's local zone.
  - Rewards everyone present can get. Make them cosmetic or short-lived boosts, never
    permanent power.
  - Never sold for Robux.
- Pair it with an Experience Event (RSVP and "Notify Me") so the start time reaches players who
  are offline. See [live ops](live-ops-and-updates.md).

## Community: Discord, Communities, talking to players

- **Outside links are 16+ only.** Since 2026-06-30, Social Links (Discord, YouTube, X…) show
  only to age-checked 16+ users on profiles, game pages, groups and the Creator Store
  (official, DevForum 2026-06). Community Standards ban URLs anywhere except through Social
  Links (official). So **under-16 players can't reach your Discord from Roblox.** Don't print
  invite text in the game.
- **Use on-platform channels instead:**
  - Communities (renamed from groups; Forums replaced walls 2025-11-30, press);
  - Experience Events and update announcements (60 characters, once per 3 days);
  - Experience Notifications, opt-in and 13+ for personalized ones ([retention](retention.md)).
- **Listen in-game:** `SocialService:PromptFeedbackSubmissionAsync` after a session milestone,
  not at join (inferred). Read Creator Dashboard > Audience > Feedback weekly.
- **Talk like a person:** a short "what changed and why" note in the update log builds trust
  (inferred). Publicly own bugs that cost players progress, and restore it. See
  [live ops](live-ops-and-updates.md).

## Roblox rules on incentives and social pressure

- **Allowed:** rewards for referrals through the official system, as long as the banner is
  accurate (official).
- **Not allowed:**
  - Gating subscription benefits behind social-media posts (official). Treat any "post to
    unlock" as off-limits (inferred).
  - Gating gameplay behind enabling notifications, or using dark patterns in notifications
    (official).
  - URLs outside Social Links, or games made only to send users off Roblox (official).
  - Real-money-prize contests without Roblox's involvement (official).
- **Likes and favorites:** no engine API lets you check whether a player liked or favorited
  your game (inferred: none found in the API reference, 2026-10). A "like for a reward" promise
  can't be verified, so it's misleading. Don't make it.
- **Community join rewards:** `GroupService:PromptJoinAsync` plus `Player:IsInGroupAsync` are
  widely used. No explicit rule was found (unverified). Keep the reward small and cosmetic.
- **Social pressure on children** (inferred, reviewer rule): no shaming of non-payers or
  non-inviters. No leaderboards of "top inviters" with real-value prizes. No team penalties when
  a teammate won't spend.

## Checklist for agents

### Do
- Add at least one reason to return *with a friend* (co-op goal, shared base, friend bonus) and
  one invite entry point placed after a shared win.
- Use `CanSendGameInviteAsync` → `PromptGameInvite` with an `InviteMessageId` and
  `LaunchData`, and read `ReferredByPlayerId` to reward both sides once, on join.
- Keep parties and invitees together: same team, same spawn, teleport to the inviter.
- Design at least one clip moment: a server-wide rarity reveal, or a conflict with a
  comeback.
- Make co-op playable without chat or voice (pings, emotes, quick chat).
- Check `IsContentSharingAllowed` before share prompts.
- Create Share Links per channel (TikTok, YouTube, Discord) to see which one brings engaged
  players.

### Don't
- Reward invite *prompts* (they can't be counted) or promise rewards for likes and favorites.
- Put Discord or other URLs in game text, signs or descriptions.
- Require voice, chat, or social-media posts to progress.
- Sell admin-event items for Robux, or make event rewards permanent power.
- Auto-prompt invites on join or on a timer.

## Related

- [Discovery](discovery-algorithm.md) (co-play signal), [retention](retention.md)
  (notifications), [live ops](live-ops-and-updates.md) (events, update timing)
- [Private servers](../patterns/private-servers.md),
  [admin abuse](../patterns/server-events-admin-abuse.md), [codes](../patterns/codes.md),
  [trading](../patterns/trading.md)
- [Trend lifecycle](trend-lifecycle.md) (peak numbers), [monetization](monetization.md)
  (Audience Expansion, Plus private-server rewards)

## Sources

1. https://create.roblox.com/docs/discovery — intentional co-play days signal, friend-acquired users excluded from ranking
2. https://about.roblox.com/newsroom/2024/12/join-the-party-on-roblox — Party (6 friends), 1.9× longer friend sessions, chat 13+
3. https://create.roblox.com/docs/reference/engine/classes/SocialService — invites, party, link sharing, calls, events, feedback APIs
4. https://create.roblox.com/docs/production/promotion/invite-prompts — ExperienceInviteOptions, launch data retries
5. https://create.roblox.com/docs/production/promotion/referral-system — ReferredByPlayerId, referral banner rules, abuse prevention
6. https://create.roblox.com/docs/production/promotion/share-links — share links, LaunchData, acquisition analytics
7. https://create.roblox.com/docs/creator-rewards — Audience Expansion via Share Link / direct link / search
8. https://create.roblox.com/docs/reference/engine/classes/CaptureService — capture and share APIs, 30 s video limit
9. https://create.roblox.com/docs/chat/voice-chat — voice eligibility, 100-player limit, audio API routing
10. https://about.roblox.com/newsroom/2026/01/roblox-age-checks-required-to-chat — age-checked chat, six age bands
11. https://create.roblox.com/docs/production/publishing/kids-and-select — Kids/Select chat defaults
12. https://devforum.roblox.com/t/roblox-kids-and-select-global-launch-upcoming-updates-to-eligibility-ads-manager-and-expedited-review/4685717 — social links 16+ from 2026-06-30
13. https://about.roblox.com/community-standards — external links only via Social Links, contests, off-platform rules
14. https://create.roblox.com/docs/production/monetization/subscriptions — no gating benefits behind social posts
15. https://create.roblox.com/docs/production/promotion/experience-notifications — no gating gameplay on opt-in, dark patterns banned
16. https://www.tubefilter.com/2025/08/25/roblox-grow-garden-steal-brainrot-admin-war-record/amp/ — admin war numbers, promotion, admin abuse format
17. https://www.pocketgamer.biz/robloxs-steal-a-brainrot-becomes-first-game-to-surpass-25m-concurrent-players/ — 47.4M platform record, Steal a Brainrot 25.4M
18. https://techcrunch.com/2025/09/05/roblox-announces-short-form-video-feed-for-gameplay-clips-new-ai-tools-for-creators-and-more — Moments beta, 13+, clips
19. https://about.roblox.com/newsroom/2025/09/roblox-moments-user-generated-discovery — Moments and promised creator APIs
20. https://devforum.roblox.com/t/introducing-roblox-communities/3268307 — groups renamed Communities
21. https://piunikaweb.com/2026/04/01/roblox-community-walls-retired-end-of-march/ — Forums launch 2025-11-30, walls retired
22. https://en.help.roblox.com/hc/articles/360026092011 — Video Stars program thresholds
23. https://roblox.fandom.com/wiki/Party — party voice 2025-03 (unverified)
24. https://devforum.roblox.com/t/introducing-roblox-plus/4567894 — Plus private server rewards
