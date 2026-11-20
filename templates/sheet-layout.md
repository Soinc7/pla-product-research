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
| D | Tier | GREEN n / ORANGE / YELLOW chip. White bold on `#1E8E3E` / `#E37400` / `#B08800` |
| E | Kalo | `HYPERLINK(product URL,"Open Kalo ↗")` |
| F | Price | Kalo list price, $0.00 |
| G | 30-day revenue | $0.0K |
| H | Rating | 0.0★. Red if under 4.0 |
| I | Winning video | `HYPERLINK(Kalo video URL,"<views> views · <orders> orders ↗")` |
| J | Orders per 1K views | 0.00. Red if under 0.6 |
| K | Meta Ad Library | `HYPERLINK(exact search URL used,"Search ↗")` |
| L | Competitor using a Kalo top-10 video | Yellow rows: `HYPERLINK(https://www.facebook.com/ads/library/?id=<Library ID>,"<Brand> ↗ copies Kalo #n")`, bold red. Others: "None found ✓" |
| M | TrendTrack appeal | `HYPERLINK(TikTok video URL,"<views> · <what it is>")`. Mark ✗ if under 100K or off-product |
| N | Google Trends | `HYPERLINK(trends explore URL, 3-month US, keyword,"Trends ↗")` |
| O | 1688 / Fabulk item cost | `HYPERLINK(offer URL,"$x · match ↗")`, or "—" |
| P | Why | One crisp line, 60 characters or fewer. Fill `#E6F4EA` / `#FEF0E0` / `#FFF8D6` by tier |

Body: Arial 10, wrapped, vertically centered. Banded rows `#FFFFFF` / `#F7F9FA`, with a thin bottom border `#D9DEE3`. Links in `#1155CC`.

**Photos:** Sheets shows "Some formulas are trying to send and receive data from external parties". The file owner must click **Allow access** once, or the IMAGE cells show #REF!. The agent never clicks it; tell the owner. When building from an .xlsx upload, write the IMAGE formulas after conversion with the Sheets API (USER_ENTERED), because they don't survive conversion.

## Tab 2 — "Top videos"
Product · Tier chip · Video #1–#3 as `HYPERLINK(Kalo video URL,"<views> views · <orders> orders ↗")` · note on the frame check.

## Tab 3 — "How it was graded"
Step · what was checked · bar to pass. Covers demand, the no-copycat check, the winning video, cost (a flag) and Google Trends (shown, not scored).

## Rules
- Unknown = "—" or MISSING. Never 0.
- Green chip only on verified Greens.
- Every claim in K–O must be a clickable link to the exact search, ad, video or offer that was used.
- No 0–5 score columns. Evidence columns replaced them in v2.
