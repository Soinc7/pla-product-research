# Tiers: Yellow → Orange → Green (and White)

v1.3, 2026-11-20 (v1.2 ladder, with the 5-keyword competitor check). This is the owner's ladder and it replaces the v1.1 rules. A product **starts at Yellow and graduates upward**. Each step needs its own proof.

| Tier | Sheet fill | How a product gets here |
|---|---|---|
| 🟢 **GREEN** | `#00FF00` | It is Orange **and** a winning video is verified. Every list needs **at least 3 Greens**. |
| 🟠 **ORANGE** | `#FFA500` | It is Yellow **and** competitors on Meta are **not** using its Kalo videos, after 5 different keyword searches all clear. |
| 🟡 **YELLOW** | `#FFFF00` | It passed the Kalo demand filters (the filter setup's revenue, price, commission and video rules). |
| ⚪ **WHITE** | no fill | A potential, not a tier. It fails a hard gate or its evidence is incomplete. |

## Step 1. Yellow: Kalo demand

- It passes the chosen filter setup (default AVD-36: 30-day revenue $20k–$100k, average price $10–$30, commission 10%+, video only).
- It has at least 10 same-product videos with their IDs recorded (the top 10 by revenue).
- Perceived sale value is at or below `sale_value_max` (default $30, in `state/intake.json`), and there is no fatal risk such as a branded or patented design, safety or medical claims, or an unclear pack size. A product that fails here is **White**.
- The intake price band sets the Kalo price filter; it does not change the sale-value rule. If the owner's band goes higher (for example $10-$40), raise `sale_value_max` with their OK.

## Step 2. Yellow → Orange: no competitor uses the Kalo videos (5-keyword check)

Run `META-AD-LIBRARY.md` for the product.

1. **Search 5 different keywords** that describe the product (mix exact-phrase and unordered; brand, function and problem words). The product must clear **all 5**.
2. Take the **first frame** of each of the product's **top 10 Kalo videos** (the thumbnail on Kalo's "Video & Ad" tab) and compare them with the video ads the searches return.
3. **If unsure, check more frames.** Open the ad and step through it (about 1s, 3s, 5s), and compare person, setting, product shot and overlay text.
4. Record each Kalo video as `MATCHED`, `LIKELY` or `NOT_FOUND`.
5. Verdict `CLEAR` (all 5 keywords searched, all 10 `NOT_FOUND`) → Orange. Any `MATCHED` or `LIKELY` → stays Yellow, and the sheet names each competitor and which Kalo videos (#) it uses.
6. Any keyword throttled or not searched → verdict `RECHECK`. The product waits at Yellow. Never treat a throttled 0 as "no competitor".
7. If no competitor is running video ads for the exact product, that counts as all `NOT_FOUND`. Say so in the record.

## Step 3. Orange → Green: a winning video is verified

All of these must be true. The data comes from Kalo (orders per video) and TrendTrack (appeal on TikTok and Meta).

| Check | Source | Pass (PROPOSED default) |
|---|---|---|
| Orders | Kalo, one video, 30 days | **500+ orders** from that video |
| Conversion | Kalo, orders ÷ views | **0.6+ orders per 1,000 views** on that same video |
| Viewership | Kalo / TrendTrack | That same video has **300k+ views** |
| Appeal | TrendTrack TikTok library and Meta ads for the product | At least one video or ad of the **same product** with **100k+ views**, showing the hook works beyond one creator |

- **One video must pass all three Kalo bars** (orders, conversion, views). Two videos that each pass part of it do not count. The winning video is the highest-revenue video that passes all three (`merge_lanes.py` does this).
- **Same product** for appeal means the same design doing the same job. A different brand of the same design counts. A different product type that solves the same problem (for example a non-contact voltage pen for a 12V circuit probe) does not: mark it `UNCERTAIN` and keep looking. Appeal `PARTIAL` means a hit was found but not yet confirmed by eye; it does not pass until it is `PROVEN`.

If any check is missing, the product stays Orange. Missing never counts as a pass.

## Launch math: ranking inside a tier

Uses the intake budget (`state/intake.json`). Price = the TikTok price as reference, unless the user gives a store price.

| Term | Formula |
|---|---|
| Margin | sale price − est. delivered |
| Break-even ROAS | price ÷ margin |
| Sales/day to break even | daily CBO budget ÷ margin |
| Price needed for 2.0 break-even ROAS | 2 × est. delivered |

- Greens are ranked inside Green by launch math, **lower break-even ROAS first**, after they pass every gate. Launch math never promotes a product to a higher tier.
- **Weak launch math** = margin ≤ 0 or break-even ROAS above `breakeven_roas_max`. Show it as a watch-out on the row, and the report says what price or bundle fixes it (use the price needed for 2.0 break-even ROAS).
- **PROPOSED default:** `breakeven_roas_max` = 3. The owner can change it in `state/intake.json`. Note any change in `CHANGELOG.md`.
- Example: price $16.63, est. delivered $7.58 → margin $9.05, break-even ROAS 1.84, at $150/day about 17 sales/day to break even, and 2.0 ROAS needs a price of $15.16 or more.

## Minimum 3 Greens

- A list must reach **at least 3 Greens**. Pull more Kalo candidates, from the next pages or another filter setup, until it does.
- Never promote without the proof above. If the daily Kalo limits run out first, deliver what is proven, marked `NEEDS_MORE_CANDIDATES`, and continue next session.
- Orange and Yellow: no fixed count. List every product that qualifies.

## Shown on every row, but not a tier gate

- **Cost:** shown on every row (Green, Orange and Yellow): the 1688 / Fabulk item cost with a match label `EXACT` / `CLOSE` / `SIMILAR`, and "Est. delivered (standard)" = item cost + $5.00 flat. See `PRICING-1688-SUPPLIER.md`. Estimates rank products but never release a Green by themselves. A real exact match and supplier-agent quote must be cleared before any launch handoff.
- **Meta crowding:** brand count, the oldest ad, and copied ad text. This helps choose between Greens.

The numbers marked PROPOSED (500 orders, 0.6 per 1,000, 300k, 100k) can be changed by the owner. Note any change in `CHANGELOG.md`.
