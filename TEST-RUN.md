# Test run (dry)

A paper walk-through of the gates using the 10 products from the last real batch (Draft 36, 2026-10-03).
No browsing was done for this test. Only the recorded numbers were used.

**Result in one line: 0 greens. Batch = HOLD. No handoff.** That matches what really happened in Draft 36.

## Input data

Filter setup: **AVD-36** ("Actual Variable Discovery Filters"). Window Sep 3 – Oct 2.
For every product the record holds: 10 observed video IDs, and 1688 source status "No verified exact 1688 match".

| # | Product | 30d video revenue | Kalo seller price | Supplier-agent base estimate (delivered US) |
|---|---|---|---|---|
| 1 | Long stainless tweezer tongs | $78.97k | $31.19–32.49 | $10.50 |
| 2 | Six-piece cupcake display stand | $21.30k | $25.89 | $12.00 |
| 3 | Adjustable stainless (kitchen) stand | $28.50k | $64.87 | $11.00 |
| 4 | 100-envelope savings challenge | $49.00k | $11.49–14.94 | $9.50 |
| 5 | Open-frame freezer organizer | $34.92k | $28.59–90.99 | $21.00 |
| 6 | Folding utility knife | $25.85k | $25.99 | $10.50 |
| 7 | Electrical-outlet wall plate | $48.60k | $25.97–59.77 | $7.00 |
| 8 | Long carboy/water-container brush | $27.13k | $14.29–20.79 | $14.00 |
| 9 | Mechanical corner-angle tool | $21.97k | $24.98 | $10.00 |
| 10 | Flip-latch door reinforcer | $24.61k | $15.99 | $8.50 |

**Not in the data (UNKNOWN):** Kalo product IDs and URLs, the video IDs themselves, video units, per-product commission, 90-day metrics, shop snapshots, the low/high estimate per product, planned selling price, which 5 are women-targeted and which 5 men-targeted, and all TrendTrack / Google Trends / Ad Library / buyer-age / store-age evidence.

## How outcomes are decided in this test

| Outcome | Rule |
|---|---|
| PASS | Every hard gate passed on proven evidence |
| FAIL | A hard gate failed on proven evidence |
| HOLD | A gate cannot be decided yet because evidence is missing |

Important: the delivered number here is an **estimate** built from historical supplier anchors. It is not an exact quote. By the package's own rules an estimate cannot release a green. For the same reason this test does not use it to fail a product. It is used only as a **cost outlook** to decide where to spend effort first:

| Cost outlook | Base estimate |
|---|---|
| `UNDER_8` | Below $8 |
| `STRETCH` | $8.00 up to and including $10.00 (stretch ceiling) |
| `OVER_STRETCH` | Above $10 |

## Gate walk

Legend: ✔ pass on given data · ◐ partial evidence · ? cannot be decided (data missing) · ✘ fail

Note: the revenue gate is 30-day **product** revenue. The source pack only gives **video** revenue, so the gate is undecided, not passed.

| # | Revenue $20k–$100k | 10 videos | 300+ video units | Commission 10%+ | Exact 1688 match | Delivered quote under $8 | Sale value $30 or less |
|---|---|---|---|---|---|---|---|
| 1 | ? video rev $78.97k (product rev not recorded) | ◐ PARTIAL (count only) | ? | ? | ? none verified | ? estimate $10.50 | ? price flag |
| 2 | ? video rev $21.30k (product rev not recorded) | ◐ PARTIAL (count only) | ? | ? | ? none verified | ? estimate $12.00 | ? |
| 3 | ? video rev $28.50k (product rev not recorded) | ◐ PARTIAL (count only) | ? | ? | ? none verified | ? estimate $11.00 | ? price flag |
| 4 | ? video rev $49.00k (product rev not recorded) | ◐ PARTIAL (count only) | ? | ? | ? none verified | ? estimate $9.50 | ? |
| 5 | ? video rev $34.92k (product rev not recorded) | ◐ PARTIAL (count only) | ? | ? | ? none verified | ? estimate $21.00 | ? range flag |
| 6 | ? video rev $25.85k (product rev not recorded) | ◐ PARTIAL (count only) | ? | ? | ? none verified | ? estimate $10.50 | ? |
| 7 | ? video rev $48.60k (product rev not recorded) | ◐ PARTIAL (count only) | ? | ? | ? none verified | ? estimate $7.00 | ? range flag |
| 8 | ? video rev $27.13k (product rev not recorded) | ◐ PARTIAL (count only) | ? | ? | ? none verified | ? estimate $14.00 | ? |
| 9 | ? video rev $21.97k (product rev not recorded) | ◐ PARTIAL (count only) | ? | ? | ? none verified | ? estimate $10.00 | ? |
| 10 | ? video rev $24.61k (product rev not recorded) | ◐ PARTIAL (count only) | ? | ? | ? none verified | ? estimate $8.50 | ? |

Notes on the columns:

- **Revenue.** The recorded figure is 30-day video revenue. All 10 sit inside $20k–$100k. #2 and #9 are close to the floor.
- **10 videos.** The count of 10 is recorded. The IDs are not in the data, so the exact-product-ID match cannot be re-checked here. Evidence state: PARTIAL.
- **Commission.** The batch filter was 10%–100%, so each product likely passed. Per-product values are not recorded.
- **Sale value.** The gate is on our perceived sale value. That number is not recorded. The Kalo seller price is only a hint. Flags: #1 is listed above $30 across its whole range. #3 is listed at $64.87. #5 and #7 have ranges that run well above $30. The batch filter was "average price $10–$30"; each product's Kalo average price is not recorded.

## Outcome per product

| # | Product | Outcome | Cost outlook | Estimate minus $8 | Estimate as % of lowest Kalo price | Main reason |
|---|---|---|---|---|---|---|
| 1 | Long stainless tweezer tongs | **HOLD** | OVER_STRETCH | +$2.50 | 34% | No exact 1688 match. Estimate above $10. Listed above $30. |
| 2 | Six-piece cupcake display stand | **HOLD** | OVER_STRETCH | +$4.00 | 46% | No exact 1688 match. Estimate above $10. |
| 3 | Adjustable stainless (kitchen) stand | **HOLD** | OVER_STRETCH | +$3.00 | 17% | No exact 1688 match. Estimate above $10. Listed at $64.87, far above the $30 value rule. |
| 4 | 100-envelope savings challenge | **HOLD** | STRETCH | +$1.50 | 83% | No exact 1688 match. Estimate above $8. Very thin room against an $11.49 listing. |
| 5 | Open-frame freezer organizer | **HOLD** | OVER_STRETCH | +$13.00 | 73% | No exact 1688 match. Estimate $21 is far above the gate. |
| 6 | Folding utility knife | **HOLD** | OVER_STRETCH | +$2.50 | 40% | No exact 1688 match. Estimate above $10. |
| 7 | Electrical-outlet wall plate | **HOLD** | UNDER_8 | −$1.00 | 27% | No exact 1688 match. Only product whose estimate is under $8. |
| 8 | Long carboy/water-container brush | **HOLD** | OVER_STRETCH | +$6.00 | 98% | No exact 1688 match. Estimate nearly equals the lowest listing. |
| 9 | Mechanical corner-angle tool | **HOLD** | STRETCH | +$2.00 | 40% | No exact 1688 match. Estimate sits at the $10 ceiling. |
| 10 | Flip-latch door reinforcer | **HOLD** | STRETCH | +$0.50 | 53% | No exact 1688 match. Estimate just above $8. |

Count: **PASS 0 · HOLD 10 · FAIL 0.**

Why no FAIL: nothing was failed on proven evidence. Why no PASS: no product has a verified exact 1688 match or an exact delivered quote, and the rule is "no exact delivered quote below $8 → no green".

Honest reading of the outlook: six products (#1, #2, #3, #5, #6, #8) would need a real quote far below the estimate to clear. In the Draft 31 wording these are cost-risk items, to be parked as **Reserve**. They are not worth 1688 effort before #7, #10, #4 and #9.

## Scores

| Dimension | State for all 10 | Why |
|---|---|---|
| Perceived Value | MISSING | No evidence recorded |
| Problem Solving | MISSING | No evidence recorded |
| Emotional problem | MISSING | No evidence recorded |
| Proven Sales Demand | PARTIAL, not scored | Revenue and video count exist. Units missing. No 0–5 rubric in the source. |
| Appeals To Impulse Purchasers | MISSING | No evidence recorded |
| Content | PARTIAL, not scored | 10 videos observed. Content quality not recorded. |
| Evergreen | MISSING | No trend or seasonal data recorded |
| Brandable | MISSING | No evidence recorded |

**Total score: not computable for any product.** A missing dimension is not a zero, so no number is shown. No product can be shown to reach 75/100.

Day-one label for all 10: `DAY1_MISSING`.

## Final batch result

| Item | Result |
|---|---|
| Greens | 0 of the 3 needed |
| Batch result | **HOLD** |
| Names filled green on the Template tab | None |
| Handoff | None. Nothing goes to the launch side. |
| Status wording | Research nomination. Market evidence not cleared. |

## What the partner's agent must do next

Work in this order: **#7, then #10, #4, #9.** Leave the six Reserve items until last.

For each product, to clear the HOLD:

| Step | Action | Clears |
|---|---|---|
| 1 | Reopen the Kalo product page. Record product ID, direct URL, commission, 30/90-day revenue and orders, video units. | Identity, commission, 300-unit screen |
| 2 | Re-verify the 10 videos: unique, exact product ID, no Lives, duplicates or compilations. Record the IDs. | Video gate |
| 3 | On 1688 (logged in), find the exact product and variant by photo and keyword. Compare 2 or more independent factories. Record offer ID, CNY, MOQ, FX date, excluded charges. | Exact 1688 match |
| 4 | Have the human request an exact delivered quote from the supplier agent for that offer, with the cost parts split out. | COGS gate (needs below $8) |
| 5 | Set the planned selling price and confirm perceived value is $30 or less. | Sale-value gate |
| 6 | Check TrendTrack, Google Trends and Ad Library for the exact product. | Required sources |
| 7 | Get purchaser-age proof (45+), store-age cohorts and recent-vs-prior trend. | Green evidence |
| 8 | Score all 8 dimensions with evidence, once the owner confirms the rubric. | Score 75/100 or more |

Product-specific notes:

| # | Extra thing to resolve |
|---|---|
| 1 | Listed above $30. Decide if a $30-or-less offer is realistic before pricing work. |
| 3 | Listed at $64.87. Likely fails the sale-value rule. Check that first; it may save all other work. |
| 4 | Even at the estimate, room against an $11.49–$14.94 listing is very small. Needs a quote well below $8. |
| 5 | Find out which variant sells. The price range is very wide ($28.59–$90.99). The estimate of $21 would have to fall by more than half. |
| 7 | Best cost outlook. Find out which variant sells ($25.97–$59.77) and match that exact variant on 1688. |
| 8 | The estimate ($14.00) nearly equals the lowest listing ($14.29). Low chance without a very different quote. |
| 9 | At the $10 ceiling. Needs a real quote more than $2 lower. |
| 10 | Closest of the stretch group. Needs a real quote only $0.51 or more below the estimate. |

If fewer than 3 products clear every gate after this work, the batch stays **HOLD**. Run a new batch. Do not lower the bar.
