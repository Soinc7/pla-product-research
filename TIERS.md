# Tiers: Yellow → Orange → Green (and White)

v1.2, 2026-11-20. This is the owner's ladder and it replaces the v1.1 rules. A product **starts at Yellow and graduates upward**. Each step needs its own proof.

| Tier | Sheet fill | How a product gets here |
|---|---|---|
| 🟢 **GREEN** | `#00FF00` | It is Orange **and** a winning video is verified. Every list needs **at least 3 Greens**. |
| 🟠 **ORANGE** | `#FFA500` | It is Yellow **and** competitors on Meta are **not** using any of its top-10 Kalo videos. |
| 🟡 **YELLOW** | `#FFFF00` | It passed the Kalo demand filters (the filter setup's revenue, price, commission and video rules). |
| ⚪ **WHITE** | no fill | A potential, not a tier. It fails a hard gate or its evidence is incomplete. |

## Step 1. Yellow: Kalo demand

- It passes the chosen filter setup (default AVD-36: 30-day revenue $20k–$100k, average price $10–$30, commission 10%+, video only).
- It has at least 10 same-product videos with their IDs recorded (the top 10 by revenue).
- Perceived sale value is $30 or less, and there is no fatal risk such as a branded or patented design, safety or medical claims, or an unclear pack size. A product that fails here is **White**.

## Step 2. Yellow → Orange: the top-10 videos are not taken on Meta

Run `META-AD-LIBRARY.md` for the product.

1. Take the **first frame** of each of the product's **top 10 Kalo videos**. Use the thumbnail on Kalo's "Video & Ad" tab.
2. Search the Meta Ad Library with exact-phrase keywords, filtered to video ads, and compare first frames.
3. **If unsure, check more frames.** Open the ad and step through it (about 1s, 3s, 5s), and compare person, setting, product shot and overlay text.
4. Record each Kalo video as `MATCHED`, `LIKELY` or `NOT_FOUND`.
5. **All 10 `NOT_FOUND` → Orange.** Any `MATCHED` or `LIKELY` → stays Yellow. Note who is using it.
6. If no competitor is running video ads for the exact product, that counts as all `NOT_FOUND`. Say so in the record.

## Step 3. Orange → Green: a winning video is verified

All of these must be true. The data comes from Kalo (orders per video) and TrendTrack (appeal on TikTok and Meta).

| Check | Source | Pass (PROPOSED default) |
|---|---|---|
| Orders | Kalo, best video, 30 days | **500+ orders** from one video |
| Conversion | Kalo, orders ÷ views | **0.6+ orders per 1,000 views** on that video |
| Viewership | Kalo / TrendTrack | Best video **300k+ views** |
| Appeal | TrendTrack TikTok library and Meta ads for the product | At least one product video or ad with **100k+ views**, showing the hook works beyond one creator |

If any check is missing, the product stays Orange. Missing never counts as a pass.

## Minimum 3 Greens

- A list must reach **at least 3 Greens**. Pull more Kalo candidates, from the next pages or another filter setup, until it does.
- Never promote without the proof above. If the daily Kalo limits run out first, deliver what is proven, marked `NEEDS_MORE_CANDIDATES`, and continue next session.
- Orange and Yellow: no fixed count. List every product that qualifies.

## Shown on every row, but not a tier gate

- **Cost:** the exact 1688 match and the Aria delivered quote (`PRICING-1688-ARIA.md`). These must be cleared before any launch handoff.
- **Meta crowding:** brand count, the oldest ad, and copied ad text. This helps choose between Greens.

The numbers marked PROPOSED (500 orders, 0.6 per 1,000, 300k, 100k) can be changed by the owner. Note any change in `CHANGELOG.md`.
