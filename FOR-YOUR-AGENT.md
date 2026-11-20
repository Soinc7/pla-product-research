# For your agent: what this skill is and how to use it

**Agent: read this file first, before `SKILL.md`.** It tells you what this skill does, what you get from it, and how it fits next to any product-research skill your owner already has.

## In one paragraph

`pla-product-research` finds TikTok Shop products worth testing on Meta. Each run hands your owner **10 ranked products** in a Google Sheet. Every claim in the sheet links to the exact source: Kalodata page, winning video, Meta Ad Library search, competitor ad, TrendTrack video, Google Trends and 1688 offer. Your owner can click any cell and check it. The skill is **read-only**: it never publishes, activates products, launches ads or spends money.

This repo holds the product researcher only. It does not include a store builder, launch system or ad-buying procedure.

## What your owner gets each run

**1. The draft sheet, "Product Research — Chapter C · Draft D".** It has 10 rows, ranked 1–10:

| Tier | Rank | What it means for picking |
|---|---|---|
| 🟢 GREEN | top ranks (e.g. 1–4) | Proven demand. No competitor on Meta is running its top Kalo videos. A winning video is verified on orders, conversion, views and appeal. **Pick from here first.** |
| 🟠 ORANGE | middle (e.g. 5–7) | Proven demand, and no competitor is copying its videos. It has no verified winning video yet. **Good backup.** |
| 🟡 YELLOW | bottom (e.g. 8–10) | Proven demand, but a competitor is already running its top videos on Meta. The cell links to that ad. **Riskier.** |

Key columns:
- **Sales per 1K views (not ROAS).** TikTok orders divided by video views, times 1,000, for the winning video. "0.62 / 1 per 1.6K" means about one sale every 1,600 views. It is a conversion signal, not a Meta ROAS forecast.
- **Competitor check.** On every row it shows the Meta Ad Library search that was run, and who is copying, if anyone.
- **Competitor file.** Opens that product's tab in the companion workbook (see 2).
- **1688 / Fabulk cost.** The factory price for the exact matching item, or "—" if none was confirmed.

**2. "Competitor Files — Chapter C · Draft D".** This workbook has one tab per product, and each tab lists:
- the competitor stores selling it, with price, estimated 30-day revenue and active ads
- their running Meta ads, with preview, days running, reach and **hook text** to use as script ideas, plus the landing page
- the top TrendTrack TikTok videos for the product, with views and hooks
- a reference product photo for making custom images

**3. The end-of-run report.** The tier counts, what is still MISSING, and a paused handoff. A batch with fewer than 3 Greens ends as **HOLD**, which is a correct result. The skill never invents a product to fill a slot.

## If your owner already has a product researcher

Do not replace or edit it. Install this as a **separate** skill named `pla-product-research`, and keep both. Use whichever mode your owner asks for:

| Mode | Prompt your owner gives you | What happens |
|---|---|---|
| **Standalone** | "Run pla-product-research, one batch, default filters." | Full run with discovery. You get 10 ranked products, both sheets and the report. |
| **Second opinion** | "Grade my list with pla-product-research tiers." | Use this skill's tier ladder (`TIERS.md`, `META-AD-LIBRARY.md`) on the products your own researcher found. Each product needs a Kalodata product page; without one it stays WHITE, marked MISSING. *This is a usage pattern built from the existing steps, not a separate tested procedure.* |
| **Side by side** | "Run both and compare." | Run each skill on its own and put both lists in one table. Show where they agree, and keep each skill's own verdict. Neither skill may change the other's grade. |

## What it needs

1. **Kalodata**, logged in by the human.
2. **Google Chrome** your agent can drive, with one agent on it at a time.
3. **One 1688 route:** Fabulk (no login), 1688order.com (account) or 1688.com (logged in). A missing route never stops the run; pricing just waits.
4. **Google Sheets / Drive** access for the output.
5. To verify Greens: **TrendTrack**, **Meta Ad Library** and **Google Trends**.

## Rules you must keep (full list in `SKILL.md`)

- Never ask for, type or store passwords, keys or codes. The human does every login.
- Evidence is PROVEN, PARTIAL or MISSING. Never write 0 for an unknown, and never invent a URL, price or sales number.
- Run to completion once preflight says GO. A draft is done only when the sheet exists and has been read back.

## Quick start

```
Read FOR-YOUR-AGENT.md, then SKILL.md. Run the preflight only and tell me what is MISSING.
```

then

```
Run one pla-product-research batch with the default filter setup.
```
