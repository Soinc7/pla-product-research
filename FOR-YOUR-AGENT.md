# For your agent: what this skill is and how to use it

**Agent: read this file first, before `SKILL.md`.** It tells you what this skill does, what you get from it, and how it fits next to any product-research skill your owner already has.

## In one paragraph

`pla-product-research` finds TikTok Shop products worth testing on Meta. Each run hands your owner **10 ranked products** in a Google Sheet. Every claim in the sheet links to the exact source: Kalodata page, winning video, Meta Ad Library search, competitor ad, TrendTrack video, Google Trends and 1688 offer. Your owner can click any cell and check it. The skill is **read-only**: it never publishes, activates products, launches ads or spends money.

This repo holds the product researcher only. It does not include a store builder, launch system or ad-buying procedure.

## Save tokens: use sub-agents

If you can start sub-agents, read [`AGENTS.md`](AGENTS.md). You act as the host (preflight, tier decisions, sheet, read-back) and give cheap workers one lane each: Kalo discovery, Meta Ad Library sweep, 1688 pricing, TrendTrack. Pass file paths, not pasted data. If you cannot start sub-agents, run the lanes yourself in the same order.

## What your owner gets each run

**1. The draft sheet, "Product Research — Chapter C · Draft D".** It has 10 rows, ranked 1–10:

| Tier | Rank | What it means for picking |
|---|---|---|
| 🟢 GREEN | top ranks (e.g. 1–4) | Proven demand. No competitor on Meta is running its top Kalo videos. A winning video is verified on orders, conversion, views and appeal. **Pick from here first.** |
| 🟠 ORANGE | middle (e.g. 5–7) | Proven demand, and all 5 Meta Ad Library keyword searches show no competitor using its Kalo videos. No verified winning video yet. **Good backup.** |
| 🟡 YELLOW | bottom (e.g. 8–10) | Proven demand, but a competitor is already running its top videos on Meta. The cell links to that ad. **Riskier.** |

Key columns:
- **Sales per 1K views (not ROAS).** TikTok orders divided by video views, times 1,000, for the winning video. "0.62 / 1 per 1.6K" means about one sale every 1,600 views. It is a conversion signal, not a Meta ROAS forecast.
- **Competitor check.** Every product is searched with 5 different keywords (exact-phrase and unordered; brand, function and problem words). It must clear all 5 to be Orange or Green. The sheet lists all 5 keywords as clickable links with result counts, then the verdict: "✓ No competitor using the Kalo videos · N pages sell it", or "✗ N competitors run its Kalo videos" with each competitor's Ad Library link and which Kalo videos (#) they use. If Meta throttles the searches, the keywords are marked "re-check", never "no competitor".
- **Competitor file.** Opens that product's tab in the companion workbook (see 2).
- **1688 / Fabulk item cost (every row, Green, Orange and Yellow).** The item cost of the closest product found, labeled EXACT, CLOSE or SIMILAR, or "—" if none was found.
- **Est. delivered (standard).** Item cost + $5.00 flat, labeled "est." until a real supplier-agent quote replaces it. It ranks products. It never releases a Green by itself.

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
- Competitor check = 5 keywords, all must clear. Never conclude "no competitor" from a throttled Meta search.
- Run to completion once preflight says GO. A draft is done only when the sheet exists and has been read back.

## Quick start

```
Read FOR-YOUR-AGENT.md, then SKILL.md. Run the preflight only and tell me what is MISSING.
```

then

```
Run one pla-product-research batch with the default filter setup.
```
