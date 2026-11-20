Files in this folder. In the user's own repo copy (fork or clone) this folder is the skill's memory.

| File | What it is |
|---|---|
| `intake.json` | The one-time intake: daily CBO budget, CBO setup, buyer, price band, categories, things to avoid, the brief. Template: `templates/intake.json`. |
| `feedback.md` | Running log of the owner's corrections and the rule each one became. Template: `templates/feedback.md`. |
| `batch-N.json` | One per batch. |
| `lane-*.json` | One per worker lane (see `AGENTS.md`, shapes in `lanes.example.json`). |
| `report.json` | Hand-off for the local report builder. Format in `FOR-YOUR-AGENT.md`. |

## Memory in the repo

1. **Intake happens once.** The first run asks the intake questions (`SKILL.md`, Step 0) and saves `state/intake.json`.
2. **Every later draft reuses it.** The agent reads `state/intake.json` and does not ask again. It re-asks only if the user says the buyer or the budget changed, then updates the file.
3. **Corrections are kept.** When the owner corrects a draft, the agent adds a row to `state/feedback.md`: date, correction, the rule it became. Every later draft applies all rules in that file.
4. **Commit both files.** At the end of each run, commit `state/intake.json` and `state/feedback.md` to the user's own fork or clone so the next session (or another agent) starts with the same memory. Do not push to the original owner's repo.
