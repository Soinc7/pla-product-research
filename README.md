# pla-product-research

A research skill for an AI agent (Claude, Codex, or a GitHub agent).
It finds TikTok Shop products worth testing, checks the real factory price on 1688, gets a delivered-cost estimate from the supplier agent, and writes the result to a Google Sheet.

It is **read-only**. It never publishes, activates products, launches ads, or spends money.

> **Agents start here → [`FOR-YOUR-AGENT.md`](FOR-YOUR-AGENT.md).** It explains in one page what this skill does, what it hands back (10 ranked products plus competitor files), and how to use it next to a product researcher you already have.

## Getting access

Clone the repo. If it's private for you, ask the owner to add your GitHub username as a collaborator and accept the email invite first.

**Agents: check access first.** `curl -s -o /dev/null -w '%{http_code}' https://github.com/Soinc7/pla-product-research` prints 200 when the repo is public to you and 404 when it is private. On a private repo a plain `git clone` does not fail: it hangs on a login prompt until your tool times out. Clone so it fails fast instead:

```
git -c credential.helper= -c core.askPass= clone https://github.com/Soinc7/pla-product-research.git
```

While the repo is private, git needs your GitHub login, and an agent can't type it for you. Sign in once yourself with the GitHub CLI, then clone:

```
gh auth login --hostname github.com --git-protocol https --web
gh auth setup-git
```

No GitHub CLI? Install it first (`winget install --id GitHub.cli -e` on Windows, `brew install gh` on Mac), and open a new terminal afterwards.

**Copying through a GitHub connector instead.** If your agent has a GitHub connector signed in to an account with access, it can copy the files without git:

1. Copy everything into one folder that becomes your repo root (a `git clone` would make a `pla-product-research/` subfolder; the connector copy does not).
2. List each folder through the connector and download every file from its `download_url`. That link carries a token that expires within a minute or two, so list a folder and download its files right away, folder by folder.
3. Some files are binary (the JPG photos in `examples/` and the PDF in `reports/`). A text read can't copy those; the `download_url` can.
4. Check your copy against `MANIFEST.txt` (path, size and git blob hash of every file).
5. The copy is not a git repo. Run `git init` and commit if you want history. Never push to the original repo.

**Windows:** run the scripts with `python` (or `py -3`). On Windows, `python3` usually opens the Microsoft Store instead.

Then tell your agent: `Read FOR-YOUR-AGENT.md, then SKILL.md, and run the preflight only.`

## What it does

0. Asks you once for the daily CBO budget, CBO setup, target buyer, price band and things to avoid, then saves it in `state/intake.json`. Later runs reuse it and apply your past corrections from `state/feedback.md`.
1. Checks that your tools work (the preflight). No tools, no research.
2. Uses Kalodata ("Kalo") to find 10 candidate products with a named filter setup.
3. Proves each one has 10 real product videos.
4. Finds the exact same product on 1688 to get the factory price (the "counter price").
5. Shows a price on every row: 1688 / Fabulk item cost (EXACT / CLOSE / SIMILAR) plus an estimated delivered cost (item + $5.00 flat) until the supplier agent gives a real quote.
6. Checks Meta Ad Library with **5 different keywords** per product (all 5 must clear for Orange or Green): competitor brands, how long their ads have run, and whether the top Kalo videos are already running as ads.
7. Sorts every product into **Green** (best), **Orange** (second) or **Yellow** (third). If fewer than 3 are Green, the batch result is **HOLD**.
8. Works out the launch math for every product at your daily budget (margin, break-even ROAS, sales/day, the price for a 2.0 ROAS) and ranks Greens by it.
9. Writes the sheet, the Competitor Files workbook, a web page and a local PDF/HTML report.
10. Before any launch handoff (never part of research): the cost gate (delivered quote under $8), the 8-point score and the day-one floor in `SKILL.md`, Steps 7-10. The handoff stays paused with $0 spend.

## The 3 tools you need

| # | Tool | Why |
|---|---|---|
| 1 | A **1688 price route**, any one of: **Fabulk** (fabulk.com, no login needed; browser only, scripts get 403), **1688order.com** (free account) or **1688.com** (logged in) | Shows factory price and MOQ. With no route, the run keeps going and pricing waits |
| 2 | **Google Chrome** that your agent can drive (for example Claude in Chrome, or Playwright attached to your real logged-in Chrome) | The agent reads Kalo, Meta Ad Library and 1688 through it |
| 3 | **Kalodata**, logged in | Product discovery and video evidence |

Also needed for output: Google Sheets / Drive access.
Needed later to release a green (not to start): TrendTrack, Google Trends, Meta Ad Library.

| Extra tool | What it is | How to connect | Cost |
|---|---|---|---|
| **TrendTrack** | trendtrack.io: TikTok videos, Shopify stores and Meta ads by keyword. Proves the "appeal" video for a Green and fills the Competitor Files. | Its MCP connector in your agent (tools such as `search_tiktok_library`, `search_products`, `search_ads`, `get_product_ads`, `check_credits`). | Paid credits, about 2 per returned item. A 6-product Competitor Files pass used about 150. Run `check_credits` before and after. |
| **Meta Ad Library** | facebook.com/ads/library, public | Any browser | Free, but throttles (see `META-AD-LIBRARY.md`) |
| **Google Trends** | trends.google.com, public | Any browser | Free |

## 5-minute onboarding

1. Clone this repo where your agent can read it.
2. Open Chrome yourself. Log in to **1688** and **Kalodata** by hand. The agent never types or sees your passwords.
3. Connect your agent's browser tool to that Chrome. Use one agent on Chrome at a time.
4. Give your agent Google Sheets / Drive access.
5. Tell your agent: `Read SKILL.md and run the preflight only.`
6. Fix anything it reports as MISSING. Each check comes with the exact fix. See `PREFLIGHT.md`.

## Save tokens with several agents

The skill can run as a host plus cheap workers, one lane each. See [`AGENTS.md`](AGENTS.md). It works in Claude Code, Codex or any agent that can start sub-agents, and falls back to one agent if yours cannot.

## Run a batch

Tell your agent:

```
Read SKILL.md. Run one batch with the default filter setup.
```

To pick a different filter setup, name it. All setups are in `FILTER-SETUPS.md`.
A Kalodata trial account allows 10 searches and 10 detail visits a day, so a batch can take more than one day. The Basic plan shows at most 500 result rows.

## What you get

Chapter 2 · Draft 1 is the owner-approved reference for all of these (`STANDARD.md`).

- **Product Research — Chapter C · Draft D**: 10 products ranked 1–10 (GREEN → ORANGE → YELLOW), with a product photo and clickable proof for every claim. Tabs: the draft, Top videos, How it was graded.
- **Competitor Files — Chapter C · Draft D**: one tab per product with competitor stores, their running Meta ads and hooks, top TrendTrack TikTok videos, and a reference photo.
- **A web page** of the draft: summary band (HOLD under 3 Greens), the Green 1 pick with its proof checks and a launch-ready seal, Orange cards that lead with what's missing, muted Yellow rows flagged "Copied on Meta", and launch math on every product. Built with `python3 tools/report/build_page.py state/report.json --out reports/<chapter>-<draft>-page`.
- A local report (PDF + HTML, photos embedded) in `reports/`, built with `python3 tools/report/build_report.py state/report.json --out reports/<chapter>-<draft>`.
- An end-of-run report: **3+ Greens** plus a paused handoff (spend $0), or **HOLD** with what's missing per product.

HOLD is a normal, correct result. The skill never lowers the bar and never invents a third product.

## Files

| File | Use |
|---|---|
| `FOR-YOUR-AGENT.md` | One-page brief for an agent: what this does, outputs, modes. Read first. |
| `AGENTS.md` | Host and worker lanes to save tokens. |
| `SKILL.md` | The full run procedure. |
| `PREFLIGHT.md`, `preflight/` | The tool and safety check. |
| `FILTER-SETUPS.md` | Every filter setup, with names and steps. |
| `PRICING-1688-SUPPLIER.md` | Factory price and delivered-quote method. |
| `META-AD-LIBRARY.md` | Competitor and reference-video check. |
| `TIERS.md` | Green / Orange / Yellow rules, plus the launch math that ranks Greens. |
| `CLAUDE.md` | Short brief for Claude Code users. |
| `state/` | The skill's memory in your own copy: `intake.json`, `feedback.md`, batch and lane files, `report.json`. |
| `STANDARD.md` | The draft checklist. Every draft must pass it before delivery. |
| `tools/report/merge_lanes.py` | Merges the lane files into `state/report.json` and applies `TIERS.md`. Later lane files win, so a re-check replaces an older verdict. |
| `tools/report/build_report.py` | Builds the local PDF and HTML report from `state/report.json`. |
| `tools/report/build_page.py` | Builds the draft web page (`templates/draft-page.html`) from `state/report.json`. |
| `tools/sheets/build_sheet.py` | Turns `state/report.json` into Drive and Sheets API request files. |
| `tools/sheets/competitor_links.py` | Links column M of a draft tab to its Competitor Files tabs. |
| `MANIFEST.txt` | Path, size and git blob hash of every file, to check a connector copy. |
| `reports/` | Where built reports are written. |
| `DRAFT-RUN-D36.md` | Live draft run on the last real batch (Draft 36). |
| `templates/` | Record schema, filter receipt, sheet layout, `intake.json`, `feedback.md`. |
| `TEST-RUN.md` | A worked dry run on 10 real past candidates. |
| `CHANGELOG.md` | Version history. |
