# AGENTS.md: run the skill with several agents to save tokens

One expensive agent doing everything re-reads the same pages and the same rules again and again. Split the work instead: one **host** thinks and checks, several cheap **workers** each do one narrow lane and write a small file.

Works in Claude Code (Agent tool, run in background, cheaper model for workers), Codex, or any agent that can start sub-agents. If your agent cannot, run the lanes yourself one after another. Nothing else changes (see "Single-agent fallback").

**Use what the machine already has.** Before the lanes, the host runs `python3 tools/check_agents.py` (writes `state/agents.json`). Per lane it picks the owner's own agent if one covers the lane (the host asks the owner once before using it, and gives it the lane's rules and output path), else the bundled worker, else the built-in general-purpose agent briefed with the worker file. The host then asks the owner once: several sub-agents or one agent (`run_mode` in `state/intake.json`). With one agent, the host runs the lanes itself in the same order.

**Claude Code: ready-made.** `/pla-run` (`.claude/commands/pla-run.md`) is the host playbook, and `.claude/agents/` holds one worker per lane: `pla-kalo-worker` (L1), `pla-meta-worker` (L2), `pla-pricing-worker` (L3), `pla-trendtrack-worker` (L4), `pla-sheets-worker` (L5 writes). Start them with the Agent tool by name, in the background, with the file paths and the Chrome deviceId. Other agents can paste a worker file as its prompt. `tools/deliver.py` replaces the host's formatting work.

## Roles

**Host (overseer, strongest model).**
- Runs the preflight (`PREFLIGHT.md`) and picks the filter setup (`FILTER-SETUPS.md`).
- Splits the 10 candidates into lanes and gives each worker a file path, not pasted data.
- Merges the worker files, applies the tier rules (`TIERS.md`), writes the sheet, reads it back.
- Never redoes a worker's production. It verifies (spot-check 2 links per lane) and corrects.

**Workers (cheap model, Sonnet or Haiku class).** One lane each, disjoint inputs, one output file under `state/`, then exit. They follow every hard rule in `SKILL.md`.

## Lanes

| Lane | Job | Input | Output (in `state/`) | Model tier | Parallel? |
|---|---|---|---|---|---|
| L1 | Kalo discovery + the top-10 video IDs per product | filter setup name, batch file | `lane-L1-kalo.json` | cheap | Yes, in its own tab group (browser) |
| L2 | Meta Ad Library 5-keyword sweep per product, plus first-frame check | `lane-L1-kalo.json` | `lane-L2-meta.json` | cheap | Yes, in its own tab group (browser) |
| L3 | 1688 / Fabulk item price and match label per product | `lane-L1-kalo.json` | `lane-L3-pricing.json` | cheap | Yes, in its own tab group (browser) |
| L4 | TrendTrack: TikTok top videos, competitor stores and ads | `lane-L1-kalo.json` | `lane-L4-trendtrack.json` | cheap | Yes. API, no browser |
| L5 | Competitor Files data (TrendTrack) and the sheet / workbook writes, following `SKILL.md` Step 12 | `lane-L1-kalo.json`, then `state/report.json` | `lane-L5-compfiles.json`, the Sheets (or local files), `competitor-files-<chapter>.json` | cheap, host reviews | TrendTrack part right after L1; the writes after the merge. No browser |

Parallel rules:
- **Browser lanes share Chrome through their own tab groups.** L1, L2 and L3 use the browser. Run them side by side when your agent tool gives each worker its own tab group (Claude in Chrome does). A worker uses only tabs it opened and never touches another's. If your tool cannot separate tabs, run them one after another.
- **Name the Chrome by deviceId, never by label.** Labels such as "Browser 1" and "Browser 2" swap when a browser reconnects, and a session can silently move to the other device. The host writes the deviceId into `state/batch-N.json` and into every browser worker's prompt. Before each lane, run `list_connected_browsers`; if `inUse` moved, `select_browser <deviceId>` again. In Claude Code, sub-agents share the parent's Chrome device and tab group, so a device switch by one affects all of them: give each worker its own tab and the deviceId.
- **Never run two Meta lanes at once.** The Meta Ad Library throttle is per browser, Facebook session and network, and every agent on that Chrome shares it. Two Meta workers in one Chrome got 0 on their very first control search. Splitting L2 by product is fine only if the pieces run one after another.
- L4 uses an API (TrendTrack), so it runs alongside any browser lane. It can't start until L1 has product names; before that only TrendTrack's preflight can run.
- L2 and L3 need L1's output. Start L4 as soon as L1 finishes.
- Splitting one lane by product (for example L3 on products 1-5 and 6-10) is fine, but each piece writes its own file: `lane-L3-pricing-a.json`, `lane-L3-pricing-b.json`. A later re-check writes a new file (`lane-L2-meta-r2d.json`); `merge_lanes.py` reads every file and later files win.

Output shapes are in `state/lanes.example.json`.

**Video numbers.** "Kalo #n" means the n-th video in the product's "Video & Ad" tab, last 30 days, sorted by revenue, as L1 recorded it. Always store the video ID next to the number. Later lanes match on the ID, never on the number alone.

## Worker prompt template

Keep it this short. Paste it with the blanks filled in.

```
Task: <lane id and one line, e.g. "L2: Meta Ad Library 5-keyword sweep">
Rules: read SKILL.md hard rules and <the one lane doc, e.g. META-AD-LIBRARY.md>. Nothing else.
Input: <path, e.g. state/lane-L1-kalo.json>
Output: write <path, e.g. state/lane-L2-meta.json> matching the "<lane key>" shape in state/lanes.example.json.
Chrome (browser lanes only): deviceId <id>. Use only tabs you open, and close them when done.
Hard rules:
- Read-only. No publishing, no ads, no spending, no logins, no passwords.
- Login, CAPTCHA or consent wall: stop that item, mark it MISSING, continue.
- Every field is PROVEN, PARTIAL or MISSING. Never write 0 for unknown. Never invent a URL, price or number.
- Never stop the whole run for one product. Mark it and move on.
- Do not use the browser unless this lane says so. Do not open extra tabs.
Finish: write the output file, then reply with at most 10 lines: files written, counts, anything MISSING or RECHECK. Then exit.
```

## Token and time budget

Measured on the Chapter 2 run (2026-11-20/21) and given as a guide, not a promise:

| Lane | Rough cost | Time | Main lever |
|---|---|---|---|
| L1 Kalo, 10 products | most of a Kalo day's detail visits | 30-45 min | page extraction, not screenshots |
| L2 Meta | about 60-80K tokens per product (frame check included) | about 10 min per product without a throttle | one worker, paced searches, a poster grid instead of one screenshot per ad |
| L3 pricing, 10 products | small | 15-30 min | one extraction per results page |
| L4 TrendTrack, 6 products | about 250K tokens on Sonnet, 146 credits | about 5 min | Haiku, 10 results per call, 3 images per product at most |
| L5 sheet writes, 1 draft + 6 tabs | about 300K tokens (copying request bodies into the connector) | about 10 min | one worker, `tools/deliver.py` builds the bodies |
| Host merge + all outputs | near zero (scripts) | 1-2 min | `tools/deliver.py` |

The slow part is Meta's throttle. Never let it hold up a delivery: deliver with `RECHECK`, then re-check later into a new lane file.

## Token-saving rules

1. **Pass file paths, not pasted data.** The host says "read `state/lane-L1-kalo.json`", it does not paste the 10 products.
2. **Workers return 10 lines or fewer.** The detail lives in the JSON file.
3. **Store page extracts in `state/*.json`.** If a page was read once, the next lane reads the file, not the page again.
4. **Reuse cached Kalo cover images.** Save the image URL in `lane-L1-kalo.json`; do not reopen the Kalo page for a picture.
5. **Batch browser actions.** One tool call with several steps beats many small calls.
6. **Load only the lane's doc.** A Meta worker reads `META-AD-LIBRARY.md`, not the whole repo.
7. **The host checks, it does not redo.** Two spot-checked links per lane. If a lane is wrong, send the specific fix back to the same worker.
8. **Meta Ad Library throttle.** After about 40-50 searches the results can go to 0, even for queries that worked before, and it can come much sooner when other agents shared the same Chrome. The L2 worker searches the control keyword first. If the control is 0, it does nothing else: it stops, waits 10 minutes or more, and checks the control again. A throttle can last well over an hour (one on 2026-11-20 lasted from 22:27 to past 00:09 UTC); keep checking the control every 20-30 minutes and run no product searches meanwhile. Keywords searched during the throttle are marked `RECHECK`. Never conclude "no competitor" from a throttled search.

## Host steps

0. Intake (once). If `state/intake.json` exists, reuse it and read `state/feedback.md`. If not, ask the five intake questions in one message (`SKILL.md`, Step 0), show the 4-6 sentence brief, save `state/intake.json`, and start. Give every worker the intake path and the feedback rules that apply to its lane.
1. Preflight. GO or GO_LIMITED, else stop and report.
2. Open `state/batch-N.json`, pick the filter setup. Starting a new chapter? First move the last batch's lane files into `state/archive/batch-N/` (`state/README.md`, rule 7), because the merge reads every lane file in `state/`.
3. Start L1. When it finishes, check it has 10 products with video IDs.
4. Start L4 in the background. Start L2, then L3. Browser lanes may run side by side when each worker has its own tab group in the same logged-in Chrome (Claude in Chrome gives each agent its own group). Never touch another agent's tabs.
5. Collect the files. Check each against the shape in `state/lanes.example.json`. Spot-check links.
6. Apply `TIERS.md`: L2 verdict `CLEAR` for Orange; Green needs the winning-video proof. `RECHECK` waits at Yellow.
7. Compute the launch math (`TIERS.md`) and rank the Greens with it.
8. Start L5, or write the sheet yourself. Merge the lane files: `python3 tools/report/merge_lanes.py --title "Product Research · Chapter C · Draft D"` (writes `state/report.json`, applies `TIERS.md`). Build the local report: `tools/report/build_report.py`. Build the web page: `tools/report/build_page.py`. Build the sheet requests: `python3 tools/sheets/build_sheet.py state/report.json --tab "Chapter C · Draft D" --out state/sheet`. Send its parts with a Sheets connector. Then read the sheet back and check the draft against `STANDARD.md`.
9. Write the end-of-run report. Update `state/batch-N.json`. Commit `state/intake.json` and `state/feedback.md` to the user's own repo copy (`git init` first if the copy is not a git repo). Never push to the original repo.

## Single-agent fallback

No sub-agents? One agent runs the same lanes in the same order and writes the same `state/lane-*.json` files. The files are the work log, so a stopped run can resume from them (see the resume rule in `SKILL.md`, Step 2).

## What never changes with many agents

- Read-only: no publishing, no activation, no ads, no spend.
- The human does every login. No agent asks for or types a password.
- Fewer than 3 Greens means HOLD. Never lower the bar.
