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

## Stop rule

| Check | If MISSING | If PARTIAL |
|---|---|---|
| B. Chrome | **STOP** | **STOP** (wrong profile or cannot navigate = cannot research) |
| A. 1688 route | **Do not stop.** Ask the user to log in or make a free account on one route, or use Fabulk (no login). Discovery continues; pricing stays HOLD. | Continue; note the route and whether prices are public list prices |
| C. Kalo | **STOP** | Continue inside the plan limits. Plan the batch across days. |
| D. Sheets / Drive | Continue. Write output as local files and say so in the report. | Continue with the limit noted |
| E. Optional tools | Continue. No product can go green without them. | Continue with the limit noted |
| F. Supplier agent (Aria) | Continue. All delivered pricing stays HOLD; no green. | Continue; log pending quotes in the batch state file |

Run order: **B first** (the others need Chrome), then A, C, D, E, F.

---

## B. Chrome connection

**What to prove:** a browser-automation tool reaches a real, logged-in Chrome.

Steps:

1. List the browsers or tabs your tool can see.
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
| **Fabulk** — fabulk.com | **Not needed** | USD price and MOQ on every result card. Keyword search: `https://www.fabulk.com/searchlist?keyword=<words>`. Photo search: camera icon in the search bar (upload the Kalo main photo). |
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

**If MISSING:** do not stop. Tell the user: "Make a free account or log in on 1688order.com or 1688.com in your own browser, or I can use Fabulk, which needs no login." Keep running discovery, Meta and TrendTrack. Pricing stays HOLD until a route works. The agent never types into a login form.

## C. Kalodata (Kalo)

**What to prove:** logged in, and the plan limits are known.

Steps:

1. Open Kalodata in the user's Chrome.
2. Confirm a logged-in state (no login wall).
3. Read the plan type from the account area if it is shown. Ask the human if it is not.
4. Write the limits into the batch record.

Known limit — **trial plan: 10 keyword searches per day and 10 product/video detail visits per day.** These are separate counters.
Limits for other plans: UNKNOWN. Ask the human or read them from the account page.

| State | When |
|---|---|
| PROVEN | Logged in, plan known, enough daily allowance for today's work |
| PARTIAL | Logged in on a trial or with today's allowance partly used. Record what is left. |
| MISSING | Login wall, or no Kalo account |

**Fix:** Human logs in to Kalodata in that Chrome profile themself. If the daily allowance is used up, continue tomorrow or use a higher plan.

## D. Google Sheets / Drive

**What to prove:** the agent can create a sheet and write to it.

Steps:

1. Confirm a Sheets/Drive tool is connected, or that Sheets opens logged in inside Chrome.
2. Confirm where the output sheet should live (ask the human for the folder).
3. Do not create test files unless the human agrees.

| State | When |
|---|---|
| PROVEN | Can create and edit a sheet in the agreed place |
| PARTIAL | Read-only access, or no agreed folder yet |
| MISSING | No access |

**Fix:** Human connects Google Drive/Sheets to the agent, or logs in to Google in Chrome themself, and names the output folder.

## E. Optional now, required for a green

TrendTrack, Google Trends, Meta Ad Library.

Check each one opens and can be read. Record a state for each.
These do not block the start of research. But a product **cannot be green** until all three have been checked for that exact product. Until then it is HOLD.

**Fix:** Human connects or logs in to the missing tool. Google Trends and Meta Ad Library need only a working browser.

---

## Recording the result

1. Copy `preflight/result.example.json` and fill in one state and a short note per check.
2. Optional: run the evaluator. It needs only Python 3.

```
python3 preflight/evaluate.py path/to/your-result.json
```

It prints `GO`, `GO_LIMITED` or `STOP` and the fix for each problem. Exit code 2 means STOP.

3. Copy the five states into the filter receipt for the batch.

Notes must never contain passwords, keys or account IDs.


---

## F. Supplier-agent (Aria) quote channel

**What to prove:** someone can get a delivered US quote this batch.

1. Ask the human which supplier agent quotes delivered cost, and on what channel.
2. Confirm the human will relay quote requests and paste replies back.
3. Do not message the supplier agent yourself unless the human says so.

PROVEN: channel named and quotes can be requested now. PARTIAL: channel exists, reply time unknown. MISSING: no supplier agent — research may run, but nothing can go green.
