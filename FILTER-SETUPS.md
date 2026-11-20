# Filter setups

These are the real setups used across past research batches. Six are filter setups (five on Kalo, one on FastMoss).

## About the names

- Only two codes existed in the original work: **`ODD_BATCH_80_CAP`** and **`EVEN_BATCH_60_CAP`**.
- The other setups had no formal code. They were known by the label written in the sheet.
- Every short code below is **PROPOSED** for this export. The original sheet label is always shown beside it. In the filter receipt, write both.

## Default: AVD-36

Use **AVD-36** ("Actual Variable Discovery Filters", Draft 36) unless told otherwise. Why:

1. It is the latest real run (2026-10-03), so it reflects current practice.
2. Its price band ($10–$30) matches the sale-value rule (perceived value $30 or less).
3. It is the only setup recorded with the supplier-agent delivered estimate.
4. It builds in the target buyer (45+ / 55+ / 65+) and a 5 women / 5 men split.

## How to enter any setup in Kalo (plain steps)

Kalo's exact button names can change, and they are not all recorded in the source. Match each filter by meaning.

1. Open Kalodata in the logged-in Chrome. Set region to **US** and currency to **USD**.
2. Open the product list (the product search/ranking page).
3. Set the **date range** the setup calls for.
4. Set **categories** if the setup names them.
5. Set **revenue** min and max.
6. Set **price** min and max.
7. Set **commission** min (and max if given).
8. Set content to **video only**. Make sure Live sales are not counted.
9. Set any extra filters the setup names (growth, rating).
10. Apply. Then go through **every result page**. Note page and rank for each product you keep.
11. Write every value you actually entered into the filter receipt. If your plan does not offer a filter, write `NOT_APPLIED`. Then check that condition by hand on each product page instead.
12. For each kept product, open its detail page: last 30 days → left menu **"Video & Ad"** → rows sorted by revenue.

Trial plan reminder: 10 keyword searches and 10 detail visits per day, counted separately. Ten candidates use a full day of detail visits.

---

## 1. SPEC-ROTATE (proposed code)

**Original label:** "Product Research Batch N" (the written skill spec, 2026-08-27). Contains the two real codes `ODD_BATCH_80_CAP` / `EVEN_BATCH_60_CAP`.

**When to use:** when you want a wider price net than the default, or when asked to follow the written spec exactly.

**Exact values**

| Filter | Value |
|---|---|
| Content | TikTok Shop product videos only. No Lives. |
| Commission | 10% or more |
| Kalo price, min | $10 |
| Kalo price, max | **$80 if batch number N is odd** (`ODD_BATCH_80_CAP`). **$60 if N is even** (`EVEN_BATCH_60_CAP`). |
| 30-day product revenue | $20,000 to $100,000, inclusive |
| Metric windows | 30 days and 90 days (revenue and orders) |
| Videos | 10 or more exact-product-ID videos |
| Shop | Snapshot of shop's top 10 products by 30-day revenue |

**How to enter:** steps 1–12 above. In step 6, look at the batch number first. Odd → max 80. Even → max 60. Write the code into the receipt.

**Output:** 10 ranked candidates with page, rank, direct URL, 30/90-day metrics, video IDs and shop snapshot. Products outside the price band are tagged `BATCH_FILTERED`. They are not rejected forever; they may fit the next batch.

### The odd/even price-cap rotation

| Batch number | Price band | Code to record |
|---|---|---|
| Odd (1, 3, 5 …) | $10–$80 | `ODD_BATCH_80_CAP` |
| Even (2, 4, 6 …) | $10–$60 | `EVEN_BATCH_60_CAP` |

- The batch number is the N in `Product Research Batch N`. It starts at 1.
- Always record the batch's parity and code in the receipt.
- The rotation sets the cap **in SPEC-ROTATE**. In AVD-36 the band is $10–$30, which is tighter than both caps, so the rotation changes nothing there.
- Note: a product priced $30–$80 can pass this setup's band and still fail the later sale-value rule ($30 or less). Expect that.

---

## 2. FM-VIDEO (proposed code)

**Original label:** "FastMoss video-only intake" (Draft 29, 2026-09-15/16). **Tool: FastMoss, not Kalo.**

**When to use:** as a second-source check, or when Kalo is not available for discovery. A FastMoss batch still needs the Kalo steps before any green.

**Exact values**

| Filter | Value |
|---|---|
| Region | US |
| Content | Video only |
| Window as run | 17 Aug – 15 Sep |
| Video revenue | $20,000 or more |
| Video units | 300 or more |
| Videos | 10 distinct video IDs |
| Target COGS | Below $8 |
| Sale price | Recorded in Draft 29 as "sale price >= $30" |

> **Conflict to flag:** Draft 29 wrote the sale price as **>= $30**. The later green rules (Draft 32) say perceived sale value **<= $30**. This package uses the later rule for all gates. Ask the owner if Draft 29's direction was intended.

**How to enter:** FastMoss screen steps are not recorded in the source (UNKNOWN). In plain terms: set region US, video-only sales, a 30-day window, minimum video revenue 20,000, minimum video units 300. Then confirm 10 different video IDs per product. Record what you entered in the receipt.

**Output:** a product list with video revenue, video units and 10 video IDs each.

---

## 3. KALO-PRO-VIDEO (proposed code)

**Original label:** "Kalo Professional" video screen (Draft 31, 2026-09-16). Run on a Kalo Professional account.

**When to use:** when a Professional plan is available and you want the plain sales screen with no price or buyer filters.

**Exact values**

| Filter | Value |
|---|---|
| Region | US |
| Video revenue | $20,000 or more |
| Units | 300 or more |
| Videos | 10 |
| Window as run | Aug 16 – Sep 14 |
| Meaning of GREEN in this draft | **Review only.** Not a release. |
| Cost-risk items | Labeled **Reserve** |

**How to enter:** steps 1–12 above. Use a 30-day window. Set video revenue min 20,000 and units min 300. Leave price open.

**Output:** a review list. Products with cost risk are parked as Reserve.

---

## 4. OLDER-BUYER (proposed code)

**Original label:** "September older-buyer screening" (Draft 32, 2026-09-16).

**When to use:** when the main question is buyer age fit (45+ / 55+ / 65+).

**Exact values**

| Filter | Value |
|---|---|
| Sales screen | Same as KALO-PRO-VIDEO: video revenue $20,000+, units 300+, 10 videos |
| Buyer fit | A 45+ / 55+ / 65+ buyer-fit hypothesis per product |
| Seasonality | Seasonal Google Trends check |
| Competition | Competitor count |
| Output scope | Green shortlist only |

**How to enter:** steps 1–12 with the sales screen. The buyer-age part is **not a Kalo filter**. For each product, write the age hypothesis, then check Google Trends by month and count competitors.

**Output:** a green shortlist with an age hypothesis for each product. A hypothesis is not proof. A green still needs purchaser age data with period and sample.

---

## 5. GROWTH-RATING-5-30 (proposed code)

**Original label:** "$5–30 average price; 30d growth > 0; rating 4.4–5; no Lives counted" (Draft 35, 2026-09-27).

**When to use:** to find lower-priced products that are still growing and well rated. It is the setup recorded with 1688 offers attached.

**Exact values**

| Filter | Value |
|---|---|
| Average price | $5–$30 |
| 30-day growth | Above 0 |
| Rating | 4.4 to 5 |
| Content | No Lives counted |
| Categories | Home Supplies; Tools & Hardware |
| Windows as run | 7-day video window (Sep 10–16) plus 30-day |
| Extra | 1688 order offers attached per product |

**How to enter:** steps 1–12. In step 4 pick the two categories. In step 6 use average price 5 to 30. In step 9 set growth above 0 and rating 4.4 to 5. Check videos in both the 7-day and the 30-day window.

**Output:** candidates with a 1688 offer note each (offer ID, item-only price, MOQ, variant, weight, province, brand note). In Draft 35 every row was HOLD: brands differed and there was no delivered quote.

Note: the $5 floor is below the $10 minimum used by SPEC-ROTATE and AVD-36.

---

## 6. AVD-36 (proposed code) — DEFAULT

**Original label:** "Actual Variable Discovery Filters" (Draft 36, 2026-10-03, the last run).

**When to use:** every batch, unless told otherwise.

**Exact values**

| Filter | Value |
|---|---|
| Window | 30 days. As run: Sep 3 – Oct 2. |
| Categories | Home / Kitchen / Tools / DIY |
| Revenue | $20,000–$100,000 |
| Average price | $10–$30 |
| Commission | 10%–100% |
| Content | Video only |
| Mix | 5 women-targeted and 5 men-targeted products |
| Buyer focus | 45+ / 55+ / 65+ |
| Videos | 10 observed video IDs per product |
| Pricing | Supplier-agent delivered estimate (low / base / high) per product |

**How to enter:** steps 1–12. For a new run, use the most recent 30 full days (the as-run dates are history, not a rule). In step 4 pick the Home, Kitchen, Tools and DIY categories as your Kalo plan names them. Revenue 20,000 to 100,000. Average price 10 to 30. Commission 10 to 100. Video only. The 5/5 split and the age focus are **your selection rules**, not Kalo filters: choose them while picking the 10.

**Output:** 10 research nominations, each with 10 video IDs, a supplier-agent delivered estimate and a 1688 source status. In Draft 36 no greens were released, because no exact 1688 match was verified.

---

## Not filter setups (for reference)

| Draft | What it was |
|---|---|
| Draft 27 (2026-08-28) | The sheet layout authority (Template A1:R11). See `templates/sheet-layout.md`. |
| Draft 30 (2026-09-16) | "New ten-product batch using the compact green Draft 29 layout." Run on Kalo. Filter values: UNKNOWN. |
| Drafts 33–34 (2026-09-16 to 18) | Structural predecessors of the Draft 35 format. Filter values: UNKNOWN. |

## Summary

| # | Proposed code | Original sheet label | Draft / date | Tool | Price band | Revenue / sales screen | Window | Special |
|---|---|---|---|---|---|---|---|---|
| 1 | SPEC-ROTATE | "Product Research Batch N" spec; `ODD_BATCH_80_CAP` / `EVEN_BATCH_60_CAP` | Spec, 2026-08-27 | Kalo | $10–$80 odd, $10–$60 even | 30-day revenue $20k–$100k | 30 + 90 days | Commission 10%+, shop top-10 snapshot |
| 2 | FM-VIDEO | "FastMoss video-only intake" | Draft 29, 2026-09-15/16 | FastMoss | None recorded | Video revenue $20k+, 300+ units | 17 Aug – 15 Sep | COGS target under $8; sale-price direction in conflict |
| 3 | KALO-PRO-VIDEO | "Kalo Professional" video screen | Draft 31, 2026-09-16 | Kalo (Professional) | None recorded | Video revenue $20k+, 300+ units | Aug 16 – Sep 14 | GREEN = review only; cost risk = Reserve |
| 4 | OLDER-BUYER | "September older-buyer screening" | Draft 32, 2026-09-16 | Kalo | None recorded | Same sales screen as #3 | Not recorded | 45+/55+/65+ hypothesis, Trends, competitor count |
| 5 | GROWTH-RATING-5-30 | "$5–30 average price; 30d growth > 0; rating 4.4–5; no Lives counted" | Draft 35, 2026-09-27 | Kalo + 1688 | $5–$30 average | Growth above 0, rating 4.4–5 | 7-day + 30-day | Home Supplies, Tools & Hardware; 1688 offers attached |
| 6 | **AVD-36 (default)** | "Actual Variable Discovery Filters" | Draft 36, 2026-10-03 | Kalo | $10–$30 average | Revenue $20k–$100k | 30 days | Commission 10–100%, 5 women / 5 men, 45+ focus, delivered estimate |

All setups share: video only, Lives never counted, 10 same-product videos.
