#!/usr/bin/env python3
"""Build every deliverable of a draft in one command, so the host spends no tokens on formatting.

Usage:
  python3 tools/deliver.py --chapter 2 --draft 1 --source "Kalodata AVD-36 · US · 10/21–11/19"
  python3 tools/deliver.py --chapter 2 --draft 2 --skip-merge --no-pdf

Steps (each one is a plain script in tools/; this file only runs them in order):
  1. merge_lanes.py        lane files -> state/report.json (tiers from TIERS.md, launch math, top 10)
  2. photos                each product's main photo saved once to state/photos/<pid>.jpg (image_file in report.json)
  3. build_report.py       reports/chapterC-draftD.html + .pdf
  4. build_page.py         reports/chapterC-draftD-page/ (index.html, page.html + img/) for the Claude web page
  5. build_sheet.py        state/sheet-chC-dD/ (1-create.json, 2-batch-N.json) for the Google Sheet
  6. competitor_links.py   state/sheet-chC-dD/3-competitor-links.json (column M), when the tab links are known
  7. build_competitor_tabs.py  state/compfiles-chC-dD/ (Competitor Files tabs), when TrendTrack data exists
Then it prints what to send, in order. Standard library only. Python 3.8+.
"""
import argparse
import glob
import json
import os
import subprocess
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def run(args):
    print("\n$ " + " ".join(os.path.relpath(x, ROOT) if os.path.isabs(x) and x.startswith(ROOT) else x for x in args[1:]), flush=True)
    r = subprocess.run(args, cwd=ROOT)
    if r.returncode != 0:
        sys.exit("Step failed (exit %d). Fix it and run again." % r.returncode)


def save_photos(report_path, state):
    rep = json.load(open(report_path, encoding="utf-8"))
    os.makedirs(os.path.join(state, "photos"), exist_ok=True)
    got = 0
    for p in rep["products"]:
        if p.get("image_file") and os.path.exists(os.path.join(state, p["image_file"])):
            got += 1
            continue
        rel = "photos/%s.jpg" % p["pid"]
        dest = os.path.join(state, rel)
        if not os.path.exists(dest) and p.get("img"):
            try:
                req = urllib.request.Request(p["img"], headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
                    f.write(r.read())
            except Exception as err:
                print("  photo for #%s not saved (%s); the builders will try the link again" % (p.get("rank"), err))
        if os.path.exists(dest):
            p["image_file"] = rel
            got += 1
    with open(report_path, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rep, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("\nphotos: %d of %d saved under %s/photos/" % (got, len(rep["products"]), os.path.relpath(state, ROOT)))
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", type=int, required=True)
    ap.add_argument("--draft", type=int, required=True)
    ap.add_argument("--source", default="Kalodata · US · last 30 days", help="filter setup and window, shown on every output")
    ap.add_argument("--state", default="state")
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--skip-merge", action="store_true", help="use the existing state/report.json")
    ap.add_argument("--no-pdf", action="store_true")
    a = ap.parse_args()

    py = sys.executable
    state = os.path.join(ROOT, a.state) if not os.path.isabs(a.state) else a.state
    report = os.path.join(state, "report.json")
    c, d = a.chapter, a.draft
    title = "Product Research · Chapter %d · Draft %d" % (c, d)
    tab = "Chapter %d · Draft %d" % (c, d)
    rep_out = os.path.join(ROOT, "reports", "chapter%d-draft%d" % (c, d))
    page_out = rep_out + "-page"
    sheet_out = os.path.join(state, "sheet-ch%d-d%d" % (c, d))
    tabs_out = os.path.join(state, "compfiles-ch%d-d%d" % (c, d))

    if not a.skip_merge:
        run([py, os.path.join(HERE, "report", "merge_lanes.py"), "--title", title, "--source", a.source,
             "--state", state, "--top", str(a.top)])
    rep = save_photos(report, state)
    run([py, os.path.join(HERE, "report", "build_report.py"), report, "--out", rep_out] + (["--no-pdf"] if a.no_pdf else []))
    run([py, os.path.join(HERE, "report", "build_page.py"), report, "--out", page_out])
    run([py, os.path.join(HERE, "sheets", "build_sheet.py"), report, "--tab", tab, "--out", sheet_out])

    linked = sum(1 for p in rep["products"] if p.get("competitor_file"))
    if linked:
        with open(os.path.join(sheet_out, "3-competitor-links.json"), "w", encoding="utf-8") as f:
            subprocess.run([py, os.path.join(HERE, "sheets", "competitor_links.py"), report, "--tab", tab], cwd=ROOT, stdout=f, check=True)
        print("\ncolumn M links: %d of %d products -> %s/3-competitor-links.json" % (linked, len(rep["products"]), os.path.relpath(sheet_out, ROOT)))

    has_tt = glob.glob(os.path.join(state, "lane-L4-trendtrack*.json")) + glob.glob(os.path.join(state, "lane-L5-compfiles*.json"))
    cf_files = sorted(glob.glob(os.path.join(state, "competitor-files-ch%d*.json" % c)))
    cf = json.load(open(cf_files[-1], encoding="utf-8")) if cf_files else {}
    have_tabs = {t.get("pid") for t in cf.get("tabs", [])}
    missing = [p["pid"] for p in rep["products"] if p["pid"] not in have_tabs]
    if has_tt and missing:
        args = [py, os.path.join(HERE, "sheets", "build_competitor_tabs.py"), report, "--out", tabs_out, "--pids", ",".join(missing)]
        if cf.get("spreadsheet_id"):
            args += ["--spreadsheet-id", cf["spreadsheet_id"], "--first-number", str(len(cf.get("tabs", [])) + 1)]
        else:
            args += ["--new-workbook", "Competitor Files — Chapter %d" % c]
        run(args)

    rel = lambda p: os.path.relpath(p, ROOT)  # noqa: E731
    print("\n" + "=" * 72)
    print("%s is built. Send it in this order (sheets worker, see .claude/agents/pla-sheets-worker.md):" % title)
    n = 1
    if has_tt and missing:
        if cf.get("spreadsheet_id"):
            print("%d. Competitor Files: send %s/1-add.json, 2-values.json, 3-format.json to workbook %s." % (n, rel(tabs_out), cf["spreadsheet_id"]))
        else:
            print("%d. Competitor Files: Drive-create %s/0-create.json (add the folder as parents), then 1-add, 2-values, 3-format." % (n, rel(tabs_out)))
        n += 1
        print("%d. Save the tab links (tabs.json + workbook id) as %s/competitor-files-ch%d.json, then run this again so column M" % (n, rel(state), c))
        print('   and the page buttons link to the new tabs:  python3 tools/deliver.py --chapter %d --draft %d --source "%s"' % (c, d, a.source))
        n += 1
    print("%d. Google Sheet: Drive-create %s/1-create.json (add the folder as parents), then each 2-batch-N.json in order%s." % (
        n, rel(sheet_out), ", then 3-competitor-links.json" if linked else ""))
    n += 1
    print("%d. Read the sheet back (tabs, rows 5-14, tiers in column D, links in column M)." % n)
    n += 1
    print("%d. Claude web page: publish %s/page.html with its img/ files (a Claude Artifact), or share index.html." % (n, rel(page_out)))
    n += 1
    print("%d. Report: %s.pdf and .html. Check the draft against STANDARD.md, then write the end-of-run report." % (n, rel(rep_out)))


if __name__ == "__main__":
    main()
