---
description: Run one pla-product-research draft end to end as the host, using the sub-agents this machine already has or the bundled ones
argument-hint: "chapter C draft D [filter setup, default AVD-36]   e.g. /pla-run chapter 3 draft 1"
---

You are the **host** of a pla-product-research run. Arguments: $ARGUMENTS
(No arguments: read the next chapter and draft from the last `state/batch-N.json`; first run = chapter 1 draft 1.)

You think, decide and check; workers do the browsing and API work. Keep your own context small: pass file paths, never pasted data, and let `tools/deliver.py` do all formatting.

## 0. Start (you, about 5 minutes)
1. Read `FOR-YOUR-AGENT.md` and the hard rules in `SKILL.md`. Don't load the other docs yourself; each worker loads its own lane doc.
2. **What this machine already has:** run `python3 tools/check_agents.py`. It writes `state/agents.json`: per lane, the owner's own agent if one covers it, else the bundled `pla-*` worker, else the built-in general-purpose agent briefed with the worker file. It also reports any product-research skill the owner already has: keep it, and offer the side-by-side or second-opinion modes in `FOR-YOUR-AGENT.md`.
3. **Intake, once** (`SKILL.md` Step 0). Reuse `state/intake.json` and apply `state/feedback.md`. Ask, in one message, only what is missing:
   - the five intake questions (first run only);
   - **run mode**: "Run with several sub-agents (lanes in parallel, faster, each on a cheaper model) or one agent (simpler, slower)?" Show the lane plan from step 2, and if it names an owner agent, ask whether to use it. If you cannot start sub-agents, say so and use one agent;
   - the **Drive folder** for the Sheets (default My Drive root, and say so).
   Save `run_mode`, `use_owner_agents` and `drive_folder_id` in `state/intake.json`.
4. **Preflight** (`PREFLIGHT.md`): `list_connected_browsers`, pick the logged-in Chrome by **deviceId**, check Kalo, the 1688 route, Sheets, TrendTrack `check_credits`, and the Meta control `"dryer vent"`. Write the states, the deviceId and the Kalo date window into `state/batch-N.json`. STOP only on Chrome or Kalo MISSING.
5. New chapter? First move the last batch's lane files into `state/archive/batch-N/` (`state/README.md`, rule 7).

## 1. Lanes
**Several sub-agents** (`run_mode` = multi): start the worker that `state/agents.json` names for each lane, in the background, with the exact output path, the intake path and the Chrome deviceId. An owner agent gets the lane's rules too: paste the matching `.claude/agents/pla-*.md` as its brief, and check its output shape; if it doesn't fit, use the bundled or built-in worker instead. A built-in general-purpose agent gets the worker file as its whole brief, with the model named in that file.

| When | Lane | Writes |
|---|---|---|
| first | L1 Kalo (`pla-kalo-worker`) | `state/lane-L1-kalo.json` |
| as soon as L1 is written, together | L4 TrendTrack (`pla-trendtrack-worker`, API) · L3 pricing (`pla-pricing-worker`, browser) · L2 Meta (`pla-meta-worker`, browser, only one) | `lane-L4-trendtrack.json` · `lane-L3-pricing.json` · `lane-L2-meta.json` |

**One agent** (`run_mode` = single): run the same lanes yourself in the same order (L1, then L3 and L4, then L2), following each worker file as your checklist, and write the same files.

- Two browser workers may share the Chrome in their own tabs; **never two Meta workers**.
- Meta throttled (control 0): don't wait in a loop. Let the rest finish, deliver with those keywords marked `RECHECK`, check the control every 20-30 minutes in the background, and run a Meta re-check later into a new file (`lane-L2-meta-r2.json`). Later files win in the merge.
- Fewer than 3 Greens looks likely: say so early. Never lower a bar.

## 2. Check (you, per lane)
Open 2 links per lane yourself (for example one Kalo product page and one Meta ad by Library ID). If a lane is wrong, send the fix back to the same worker (SendMessage); don't redo it.

## 3. Deliver
```
python3 tools/deliver.py --chapter C --draft D --source "<filter setup> · US · <Kalo window from batch-N.json, e.g. 10/21–11/19>"
```
It merges the lanes (`TIERS.md`, launch math, top 10), saves the photos, and builds the PDF report, the Claude web page, the Google Sheet requests, the Competitor Files tabs and the column M links, then prints the send order. Set `PLA_CHROME` if Chrome is not in a standard place.

Start the L5 sheets worker (`pla-sheets-worker`, or what `state/agents.json` names) with that send order, `drive_folder_id`, and the workbook id from `state/competitor-files-chC.json` if it exists. Then:
1. If the tabs go to a **new** Competitor Files workbook, the worker creates it, sends the tabs, saves `state/competitor-files-chC.json`, and stops. Run the same `tools/deliver.py` command again (it now links the tabs), then SendMessage the same worker (or start a new one) with the new send order: it sends the draft sheet only.
2. Otherwise it sends the tabs and the draft sheet in one go.
In single mode, send the files yourself in the same order.
Publish `reports/chapterC-draftD-page/page.html` with its `img/` files as a Claude Artifact (new draft = new page) and keep the link.

## 4. Close
Check the draft against `STANDARD.md`. Write the end-of-run report (`SKILL.md`): intake, setup, run mode and which agents ran each lane, preflight, the 10 outcomes, Greens or HOLD, the sheet, Competitor Files and page links, the report path, watch-outs, everything still MISSING or RECHECK. Log owner corrections in `state/feedback.md`.

## Token and time budget
- Host on the strongest model; workers on the models in their files (Sonnet; Haiku for the API-only TrendTrack lane).
- Workers return 10 lines; details live in `state/*.json`. Read those files only for the checks above.
- Browser workers read pages with one `javascript_tool` extraction or `get_page_text`; screenshots only to find a control, at scale 0.5.
- Later drafts of a chapter reuse the saved lane files: no new Kalo work, only re-checks.
- Time: Chapter 2 · Draft 1 went from preflight to a read-back sheet in about 1.5 hours with parallel lanes. The slow part is Meta's throttle, which can add a couple of hours to a re-check; never let it hold up the delivery.
