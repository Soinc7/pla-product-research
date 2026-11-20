# Tiers: Green, Orange, Yellow

Every batch sorts its 10 candidates into three tiers of "best contenders", plus a not-tiered group.

| Rank | Tier | Sheet fill | Meaning |
|---|---|---|---|
| 1 | **GREEN** | `#00FF00` | Ready for the launch side. Everything is proven. |
| 2 | **ORANGE** | `#FFA500` | Strong contender. One gate is still open, and one step closes it. |
| 3 | **YELLOW** | `#FFFF00` | Watchlist. Demand is real, but cost or competition holds it back. |
| — | Not tiered | no fill | Fails a hard gate. Rejected for this batch. |

Order: **Green > Orange > Yellow.** Within a tier, rank by score. Where scores are missing, rank by the lowest delivered cost.

## Gates every tier needs (demand)

- 30-day product revenue from $20k to $100k, or the filter setup's own revenue band.
- At least 10 same-product videos and at least 300 video units.
- Perceived sale value of **$30 or less**. A Kalo seller price far above that, such as $64.87, means not tiered.
- No fatal risk. Fatal risks include a branded or patented design, safety or medical claims, and an unclear pack size.
- The Meta Ad Library check was run (`META-AD-LIBRARY.md`).

## Tier rules

| | GREEN | ORANGE | YELLOW |
|---|---|---|---|
| 1688 | **Exact match verified** (several factories) | Exact match pending or verified | Any |
| Delivered cost | **Real Aria quote under $8** | Real quote $8–$9.99, or an estimate under $9 | Estimate $9–$12, or a quote $10–$12 |
| Meta band | `HEALTHY` | `NONE`, `LIGHT`, `HEALTHY` or `CROWDED` | Any, including `SATURATED` |
| Kalo top-3 videos already running on Meta | None `MATCHED` | No more than 1 `MATCHED` | Any |
| Green evidence (TrendTrack, Google Trends, buyer age, store age, current trend) | All PROVEN | May be PARTIAL | May be MISSING |
| Score | 75/100 or more | 60–74, or not computable yet | 45–59, or not computable yet |
| Next step | Paused handoff | Get the one missing proof (usually the Aria quote) | Re-check next batch, or look for a cheaper factory |

A product is placed in the **highest tier whose every row it meets**. The Meta band caps can push it down: `CROWDED` caps it at Orange, and `SATURATED` caps it at Yellow.

## Batch result

- **3 or more Greens**: release the top 3 for the paused handoff. Spend stays $0.
- **Fewer than 3 Greens**: the batch result is `HOLD`. Orange and Yellow are still listed so you know where to work next. A missing Green is never filled from Orange.

## Defaults the owner can change

The cost bands ($8 / $9 / $10 / $12) and score bands (75 / 60 / 45) are **PROPOSED v1.1 defaults**, set 2026-11-20. Change them here and note the change in `CHANGELOG.md`.
