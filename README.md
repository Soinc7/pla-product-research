# pla-product-research

A research skill for an AI agent (Claude, Codex, or a GitHub agent).
It finds TikTok Shop products worth testing, checks the real factory price on 1688, gets a delivered-cost estimate from the supplier agent, and writes the result to a Google Sheet.

It is **read-only**. It never publishes, activates products, launches ads, or spends money.

## What it does

1. Checks that your tools work (the preflight). No tools, no research.
2. Uses Kalodata ("Kalo") to find 10 candidate products with a named filter setup.
3. Proves each one has 10 real product videos.
4. Finds the exact same product on 1688 to get the factory price (the "counter price").
5. Gets a delivered-to-US cost from the supplier agent ("Aria").
6. Applies the cost gate: all-in cost under $8, sale value $30 or less.
7. Scores each product on 8 points.
8. Checks Meta Ad Library: competitor brands, how long their ads have run, and whether the top Kalo videos are already running as ads.
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

## Run a batch

Tell your agent:

```
Read SKILL.md. Run one batch with the default filter setup.
```

To pick a different filter setup, name it. All setups are in `FILTER-SETUPS.md`.
A Kalodata trial account allows 10 searches and 10 detail visits a day, so a batch can take more than one day.

## What you get

- A Google Sheet with two tabs:
  - **Template** — 10 products, links, cost, price, margin, 8 scores. Up to 3 names filled green.
  - **Candidates** — the filter receipt (exactly which filters ran) and the evidence for every product.
- One of two results:
  - **3 greens** plus a handoff note. The handoff is always paused, with spend set to $0.
  - **HOLD**, with a list of what is missing for each product.

HOLD is a normal, correct result. The skill never lowers the bar and never invents a third product.

## Files

| File | Use |
|---|---|
| `SKILL.md` | Agent entry point. The full run procedure. |
| `PREFLIGHT.md`, `preflight/` | The tool and safety check. |
| `FILTER-SETUPS.md` | Every filter setup, with names and steps. |
| `PRICING-1688-ARIA.md` | Factory price and delivered-quote method. |
| `META-AD-LIBRARY.md` | Competitor and reference-video check. |
| `TIERS.md` | Green / Orange / Yellow rules. |
| `DRAFT-RUN-D36.md` | Live draft run on the last real batch (Draft 36). |
| `templates/` | Record schema, filter receipt, sheet layout. |
| `TEST-RUN.md` | A worked dry run on 10 real past candidates. |
| `CHANGELOG.md` | Version history. |
