# Report generator

Turns a research `report.json` into one self-contained HTML page and a Letter-size PDF of the ranked products. It needs no web artifacts and no internet: every product photo is embedded in the file.

## Run it

```
python3 tools/report/build_report.py examples/chapter1/report.json --out reports/chapter1-draft3
```

This writes `reports/chapter1-draft3.html` and `reports/chapter1-draft3.pdf`.

- `--out` is the output path without an extension. Default: `reports/<name of the JSON's folder>`.
- `--no-pdf` writes the HTML only.
- Needs Python 3 only. Pillow is optional (it shrinks photos larger than 640 px).
- The PDF is printed with headless Chrome. The script looks for `google-chrome`, `chromium`, `chromium-browser`, `msedge` (plus the standard Mac and Windows install paths), then Playwright. If none is found it writes the HTML, says so, and you can print it from any browser (Letter, background graphics on).

## What the page shows

1. Title bar and the **Intake** card (budget, demographic, price band, categories, research brief).
2. **How to read this**: the three tiers in one sentence each.
3. **Pick this first**: the Green 1 hero with its proof checklist and launch math, then a podium of the other Greens.
4. A scoreboard of every product against every gate.
5. One card per product. Green is large and saturated, Orange is medium and names what is missing, Yellow is muted and lists the competitors copying it.
6. Grading rules and the cost rule.

Ticks and crosses are worked out from the numbers, not from the tier label, so a weak number always shows.

## Launch math

Budget `B` = `intake.cbo_daily_budget_usd` (150 if missing).

| Number | Formula |
|---|---|
| Margin per sale | `price − est_delivered` |
| Break-even ROAS | `price ÷ margin` ("not profitable at this price" if margin ≤ 0) |
| Sales/day to break even | `B ÷ margin`, rounded up |
| Price for a 2.0 break-even ROAS | `2 × est_delivered` |
| Kalo orders per month | `rev ÷ price` |

It uses the TikTok price as reference; the store price and bundles change it. Ad fees, refunds and payment fees are not included. A **Watch-outs** line appears when margin ≤ 0 or break-even ROAS is above 3, when the factory match is `SIMILAR`, or when the rating is under 4.0.

## JSON fields

Top level: `title`, `date`, `source`, `est_rule`, `intake`, `products`.

`intake`: `cbo_daily_budget_usd`, `cbo_setup`, `demographic`, `price_band`, `categories`, `brief`.

Each item in `products`:

| Field | Meaning |
|---|---|
| `rank`, `tier`, `color` | Order, label ("GREEN 1") and `GREEN` / `ORANGE` / `YELLOW` |
| `name`, `variant`, `why` | Product name, variant, one-line reason |
| `image_file`, `img` | Local photo (path relative to the JSON file) and the remote photo URL |
| `price`, `rev`, `rating` | TikTok price, 30-day revenue, rating |
| `views`, `orders`, `cvr`, `per` | Winning video views and orders, sales per 1K views, views per sale |
| `topvid` | Views of the best appeal video ("—" if none) |
| `keywords` | Five items of `{q, url, results}` from the Meta Ad Library |
| `sellers`, `competitors` | Seller count, and `{name, ad, videos}` for each competitor using its Kalo videos |
| `item_txt`, `match`, `item_url`, `est_delivered` | Item cost, `EXACT` / `CLOSE` / `SIMILAR`, source link, estimated delivered cost |
| `kalo`, `video`, `competitor_file`, `trends` | Links |

Numbers such as "2.25M", "1.4k" and "2,300" are understood. "—" or a missing value counts as not proven.

## How images are embedded

For each product the script reads `image_file` (relative to the JSON file) and writes it into the HTML as a base64 `data:` URI. If the file is missing it downloads `img`. If that also fails it uses a neutral grey placeholder. The run prints a note for every product that did not use its local file. The finished HTML makes no network requests for images, CSS, fonts or scripts.
