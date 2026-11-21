# Changelog

## v1.12.0 — 2026-11-21

The competitor check is the **Ad Library**, and the skill calls it that everywhere. Product research searches the Ad Library (facebook.com/ads/library) for competitors already running the product's Kalo videos; those search links are the evidence on the sheet and the page.

- Renamed throughout: `AD-LIBRARY.md` (the check's guide), the `pla-adlibrary-worker` sub-agent, lane files `lane-L2-adlibrary*.json` with the key `adlibrary_sweep`, the preflight check `ad_library` (E2), the batch-state `ad_library` block, and every label on the sheet, the Competitor Files tabs, the web page and the PDF ("Ad Library keywords", "Copied in Ad Library", "Clear in the Ad Library").
- The code reads only the new names. Move older lane files over before merging (rename `lane-L2-…` files and their `…_sweep` key).
- Removed `reports/chapter1-draft3.html` and `.pdf` (generated files with the old wording). Rebuild the example any time: `python3 tools/report/build_report.py examples/chapter1/report.json --out reports/example`.
- Includes v1.11.1 (the tool safety net), which was not pushed separately.

## v1.11.1 — 2026-11-21

Tool safety net: every main tool is checked on every run, and a missing one triggers "ask the owner, then search the web".

- **Preflight checks all five main tools every run:** Kalo, a 1688 route, TrendTrack, Ad Library and Google Trends. TrendTrack, Ad Library and Google Trends are now three separate checks (E1-E3) in `PREFLIGHT.md`, `preflight/checklist.json` and `preflight/result.example.json`. A Ad Library throttle is PARTIAL, not missing.
- **New `PREFLIGHT.md` section G and `TOOL-ALTERNATIVES.md`:** when a main tool is missing, say what it blocks, ask the owner what they use instead, and if they have nothing, search the web for current alternatives and show two or three. The chosen substitute is recorded in `tool_substitutes` and the check marked PARTIAL. A substitute counts only for the proof it really gives; the tier bars never change. Chrome missing, or Kalo missing with no substitute, is still a STOP.
- `TOOL-ALTERNATIVES.md` has a starting list checked on 2026-11-21 (FastMoss, EchoTik, Tabcut for Kalo; English 1688 agents; PiPiADS, Minea, BigSpy, WinningHunter, TikTok Creative Center for TrendTrack; Glimpse, Exploding Topics, Pinterest Trends for Google Trends), with a note that most comparison pages are written by vendors.
- `preflight/evaluate.py` ends with a "Missing main tools" line pointing to section G.
- SKILL.md Step 0b, `/pla-run`, README, CLAUDE.md and FOR-YOUR-AGENT.md say the same.

## v1.11.0 — 2026-11-21

Ready to share: multi-agent out of the box in Claude Code, one command for every deliverable, and the Competitor Files builder.

- **Claude Code sub-agents** in `.claude/agents/`, one per lane, each with its model, inputs, output file and token rules: `pla-kalo-worker` (L1, Sonnet), `pla-adlibrary-worker` (L2, Sonnet, one at a time, throttle protocol), `pla-pricing-worker` (L3, Sonnet), `pla-trendtrack-worker` (L4, Haiku, API only: appeal video plus Competitor Files data), `pla-sheets-worker` (L5 writes, Sonnet).
- **`/pla-run`** (`.claude/commands/pla-run.md`): the host playbook. Preflight, lanes in parallel, 2-link checks per lane, delivery, and the token and time budget.
- **Uses what the machine already has.** `tools/check_agents.py` scans the project, `~/.claude/agents`, `~/.claude/skills` and installed plugins, and picks a worker per lane: the owner's own agent (asked first), else the bundled `pla-*` worker, else the built-in general-purpose agent briefed with the worker file. It reports an existing product-research skill so it is kept, not replaced. The intake now asks once: several sub-agents or one agent (`run_mode`), whether to use the owner's agents (`use_owner_agents`), and the Drive folder (`drive_folder_id`).
- **Merge order fix:** re-check lane files now always win. Before, `lane-L2-adlibrary.json` sorted after `lane-L2-adlibrary-r2.json` ('-' before '.'), so a re-check of a round-1 product could be overwritten by the old verdict (Chapter 2's drafts were not affected; both reproduce exactly). Ties in break-even ROAS now break on the unrounded value, then revenue.
- `state/lanes.example.json`: `pid` on the L2 and L3 examples, and an L4 example with the keys the scripts read (stores, running ads, TikTok videos with `match`).
- `/pla-run`: the run-setup question, the Drive folder, the Kalo window for `--source`, an example call, and the Competitor Files loop (new workbook, rerun `tools/deliver.py`, then the same worker sends the draft sheet).
- **`tools/deliver.py`**: one command runs the merge, saves each photo once, and builds the PDF report, the Claude web page, the Google Sheet requests, the Competitor Files tabs and the column M links, then prints the send order.
- **`tools/sheets/build_competitor_tabs.py`**: the Competitor Files tabs (stores, running ads with hooks, Ad Library competitors running the Kalo videos, top TikTok videos, reference photo) as Sheets API bodies, for a new workbook or added to an existing one. It reads the TrendTrack data from `lane-L4-trendtrack*.json` (or the older `lane-L5-compfiles*.json`).
- **PDF printing**: `PLA_CHROME` points the report builder at any Chrome, Edge or Chromium; `~/Applications` and `~/Desktop` are searched on a Mac; the throwaway browser profile sits next to the output, so the PDF also prints inside sandboxed agents; a found-but-failed browser is reported as such.
- **Web page**: the Yellow heading and legend say when a product is waiting on a Ad Library re-check instead of calling it copied.
- **Docs**: README "Run it in Claude Code" (workers table, `/pla-run`, installing as a user skill), AGENTS.md token and time budget measured on Chapter 2, SKILL.md Step 12 uses `tools/deliver.py` and the tab builder, one Competitor Files workbook per chapter.
- Privacy sweep of every public file: only public sites are linked (Ad Library, Kalodata, Fabulk, 1688, Google Trends, TikTok); no emails, document links, account or device IDs.

## v1.10.2 — 2026-11-21

Repo completion: the Chapter 2 · Draft 1 design is the standard, and the fresh-session test findings are folded in.

- **Chapter 2 · Draft 1 is the reference** (owner-approved): `STANDARD.md` (new D6 web page and E5 delivery checks), README, FOR-YOUR-AGENT.md, SKILL.md Step 12, CLAUDE.md and `templates/sheet-layout.md`.
- **New web page design.** `templates/draft-page.html` + `tools/report/build_page.py`: summary band with a HOLD flag under 3 Greens and a 10-slot tier strip, the Green 1 hero with a launch-ready seal and stacked proof checks, Orange cards that lead with what's missing, muted Yellow rows with a red "Copied in Ad Library" flag naming the rivals (ads grouped by advertiser), launch math on every product, intake and grading rules. Phone width, light and dark mode. Writes `index.html` (local) and `page.html` (for a Claude Artifact) plus `img/`. Uses the same bars and formulas as `build_report.py`; budget and ROAS limit from the intake.
- `merge_lanes.py`: later lane files win, so a re-check file replaces an older verdict for the same product.
- **Getting the repo** (findings 1-3): check access first, clone with `git -c credential.helper= -c core.askPass=` so it fails fast, a step-by-step connector copy (download links expire in a minute or two; binaries need `download_url`), new `MANIFEST.txt`, and `git init` when the copy is not a git repo.
- **Intake** (5, 7, 18): `sale_value_max` (default 30) and optional `supplier_agent` in `templates/intake.json`; the intake band sets the Kalo filter and the sale-value rule still applies; target buyer comes from the intake.
- **Naming and folders** (8): the owner's draft name wins; a first run with no folder named uses My Drive root and says so.
- **Preflight** (9, 11, 20, 21, 23): new `PENDING` state in `PREFLIGHT.md` and `preflight/evaluate.py` (exit code 3); Chrome identified by deviceId; Kalo Basic plan (500 rows) and mid-run logout; Fabulk is browser only (scripts get 403); TrendTrack defined with its credit cost; Sheets proxy route.
- **Lanes** (10, 30, 33, 34): L4 can't start before L1 has names; never run two Ad Library lanes at once (the throttle is shared by the Chrome, Facebook session and network); workers get the deviceId, never a label.
- **Ad Library check** (12, 14, 27, 33): counts and frame check both use video ads (`media_type=video`); no Ad Library check keeps a product Yellow instead of untiered; the competition band is shown, not a tier gate; the frame check covers the top 10 Kalo videos with the public cover link; a throttle can last over an hour (control first, wait, re-check every 20-30 minutes).
- **Tiers** (13, 28, 29): SKILL.md says v1.3; one video must pass all three Kalo bars; appeal needs the same product (same design), and PARTIAL appeal does not pass.
- **Sheet** (15, 16): SKILL.md Step 12 now lists the three v2.1 tabs (the filter receipt is a file, not a tab); how to send column K's multi-link cells through a proxy `batchUpdate`, with a fallback.
- **Kalo** (6, 17, 22, 24, 25, 26, 31): category names for AVD-36, the exact filter clicks (Apply stages, Submit runs), Revenue Source (Content) = Video, UI only (its API returns the wrong region), 90-day window optional for research, video IDs and the public cover and photo links, link `/video/detail` but don't open it.
- **Moving computers mid-batch** (32): what to save and how to resume, in SKILL.md and `state/README.md`.
- SKILL.md: the skill description and outcome words now describe the Green / Orange / Yellow ladder; the cost gate, score and day-one floor are the launch gate only.
- CHANGELOG sorted newest first with one version style (19).
- Fresh-eyes review fixes: Steps 5-9 and the pricing decision rules now say "no launch handoff" instead of "no green" (the research tier only comes from `TIERS.md`); the merge runs before the sheet (Step 12); a Competitor Files recipe (TrendTrack → `lane-L5-compfiles.json` → workbook tabs → `competitor-files-<chapter>.json` → `competitor_links.py`); `host-overrides.json` and `competitor-files-*.json` documented in `state/README.md`; archive a batch's lane files before the next chapter; earlier chapters' product IDs go into the intake `avoid` list; `templates/batch-state.json` gains `report_name`, `chrome_device_id`, region, currency, account check and a Ad Library control log; Step 13 handoff spelled out; preflight copies six states; where the Chapter 2 reference lives and how to rebuild the design from the shipped example.

## v1.10.1 — 2026-11-20

- `tools/report/build_page.py` + `templates/draft-page.html`: the draft web page built from `report.json`, photos saved as `img/<rank>.jpg`.
- `tools/sheets/competitor_links.py`: links Sheet column M to the Competitor Files tabs.
- `merge_lanes.py`: reads every round's lane files, `--top 10`, `--l1` to pick rounds, and fills `competitor_file` from `state/competitor-files*.json`.
- `build_sheet.py`: legend row 52 px and header row 64 px so no text is cut; no frozen columns (they conflict with the merged banners); column M links to the Competitor File.
- `AGENTS.md`: browser lanes run in parallel in their own tab groups.
- Owner rules: every batch aims for 3 Greens; later drafts reuse saved lane data and links instead of new Kalo work.

## v1.10.0 — 2026-11-20

- `STANDARD.md`: the draft checklist, set by Chapter 1 · Draft 2.
- `tools/report/merge_lanes.py`: merges the lane files into `state/report.json`. It picks the highest-revenue video that clears the Green bars.
- `tools/sheets/build_sheet.py`: builds the sheet (sheet-layout v2.1) as Drive and Sheets request files, in parts of 30 KB or less.
- Parallel browser lanes: workers run side by side, each in its own tab group.
- Multi-browser Kalo check (already in `PREFLIGHT.md`).

## v1.9.1 — 2026-11-20 (Claude Code run-through fixes)
- README: how to log in to clone a private repo (`gh auth login`, `gh auth setup-git`, installing the GitHub CLI), and a connector fallback. Windows note: use `python` / `py -3`, because `python3` opens the Microsoft Store. The same note is in CLAUDE.md and PREFLIGHT.md.
- One rule for "no supplier agent". The research tier follows TIERS.md v1.3, and the +$5.00 estimate ranks products. SKILL.md Steps 7-10 are the launch gate before the Step 13 handoff. Updated the preflight checklist message, PREFLIGHT.md and a note in SKILL.md Step 7.
- SKILL.md Step 1: maps "Batch N" to the owner's "Chapter C · Draft D" names (`report_name` in `batch-N.json`).
- AD-LIBRARY.md: search a control keyword before the sweep and about every 15 searches to catch throttling.
- AGENTS.md: "Kalo #n" means revenue order on "Video & Ad"; always store the video ID too.
- `state/lanes.example.json`: added the L1 (Kalo) and L4 (TrendTrack) shapes, video IDs on competitors, and `media_type=video` in the Ad Library URLs.
- Chapter 1 example: the solar flood light re-check (no throttle) found Gladchaser running 2 of its Kalo videos. Rebuilt `reports/chapter1-draft3`.

## v1.9.0 — 2026-11-20
- **Intake, once.** New SKILL.md Step 0: before any search, ask the 5 intake questions in one message (daily CBO budget, default $150; CBO setup, default "Flash Plus CBO"; buyer; price band and categories; things to avoid), show a 4-6 sentence brief and start the hunt. Saved to `state/intake.json` (new `templates/intake.json`). Also in FOR-YOUR-AGENT.md and AGENTS.md host steps.
- **Memory in the repo.** The intake is saved once in the user's own copy and reused. `state/feedback.md` (new `templates/feedback.md`) logs each owner correction and the rule it became; every later draft applies them. Both files are committed to the user's fork or clone. Explained in `state/README.md` and SKILL.md.
- **Launch math.** TIERS.md and FOR-YOUR-AGENT.md define margin, break-even ROAS, sales/day to break even and the price needed for 2.0 ROAS. Greens are ranked by lowest break-even ROAS; weak math (margin <= 0 or ROAS above `breakeven_roas_max`) is a watch-out with a price or bundle fix. PROPOSED default: `breakeven_roas_max` = 3.
- **Deliverables.** Each run gives the Google Sheet (if Sheets access exists) and a local PDF + HTML report from `tools/report/build_report.py`. `state/report.json` is the documented hand-off format (reference `examples/chapter1/report.json`).
- Added `CLAUDE.md` for Claude Code users. README files table updated.

## v1.8.0 — 2026-11-20
- Added `AGENTS.md`: host and worker lanes (Kalo, Ad Library check, pricing, TrendTrack, sheet builder) so several cheaper agents can share a run and save tokens. Includes a short worker prompt, token-saving rules and a single-agent fallback. Linked from README, SKILL.md and FOR-YOUR-AGENT.md. Added `state/lanes.example.json` with the lane output shapes.
- New competitor standard: every product is searched with 5 different Ad Library keywords (exact-phrase and unordered). It must clear all 5 to be Orange or Green. The sheet shows all 5 keywords as links with counts, then a verdict line, with each competitor's Ad Library link and the Kalo videos (#) it uses. Added the throttle rule (about 40-50 searches, pause 10+ minutes, mark `RECHECK`). Updated AD-LIBRARY.md, TIERS.md (v1.3), SKILL.md, sheet-layout.md and FOR-YOUR-AGENT.md.
- Prices on every row (Green, Orange, Yellow): item cost with an EXACT / CLOSE / SIMILAR label, plus "Est. delivered (standard)" = item cost + $5.00 flat until a real quote replaces it. Estimates rank products and never release a Green by themselves.
- Sheet banner: no "delivered quotes pending" text. The legend is now a row of colored chips.
- Cleaned for a public repo: removed personal and owner-specific names and details. The supplier-agent role is now just "supplier agent". The pricing file is now `PRICING-1688-SUPPLIER.md`. Batch name is now `Product Research Batch N`.

## v1.7.0 — 2026-11-20
- Added `FOR-YOUR-AGENT.md`, a one-page brief so a partner's agent knows what this skill does, what it returns (10 ranked products plus Competitor Files) and how to run it next to its own product researcher: standalone, second opinion or side by side.
- README: points agents to the brief first, adds a "Getting access" section for the private repo, and updates "What you get" to the Chapter format.

## v1.6.0 — 2026-11-20
- Tiers ranked 1–10 across the draft (GREEN 1–4, ORANGE 5–7, YELLOW 8–10 for a 4/3/3 draft).
- Column J renamed "Sales per 1K views (not ROAS)" with a "1 per N views" line, so it isn't read as Ad Library ROAS.
- Column L now links the Ad Library search for Green and Orange rows too ("Checked ✓ none copying ↗"), so the check is visible on every row.
- Column M now opens a per-product tab in a new companion workbook, "Competitor Files": competitor stores, their running ads with hooks and landing pages, top TrendTrack TikTok videos and the Kalo reference photo.
- Applied to Product Research — Chapter 1 · Draft 1.

## v1.5.0 — 2026-11-20
- New sheet design (`templates/sheet-layout.md` v2, "Chapter" format): banner rows, real product photos via `IMAGE(url,1)`, tier chips, and clickable proof columns for Kalo, the winning video, the Ad Library search, the competitor ad (by Library ID), TrendTrack, Google Trends and 1688/Fabulk. The "Why" line is short and crisp. The 0–5 score columns are dropped.
- Delivered "Product Research — Chapter 1 · Draft 1" (4 Green / 3 Orange / 3 Yellow). Photos need the owner's one-time "Allow access" click in Sheets.

## v1.4.0 — 2026-11-20
- **Run-to-completion rules** (SKILL.md hard rules 8–10): never pause for "go"; a draft counts as done only when the next-numbered Draft sheet is in Drive and has been read back; one stalled product never blocks the batch. On an early stop, the agent still writes and delivers what it has.
- sheet-layout.md: Kalo images can't be embedded in Sheets, so column C uses `HYPERLINK(...,"PHOTO")`.
- Delivered "Product Research Draft 37" (Google Sheet, same folder as Draft 36): 4 Green, 3 Orange, 3 Yellow.

## v1.3.0 — 2026-11-20
- **1688 no longer stops a run.** Check A is now "1688 price route (any one)": Fabulk (fabulk.com, no login), 1688order.com (free account) or 1688.com (logged in). If none works, the agent asks the user to log in or make a free account on one, keeps doing discovery, Ad Library and TrendTrack, and holds pricing only. The evaluator has a new `missing_blocks: false` flag, so a missing 1688 route gives GO_LIMITED, not STOP.
- PRICING-1688-SUPPLIER.md, SKILL.md, README.md and PREFLIGHT.md updated with the 3 routes and Fabulk photo search (camera icon, upload the Kalo main photo).
- LIST-2026-11-20.md: item prices from Fabulk. Dryer vent $2.58 (exact photo), windshield $7.31 (close), inverter $17.40–18.29 (generic close). Work light not found, so it needs a supplier-agent quote.

## v1.2.2 — 2026-11-20
- Screened both Whites. The Azocek inverter passes Kalo (2.8k / 3.01M / 0.93), TrendTrack (800k) and the Ad Library check, so it is Green 4. The bathroom organizer fails the TrendTrack appeal check, so it is Orange. The list is now 4 Green, 3 Orange, 3 Yellow.
- 1688 check blocked: no Chrome profile is logged into 1688.

## v1.2.1 — 2026-11-20
- Added `LIST-2026-11-20.md`, a live run: Kalo logged in, Ad Library first-frame check against the Kalo top-10 videos, TrendTrack appeal check. Result: 3 Green, 2 Orange, 3 Yellow, 2 White, so the 3-Green minimum is met.
- Marked `LIST-2026-11-20-PROVISIONAL.md` as superseded.

## v1.2.0 — 2026-11-20
- TIERS.md rewritten to the owner's ladder: Yellow (Kalo demand) → Orange (top-10 Kalo videos not used in the Ad Library, first-frame + extra-frame check) → Green (winning video: Kalo orders, conversion, views + TrendTrack appeal). White = potential. Minimum 3 Greens per list; cost and crowding shown as flags, not gates.
- Added LIST-2026-11-20-PROVISIONAL.md: 2 Green / 4 Orange / 2 Yellow / 2 White, flagged NEEDS_MORE_CANDIDATES until a fresh Kalo pull.

## v1.1.0 — 2026-11-20
- Added `AD-LIBRARY.md`: exact-phrase keyword search, competitor brands grouped and counted, oldest active ad, cloned copy, and matching the Kalo top-3 videos against running video ads in the Ad Library. Competition bands NONE / LIGHT / HEALTHY / CROWDED / SATURATED.
- Added `TIERS.md`: GREEN (top) > ORANGE (second) > YELLOW (third) > not tiered, with sheet fills #00FF00 / #FFA500 / #FFFF00. Band and cost thresholds are PROPOSED defaults the owner can change.
- SKILL.md: new Step 7b (Ad Library check required for any tier); Step 11 now tiers every candidate.
- Added `DRAFT-RUN-D36.md`: live draft run on Draft 36, with 0 Green / 1 Orange / 5 Yellow / 4 not tiered; the batch result is HOLD.

## v1.0.1 — 2026-11-20
- Chrome PARTIAL now STOPs (evaluator + docs).
- Added check F: supplier agent quote channel.
- Added `state/batch-N.json` batch state + resume rule; partner numbering starts at 1.
- Test run: revenue gate shown as undecided (video revenue only); video evidence shown as PARTIAL.
- Marked photo search, storefront rule and 2-factory minimum as PROPOSED.
- Picked as winner of a Fable 5.2 vs Opus 5.5 bake-off with cross-rebuttal.

## v1.0.0 — 2026-11-20

First standalone export for partner use.

**Source**

- The source skill `pla-product-research`, last changed 2026-08-31 (core rules: batch record, gates, scoring, sheet layout, handoff).
- Draft 36 practice, 2026-10-03 (last real run: discovery filters, supplier-agent delivered estimate, 1688 status column).
- Green qualification rules from Draft 32, 2026-09-16.
- Kalodata how-to, proven 2026-11-05.

**Added in this export**

- Preflight tool and safety check with PROVEN / PARTIAL / MISSING results and a small evaluator script.
- Filter setups collected in one file, with proposed short codes shown beside the original sheet labels.
- 1688 exact-match and supplier-agent quote method written as steps.
- Dry test run on the 10 Draft 36 products.

**Removed for sharing**

- Machine names, account IDs, store names and domains, and all secrets.

**Known gaps**

- See "UNKNOWN" notes in `SKILL.md`, `FILTER-SETUPS.md` and `TEST-RUN.md`. They are open questions for the owner, not defects to guess around.
