# Sheet layout (v2 — "Chapter" format, 2026-11-20)

One Google Sheet per draft, named `Product Research — Chapter C · Draft D`, saved in the same Drive folder as the last draft. Reference build: Chapter 1 · Draft 1.

## Tab 1 — "Chapter C · Draft D"

**Banner rows (merged A:P)**
1. Title, Montserrat 16 bold white on `#1F4E3D`.
2. Date · Kalo filter and window · tier counts · cost status, Montserrat 10 white on `#2F6F56`.
3. Tier legend in one line, italic 9, grey `#F1F3F4`.

**Row 4 headers:** Montserrat 10 bold white on `#2F6F56`, centered and wrapped, with a medium bottom border. Freeze at D5.

| Col | Header | Content |
|---|---|---|
| A | # | Rank (narrow) |
| B | Picture | `=IMAGE("<Kalo product image URL>",1)`. Row height 96. Column ~118 px |
| C | Product | Short name · key variant. Montserrat bold |
| D | Tier | Ranked 1–10 across the whole draft: `GREEN 1`…, then `ORANGE n`…, then `YELLOW n`… down to the last row (e.g. 4G/3O/3Y → GREEN 1–4, ORANGE 5–7, YELLOW 8–10). White bold on `#1E8E3E` / `#E37400` / `#B08800` |
| E | Kalo | `HYPERLINK(product URL,"Open Kalo ↗")` |
| F | Price | Kalo list price, $0.00 |
| G | 30-day revenue | $0.0K |
| H | Rating | 0.0★. Red if under 4.0 |
| I | Winning video | `HYPERLINK(Kalo video URL,"<views> views · <orders> orders ↗")` |
| J | Sales per 1K views (not ROAS) | Kalo orders ÷ video views × 1,000 for the winning video. Show `0.62` and on a second line `1 per 1.6K` (one sale per that many views). It is a TikTok conversion signal, never a Meta ROAS prediction. Red if under 0.6 |
| K | Meta Ad Library | `HYPERLINK(exact search URL used,"Search ↗")` |
| L | Competitor check (Meta Ad Library) | Every row must show the check was done. Yellow rows: `HYPERLINK(https://www.facebook.com/ads/library/?id=<Library ID>,"<Brand> ↗ copies Kalo #n")`, bold red. Green and Orange rows: `HYPERLINK(<exact Meta search URL used>,"Checked ✓ none copying ↗")` — never plain text |
| M | Competitor file | `HYPERLINK(<Competitor Files sheet>#gid=<product tab>,"Open file ↗ · top video <views>")`. Opens that product's tab in the Competitor Files workbook (see below), not a single TikTok video |
| N | Google Trends | `HYPERLINK(trends explore URL, 3-month US, keyword,"Trends ↗")` |
| O | 1688 / Fabulk item cost | `HYPERLINK(offer URL,"$x · match ↗")`, or "—" |
| P | Why | One crisp line, 60 characters or fewer. Fill `#E6F4EA` / `#FEF0E0` / `#FFF8D6` by tier |

Body: Arial 10, wrapped, vertically centered. Banded rows `#FFFFFF` / `#F7F9FA`, with a thin bottom border `#D9DEE3`. Links in `#1155CC`.

**Photos:** Sheets shows "Some formulas are trying to send and receive data from external parties". The file owner must click **Allow access** once, or the IMAGE cells show #REF!. The agent never clicks it; tell the owner. When building from an .xlsx upload, write the IMAGE formulas after conversion with the Sheets API (USER_ENTERED), because they don't survive conversion.

## Companion workbook — "Competitor Files — Chapter C · Draft D"
Same folder. One tab per product, named `T<rank> · <short name>` (rank = the number in column D). Each tab:
1. Banner: tier label + product name; A2 = `Open Kalo ↗`.
2. **Competitor stores** — store, product-page link, price, est. 30-day revenue, active Meta ads, note (TrendTrack `search_products`, AND query "a + b").
3. **Their running Meta ads** — preview `IMAGE(thumbnail,1)`, advertiser, days running, reach/spend, hook text (script idea), Watch video, Ad Library link by Library ID, landing page (TrendTrack `search_ads` / `get_product_ads`).
4. **TrendTrack top TikTok videos** — up to 10, preview, creator, views, likes, hook/caption, engagement, open link (`search_tiktok_library`, `keyword_mode:"all"`, `search_area:"caption"`). Say so when none reach 100K.
5. **Reference photo** — the Kalo main product image, for custom PLA images alongside the previews above.
IMAGE formulas go in after the .xlsx converts (Sheets API, USER_ENTERED), and need the owner's Allow access click like tab 1.

## Tab 2 — "Top videos"
Product · Tier chip · Video #1–#3 as `HYPERLINK(Kalo video URL,"<views> views · <orders> orders ↗")` · note on the frame check.

## Tab 3 — "How it was graded"
Step · what was checked · bar to pass. Covers demand, the no-copycat check, the winning video, cost (a flag) and Google Trends (shown, not scored).

## Rules
- Unknown = "—" or MISSING. Never 0.
- Green chip only on verified Greens.
- Every claim in K–O must be a clickable link to the exact search, ad, video or offer that was used.
- No 0–5 score columns. Evidence columns replaced them in v2.
