# Sheet layout

One Google Sheet per batch. Title = the batch name. Two tabs.

## Tab 1 — "Template" (range A1:R11)

Row 1 is the header. Rows 2–11 are the 10 products in rank order.

| Col | Header | What goes in rows 2–11 |
|---|---|---|
| A | (product name) | The 10 names, A2:A11 |
| B | (link) | The word `LINK` as a rich hyperlink to the product's Kalo URL, B2:B11 |
| C | Pictures | Product picture. Kalo's image host blocks Google Sheets `=IMAGE()` (shows #REF!), so use `=HYPERLINK("<image url>","PHOTO")` |
| D | Amazon Link | Link, if found. Leave blank if not. Never invent. |
| E | COGS | All-in delivered cost, USD |
| F | Selling Price | Planned sale price, USD |
| G | (spacer) | Empty |
| H | Gross Profit % | From E and F |
| I | Margin $ | F minus E |
| J | Perceived Value | Score 0–5 |
| K | Problem Solving | Score 0–5 |
| L | Emotional problem | Score 0–5 |
| M | Proven Sales Demand | Score 0–5 |
| N | Appeals To Impulse Purchasers | Score 0–5 |
| O | Content | Score 0–5 |
| P | Evergreen | Score 0–5 |
| Q | Brandable | Score 0–5 |
| R | Notes | Outcome, reason, what is missing |

Formatting:

- Header row: fill `#5B95F9`, bold, 12 pt.
- Tier fill on the **name cell**: Green `#00FF00`, Orange `#FFA500`, Yellow `#FFFF00`, not tiered = no fill (see `TIERS.md`).
- Green fill only on verified Greens. A HOLD batch can still show Orange and Yellow.
- Unknown values: leave the cell empty or write `MISSING`. Never write 0 for unknown.

Notes on this layout:

- The header text for columns A and B is not recorded in the source (UNKNOWN). Proposed: "Product" and "Link".
- Formulas for H and I are not recorded. Proposed: `I = F − E`, `H = I ÷ F`.
- Enter COGS in column E only from an exact delivered quote. If you only have an estimate, put it in Notes and mark it as an estimate.

## Tab 2 — "Candidates"

Top of the tab: the **FILTER RECEIPT** (`templates/filter-receipt.md`).
Below it: one evidence row per candidate.

The source fixes the receipt-above-headers rule but not the exact evidence headers. The columns below are **proposed**. They follow `templates/candidate-record.json`.

| Group | Columns |
|---|---|
| Identity | Rank, Product name, Target group, Kalo product ID, Kalo detail URL, Result page, Result rank |
| Kalo metrics | Price low, Price high, Commission %, 30d revenue, 30d orders, 90d revenue, 90d orders, 30d video revenue, 30d video units |
| Videos | Video ID 1 … Video ID 10, Video evidence state |
| Shop | Shop top-10 snapshot (link or note) |
| 1688 | 1688 source status, Offer ID(s), CNY price, MOQ, FX rate, FX date, Item-only USD, Excluded charges, Match status |
| Supplier agent | Type (QUOTE / ESTIMATE), Delivered low, Delivered base, Delivered high, Method, Quote date, Inclusions |
| Green evidence | TrendTrack, Google Trends, Meta Ad Library, Buyer age, Store-age cohorts, Current trend (each PROVEN / PARTIAL / MISSING) |
| Decision | Gate results, Score /100, Day-one label, Fatal risk, Outcome, Reason, To clear |
