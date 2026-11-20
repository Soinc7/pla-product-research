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
- Added check F: supplier agent quote channel.
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
- PRICING-1688-SUPPLIER.md, SKILL.md, README.md and PREFLIGHT.md updated with the 3 routes and Fabulk photo search (camera icon, upload the Kalo main photo).
- LIST-2026-11-20.md: item prices from Fabulk. Dryer vent $2.58 (exact photo), windshield $7.31 (close), inverter $17.40–18.29 (generic close). Work light not found, so it needs a supplier-agent quote.

## 1.4.0 — 2026-11-20
- **Run-to-completion rules** (SKILL.md hard rules 8–10): never pause for "go"; a draft counts as done only when the next-numbered Draft sheet is in Drive and has been read back; one stalled product never blocks the batch. On an early stop, the agent still writes and delivers what it has.
- sheet-layout.md: Kalo images can't be embedded in Sheets, so column C uses `HYPERLINK(...,"PHOTO")`.
- Delivered "Product Research Draft 37" (Google Sheet, same folder as Draft 36): 4 Green, 3 Orange, 3 Yellow.

## 1.7.0 — 2026-11-20
- Added `FOR-YOUR-AGENT.md`, a one-page brief so a partner's agent knows what this skill does, what it returns (10 ranked products plus Competitor Files) and how to run it next to its own product researcher: standalone, second opinion or side by side.
- README: points agents to the brief first, adds a "Getting access" section for the private repo, and updates "What you get" to the Chapter format.

## 1.6.0 — 2026-11-20
- Tiers ranked 1–10 across the draft (GREEN 1–4, ORANGE 5–7, YELLOW 8–10 for a 4/3/3 draft).
- Column J renamed "Sales per 1K views (not ROAS)" with a "1 per N views" line, so it isn't read as Meta ROAS.
- Column L now links the Meta search for Green and Orange rows too ("Checked ✓ none copying ↗"), so the check is visible on every row.
- Column M now opens a per-product tab in a new companion workbook, "Competitor Files": competitor stores, their running Meta ads with hooks and landing pages, top TrendTrack TikTok videos and the Kalo reference photo.
- Applied to Product Research — Chapter 1 · Draft 1.

## 1.5.0 — 2026-11-20
- New sheet design (`templates/sheet-layout.md` v2, "Chapter" format): banner rows, real product photos via `IMAGE(url,1)`, tier chips, and clickable proof columns for Kalo, the winning video, the Meta search, the competitor ad (by Library ID), TrendTrack, Google Trends and 1688/Fabulk. The "Why" line is short and crisp. The 0–5 score columns are dropped.
- Delivered "Product Research — Chapter 1 · Draft 1" (4 Green / 3 Orange / 3 Yellow). Photos need the owner's one-time "Allow access" click in Sheets.

## v1.8.0 — 2026-11-20
- Added `AGENTS.md`: host and worker lanes (Kalo, Meta sweep, pricing, TrendTrack, sheet builder) so several cheaper agents can share a run and save tokens. Includes a short worker prompt, token-saving rules and a single-agent fallback. Linked from README, SKILL.md and FOR-YOUR-AGENT.md. Added `state/lanes.example.json` with the lane output shapes.
- New competitor standard: every product is searched with 5 different Meta Ad Library keywords (exact-phrase and unordered). It must clear all 5 to be Orange or Green. The sheet shows all 5 keywords as links with counts, then a verdict line, with each competitor's Ad Library link and the Kalo videos (#) it uses. Added the throttle rule (about 40-50 searches, pause 10+ minutes, mark `RECHECK`). Updated META-AD-LIBRARY.md, TIERS.md (v1.3), SKILL.md, sheet-layout.md and FOR-YOUR-AGENT.md.
- Prices on every row (Green, Orange, Yellow): item cost with an EXACT / CLOSE / SIMILAR label, plus "Est. delivered (standard)" = item cost + $5.00 flat until a real quote replaces it. Estimates rank products and never release a Green by themselves.
- Sheet banner: no "delivered quotes pending" text. The legend is now a row of colored chips.
- Cleaned for a public repo: removed personal and owner-specific names and details. The supplier-agent role is now just "supplier agent". The pricing file is now `PRICING-1688-SUPPLIER.md`. Batch name is now `Product Research Batch N`.

## v1.9.0 — 2026-11-20
- **Intake, once.** New SKILL.md Step 0: before any search, ask the 5 intake questions in one message (daily CBO budget, default $150; CBO setup, default "Flash Plus CBO"; buyer; price band and categories; things to avoid), show a 4-6 sentence brief and start the hunt. Saved to `state/intake.json` (new `templates/intake.json`). Also in FOR-YOUR-AGENT.md and AGENTS.md host steps.
- **Memory in the repo.** The intake is saved once in the user's own copy and reused. `state/feedback.md` (new `templates/feedback.md`) logs each owner correction and the rule it became; every later draft applies them. Both files are committed to the user's fork or clone. Explained in `state/README.md` and SKILL.md.
- **Launch math.** TIERS.md and FOR-YOUR-AGENT.md define margin, break-even ROAS, sales/day to break even and the price needed for 2.0 ROAS. Greens are ranked by lowest break-even ROAS; weak math (margin <= 0 or ROAS above `breakeven_roas_max`) is a watch-out with a price or bundle fix. PROPOSED default: `breakeven_roas_max` = 3.
- **Deliverables.** Each run gives the Google Sheet (if Sheets access exists) and a local PDF + HTML report from `tools/report/build_report.py`. `state/report.json` is the documented hand-off format (reference `examples/chapter1/report.json`).
- Added `CLAUDE.md` for Claude Code users. README files table updated.

## v1.9.1 — 2026-11-20 (Claude Code run-through fixes)
- README: how to log in to clone a private repo (`gh auth login`, `gh auth setup-git`, installing the GitHub CLI), and a connector fallback. Windows note: use `python` / `py -3`, because `python3` opens the Microsoft Store. The same note is in CLAUDE.md and PREFLIGHT.md.
- One rule for "no supplier agent". The research tier follows TIERS.md v1.3, and the +$5.00 estimate ranks products. SKILL.md Steps 7-10 are the launch gate before the Step 13 handoff. Updated the preflight checklist message, PREFLIGHT.md and a note in SKILL.md Step 7.
- SKILL.md Step 1: maps "Batch N" to the owner's "Chapter C · Draft D" names (`report_name` in `batch-N.json`).
- META-AD-LIBRARY.md: search a control keyword before the sweep and about every 15 searches to catch throttling.
- AGENTS.md: "Kalo #n" means revenue order on "Video & Ad"; always store the video ID too.
- `state/lanes.example.json`: added the L1 (Kalo) and L4 (TrendTrack) shapes, video IDs on competitors, and `media_type=video` in the Meta URLs.
- Chapter 1 example: the solar flood light re-check (no throttle) found Gladchaser running 2 of its Kalo videos. Rebuilt `reports/chapter1-draft3`.
