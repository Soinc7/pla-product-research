# Tool alternatives: when a main tool is missing

The skill runs on five main tools. The preflight (`PREFLIGHT.md`) checks **every one of them on every run**. When one is missing, the agent does not skip it and does not guess. It follows the steps below.

| Main tool | What it proves in this skill | Where it is used |
|---|---|---|
| **Kalodata** ("Kalo") | TikTok Shop demand: 30-day revenue, price, commission, the top 10 videos with views and orders | Yellow tier, the winning-video bars for Green (`TIERS.md`) |
| **A 1688 route** (Fabulk, 1688order.com or 1688.com) | The factory item cost and MOQ | Cost on every row, launch math |
| **TrendTrack** | The 100K+ appeal video, competitor stores and their running ads | Green's appeal check, the Competitor Files |
| **Ad Library** | Whether competitors already run the product's Kalo videos | Orange and Green |
| **Google Trends** | Search interest over time | Shown on every row (not a tier gate) |

## What to do when one is missing

1. **Say exactly what is missing and what it blocks.** For example: "TrendTrack isn't connected, so no product can pass Green's appeal check, and the Competitor Files will have no stores or ads."
2. **Ask the owner first:** "Do you use another tool for this? Which one, and is it logged in in this Chrome?" Their answer wins.
3. **No answer, or they don't have one: search the web for current options** (for example "Kalodata alternative TikTok Shop analytics <current year>"). Show two or three with price, whether they need a login, and whether they give the same proof. Comparison pages are often written by one of the vendors; say so, and never pay or sign up for the owner.
4. **Record the choice** in `state/batch-N.json` as `tool_substitutes` (`{"kalo": {"use": "FastMoss", "proof": "PARTIAL", "note": "..."}}`) and mark that preflight check `PARTIAL` with the substitute named in its note.
5. **Keep the bars.** A substitute counts only for the proof it really gives. If it cannot show the same evidence (for example orders per video for the winning-video bars), that evidence is `PARTIAL` or `MISSING`, and the tier rules in `TIERS.md` don't change. Never lower a bar to fit a tool.
6. **No tool at all for Kalo or Chrome** is still a STOP: research can't start without product discovery and a browser. Every other missing tool lets the run continue, with what it blocks written into the end-of-run report.

## Starting list (checked 2026-11-21; verify before relying on it)

Prices and features change. Many comparison pages are written by one of the vendors, so treat their rankings as marketing. Check the vendor's own page and ask the owner before anything is bought.

| Missing tool | Alternatives to look at | Gives the same proof? |
|---|---|---|
| **Kalodata** | **FastMoss** (TikTok Shop analytics, strong on livestreams), **EchoTik** (lighter, quick product browsing), **Tabcut** (has an API) | Usually revenue and top videos per product. Check that it shows **orders per video** and **video IDs**; without them the winning-video bars stay `PARTIAL`. |
| **A 1688 route** | The three routes already in `PREFLIGHT.md` A (Fabulk with no login, 1688order.com, 1688.com). Also English buying agents such as **Sugargoo** (search 1688 in English, no Chinese account), or the owner's own 1688 account paid through WorldFirst World Pay. Alibaba.com prices are a reference only, never 1688 proof. | Yes for item cost, when the offer page shows price and MOQ. Agent prices may include their fee; note it. |
| **TrendTrack** | **PiPiADS** (TikTok and Facebook ads, large TikTok ad library), **Minea** (several networks incl. Pinterest; its free plan has no TikTok ad spy), **BigSpy** (cheap, shallower), **WinningHunter** (TikTok and Facebook ads plus Shopify sales tracking). Free, official: **TikTok Creative Center** (top ads and trending products), **Google Ads Transparency Center** (an advertiser's Google ads). | Appeal videos: usually yes (views per ad or video). Store revenue estimates differ by tool; mark them as that tool's estimate. |
| **Ad Library** | It is free and public, so it is rarely truly missing: try another Chrome or wait out a throttle (`AD-LIBRARY.md`). Paid ad-spy tools that index Ad Library ads (PiPiADS, Minea, BigSpy, WinningHunter) can help find competitors. | Partly. A spy tool's index is not the whole library, so "no competitor found" from it alone is `PARTIAL`; Orange still needs the Ad Library itself. |
| **Google Trends** | **Glimpse** (a Chrome extension on top of Google Trends that adds absolute volumes; small free plan), **Exploding Topics** (trend detection, paid with a limited free plan), **Pinterest Trends** (free) | Yes for the "shown, not a gate" trend line. |

Sources used for this list (2026-11-21, mostly vendor-written): SmartScout's Kalodata and FastMoss alternatives pages, EchoTik's Kalodata comparison, TrendTrack's Minea / PiPiADS comparison, WorldFirst and Sugargoo guides to buying from 1688, Glimpse's and Exploding Topics' Google Trends alternatives pages.
