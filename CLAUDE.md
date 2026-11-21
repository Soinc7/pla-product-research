# CLAUDE.md: pla-product-research (Claude Code)

Read-only TikTok Shop product research. It never publishes, activates products, launches ads or spends money.

1. Read `FOR-YOUR-AGENT.md`, then `SKILL.md`. Run the preflight (`PREFLIGHT.md`) before any research page.
2. Intake once. If `state/intake.json` exists, reuse it and apply every rule in `state/feedback.md`. If not, ask the 5 intake questions in one message (SKILL.md, Step 0), show the brief, save it, start the hunt. In the same message (or alone, if only these are missing), ask the run setup after `python3 tools/check_agents.py`: several sub-agents or one agent, whether to use the owner's own agents it found, and the Drive folder.
3. Redo the intake only if the user says the buyer or budget changed. Log each owner correction in `state/feedback.md`. Commit both files to the user's own fork or clone.
4. Use the lanes in `AGENTS.md` with the Agent tool: `/pla-run` is the host playbook, and the workers are ready in `.claude/agents/` (`pla-kalo-worker`, `pla-meta-worker`, `pla-pricing-worker`, `pla-trendtrack-worker`, `pla-sheets-worker`). Run them in the background with file paths and the Chrome deviceId, and verify (spot-check 2 links per lane, then merge). `python3 tools/deliver.py --chapter C --draft D` builds every output.
5. Browser: one Chrome owner at a time. Never type, read or ask for passwords or codes. The human logs in. On a login, CAPTCHA or consent wall, mark the item MISSING and move on.
6. Outputs every run (Chapter 2 · Draft 1 is the reference, `STANDARD.md`): the Google Sheet (if Sheets access exists), the Competitor Files workbook, the local report and the web page:
   `python3 tools/report/build_report.py state/report.json --out reports/<chapter>-<draft>` (PDF + HTML).
   `python3 tools/report/build_page.py state/report.json --out reports/<chapter>-<draft>-page` (publish `page.html` with `img/` as an Artifact).
   Download each product's main Kalo photo into `reports/<run>/images/` so no image is missing.
   On Windows use `python` (or `py -3`) instead of `python3`, which opens the Microsoft Store.
7. Rank Greens by launch math (`TIERS.md`); show weak math as a watch-out with the price or bundle fix.
8. Meta Ad Library throttle: one Meta worker at a time. Search the control (`"dryer vent"`) first; if it is 0, wait 10+ minutes and check again (it can last over an hour). Mark throttled keywords `RECHECK`. Never conclude "no competitor" from a throttled search.
9. Evidence is PROVEN, PARTIAL or MISSING. Never invent a URL, price or number. Fewer than 3 Greens = HOLD.
10. Never publish, activate or spend. Run every step to the end, then give a plain end-of-run report.
11. Chrome: identify it by deviceId (`list_connected_browsers`), never by its "Browser 1/2" label, and give workers the deviceId.
