# AGENTS.md: run the skill with several agents to save tokens

One expensive agent doing everything re-reads the same pages and the same rules again and again. Split the work instead: one **host** thinks and checks, several cheap **workers** each do one narrow lane and write a small file.

Works in Claude Code (Agent tool, run in background, cheaper model for workers), Codex, or any agent that can start sub-agents. If your agent cannot, run the lanes yourself one after another. Nothing else changes (see "Single-agent fallback").

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
| L1 | Kalo discovery + the top-10 video IDs per product | filter setup name, batch file | `lane-L1-kalo.json` | cheap | No. Browser, one owner |
| L2 | Meta Ad Library 5-keyword sweep per product, plus first-frame check | `lane-L1-kalo.json` | `lane-L2-meta.json` | cheap | No. Browser, one owner |
| L3 | 1688 / Fabulk item price and match label per product | `lane-L1-kalo.json` | `lane-L3-pricing.json` | cheap | No. Browser, one owner |
| L4 | TrendTrack: TikTok top videos, competitor stores and ads | `lane-L1-kalo.json` | `lane-L4-trendtrack.json` | cheap | Yes. API, no browser |
| L5 | Sheet and Competitor Files builder | all lane files | the Sheets (or local files) | cheap, host reviews | After L1-L4. No browser |

Parallel rules:
- **One Chrome owner at a time.** L1, L2 and L3 use the browser, so run them one after another. Run them side by side only if your agent tool gives each worker its own separate tab or profile.
- L4 uses an API (TrendTrack), so it runs alongside any browser lane.
- L2 and L3 need L1's output. L4 needs only L1's product names. Start L4 as soon as L1 finishes.
- Splitting one lane by product (for example L2 on products 1-5 and 6-10) is fine, but each piece writes its own file: `lane-L2-meta-a.json`, `lane-L2-meta-b.json`.

Output shapes are in `state/lanes.example.json`.

## Worker prompt template

Keep it this short. Paste it with the blanks filled in.

```
Task: <lane id and one line, e.g. "L2: Meta Ad Library 5-keyword sweep">
Rules: read SKILL.md hard rules and <the one lane doc, e.g. META-AD-LIBRARY.md>. Nothing else.
Input: <path, e.g. state/lane-L1-kalo.json>
Output: write <path, e.g. state/lane-L2-meta.json> matching the "<lane key>" shape in state/lanes.example.json.
Hard rules:
- Read-only. No publishing, no ads, no spending, no logins, no passwords.
- Login, CAPTCHA or consent wall: stop that item, mark it MISSING, continue.
- Every field is PROVEN, PARTIAL or MISSING. Never write 0 for unknown. Never invent a URL, price or number.
- Never stop the whole run for one product. Mark it and move on.
- Do not use the browser unless this lane says so. Do not open extra tabs.
Finish: write the output file, then reply with at most 10 lines: files written, counts, anything MISSING or RECHECK. Then exit.
```

## Token-saving rules

1. **Pass file paths, not pasted data.** The host says "read `state/lane-L1-kalo.json`", it does not paste the 10 products.
2. **Workers return 10 lines or fewer.** The detail lives in the JSON file.
3. **Store page extracts in `state/*.json`.** If a page was read once, the next lane reads the file, not the page again.
4. **Reuse cached Kalo cover images.** Save the image URL in `lane-L1-kalo.json`; do not reopen the Kalo page for a picture.
5. **Batch browser actions.** One tool call with several steps beats many small calls.
6. **Load only the lane's doc.** A Meta worker reads `META-AD-LIBRARY.md`, not the whole repo.
7. **The host checks, it does not redo.** Two spot-checked links per lane. If a lane is wrong, send the specific fix back to the same worker.
8. **Meta Ad Library throttle.** After about 40-50 searches the results can go to 0, even for queries that worked before. The L2 worker stops, waits 10 minutes or more, then resumes. Keywords searched during the throttle are marked `RECHECK`. Never conclude "no competitor" from a throttled search.

## Host steps

0. Intake (once). If `state/intake.json` exists, reuse it and read `state/feedback.md`. If not, ask the five intake questions in one message (`SKILL.md`, Step 0), show the 4-6 sentence brief, save `state/intake.json`, and start. Give every worker the intake path and the feedback rules that apply to its lane.
1. Preflight. GO or GO_LIMITED, else stop and report.
2. Open `state/batch-N.json`, pick the filter setup.
3. Start L1. When it finishes, check it has 10 products with video IDs.
4. Start L4 in the background. Start L2, then L3, one browser lane at a time.
5. Collect the files. Check each against the shape in `state/lanes.example.json`. Spot-check links.
6. Apply `TIERS.md`: L2 verdict `CLEAR` for Orange; Green needs the winning-video proof. `RECHECK` waits at Yellow.
7. Compute the launch math (`TIERS.md`) and rank the Greens with it.
8. Start L5, or write the sheet yourself. Read it back. Write `state/report.json` and build the local report (`tools/report/build_report.py`).
9. Write the end-of-run report. Update `state/batch-N.json`. Commit `state/intake.json` and `state/feedback.md` to the user's own repo copy.

## Single-agent fallback

No sub-agents? One agent runs the same lanes in the same order and writes the same `state/lane-*.json` files. The files are the work log, so a stopped run can resume from them (see the resume rule in `SKILL.md`, Step 2).

## What never changes with many agents

- Read-only: no publishing, no activation, no ads, no spend.
- The human does every login. No agent asks for or types a password.
- Fewer than 3 Greens means HOLD. Never lower the bar.
