# CLAUDE.md: pla-product-research (Claude Code)

Read-only TikTok Shop product research. It never publishes, activates products, launches ads or spends money.

1. Read `FOR-YOUR-AGENT.md`, then `SKILL.md`. Run the preflight (`PREFLIGHT.md`) before any research page.
2. Intake once. If `state/intake.json` exists, reuse it and apply every rule in `state/feedback.md`. If not, ask the 5 intake questions in one message (SKILL.md, Step 0), show the brief, save it, start the hunt.
3. Redo the intake only if the user says the buyer or budget changed. Log each owner correction in `state/feedback.md`. Commit both files to the user's own fork or clone.
4. Use the lanes in `AGENTS.md` with the Agent tool: run workers in the background, use a cheap model for workers, and let the host verify (spot-check 2 links per lane, then merge).
5. Browser: one Chrome owner at a time. Never type, read or ask for passwords or codes. The human logs in. On a login, CAPTCHA or consent wall, mark the item MISSING and move on.
6. Outputs every run: the Google Sheet (if Sheets access exists) and the local report:
   `python3 tools/report/build_report.py state/report.json --out reports/<chapter>-<draft>` (PDF + HTML).
   Download each product's main Kalo photo into `reports/<run>/images/` so no image is missing.
7. Rank Greens by launch math (`TIERS.md`); show weak math as a watch-out with the price or bundle fix.
8. Meta Ad Library throttle: after about 40-50 searches, stop, wait 10+ minutes, mark throttled keywords `RECHECK`. Never conclude "no competitor" from a throttled search.
9. Evidence is PROVEN, PARTIAL or MISSING. Never invent a URL, price or number. Fewer than 3 Greens = HOLD.
10. Never publish, activate or spend. Run every step to the end, then give a plain end-of-run report.
