---
name: pla-product-research
description: Read-only TikTok Shop product research. Runs a tool preflight, finds 10 candidates on Kalodata with a named filter setup, proves 10 exact-product videos each, checks Meta Ad Library with 5 keywords for competitors running the Kalo videos, prices the closest 1688 / Fabulk item, and grades every product Green / Orange / Yellow (3+ Greens or HOLD) with budget launch math. Delivers a Google Sheet, a Competitor Files workbook, a web page and a PDF report. Use when asked to run product research, a research batch or draft, a Kalo screen, a Meta competitor check, a 1688 price check, or a preflight for these tools.
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
9. **A draft is done only when the deliverables exist: the sheet (if Sheets access exists), the local report and the web page.** Done means: the next-numbered draft sheet (named as in Step 1) is in the same Drive folder as the last one, with all 10 rows, tier fills and the three tabs in `templates/sheet-layout.md`, and it has been read back. If the owner gives a name or folder, use it. On a first run with no folder named, use My Drive root and say so in the end-of-run report. A chat summary or repo file alone is not a delivered draft.
10. **Never block on one product.** If one product's 1688 match, Meta check or TrendTrack check stalls, mark that field MISSING with the reason, keep going with the rest, and finish the sheet.

## Outcome words

| Word | Meaning |
|---|---|
| GREEN / ORANGE / YELLOW | The research tier from `TIERS.md` (v1.3 ladder). WHITE = a potential that fails a hard gate or has incomplete evidence. |
| HOLD | A draft with fewer than 3 Greens, or a field whose evidence is missing or not yet matched. Can be cleared later. |
| FAIL | A hard gate is failed on real evidence |
| BATCH_FILTERED | Outside this batch's price band. Not rejected forever. |

The launch gate (Steps 7-10: delivered quote under $8, 75/100 score, day-one floor) is separate. It must pass before the paused handoff in Step 13, and it never changes a research tier.

## Run procedure

### Step 0 — Intake (once, before any search)

Look for `state/intake.json`. If it exists, reuse it and **do not ask again**. Also read `state/feedback.md` and apply every rule in it to this draft. Only redo the intake if the user says the buyer or the budget changed.

If there is no `state/intake.json`, ask the user **in one message**, before opening any page:

1. Daily CBO budget the products will launch with (if they say "default": **$150/day**).
2. CBO setup name (default: **Flash Plus CBO**).
3. Target buyer / demographic.
4. Price band and categories (default: the filter setup's).
5. Anything to avoid.

Optional, in the same message: which supplier agent quotes delivered cost (default: none, so rows use the +$5.00 estimate).

Also in the same message, the run setup:

6. **Sub-agents or one agent?** First run `python3 tools/check_agents.py`. It lists the agents and skills this machine already has and picks a worker per lane: the owner's own agent if one covers the lane, else the bundled `pla-*` worker, else the built-in general-purpose agent briefed with the worker file. Show that plan and ask: "Run with several sub-agents (lanes in parallel, faster, each on a cheaper model) or one agent (simpler, slower)?" If the owner has their own agent for a lane, ask whether to use it. If your agent cannot start sub-agents, say so and use one agent. Default: several sub-agents when available.
7. **Drive folder** for the Sheets (a link or id; default My Drive root, and say so).

Save the answers as `run_mode`, `use_owner_agents` and `drive_folder_id` in `state/intake.json`, so later runs don't ask again. If the owner already has a product-research skill (`check_agents.py` reports it), keep it and offer the side-by-side or second-opinion modes in `FOR-YOUR-AGENT.md`.

Then write a **rough-draft paragraph of 4-6 sentences**: what kind of 10 products you intend to find for that buyer and budget. Show it to the user and **start the hunt**. Do not wait for approval unless the user asked to approve first.

Save `state/intake.json` from `templates/intake.json` (fields: `cbo_daily_budget_usd`, `cbo_setup`, `demographic`, `price_band`, `categories`, `avoid`, `brief`, `created`, plus `breakeven_roas_max` (default 3), `sale_value_max` (default 30), `supplier_agent` (default "none"), `run_mode`, `use_owner_agents` and `drive_folder_id`).

**Price band vs sale value.** The intake price band sets the Kalo price filter. The sale-value rule still applies: a product whose perceived sale value is above `sale_value_max` is WHITE. If the owner's band goes higher (for example $10-$40), raise `sale_value_max` to match, with their OK.

**Memory in the repo.** `state/intake.json` and `state/feedback.md` live in the user's own copy of this repo. Commit both to their fork or clone at the end of the run. If your copy is not a git repo (for example it was copied through a connector), run `git init` and commit locally, or keep the files and say so in the end-of-run report. Never push to the original owner's repo. When the owner corrects a draft, add a row to `state/feedback.md` (date, correction, rule it became; template `templates/feedback.md`). Every later draft reuses the saved intake and applies all earlier corrections. See `state/README.md`.

The budget feeds the launch math in `TIERS.md`, which ranks the Greens.

### Step 0b — Preflight

Follow `PREFLIGHT.md`. Record each check as PROVEN / PARTIAL / MISSING.
Any MISSING on **Chrome or Kalo** = STOP. Report the exact fix and end the run.

**1688 never stops the run.** Use any one route: **Fabulk** (fabulk.com, no login), **1688order.com** (free account) or **1688.com** (logged in). If none works, ask the user to log in or make a free account on one of them, keep doing discovery, Meta and TrendTrack, and hold pricing.

### Step 1 — Open the batch record

- Name the batch `Product Research Batch N`. Your own numbering: your first batch is N = 1. Read the last N from `state/` (highest `batch-N.json`); if none exists, N = 1. Older "Product Research Draft" titles do not advance N.
- Owner-facing names: each batch is a **Chapter**, and each delivered version of it is a **Draft** ("Product Research — Chapter C · Draft D"). A fresh 10-product hunt starts a new chapter at Draft 1. A correction or re-check of the same 10 products is the next draft of the same chapter. If the owner names the draft, their name wins. Write the mapping in `state/batch-N.json` (`report_name`, e.g. `chapter2-draft1`).
- Record the Chrome you use by its **deviceId** (from `list_connected_browsers`) in `state/batch-N.json`. Browser labels such as "Browser 1" change when a browser reconnects; the deviceId does not.
- Create `state/batch-N.json` from `templates/batch-state.json`. Update it after every page, every Kalo detail visit and every quote request.
- Record: `observed_at_utc`, `region`, `currency`, `account_check` (`MATCH`, `MISMATCH` or `NOT_CHECKED`). Never store the account ID itself.
- Pick the filter setup from `FILTER-SETUPS.md`. Default: **AVD-36**.
- Note whether N is odd or even and write the price-cap code (`ODD_BATCH_80_CAP` or `EVEN_BATCH_60_CAP`). See `FILTER-SETUPS.md` for when the cap applies.
- Start the filter receipt from `templates/filter-receipt.md`. Fill it as you go.

### Step 2 — Kalo discovery

- Content type is **TikTok Shop product videos**. Lives are excluded and never counted.
- **Drive Kalo through its UI only.** Its internal API needs a region header that page scripts don't send, so direct calls silently return Singapore data. The exact clicks are in `FILTER-SETUPS.md` ("How to enter any setup in Kalo"). **Apply** only stages a filter; **Submit** runs it.
- Enter the chosen filter setup exactly. Write every value you actually entered into the receipt. If a filter is not available on your plan, write `NOT_APPLIED`, do not pretend.
- Go through **all result pages your plan shows** (the Basic plan stops at 500 rows; record the rest as `NOT_READ (plan limit)`). For every product you keep, record result page and rank.
- Record the **direct product-detail URL**. Pattern:
  `https://www.kalodata.com/product/detail?id=<ID>&region=US&currency=USD&language=en-US`
- Capture the 30-day window (revenue and orders). The 90-day window is optional for a research draft: record it when the detail page is already open. It is required before a launch handoff.
- Mind the plan limits noted in preflight. On a trial, plan the batch across days instead of skipping checks. Kalo can log itself out mid-run; if it does, the human logs in again and you resume.
- **Resume rule:** when a run stops (daily limit, waiting on a quote, session end), save `state/batch-N.json` and stop. Next run: rerun preflight, open the same `batch-N.json`, continue from `next_step`. Never restart a batch or repeat a done step.
- **Moving to another computer mid-batch.** Save `state/*` (batch, lane and intake files), `reports/<run>/images/` and the Chrome deviceId, and note `next_step` in `batch-N.json`. Lane files may hold half-done work tied to one Chrome's tabs: mark those items `RECHECK`. On the new computer, copy the files in, rerun the preflight, then resume.

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
- Sales screen (only for filter setups that list one; AVD-36 does not): 30-day video revenue of $20,000 or more, 300 or more video-attributed units, 10 same-product video references. The winning-video bars for Green are in `TIERS.md` Step 3.
- To save a clip: row thumbnail → preview → "Download". Link `/video/detail` pages in outputs, but do **not** open them for data (blank player).
- **Video IDs.** The Video & Ad table shows no IDs on the page; they are in the table's own data (the page's network response). Store every video as `n` (its revenue order) plus its ID. Public image patterns: video cover `https://img.kalocdn.com/tiktok.video/<VIDEO_ID>/cover.png`, product photo `https://img.kalocdn.com/tiktok.product/<PRODUCT_ID>/cover.png`. Some covers return 404; then use the Kalo row thumbnail or `https://www.tiktok.com/player/v1/<VIDEO_ID>`.
- Fewer than 10 valid videos = that evidence is PARTIAL and the product is WHITE (`TIERS.md` Step 1).

### Step 5 — 1688 exact-match factory price (the "counter price")

Follow `PRICING-1688-SUPPLIER.md`, part A.
Short version: find the **exact** product and variant through any 1688 route (Fabulk photo search first: camera icon, upload the Kalo main photo), compare several independent factories, record offer ID, CNY price, FX date and what the price excludes.
The research row always shows the closest item found (`EXACT`, `CLOSE` or `SIMILAR`). No exact match = no launch handoff yet (`HOLD` for launch); it never changes the research tier.

### Step 6 — Supplier-agent delivered estimate

Follow `PRICING-1688-SUPPLIER.md`, part B.
Until a real quote exists, show "Est. delivered (standard)" = item cost + $5.00 flat on every row. It ranks, it never releases a Green.
Record low / base / high delivered-to-US cost in USD and the method.
An item-only 1688 price is **not** a delivered quote.

### Step 7 — COGS gate

> **Which rule sets the tier?** The research tier (Green / Orange / Yellow) comes from `TIERS.md` (v1.3 ladder). Steps 7-10 are the **launch gate**: they must all pass before the paused handoff in Step 13. An estimate-only cost never blocks a research Green and never releases a launch.

| Gate | Rule |
|---|---|
| All-in COGS | Below **$8** per unit, after supplier uplift and logistics. $10 is a stretch ceiling, not a pass. |
| Sale value | Perceived sale value at or below `sale_value_max` (default **$30**) |
| Proof | An exact delivered quote below $8. No such quote = no launch handoff (the research tier is unchanged). |

`supplier_landed_cost_usd` is its own field. It is never copied from the Kalo price.

### Step 7b — Meta Ad Library check (required for Orange or Green)

Run `META-AD-LIBRARY.md` for every candidate: **5 different keywords** (mix exact-phrase and unordered; a product must clear all 5 to be Orange or Green), competitor brands grouped and counted, oldest active ad, cloned copy, and the first frames of the product's top 10 Kalo videos matched against running video ads. Record the competition band (`NONE` / `LIGHT` / `HEALTHY` / `CROWDED` / `SATURATED`); it is shown, not a tier gate. Not run, or any keyword throttled (`RECHECK`) = the product stays Yellow and cannot be Orange or Green yet. Never conclude "no competitor" from a throttled search, and never run two Meta lanes at once.

### Step 8 — Launch evidence checklist (launch gate, not the research tier)

A launch handoff needs all of these for the exact product. Any one missing = no handoff (`HOLD` for launch). None of them changes the research tier from `TIERS.md`.

| Evidence | Rule |
|---|---|
| Sources | Kalo, 1688, TrendTrack, Google Trends checked; Meta Ad Library band `HEALTHY` (see `META-AD-LIBRARY.md`) |
| Buyer age | Purchasers proven 45+, better 55+ or 65+, with conversion data (period and sample). Search interest or creator audience is not proof. Target buyer = `intake.demographic`. |
| Store-age cohorts | Real store creation dates for 30-day and 180-day cohorts. Product first-seen dates and ad start dates do not count. |
| Current trend | Recent vs prior Kalo video revenue and units, plus monthly seasonal search |
| URLs | Complete for every claim |
| Fatal risk | None |
| Day-one floor | Projected seasonal day-one floor met (see below) |

Tie-break preference: favor products that convert very well and whose 1688 cost makes them a good fit for a paid membership (VIP) offer.

### Step 9 — Scoring

- 8 dimensions, each 0–5, each with evidence. The launch gate needs **75/100 or more** (the research tier does not use this score).
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

- Apply `TIERS.md` (v1.3 owner ladder, then the launch math to rank inside each tier): every product starts **YELLOW** (Kalo demand), graduates to **ORANGE** when no Meta competitor uses any of its top-10 Kalo videos (first-frame match, more frames when unsure), and to **GREEN** when a winning video is verified: **one** video passes all three Kalo bars (orders, conversion, views), plus a TrendTrack appeal video of the same product. **WHITE** = potential, fails a hard gate.
- A list needs at least 3 Greens: keep pulling Kalo candidates until it has them. Never promote without proof.

### Step 11b — Launch math

For each product compute the launch math in `TIERS.md` using the saved intake budget. Rank Greens by it (lower break-even ROAS first), after they pass every gate. A weak result (margin <= 0 or break-even ROAS above `breakeven_roas_max`) is a watch-out, and the report says what price or bundle fixes it.

### Step 12 — Outputs
Every run delivers: (1) the Google Sheet below, if Sheets access exists, (2) the Competitor Files workbook, (3) the local report (Step 12b) and (4) the web page (Step 12c). Chapter 2 · Draft 1 is the reference for all four (`STANDARD.md`).

**One command builds all of it:** `python3 tools/deliver.py --chapter C --draft D --source "<filter setup> · US · <window>"` runs the merge, saves the photos, builds the report, the page, the sheet requests, the Competitor Files tabs and the column M links, and prints the send order. The rest of this step explains what it does; in Claude Code the `pla-sheets-worker` sends the files.

Names: replace C and D with the chapter and draft numbers from `report_name` in `batch-N.json` (`chapter2-draft1` → "Chapter 2 · Draft 1").

**Merge first.** Every output reads `state/report.json`, which the merge writes from the lane files and `TIERS.md`:

```
python3 tools/report/merge_lanes.py --title "Product Research · Chapter C · Draft D" --source "<filter setup> · US · <window>"
```

The format is in `FOR-YOUR-AGENT.md` (reference `examples/chapter1/report.json`). The merge also reads `state/host-overrides.json` (the host's short names, variants and Trends keywords per product) and `state/competitor-files*.json` (the Competitor Files tab links); both are described in `state/README.md`.

**Competitor Files workbook** ("Competitor Files — Chapter C", same Drive folder, one tab per product):

1. The L4 TrendTrack lane gathers the data per product (`search_products` with an AND query such as "faucet + cover", `search_ads` / `get_product_ads`, `search_tiktok_library`) into `state/lane-L4-trendtrack.json` (older runs used a separate `lane-L5-compfiles.json`; both are read). Only rows for the same product; look-alikes are `UNCERTAIN`.
2. `python3 tools/sheets/build_competitor_tabs.py state/report.json --out state/compfiles-chC-dD [--spreadsheet-id <id> | --new-workbook "Competitor Files — Chapter C"]` (run by `tools/deliver.py`) writes the tab bodies, laid out as in `templates/sheet-layout.md` ("Companion workbook"), named `T<rank> · <short name>`. A product with nothing found gets a "none found: <query> returned <what>" line, never a blank tab.
3. After sending them, save the tab links as `state/competitor-files-chC.json` (`{"spreadsheet_id": "...", "tabs": [{"rank", "pid", "title", "sheetId", "gid_url"}]}`) and run `tools/deliver.py` again: the merge fills `competitor_file`, and `competitor_links.py` writes column M (`3-competitor-links.json`, sent to `values:batchUpdate`).

Build the sheet from `templates/sheet-layout.md` (v2.1), three tabs:

- Tab 1 **Chapter C · Draft D**: the 10 ranked rows, columns A-Q. Fill each name by tier: Green `#00FF00`, Orange `#FFA500`, Yellow `#FFFF00`, not tiered = no fill. Green fill only on verified Greens. Tier chips in column D use the darker `#1E8E3E` / `#E37400` / `#B08800`.
- Tab 2 **Top videos** and Tab 3 **How it was graded**.
- The filter receipt is saved as `state/filter-receipt-batch-N.md`, not as a tab.
- Also save one record per product using `templates/candidate-record.json`.

`python3 tools/sheets/build_sheet.py state/report.json --tab "Chapter C · Draft D" --out state/sheet` writes the request bodies. Column K holds 5 links in one cell, which needs a raw Sheets `batchUpdate` (`textFormatRuns`). If your Sheets connector has no raw batchUpdate tool, send the bodies through a proxy call (for example Composio `COMPOSIO_PROXY_EXECUTE`); see `templates/sheet-layout.md`.

### Step 12b — Local report (PDF + HTML)

From the merged `state/report.json`, run:

```
python3 tools/report/build_report.py state/report.json --out reports/<chapter>-<draft>
```

It writes a self-contained HTML (photos embedded) and a PDF. Download each product's main Kalo photo into `reports/<run>/images/` first (or let the builder fetch it) so no image is ever missing.

### Step 12c — Web page

```
python3 tools/report/build_page.py state/report.json --out reports/<chapter>-<draft>-page
```

It writes `index.html` (opens locally) and `page.html` (the same page without the html/head/body wrapper) plus `img/1.jpg` ... `img/10.jpg`. If your agent can publish a web page (for example a Claude Artifact), publish `page.html` with the `img/` files and send the owner the link. Otherwise share `index.html` with its `img/` folder. Check every draft against `STANDARD.md` before delivery.

### Step 13 — Paused handoff

Only when there are 3 greens. The handoff contains:

- 3 products that passed the launch gate (Steps 7-10), each with its 10 Kalo video IDs: the 30 reference videos the creatives will be made from. Research makes no creatives itself.
- `authorized_spend_usd = 0`
- `state = PAUSED/OFF`

Then stop. Research never launches, publishes or spends. A human decides what happens next.

## End-of-run report

Report in plain words: the intake used (budget, buyer), batch name, filter setup used, preflight states, 10 candidates with outcome and reason, greens or HOLD, sheet link, Competitor Files link, web page link, report path, the launch-math watch-outs, and every item still MISSING or RECHECK.
