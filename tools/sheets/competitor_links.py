#!/usr/bin/env python3
"""Body for a Sheets values:batchUpdate that links column M of a draft tab to the Competitor Files tabs.

Usage: python3 tools/sheets/competitor_links.py state/report.json --tab "Chapter 2 · Draft 1" > body.json
Send to POST https://sheets.googleapis.com/v4/spreadsheets/<id>/values:batchUpdate. Standard library only.
"""
import argparse
import json

ap = argparse.ArgumentParser()
ap.add_argument("report")
ap.add_argument("--tab", required=True)
a = ap.parse_args()
rep = json.load(open(a.report, encoding="utf-8"))
vals = []
for p in rep["products"]:
    url = p.get("competitor_file")
    label = "Open file ↗ · top video %s" % (p.get("topvid") or "—")
    vals.append(['=HYPERLINK("%s","%s")' % (url, label)] if url else ["—"])
n = len(vals)
print(json.dumps({"valueInputOption": "USER_ENTERED",
                  "data": [{"range": "'%s'!M5:M%d" % (a.tab, 4 + n), "values": vals}]}, ensure_ascii=False))
