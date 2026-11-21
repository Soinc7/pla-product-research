# Preflight — safety and tool check

Run this before any research. It takes a few minutes.
The machine-readable version is `preflight/checklist.json`.

## Rules

- The human logs in. The agent only looks.
- **Never ask for, type, read or store a password, key, SMS code or passkey.**
- Do not sign in for the user. Do not accept consent screens for the user. Report the wall and stop.
- One agent drives Chrome at a time. If another agent is using it, wait.
- Never write an account ID into any file. Record only `MATCH`, `MISMATCH` or `NOT_CHECKED`.
- Preflight is look-only. Do not run a Kalo search during preflight; searches are limited.

## Result states

| State | Meaning |
|---|---|
| `PROVEN` | Checked just now and it works |
| `PARTIAL` | Works with a limit. Write the limit down. |
| `MISSING` | Not available or not logged in |
| `PENDING` | Not run yet (for example, Chrome is busy with another agent). Run it before research. Never write MISSING for a check you could not run yet. |

## Stop rule

| Check | If MISSING | If PARTIAL |
|---|---|---|
| B. Chrome | **STOP** | **STOP** (wrong profile or cannot navigate = cannot research) |
| A. 1688 route | **Do not stop.** Ask the user to log in or make a free account on one route, or use Fabulk (no login). Discovery continues; pricing stays HOLD. | Continue; note the route and whether prices are public list prices |
| C. Kalo | **STOP**, unless the owner names a substitute (section G); then PARTIAL | Continue inside the plan limits. Plan the batch across days. |
| D. Sheets / Drive | Continue. Write output as local files and say so in the report. | Continue with the limit noted |
| E1. TrendTrack | Continue, after section G. No product can pass Green's appeal check; Competitor Files have no stores or ads. | Continue with the limit noted (few credits, or a substitute) |
| E2. Ad Library | Continue, after section G. No product can be Orange or Green; keywords stay RECHECK. | Throttled: deliver with RECHECK, re-check later |
| E3. Google Trends | Continue, after section G. Rows link the search instead of a trend line. | Continue with the limit noted |
| F. Supplier agent | Continue. Rows use Est. delivered (item + $5.00). Tiers follow `TIERS.md`; no launch handoff until a real quote exists. | Continue; log pending quotes in the batch state file |

Run order: **B first** (the others need Chrome), then A, C, D, E1-E3, F. **Run every check on every run**, even for a later draft that only re-checks a few products: tools log out, throttle and run out of credits between runs.

**A main tool missing?** (Kalo, a 1688 route, TrendTrack, Ad Library, Google Trends): never skip it silently. Go to section G before any research page.

---

## B. Chrome connection

**What to prove:** a browser-automation tool reaches a real, logged-in Chrome.

Steps:

1. List the browsers or tabs your tool can see. If more than one Chrome is connected, open Kalodata in each and use the one that is logged in. A login page in one browser does not mean Kalo is logged out. **Identify the browser by its deviceId**, not its label: labels such as "Browser 1" and "Browser 2" swap when a browser reconnects. Write the deviceId into `state/batch-N.json`, and check `list_connected_browsers` again before each lane.
2. Open a new tab. Load any simple page. Read its title back.
3. Confirm this is the user's real Chrome profile (the one with their logins), not a blank or throwaway browser.
4. Confirm no other agent is driving this Chrome right now.

| State | When |
|---|---|
| PROVEN | Tool opens a tab, navigates and reads the page, in the user's real profile |
| PARTIAL | Tool connects but is on a profile without the logins, or can read but not navigate |
| MISSING | No browser tool, or it cannot reach Chrome |

**Fix:** Human opens Chrome, reconnects the browser tool, and selects the profile that holds the 1688 and Kalo logins. Then rerun this check.

## A. 1688 price route (any one of three)

1688 can be reached three ways. **Any one is enough.** A missing 1688 login never stops the run.

| Route | Login | What you get |
|---|---|---|
| **Fabulk** — fabulk.com | **Not needed** | USD price and MOQ on every result card. Keyword search: `https://www.fabulk.com/searchlist?keyword=<words>`. Photo search: camera icon in the search bar (upload the Kalo main photo). Browser only: plain HTTP from a script gets 403. |
| **1688order** — 1688order.com | Free account | English 1688 agent site with factory prices |
| **1688.com** | Needed for SKU tiers, image search and counter price | Public search shows CNY list prices without login |

Steps:

1. Try **Fabulk first**. Run one keyword search and confirm price and MOQ show.
2. If Fabulk is down, try 1688order.com, then 1688.com, in the user's Chrome.
3. Open one offer and confirm price and MOQ are visible. Record the route.

| State | When |
|---|---|
| PROVEN | Any route shows price and MOQ for an offer |
| PARTIAL | Only 1688.com public list prices (no SKU tiers), or a verification page blocks some pages |
| MISSING | No route works: Fabulk down and no login on 1688order or 1688.com |

**If MISSING:** do not stop. Tell the user: "Make a free account or log in on 1688order.com or 1688.com in your own browser, or I can use Fabulk, which needs no login." Keep running discovery, Ad Library and TrendTrack. Pricing stays HOLD until a route works. The agent never types into a login form.

## C. Kalodata (Kalo)

**What to prove:** logged in, and the plan limits are known.

Steps:

1. Open Kalodata in the user's Chrome.
2. Confirm a logged-in state (no login wall).
3. Read the plan type from the account area if it is shown. Ask the human if it is not.
4. Write the limits into the batch record.

Known limits:

| Plan | Limit |
|---|---|
| Trial | 10 keyword searches per day and 10 product/video detail visits per day (separate counters) |
| Basic | At most 500 result rows per list; page 11 (rows 501+) asks to upgrade. Detail-visit limit unknown, so count every visit. |
| Other plans | UNKNOWN. Ask the human or read them from the account page. |

Kalo can log itself out mid-run (seen after 3 detail visits). If it does, the human logs in again and the run resumes; this is not a STOP. Drive Kalo through its UI only: its internal API returns the wrong region when called from a page script.

| State | When |
|---|---|
| PROVEN | Logged in, plan known, enough daily allowance for today's work |
| PARTIAL | Logged in on a trial or with today's allowance partly used. Record what is left. |
| MISSING | Login wall, or no Kalo account |

**Fix:** Human logs in to Kalodata in that Chrome profile themself. If the daily allowance is used up, continue tomorrow or use a higher plan.

## D. Google Sheets / Drive

**What to prove:** the agent can create a sheet and write to it.

Steps:

1. Confirm a Sheets/Drive tool is connected, or that Sheets opens logged in inside Chrome. The sheet builder writes raw Sheets `batchUpdate` bodies; if your connector has no raw batchUpdate tool, it needs a proxy call (for example Composio `COMPOSIO_PROXY_EXECUTE`). Note which route works.
2. Confirm where the output sheet should live (ask the human for the folder). If none is named on a first run, use My Drive root and say so.
3. Do not create test files unless the human agrees.

| State | When |
|---|---|
| PROVEN | Can create and edit a sheet in the agreed place |
| PARTIAL | Read-only access, or no agreed folder yet |
| MISSING | No access |

**Fix:** Human connects Google Drive/Sheets to the agent, or logs in to Google in Chrome themself, and names the output folder.

## E. TrendTrack, Ad Library, Google Trends (three separate checks)

Optional to start research, required for a Green. Record one state for each:

- **E1. TrendTrack** (trendtrack.io) is a paid MCP connector: TikTok videos, Shopify stores and ads by keyword. Check it with `check_credits` and write the credits left into the batch record (about 2 credits per returned item).
- **E2. Ad Library** is public. Check it with the control search (`"dryer vent"`, exact phrase, US, active, video: about 2,300 ads). A 0 means throttled (PARTIAL), not missing; see `AD-LIBRARY.md`.
- **E3. Google Trends** is public; open one explore page.
These do not block the start of research. But a product **cannot be Green** until they have been checked for that exact product: with no Ad Library check it stays Yellow, and with no TrendTrack appeal video it is Orange at most. There is no launch handoff either.

**Fix:** Human connects or logs in to the missing tool. Google Trends and Ad Library need only a working browser. Still missing: section G.

---

## G. A main tool is missing: ask, then search

Applies to Kalo, the 1688 route, TrendTrack, Ad Library and Google Trends. Full guide and a starting list of alternatives: `TOOL-ALTERNATIVES.md`.

1. Tell the owner, in one message with the other preflight results, what is missing and what it blocks.
2. Ask what they use instead (and whether it is logged in in this Chrome). Their answer wins.
3. If they have nothing, search the web for current alternatives, and show two or three with price, login and whether they give the same proof. Vendor comparison pages are marketing; say so. Never sign up or pay for the owner.
4. Record the choice in `state/batch-N.json` as `tool_substitutes`, and mark the check `PARTIAL` with the substitute in its note.
5. A substitute counts only for the proof it really gives; the tier bars in `TIERS.md` never change. Chrome missing, or Kalo missing with no substitute, is still a STOP.

---

## Recording the result

1. Copy `preflight/result.example.json` and fill in one state and a short note per check.
2. Optional: run the evaluator. It needs only Python 3.

```
python3 preflight/evaluate.py path/to/your-result.json
```

(On Windows: `python preflight/evaluate.py ...`.)

It prints `GO`, `GO_LIMITED`, `PENDING` or `STOP` and the fix for each problem. Exit code 2 means STOP, 3 means some checks are still PENDING (run them, then evaluate again).

3. Copy the eight states (A, B, C, D, E1, E2, E3, F) into the filter receipt for the batch. The evaluator ends with a "Missing main tools" line when any main tool is missing: do section G before research.

Notes must never contain passwords, keys or account IDs.


---

## F. Supplier-agent quote channel

**What to prove:** someone can get a delivered US quote this batch.

1. Ask the human which supplier agent quotes delivered cost, and on what channel.
2. Confirm the human will relay quote requests and paste replies back.
3. Do not message the supplier agent yourself unless the human says so.

PROVEN: channel named and quotes can be requested now. PARTIAL: channel exists, reply time unknown. MISSING: no supplier agent. Research runs with the +$5.00 estimate and tiers follow `TIERS.md`, but nothing is handed off for launch until a real quote exists.
