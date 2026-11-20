# pla-product-research

A research skill for an AI agent (Claude, Codex, or a GitHub agent).
It finds TikTok Shop products worth testing, checks the real factory price on 1688, gets a delivered-cost estimate from the supplier agent, and writes the result to a Google Sheet.

It is **read-only**. It never publishes, activates products, launches ads, or spends money.

> **Agents start here → [`FOR-YOUR-AGENT.md`](FOR-YOUR-AGENT.md).** It explains in one page what this skill does, what it hands back (10 ranked products plus competitor files), and how to use it next to a product researcher you already have.

## Getting access

Clone the repo. If it's private for you, ask the owner to add your GitHub username as a collaborator and accept the email invite first.

```
git clone https://github.com/Soinc7/pla-product-research.git
```

Then tell your agent: `Read FOR-YOUR-AGENT.md, then SKILL.md, and run the preflight only.`

## What it does

1. Checks that your tools work (the preflight). No tools, no research.
2. Uses Kalodata ("Kalo") to find 10 candidate products with a named filter setup.
3. Proves each one has 10 real product videos.
4. Finds the exact same product on 1688 to get the factory price (the "counter price").
5. Shows a price on every row: 1688 / Fabulk item cost (EXACT / CLOSE / SIMILAR) plus an estimated delivered cost (item + $5.00 flat) until the supplier agent gives a real quote.
6. Applies the cost gate: all-in cost under $8, sale value $30 or less.
7. Scores each product on 8 points.
8. Checks Meta Ad Library with **5 different keywords** per product (all 5 must clear for Orange or Green): competitor brands, how long their ads have run, and whether the top Kalo videos are already running as ads.
9. Sorts every product into **Green** (best), **Orange** (second) or **Yellow** (third). If fewer than 3 are Green, the batch result is **HOLD**.
10. Writes a sheet and a paused handoff note.

## The 3 tools you need

| # | Tool | Why |
|---|---|---|
| 1 | A **1688 price route**, any one of: **Fabulk** (fabulk.com, no login needed), **1688order.com** (free account) or **1688.com** (logged in) | Shows factory price and MOQ. With no route, the run keeps going and pricing waits |
| 2 | **Google Chrome** that your agent can drive (for example Claude in Chrome, or Playwright attached to your real logged-in Chrome) | The agent reads Kalo and 1688 through it |
| 3 | **Kalodata**, logged in | Product discovery and video evidence |

Also needed for output: Google Sheets / Drive access.
Needed later to release a green (not to start): TrendTrack, Google Trends, Meta Ad Library.

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
A Kalodata trial account allows 10 searches and 10 detail visits a day, so a batch can take more than one day.

## What you get

- **Product Research — Chapter C · Draft D**: 10 products ranked 1–10 (GREEN → ORANGE → YELLOW), with a product photo and clickable proof for every claim. Tabs: the draft, Top videos, How it was graded.
- **Competitor Files — Chapter C · Draft D**: one tab per product with competitor stores, their running Meta ads and hooks, top TrendTrack TikTok videos, and a reference photo.
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
| `TIERS.md` | Green / Orange / Yellow rules. |
| `DRAFT-RUN-D36.md` | Live draft run on the last real batch (Draft 36). |
| `templates/` | Record schema, filter receipt, sheet layout. |
| `TEST-RUN.md` | A worked dry run on 10 real past candidates. |
| `CHANGELOG.md` | Version history. |
