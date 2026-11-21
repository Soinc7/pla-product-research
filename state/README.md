Files in this folder. In the user's own repo copy (fork or clone) this folder is the skill's memory.

| File | What it is |
|---|---|
| `intake.json` | The one-time intake: daily CBO budget, CBO setup, buyer, price band, categories, things to avoid, the brief. Template: `templates/intake.json`. |
| `feedback.md` | Running log of the owner's corrections and the rule each one became. Template: `templates/feedback.md`. |
| `batch-N.json` | One per batch. |
| `lane-*.json` | One per worker lane (see `AGENTS.md`, shapes in `lanes.example.json`). Re-checks add files such as `lane-L2-meta-r2d.json`. `lane-L5-compfiles.json` holds the TrendTrack data for the Competitor Files. |
| `host-overrides.json` | Optional, written by the host: `{"<pid>": {"name": "...", "variant": "...", "trend": "<Google Trends keyword>"}}`. Short display names, variants and Trends keywords that `merge_lanes.py` uses instead of the long Kalo titles. It may also override `price`, `item_usd`, `match`, `source_url` and `note`. |
| `competitor-files-<chapter>.json` | The Competitor Files workbook's tab links: `{"spreadsheet_id": "...", "tabs": [{"rank", "pid", "title", "sheetId", "gid_url"}]}`. `merge_lanes.py` puts each `gid_url` into the product's `competitor_file`, which fills column M and the page's "Competitor file" button. |
| `filter-receipt-batch-N.md` | The filter receipt (template `templates/filter-receipt.md`). |
| `report.json` | Hand-off for the report, page and sheet builders, written by `merge_lanes.py`. Format in `FOR-YOUR-AGENT.md`. |
| `archive/batch-N/` | Lane files of a finished batch (see rule 7). |

## Memory in the repo

1. **Intake happens once.** The first run asks the intake questions (`SKILL.md`, Step 0) and saves `state/intake.json`.
2. **Every later draft reuses it.** The agent reads `state/intake.json` and does not ask again. It re-asks only if the user says the buyer or the budget changed, then updates the file.
3. **Corrections are kept.** When the owner corrects a draft, the agent adds a row to `state/feedback.md`: date, correction, the rule it became. Every later draft applies all rules in that file.
4. **Commit both files.** At the end of each run, commit `state/intake.json` and `state/feedback.md` to the user's own fork or clone so the next session (or another agent) starts with the same memory. Do not push to the original owner's repo. If your copy is not a git repo (for example it was copied through a GitHub connector), run `git init` and commit locally, or keep the files and say so in the end-of-run report.
5. **Re-checks add files.** A later re-check writes a new lane file (for example `lane-L2-meta-r2d.json`) instead of editing an old one. `tools/report/merge_lanes.py` reads every lane file, and later files win for the same product.
6. **Moving computers.** Copy the whole `state/` folder (and `reports/<run>/images/`) to the new computer, rerun the preflight, and resume from `next_step` in `batch-N.json`.
7. **New batch, new lane files.** `merge_lanes.py` reads every `lane-*.json` in `state/`. Before a new batch (a new chapter), move the old batch's `lane-*.json`, `report.json` and `competitor-files-*.json` into `state/archive/batch-N/`. Drafts of the same chapter keep them in place. Keep `intake.json` and `feedback.md` where they are.
8. **No repeats across chapters.** Add each finished chapter's Kalo product IDs to `avoid` in `intake.json` (Chapter 2 did this for Chapter 1's 10), and check the archived `report.json` files when unsure.
