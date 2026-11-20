# Meta Ad Library check: competitors and reference videos

Every candidate must pass this check before it gets any tier (Green, Orange or Yellow). If it was not run, the product cannot be tiered and is marked `HOLD`.

The Meta Ad Library (facebook.com/ads/library) is public. A normal Chrome window can open it without logging in. One agent drives Chrome at a time.

## What it answers

1. **Is anyone already selling this exact product with Meta ads?** If yes, how many brands are there, and how long have they been running?
2. **Are the top Kalo videos for this product already running as Meta ads?** If they are, the best footage is already taken.

## Steps (per product)

### A. Keyword search: 5 keywords, all must clear (v1.8.0)

Every product is searched with **5 different keywords** that describe it. A product must clear **all 5** to be Orange or Green. A competitor found on any one of them keeps it Yellow.

1. Open each search with these settings: country **United States**, ad category **All ads**, status **Active**, media type **All**.
   Exact-phrase URL: `https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=US&q=%22KEYWORD%22&search_type=keyword_exact_phrase&media_type=all`
   Unordered URL (same, but `search_type=keyword_unordered` and no quotes around the keyword).
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

**Throttling.** Meta Ad Library may start returning 0 results, even for queries that worked before, after about 40-50 searches in a session. If a known query suddenly returns 0, stop. Pause about 10 minutes or more, then resume. Mark the keywords searched during the throttle as `RECHECK`. Never conclude "no competitor" from a throttled search. A product with any `RECHECK` keyword cannot be Orange or Green yet.

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

1. Take the product's **top 3 Kalo videos** by revenue (their IDs are on the Kalo evidence tab).
2. Get a first frame for each one. Either open `https://www.tiktok.com/player/v1/<VIDEO_ID>`, or view the thumbnail on the Kalo "Video & Ad" tab. TikTok rate-limits these players, but the error tile still shows a small thumbnail.
3. Switch the Meta search to **Media type: Videos**, scroll through it, and compare frames: same person, same setting, same product shot, same overlay text.
4. Record each Kalo video as `MATCHED` (same footage running as an ad, give the advertiser), `LIKELY` (same scene or creator, not 100% sure), or `NOT_FOUND`.

### C. Competition band

| Band | Rule | Effect on tier |
|---|---|---|
| `NONE` | 0 relevant direct-to-consumer brands | Not proven on Meta. Highest possible tier is **Orange**. |
| `LIGHT` | 1–10 brands, none running 30+ days | Room to enter, but nobody has proved it yet. Highest possible tier is **Orange**. |
| `HEALTHY` | 1–10 brands, and at least one running **30+ days** | Proven, not crowded. **Green is allowed.** |
| `CROWDED` | 11–20 brands | Highest possible tier is **Orange**. |
| `SATURATED` | 21+ brands, **or** the same ad copy cloned across 4+ pages, **or** one Kalo top-3 video `MATCHED` at 3+ advertisers | Highest possible tier is **Yellow**. |

Any `MATCHED` or `LIKELY` video: drop that video from your creative plan and note it. You will need fresh footage.

> The band cut-offs (10 / 20 brands, 30 days, 4 clones, 3 matches) are **PROPOSED v1.1 defaults**. The owner can change them in `TIERS.md`.

## What to record per product

| Field | Example |
|---|---|
| `meta_keywords` | 5 entries: query, URL, result count. For example `"outlet spacers"` (exact, 78), `outlet loose plug` (unordered, 41) |
| `meta_results_count` | `~78` |
| `meta_dtc_brands` | `22` |
| `meta_big_box` | `Amazon.com` |
| `meta_oldest_active_start` | `2026-08-19 (Enjoyaitlife-US, 37 ads)` |
| `meta_clone_copy` | `yes: same copy on 5 pages` |
| `meta_band` | `SATURATED` |
| `meta_verdict` | `CLEAR`, `MATCH`, `LIKELY` or `RECHECK` |
| `meta_competitors_using_kalo` | Advertiser, Library ID, which Kalo videos (#) |
| `ref_video_matches` | `V1 NOT_FOUND, V2 NOT_FOUND, V3 LIKELY (Goproceeding&QV)` |
| `meta_checked_at_utc` | timestamp |

## Rules

- This check is read-only. Never click "Shop now", log in, or contact advertisers.
- Missing stays missing. If the search failed or was throttled, write `RECHECK` or `MISSING`, not 0 brands.
- A brand that runs several creator pages counts as **one** brand.
