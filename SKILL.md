---
name: pla-product-research
description: Read-only TikTok Shop product research. Runs a tool preflight, discovers 10 candidates on Kalodata with a named filter setup, proves 10 exact-product videos each, confirms the factory price on 1688, gets a supplier-agent delivered estimate, applies the under-$8 cost gate and 8-point scoring, then outputs the top 3 greens or HOLD to a Google Sheet with a paused handoff. Use when asked to run product research, a research batch, a Kalo screen, a 1688 counter-price check, or a preflight for these tools.
---

# PLA Product Research

> Running with several agents to save tokens? Read [`AGENTS.md`](AGENTS.md): the host runs preflight and checks, cheap workers each take one lane. Single-agent runs follow the steps below as written.

## Hard rules (read first)

1. **Read-only.** No publishing. No product activation. No ad launch. No spend. Ever.
2. **Preflight first.** Do not open a research page until `PREFLIGHT.md` says GO.
3. **Never ask for, type, read or store passwords, keys or codes.** The human logs in themself. If you hit a login wall or consent screen, stop and report it.
4. **One agent drives Chrome at a time.**
5. **Evidence has three states only:** `PROVEN`, `PARTIAL`, `MISSING`. Missing stays missing. Never write zero for unknown. Never invent a URL, price, sales figure or supplier.
6. **Never lower the bar.** Fewer than 3 qualifying products means `HOLD`. Never fabricate a third.
7. **Nothing private in outputs.** No account IDs, customer data or financial account data.
8. **Run to completion. Never pause for "go".** Once preflight says GO or GO_LIMITED, run every step through to the delivered draft sheet in one pass. Do not stop to ask "should I continue?", and do not end a turn with a half-done draft. The only reasons to stop early are a hard STOP (Chrome or Kalo MISSING), a login, CAPTCHA or consent wall that only the human can clear, or an explicit "stop" from the human. Even then, first write everything already found into the draft sheet, marking the rest HOLD or MISSING, and deliver it.
9. **A draft is done only when the sheet exists.** Done means: the next-numbered batch sheet (named as in Step 1) is in the same Drive folder as the last one, with all 10 rows, tier fills, notes and the Candidates tab, and it has been read back. A chat summary or repo file alone is not a delivered draft.
10. **Never block on one product.** If one product's 1688 match, Meta check or TrendTrack check stalls, mark that field MISSING with the reason, keep going with the rest, and finish the sheet.

## Outcome words

| Word | Meaning |
|---|---|
| GREEN | Passed every hard gate, has all required evidence, scored 75/100 or more, no fatal risk |
| HOLD | Evidence missing or not yet matched. Can be cleared later. |
| FAIL | A hard gate is failed on real evidence |
| BATCH_FILTERED | Outside this batch's price band. Not rejected forever. |

## Run procedure

### Step 0 — Preflight

Follow `PREFLIGHT.md`. Record each check as PROVEN / PARTIAL / MISSING.
Any MISSING on **Chrome or Kalo** = STOP. Report the exact fix and end the run.

**1688 never stops the run.** Use any one route: **Fabulk** (fabulk.com, no login), **1688order.com** (free account) or **1688.com** (logged in). If none works, ask the user to log in or make a free account on one of them, keep doing discovery, Meta and TrendTrack, and hold pricing.

### Step 1 — Open the batch record

- Name the batch `Product Research Batch N`. Your own numbering: your first batch is N = 1. Read the last N from `state/` (highest `batch-N.json`); if none exists, N = 1. Older "Product Research Draft" titles do not advance N.
- Create `state/batch-N.json` from `templates/batch-state.json`. Update it after every page, every Kalo detail visit and every quote request.
- Record: `observed_at_utc`, `region`, `currency`, `account_check` (`MATCH`, `MISMATCH` or `NOT_CHECKED`). Never store the account ID itself.
- Pick the filter setup from `FILTER-SETUPS.md`. Default: **AVD-36**.
- Note whether N is odd or even and write the price-cap code (`ODD_BATCH_80_CAP` or `EVEN_BATCH_60_CAP`). See `FILTER-SETUPS.md` for when the cap applies.
- Start the filter receipt from `templates/filter-receipt.md`. Fill it as you go.

### Step 2 — Kalo discovery

- Content type is **TikTok Shop product videos**. Lives are excluded and never counted.
- Enter the chosen filter setup exactly. Write every value you actually entered into the receipt. If a filter is not available on your plan, write `NOT_APPLIED`, do not pretend.
- Go through **all result pages**. For every product you keep, record result page and rank.
- Record the **direct product-detail URL**. Pattern:
  `https://www.kalodata.com/product/detail?id=<ID>&region=US&currency=USD&language=en-US`
- Capture both metric windows: 30 days and 90 days, revenue and orders.
- Mind the plan limits noted in preflight. On a trial, plan the batch across days instead of skipping checks.
- **Resume rule:** when a run stops (daily limit, waiting on a quote, session end), save `state/batch-N.json` and stop. Next run: rerun preflight, open the same `batch-N.json`, continue from `next_step`. Never restart a batch or repeat a done step.

### Step 3 — Select exactly 10 candidates

- Exactly 10, ranked 1–10.
- Hard screens at this step:
  - 30-day product revenue from $20,000 to $100,000, inclusive.
  - Commission 10% or more.
  - Price inside the batch band. Outside the band = `BATCH_FILTERED`.
- For each candidate's shop, snapshot the shop's **top 10 products by 30-day revenue**.
- If the setup asks for a split (AVD-36: 5 women-targeted, 5 men-targeted, older-buyer focus), keep the split.

### Step 4 — Video evidence

- On the product page: last 30 days, left menu **"Video & Ad"**. Rows are sorted by revenue.
- Collect at least **10 unique TikTok Shop videos** whose product ID exactly matches the candidate's Kalo product ID.
- Do not count: Lives, duplicates, compilations, or videos for a different product.
- Sales screen: 30-day video revenue of $20,000 or more, 300 or more video-attributed units, 10 same-product video references.
- To save a clip: row thumbnail → preview → "Download". Do **not** open `/video/detail` pages (blank player).
- Fewer than 10 valid videos = that evidence is PARTIAL and the product cannot be green.

### Step 5 — 1688 exact-match factory price (the "counter price")

Follow `PRICING-1688-SUPPLIER.md`, part A.
Short version: find the **exact** product and variant through any 1688 route (Fabulk photo search first: camera icon, upload the Kalo main photo), compare several independent factories, record offer ID, CNY price, FX date and what the price excludes.
No exact match = `HOLD`.

### Step 6 — Supplier-agent delivered estimate

Follow `PRICING-1688-SUPPLIER.md`, part B.
Until a real quote exists, show "Est. delivered (standard)" = item cost + $5.00 flat on every row. It ranks, it never releases a Green.
Record low / base / high delivered-to-US cost in USD and the method.
An item-only 1688 price is **not** a delivered quote.

### Step 7 — COGS gate

| Gate | Rule |
|---|---|
| All-in COGS | Below **$8** per unit, after supplier uplift and logistics. $10 is a stretch ceiling, not a pass. |
| Sale value | Perceived sale value **$30 or less** |
| Proof | An exact delivered quote below $8. No such quote = no green. |

`supplier_landed_cost_usd` is its own field. It is never copied from the Kalo price.

### Step 7b — Meta Ad Library check (required for any tier)

Run `META-AD-LIBRARY.md` for every candidate: **5 different keywords** (mix exact-phrase and unordered; a product must clear all 5 to be Orange or Green), competitor brands grouped and counted, oldest active ad, cloned copy, and the Kalo top-3 videos matched against running video ads. Record the competition band (`NONE` / `LIGHT` / `HEALTHY` / `CROWDED` / `SATURATED`). Not run, or any keyword throttled (`RECHECK`) = the product cannot be Orange or Green. Never conclude "no competitor" from a throttled search.

### Step 8 — Green evidence checklist

A green needs all of these for the exact product. Any one missing = HOLD.

| Evidence | Rule |
|---|---|
| Sources | Kalo, 1688, TrendTrack, Google Trends checked; Meta Ad Library band `HEALTHY` (see `META-AD-LIBRARY.md`) |
| Buyer age | Purchasers proven 45+, better 55+ or 65+, with conversion data (period and sample). Search interest or creator audience is not proof. Target buyer is 55–65 and not tech-savvy. |
| Store-age cohorts | Real store creation dates for 30-day and 180-day cohorts. Product first-seen dates and ad start dates do not count. |
| Current trend | Recent vs prior Kalo video revenue and units, plus monthly seasonal search |
| URLs | Complete for every claim |
| Fatal risk | None |
| Day-one floor | Projected seasonal day-one floor met (see below) |

Tie-break preference: favor products that convert very well and whose 1688 cost makes them a good fit for a paid membership (VIP) offer.

### Step 9 — Scoring

- 8 dimensions, each 0–5, each with evidence. Green needs **75/100 or more**.
- The 8 dimensions are the sheet's scoring columns: Perceived Value, Problem Solving, Emotional problem, Proven Sales Demand, Appeals To Impulse Purchasers, Content, Evergreen, Brandable.
- A dimension with no evidence is `MISSING`. It is not scored 0, and the total is then "not computable".

> **UNKNOWN — ask the owner before first live scoring:**
> (1) The source lists 8 dimensions and 8 sheet scoring columns but does not state in words that they are the same list. This mapping is assumed.
> (2) How 8 × 5 = 40 points becomes a score out of 100 is not stated. Proposed: total × 2.5, equal weights, so 30/40 = 75.
> (3) The 0–5 rubric per dimension is not in the source.

### Step 10 — Day-one labels

These labels describe first-day purchases. Never call a winner from revenue or ROAS alone.

| Label | Rule |
|---|---|
| `DAY1_REJECT` | Fewer than 4 purchases |
| `SEASONAL_TARGET_MISS` | Q3/Q4 with 4–5 purchases |
| `DAY1_TARGET` | Q1/Q2: 4–8. Q3/Q4: 6–10. |
| `DAY1_ABOVE_TARGET` | Above the target range |
| `DAY1_MISSING` | No day-one data |

Research has no launch data, so the label is `DAY1_MISSING` until the launch side reports back.
UNKNOWN: the method for the "projected seasonal day-one floor" is not in the source. Ask the owner; until then mark it MISSING.

### Step 11 — Tier every candidate: Green, Orange, Yellow

- Apply `TIERS.md` (v1.2 owner ladder): every product starts **YELLOW** (Kalo demand), graduates to **ORANGE** when no Meta competitor uses any of its top-10 Kalo videos (first-frame match, more frames when unsure), and to **GREEN** when a winning video is verified (Kalo orders + conversion + views, TrendTrack appeal). **WHITE** = potential, fails a hard gate.
- A list needs at least 3 Greens: keep pulling Kalo candidates until it has them. Never promote without proof.

### Step 12 — Sheet output

Build the sheet from `templates/sheet-layout.md`:

- Tab 1 **Template**: 10 names, LINK cells to the Kalo URL, cost and score columns. Fill each name by tier: Green `#00FF00`, Orange `#FFA500`, Yellow `#FFFF00`, not tiered = no fill. Green fill only on verified Greens.
- Tab 2 **Candidates**: filter receipt on top, evidence table below.
- Also save one record per product using `templates/candidate-record.json`.

### Step 13 — Paused handoff

Only when there are 3 greens. The handoff contains:

- 3 products, 10 videos each, 30 creatives.
- `authorized_spend_usd = 0`
- `state = PAUSED/OFF`

Then stop. Research never launches, publishes or spends. A human decides what happens next.

## End-of-run report

Report in plain words: batch name, filter setup used, preflight states, 10 candidates with outcome and reason, greens or HOLD, sheet link, and every item still MISSING.
