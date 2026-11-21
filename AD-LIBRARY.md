# Ad Library check: competitors and reference videos

Every candidate needs this check before it can be Orange or Green. Until it is run, or while any keyword is `RECHECK`, the product stays Yellow (its Kalo-demand tier) and the sheet says why.

The Ad Library (facebook.com/ads/library) is public. A normal Chrome window can open it without logging in. One agent drives Chrome at a time.

## What it answers

1. **Is anyone already selling this exact product with ads in the Ad Library?** If yes, how many brands are there, and how long have they been running?
2. **Are the top Kalo videos for this product already running as ads in the Ad Library?** If they are, the best footage is already taken.

## Steps (per product)

### A. Keyword search: 5 keywords, all must clear (v1.8.0)

Every product is searched with **5 different keywords** that describe it. A product must clear **all 5** to be Orange or Green. A competitor found on any one of them keeps it Yellow.

1. Open each search with these settings: country **United States**, ad category **All ads**, status **Active**, media type **Videos**. Both the result counts and the frame check (Part B) use video ads, so one search does both jobs.
   Exact-phrase URL: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q=%22KEYWORD%22&search_type=keyword_exact_phrase&media_type=video`
   Unordered URL (same, but `search_type=keyword_unordered` and no quotes around the keyword).
   If the page remembers a sort such as "Impressions: high to low", the results are the same; the sort is not a cause of 0.
2. Pick 5 keywords that describe the product from different sides. Mix exact-phrase and unordered searches:
   - K1 exact phrase: the plain product name (for example `"tweezer tongs"`)
   - K2 exact phrase: the brand name from the Kalo listing, if there is one, otherwise a second name people use
   - K3 unordered: the function (for example `tongs kitchen grip`)
   - K4 exact phrase: the problem it solves (for example `"wobbly outlet"`)
   - K5 unordered: a problem or benefit word set (for example `outlet loose plug fix`)
   If a keyword returns 0, that is still a result, but check that it is not a throttle (see below). A shorter or more common phrase may find more (`"carboy brush"` returned 0, `"jug brush"` returned 1).
3. Scroll until no more results load, or until about 60 ads have loaded.
4. For each ad, record: the advertiser, the brand (the part after "with" in a creator post such as "Emily Carter **with Sakerplus**"), the start date, and the landing domain.
5. Count only the **relevant** ads, meaning the ad text names the product. Group them by brand.
6. Keep big retailers (Target, Walmart, Amazon, Lowe's, Home Depot, Temu and similar) separate. They show that the product category sells, but they are not direct dropshipping competition.

**Control keyword.** Before the sweep, and again about every 15 searches, search a control keyword that always has ads (for example `"dryer vent"`, about 2,300 US video ads). If the control returns 0, you are throttled: everything since the last good control is `RECHECK`.

**Throttling.** Ad Library may start returning 0 results ("No ads match your search criteria"), even for queries that worked before, after about 40-50 searches in a session. The throttle is shared by everything on that Chrome, Facebook session and network, so it can come much sooner when other agents searched first.
- **Never run two Ad Library lanes at once.** One worker, one product at a time.
- If the first control is 0, do nothing else. Wait 10 minutes or more, then check the control again.
- If a known query suddenly returns 0 mid-sweep, stop and treat it the same way.
- A throttle can last well over an hour (one on 2026-11-20 lasted from 22:27 to past 00:09 UTC). Keep checking the control every 20-30 minutes, run no product searches meanwhile, and say in the end-of-run report what is still waiting.
- Mark the keywords searched during the throttle as `RECHECK`. Never conclude "no competitor" from a throttled search. A product with any `RECHECK` keyword cannot be Orange or Green yet.

**Verdict per product**

| Verdict | Rule |
|---|---|
| `CLEAR` | All 5 keywords were searched with no throttle, and none shows a competitor running the product's Kalo videos |
| `MATCH` | At least one competitor runs a Kalo video of this product (same footage). Stays Yellow |
| `LIKELY` | A competitor runs the same scene or creator, not 100% sure. Stays Yellow until checked |
| `RECHECK` | One or more keywords were throttled or failed. Not Orange yet |

**How the verdict is shown on the sheet (column L).** All 5 keywords as clickable links, each with its result count, then the verdict line:
- Clear: `✓ No competitor using the Kalo videos · N pages sell it`
- Not clear: `✗ N competitors run its Kalo videos`, then each competitor's Ad Library link and which Kalo videos (#) they use.

"N pages sell it" means the number of pages found selling the product across the 5 searches. Pages that sell it but do not use the Kalo videos do not block Orange.

### B. Reference-video match

1. Take the product's **top 10 Kalo videos** by revenue (their IDs are in `lane-L1-kalo.json`; how they are collected is in `SKILL.md` Step 4 and the "Video numbers" note in `AGENTS.md`).
2. Get a first frame for each one. The cover image is public: `https://img.kalocdn.com/tiktok.video/<VIDEO_ID>/cover.png`. If a cover returns 404, open `https://www.tiktok.com/player/v1/<VIDEO_ID>` (TikTok rate-limits these players, but the error tile still shows a small thumbnail) or view the thumbnail on the Kalo "Video & Ad" tab.
3. Scroll through each video search from Part A and compare frames: same person, same setting, same product shot, same overlay text. Ads that TrendTrack or the Competitor Files already found for this product are worth checking first.
4. Record each Kalo video as `MATCHED` (same footage running as an ad, give the advertiser and Library ID), `LIKELY` (same scene or creator, not 100% sure), or `NOT_FOUND`.

### C. Competition band

The band is **shown on every row, not a tier gate** (`TIERS.md` sets the tier). It helps choose between products of the same tier, and the launch gate uses it (`SKILL.md` Step 8).

| Band | Rule | What it tells you |
|---|---|---|
| `NONE` | 0 relevant direct-to-consumer brands | Not proven in the Ad Library yet. |
| `LIGHT` | 1–10 brands, none running 30+ days | Room to enter, but nobody has proved it yet. |
| `HEALTHY` | 1–10 brands, and at least one running **30+ days** | Proven, not crowded. The best band for a launch. |
| `CROWDED` | 11–20 brands | Harder to stand out. |
| `SATURATED` | 21+ brands, **or** the same ad copy cloned across 4+ pages, **or** one Kalo top-3 video `MATCHED` at 3+ advertisers | Very crowded. Pick another product of the same tier first. |

Any `MATCHED` or `LIKELY` video: drop that video from your creative plan and note it. You will need fresh footage.

> The band cut-offs (10 / 20 brands, 30 days, 4 clones, 3 matches) are **PROPOSED v1.1 defaults**. The owner can change them in `TIERS.md`.

## What to record per product

| Field | Example |
|---|---|
| `adlib_keywords` | 5 entries: query, URL, result count. For example `"outlet spacers"` (exact, 78), `outlet loose plug` (unordered, 41) |
| `adlib_results_count` | `~78` |
| `adlib_dtc_brands` | `22` |
| `adlib_big_box` | `Amazon.com` |
| `adlib_oldest_active_start` | `2026-08-19 (Enjoyaitlife-US, 37 ads)` |
| `adlib_clone_copy` | `yes: same copy on 5 pages` |
| `adlib_band` | `SATURATED` |
| `adlib_verdict` | `CLEAR`, `MATCH`, `LIKELY` or `RECHECK` |
| `adlib_competitors_using_kalo` | Advertiser, Library ID, which Kalo videos (#) |
| `ref_video_matches` | `V1 NOT_FOUND, V2 NOT_FOUND, V3 LIKELY (Goproceeding&QV)` |
| `adlib_checked_at_utc` | timestamp |

## Rules

- This check is read-only. Never click "Shop now", log in, or contact advertisers.
- Missing stays missing. If the search failed or was throttled, write `RECHECK` or `MISSING`, not 0 brands.
- A brand that runs several creator pages counts as **one** brand.
