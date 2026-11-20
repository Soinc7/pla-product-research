# Changelog

## v1.0.0 — 2026-11-20

First standalone export for partner use.

**Source**

- The source skill `pla-product-research`, last changed 2026-08-31 (core rules: batch record, gates, scoring, sheet layout, handoff).
- Draft 36 practice, 2026-10-03 (last real run: discovery filters, supplier-agent delivered estimate, 1688 status column).
- Green qualification rules from Draft 32, 2026-09-16.
- Kalodata how-to, proven 2026-11-05.

**Added in this export**

- Preflight tool and safety check with PROVEN / PARTIAL / MISSING results and a small evaluator script.
- Filter setups collected in one file, with proposed short codes shown beside the original sheet labels.
- 1688 exact-match and supplier-agent quote method written as steps.
- Dry test run on the 10 Draft 36 products.

**Removed for sharing**

- Machine names, account IDs, store names and domains, and all secrets.

**Known gaps**

- See "UNKNOWN" notes in `SKILL.md`, `FILTER-SETUPS.md` and `TEST-RUN.md`. They are open questions for the owner, not defects to guess around.

## 1.0.1 — 2026-11-20
- Chrome PARTIAL now STOPs (evaluator + docs).
- Added check F: supplier-agent (Aria) quote channel.
- Added `state/batch-N.json` batch state + resume rule; partner numbering starts at 1.
- Test run: revenue gate shown as undecided (video revenue only); video evidence shown as PARTIAL.
- Marked photo search, storefront rule and 2-factory minimum as PROPOSED.
- Picked as winner of a Fable 5.2 vs Opus 5.5 bake-off with cross-rebuttal.

## 1.1.0 — 2026-11-20
- Added `META-AD-LIBRARY.md`: exact-phrase keyword search, competitor brands grouped and counted, oldest active ad, cloned copy, and matching the Kalo top-3 videos against running Meta video ads. Competition bands NONE / LIGHT / HEALTHY / CROWDED / SATURATED.
- Added `TIERS.md`: GREEN (top) > ORANGE (second) > YELLOW (third) > not tiered, with sheet fills #00FF00 / #FFA500 / #FFFF00. Band and cost thresholds are PROPOSED defaults the owner can change.
- SKILL.md: new Step 7b (Meta check required for any tier); Step 11 now tiers every candidate.
- Added `DRAFT-RUN-D36.md`: live draft run on Draft 36, with 0 Green / 1 Orange / 5 Yellow / 4 not tiered; the batch result is HOLD.

## 1.2.0 — 2026-11-20
- TIERS.md rewritten to the owner's ladder: Yellow (Kalo demand) → Orange (top-10 Kalo videos not used on Meta, first-frame + extra-frame check) → Green (winning video: Kalo orders, conversion, views + TrendTrack appeal). White = potential. Minimum 3 Greens per list; cost and crowding shown as flags, not gates.
- Added LIST-2026-11-20-PROVISIONAL.md: 2 Green / 4 Orange / 2 Yellow / 2 White, flagged NEEDS_MORE_CANDIDATES until a fresh Kalo pull.

## 1.2.1 — 2026-11-20
- Added `LIST-2026-11-20.md`, a live run: Kalo logged in, Meta first-frame check against the Kalo top-10 videos, TrendTrack appeal check. Result: 3 Green, 2 Orange, 3 Yellow, 2 White, so the 3-Green minimum is met.
- Marked `LIST-2026-11-20-PROVISIONAL.md` as superseded.

## 1.2.2 — 2026-11-20
- Screened both Whites. The Azocek inverter passes Kalo (2.8k / 3.01M / 0.93), TrendTrack (800k) and the Meta check, so it is Green 4. The bathroom organizer fails the TrendTrack appeal check, so it is Orange. The list is now 4 Green, 3 Orange, 3 Yellow.
- 1688 check blocked: no Chrome profile is logged into 1688.

## 1.3.0 — 2026-11-20
- **1688 no longer stops a run.** Check A is now "1688 price route (any one)": Fabulk (fabulk.com, no login), 1688order.com (free account) or 1688.com (logged in). If none works, the agent asks the user to log in or make a free account on one, keeps doing discovery, Meta and TrendTrack, and holds pricing only. The evaluator has a new `missing_blocks: false` flag, so a missing 1688 route gives GO_LIMITED, not STOP.
- PRICING-1688-ARIA.md, SKILL.md, README.md and PREFLIGHT.md updated with the 3 routes and Fabulk photo search (camera icon, upload the Kalo main photo).
- LIST-2026-11-20.md: item prices from Fabulk. Dryer vent $2.58 (exact photo), windshield $7.31 (close), inverter $17.40–18.29 (generic close). Work light not found, so it needs an Aria quote.

## 1.4.0 — 2026-11-20
- **Run-to-completion rules** (SKILL.md hard rules 8–10): never pause for "go"; a draft counts as done only when the next-numbered Draft sheet is in Drive and has been read back; one stalled product never blocks the batch. On an early stop, the agent still writes and delivers what it has.
- sheet-layout.md: Kalo images can't be embedded in Sheets, so column C uses `HYPERLINK(...,"PHOTO")`.
- Delivered "Product Research Draft 37" (Google Sheet, same folder as Draft 36): 4 Green, 3 Orange, 3 Yellow.

## 1.5.0 — 2026-11-20
- New sheet design (`templates/sheet-layout.md` v2, "Chapter" format): banner rows, real product photos via `IMAGE(url,1)`, tier chips, and clickable proof columns for Kalo, the winning video, the Meta search, the competitor ad (by Library ID), TrendTrack, Google Trends and 1688/Fabulk. The "Why" line is short and crisp. The 0–5 score columns are dropped.
- Delivered "Product Research — Chapter 1 · Draft 1" (4 Green / 3 Orange / 3 Yellow). Photos need the owner's one-time "Allow access" click in Sheets.
