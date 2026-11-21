# The draft standard (set by Chapter 2 · Draft 1)

Every delivered draft must pass every check below. **Chapter 2 · Draft 1** (2026-11-20, owner-approved) is the reference for the sheet, the Competitor Files, the web page and the report. Its outputs live in the owner's Drive and web page, not in this repo. To see the same design from shipped data, build it from the example: `python3 tools/report/build_page.py examples/chapter1/report.json --out reports/example-page` (page) and `python3 tools/report/build_report.py examples/chapter1/report.json --out reports/example` (report). Shipped examples: `examples/chapter1/report.json` with its photos, and `reports/chapter1-draft3.*` (a later rebuild of Chapter 1, whose Draft 2 was the first reference). The host checks each item at read-back and marks it PASS, FAIL or N/A, with the reason. A draft with any FAIL is not delivered until it's fixed or the FAIL is shown as a watch-out.

## A. The list
- [ ] A1. Exactly 10 products, ranked 1-10, ordered GREEN → ORANGE → YELLOW. Inside Green, the lowest break-even ROAS comes first.
- [ ] A2. Every tier has its proof (`TIERS.md`). There are at least 3 Greens, or the batch says HOLD / NEEDS_MORE_CANDIDATES. No Green without a verified winning video.
- [ ] A3. Nothing on the intake avoid-list, and no repeat of a product from an earlier chapter (earlier chapters' Kalo product IDs go into `avoid` in `intake.json`; see `state/README.md`).

## B. Every product row or card shows
- [ ] B1. A product photo (embedded or local file; never a broken remote link).
- [ ] B2. The tier label and its color: Green `#00FF00`, Orange `#FFA500`, Yellow `#FFFF00`.
- [ ] B3. Name and variant.
- [ ] B4. TikTok price, 30-day revenue and rating.
- [ ] B5. Winning video: views and orders, linked to the video.
- [ ] B6. Sales per 1K views, plus "1 per N views", labeled "not ROAS".
- [ ] B7. 1688 / Fabulk item cost, linked to the offer, with EXACT / CLOSE / SIMILAR (or "—" if not found).
- [ ] B8. Est. delivered = item cost + $5.00, labeled as an estimate.
- [ ] B9. The Meta Ad Library check: all 5 keywords, each a clickable search link with its result count. Throttled keywords show "re-check", never 0.
- [ ] B10. The verdict line. Either "✓ No competitor using the Kalo videos · N pages sell it", or "✗ N competitors run its Kalo videos" with each competitor's Ad Library link and which Kalo videos (# and video ID) it uses.
- [ ] B11. Links: Open Kalo, Competitor file (with top video views), Google Trends.
- [ ] B12. A one-line "Why" that explains the tier.

## C. Launch math (at the intake budget)
- [ ] C1. Margin, break-even ROAS, sales/day to break even at the CBO budget, and the price needed for a 2.0 break-even ROAS, on every product.
- [ ] C2. Weak math (margin ≤ 0, or break-even ROAS above `breakeven_roas_max`) is shown as a watch-out with the price or bundle fix, never hidden.

## D. The page or report
- [ ] D1. Intake card: budget, CBO setup, buyer, price band, categories and the brief.
- [ ] D2. A tier legend: what Green, Orange and Yellow mean, one sentence each.
- [ ] D3. Green looks like the pick (hero, stacked proof, launch-ready seal). Orange says what is missing. Yellow is muted, with a red "copied on Meta" warning.
- [ ] D4. A footer with the grading rules and the cost rule (+$5.00 estimate).
- [ ] D5. Works with no network: photos embedded, PDF and HTML both built.
- [ ] D6. Web page built with `tools/report/build_page.py` (the Chapter 2 · Draft 1 design): a summary band with a HOLD flag when there are fewer than 3 Greens, the Green 1 hero with a launch-ready seal and stacked proof checks, Orange cards that lead with what is missing, muted Yellow rows with a red "Copied on Meta" flag naming the rivals, launch math on every product (watch-out when margin ≤ 0 or break-even ROAS is above the limit). Works at phone width and in light and dark mode.

## E. Delivery
- [ ] E1. Google Sheet "Product Research — Chapter C · Draft D" in the agreed Drive folder: 10 rows, tier fills, multi-link cells, read back after writing.
- [ ] E2. Competitor Files workbook: one tab per product (stores, running ads with hooks, top TikTok videos, reference photo).
- [ ] E3. Local report `reports/<chapter>-<draft>.pdf` and `.html`, opened and checked.
- [ ] E4. End-of-run report: intake used, filter setup, preflight states, the 10 outcomes, Greens or HOLD, links, watch-outs and every MISSING item.
- [ ] E5. Web page published (for example as a Claude Artifact) or `index.html` shared with its `img/` folder, and its link in the end-of-run report.

## F. Evidence rules (any breach = FAIL)
- [ ] F1. Every number and URL comes from a source page. Nothing invented. Unknown shows "—" or MISSING, never 0.
- [ ] F2. Evidence is rated PROVEN / PARTIAL / MISSING.
- [ ] F3. No passwords, keys, account IDs or personal emails anywhere in the outputs.
- [ ] F4. Read-only: nothing published, activated or spent.
