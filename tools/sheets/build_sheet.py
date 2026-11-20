#!/usr/bin/env python3
"""Turn state/report.json into Google Sheets API requests (templates/sheet-layout.md, tab 1-3).

Usage: python3 tools/sheets/build_sheet.py state/report.json --tab "Chapter 2 · Draft 1" --out state/sheet

Writes:
  <out>/1-create.json   body for POST https://www.googleapis.com/drive/v3/files?supportsAllDrives=true
                        (add "parents": ["<Drive folder id>"] before sending)
  <out>/2-batch-N.json  bodies for POST https://sheets.googleapis.com/v4/spreadsheets/<id>:batchUpdate, sent in order
Send them with any Sheets/Drive connector (for example Composio PROXY_EXECUTE), then read the sheet back.
The first tab of a new spreadsheet has sheetId 0. IMAGE() needs the owner's one-time "Allow access" click.
Standard library only.
"""
import argparse
import json
import os

GREEN, ORANGE, YELLOW, GREY = "#1E8E3E", "#E37400", "#B08800", "#5F6368"
WHY_FILL = {"GREEN": "#E6F4EA", "ORANGE": "#FEF0E0", "YELLOW": "#FFF8D6", "WHITE": "#FFFFFF"}
NAME_FILL = {"GREEN": "#00FF00", "ORANGE": "#FFA500", "YELLOW": "#FFFF00", "WHITE": "#FFFFFF"}
TIER_FILL = {"GREEN": GREEN, "ORANGE": ORANGE, "YELLOW": YELLOW, "WHITE": GREY}
LINK = "#1155CC"
HEAD = ["#", "Picture", "Product", "Tier", "Kalo", "Price", "30-day revenue", "Rating", "Winning video",
        "Sales per 1K views\n(not ROAS)", "Meta Ad Library\n5 keywords", "Competitor check\n(uses Kalo videos?)",
        "Competitor file", "Google Trends", "1688 / Fabulk\nitem cost", "Est. delivered\n(standard)", "Why"]
WIDTHS = [36, 118, 210, 96, 92, 70, 84, 64, 170, 110, 260, 230, 120, 84, 130, 100, 240]


def rgb(h):
    h = h.lstrip("#")
    return {"red": int(h[0:2], 16) / 255, "green": int(h[2:4], 16) / 255, "blue": int(h[4:6], 16) / 255}


def q(s):
    return str(s).replace('"', '""')


def link_cell(url, label):
    if not url:
        return {"userEnteredValue": {"stringValue": label}}
    return {"userEnteredValue": {"formulaValue": '=HYPERLINK("%s","%s")' % (q(url), q(label))},
            "userEnteredFormat": {"textFormat": {"foregroundColor": rgb(LINK)}}}


def runs_cell(parts, base=None):
    """parts: list of (text, url_or_None, fmt_dict_or_None). Builds one cell with several links (textFormatRuns)."""
    text, runs = "", []
    for t, url, fmt in parts:
        f = dict(fmt or {})
        if url:
            f.update({"foregroundColor": rgb(LINK), "underline": True, "link": {"uri": url}})
        runs.append({"startIndex": len(text), "format": f})
        text += t
    runs = [r for i, r in enumerate(runs) if r["startIndex"] < len(text) and (i == 0 or r["startIndex"] != runs[i - 1]["startIndex"])]
    cell = {"userEnteredValue": {"stringValue": text}, "textFormatRuns": runs}
    if base:
        cell["userEnteredFormat"] = base
    return cell


def num(v):
    try:
        return float(str(v).replace(",", "").replace("$", ""))
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--tab", required=True)
    ap.add_argument("--out", default="state/sheet")
    a = ap.parse_args()
    rep = json.load(open(a.report, encoding="utf-8"))
    ps = rep["products"]
    budget = (rep.get("intake") or {}).get("cbo_daily_budget_usd") or 150
    os.makedirs(a.out, exist_ok=True)
    counts = {}
    for p in ps:
        counts[p["color"]] = counts.get(p["color"], 0) + 1
    tiers = " / ".join("%d %s" % (counts[c], c.title()) for c in ("GREEN", "ORANGE", "YELLOW", "WHITE") if counts.get(c))

    title = rep["title"].replace("Product Research · ", "Product Research — ")
    json.dump({"name": title, "mimeType": "application/vnd.google-apps.spreadsheet"},
              open(os.path.join(a.out, "1-create.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    reqs = [
        {"updateSheetProperties": {"properties": {"sheetId": 0, "title": a.tab,
                                                  "gridProperties": {"frozenRowCount": 4, "frozenColumnCount": 3}},
                                   "fields": "title,gridProperties.frozenRowCount,gridProperties.frozenColumnCount"}},
        {"addSheet": {"properties": {"sheetId": 1001, "title": "Top videos"}}},
        {"addSheet": {"properties": {"sheetId": 1002, "title": "How it was graded"}}},
    ]
    for i, w in enumerate(WIDTHS):
        reqs.append({"updateDimensionProperties": {"range": {"sheetId": 0, "dimension": "COLUMNS", "startIndex": i, "endIndex": i + 1},
                                                   "properties": {"pixelSize": w}, "fields": "pixelSize"}})
    for r0, h in ((0, 34), (1, 24), (2, 28), (3, 44)):
        reqs.append({"updateDimensionProperties": {"range": {"sheetId": 0, "dimension": "ROWS", "startIndex": r0, "endIndex": r0 + 1},
                                                   "properties": {"pixelSize": h}, "fields": "pixelSize"}})
    reqs.append({"updateDimensionProperties": {"range": {"sheetId": 0, "dimension": "ROWS", "startIndex": 4, "endIndex": 4 + len(ps)},
                                               "properties": {"pixelSize": 120}, "fields": "pixelSize"}})
    for r0 in (0, 1):
        reqs.append({"mergeCells": {"range": {"sheetId": 0, "startRowIndex": r0, "endRowIndex": r0 + 1, "startColumnIndex": 0, "endColumnIndex": 17}, "mergeType": "MERGE_ALL"}})
    # legend chips in row 3: A:D, E:H, I:L, M:Q
    for c0, c1 in ((0, 4), (4, 8), (8, 12), (12, 17)):
        reqs.append({"mergeCells": {"range": {"sheetId": 0, "startRowIndex": 2, "endRowIndex": 3, "startColumnIndex": c0, "endColumnIndex": c1}, "mergeType": "MERGE_ALL"}})

    banner = {"textFormat": {"fontFamily": "Montserrat", "bold": True, "fontSize": 16, "foregroundColor": rgb("#FFFFFF")},
              "backgroundColor": rgb("#1F4E3D"), "verticalAlignment": "MIDDLE"}
    sub = {"textFormat": {"fontFamily": "Montserrat", "fontSize": 10, "foregroundColor": rgb("#FFFFFF")},
           "backgroundColor": rgb("#2F6F56"), "verticalAlignment": "MIDDLE"}
    chip = lambda bg: {"textFormat": {"fontFamily": "Montserrat", "bold": True, "fontSize": 10, "foregroundColor": rgb("#FFFFFF")},
                       "backgroundColor": rgb(bg), "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE", "wrapStrategy": "WRAP"}
    status = "HOLD — fewer than 3 Greens, more candidates next draft" if counts.get("GREEN", 0) < 3 else "3+ Greens"
    rows = [
        {"values": [{"userEnteredValue": {"stringValue": title}, "userEnteredFormat": banner}]},
        {"values": [{"userEnteredValue": {"stringValue": "%s · %s · %s · %s · launch math at $%s/day %s" % (
            rep.get("date", ""), rep.get("source", ""), tiers, status, budget, (rep.get("intake") or {}).get("cbo_setup") or "")},
            "userEnteredFormat": sub}]},
        {"values": [
            {"userEnteredValue": {"stringValue": "GREEN = winning video verified"}, "userEnteredFormat": chip(GREEN)}, {}, {}, {},
            {"userEnteredValue": {"stringValue": "ORANGE = no competitor uses the Kalo videos, all 5 keywords clear"}, "userEnteredFormat": chip(ORANGE)}, {}, {}, {},
            {"userEnteredValue": {"stringValue": "YELLOW = demand proven, a competitor uses the videos or a check is pending"}, "userEnteredFormat": chip(YELLOW)}, {}, {}, {},
            {"userEnteredValue": {"stringValue": "EXACT / CLOSE / SIMILAR = price match · Est. delivered = item + $5.00"}, "userEnteredFormat": chip(GREY)}]},
        {"values": [{"userEnteredValue": {"stringValue": h},
                     "userEnteredFormat": {"textFormat": {"fontFamily": "Montserrat", "bold": True, "fontSize": 10, "foregroundColor": rgb("#FFFFFF")},
                                           "backgroundColor": rgb("#2F6F56"), "horizontalAlignment": "CENTER", "verticalAlignment": "MIDDLE", "wrapStrategy": "WRAP"}}
                    for h in HEAD]},
    ]
    body_fmt = {"textFormat": {"fontFamily": "Arial", "fontSize": 10}, "verticalAlignment": "MIDDLE", "wrapStrategy": "WRAP"}
    for i, p in enumerate(ps):
        band = "#FFFFFF" if i % 2 == 0 else "#F7F9FA"
        c = p["color"]
        kw_parts = []
        for j, k in enumerate(p.get("keywords") or []):
            res = k.get("results")
            res = "RECHECK" if res in (None, "—") else res
            kw_parts.append(("%d. %s · %s ↗" % (j + 1, k.get("q"), res), k.get("url"), None))
            kw_parts.append(("\n", None, None))
        if kw_parts:
            kw_parts.pop()
        comps = p.get("competitors") or []
        sellers = p.get("sellers")
        if not p.get("keywords"):
            ver = runs_cell([("⟳ Meta check not run", None, {"foregroundColor": rgb("#B06000"), "bold": True})])
        elif any((k.get("results") in (None, "—")) for k in p["keywords"]):
            ver = runs_cell([("⟳ Re-check: throttled keywords", None, {"foregroundColor": rgb("#B06000"), "bold": True})])
        elif not comps:
            ver = runs_cell([("✓ No competitor using\nthe Kalo videos", None, {"foregroundColor": rgb("#196633"), "bold": True}),
                             (("\n%s pages sell it" % sellers) if sellers is not None else "", None, {"foregroundColor": rgb("#595959")})])
        else:
            parts = [("✗ %d competitor%s run%s its\nKalo videos" % (len(comps), "" if len(comps) == 1 else "s", "s" if len(comps) == 1 else ""),
                      None, {"foregroundColor": rgb("#CC1919"), "bold": True})]
            for x in comps[:6]:
                parts.append(("\n", None, None))
                parts.append(("%s · %s ↗" % (x["name"], x.get("videos") or ""), x.get("ad"), None))
            if len(comps) > 6:
                parts.append(("\n+%d more" % (len(comps) - 6), None, {"foregroundColor": rgb("#595959")}))
            ver = runs_cell(parts)
        cvr = p.get("cvr")
        per = p.get("per")
        cvr_txt = ("%.2f\n1 per %s" % (cvr, "{:,}".format(int(per)) if per else "—")) if cvr is not None else "—"
        rating = num(p.get("rating"))
        item_lbl = "%s · %s ↗" % (p.get("item_txt"), p.get("match")) if p.get("item_url") else (p.get("item_txt") or "—")
        est = p.get("est_delivered")
        row = [
            {"userEnteredValue": {"numberValue": p["rank"]}, "userEnteredFormat": {"horizontalAlignment": "CENTER"}},
            {"userEnteredValue": {"formulaValue": '=IMAGE("%s",1)' % q(p["img"])}} if p.get("img") else {"userEnteredValue": {"stringValue": "—"}},
            {"userEnteredValue": {"stringValue": "%s\n%s" % (p["name"], p.get("variant") or "")},
             "userEnteredFormat": {"textFormat": {"fontFamily": "Montserrat", "bold": True}, "backgroundColor": rgb(NAME_FILL[c])}},
            {"userEnteredValue": {"stringValue": p["tier"]},
             "userEnteredFormat": {"textFormat": {"bold": True, "foregroundColor": rgb("#FFFFFF")}, "backgroundColor": rgb(TIER_FILL[c]), "horizontalAlignment": "CENTER"}},
            link_cell(p.get("kalo"), "Open Kalo ↗"),
            {"userEnteredValue": {"numberValue": num(p.get("price"))} if num(p.get("price")) is not None else {"stringValue": "—"},
             "userEnteredFormat": {"numberFormat": {"type": "CURRENCY", "pattern": "$0.00"}}},
            {"userEnteredValue": {"stringValue": "$%.1fK" % (num(p.get("rev")) / 1000) if num(p.get("rev")) else "—"}},
            {"userEnteredValue": {"stringValue": ("%.1f★" % rating) if rating is not None else "—"},
             "userEnteredFormat": {"textFormat": {"foregroundColor": rgb("#CC1919" if rating is not None and rating < 4.0 else "#000000")}}},
            link_cell(p.get("video"), "%s views · %s orders ↗" % (p.get("views"), p.get("orders"))),
            {"userEnteredValue": {"stringValue": cvr_txt},
             "userEnteredFormat": {"textFormat": {"foregroundColor": rgb("#CC1919" if cvr is not None and cvr < 0.6 else "#000000")}}},
            runs_cell(kw_parts) if kw_parts else {"userEnteredValue": {"stringValue": "—"}},
            ver,
            {"userEnteredValue": {"stringValue": "top video %s" % p.get("topvid", "—") if p.get("topvid") not in (None, "—") else "—"}},
            link_cell(p.get("trends"), "Trends ↗"),
            link_cell(p.get("item_url"), item_lbl),
            {"userEnteredValue": {"stringValue": ("$%.2f est." % est) if est is not None else "—"}},
            {"userEnteredValue": {"stringValue": p.get("why") or ""}, "userEnteredFormat": {"backgroundColor": rgb(WHY_FILL[c])}},
        ]
        for cell in row:
            f = dict(body_fmt)
            f["backgroundColor"] = rgb(band)
            f.update(cell.get("userEnteredFormat") or {})
            if "textFormat" in (cell.get("userEnteredFormat") or {}):
                tf = dict(body_fmt["textFormat"])
                tf.update(cell["userEnteredFormat"]["textFormat"])
                f["textFormat"] = tf
            cell["userEnteredFormat"] = f
        rows.append({"values": row})
    for s in range(0, len(rows), 3):
        reqs.append({"updateCells": {"rows": rows[s:s + 3], "start": {"sheetId": 0, "rowIndex": s, "columnIndex": 0},
                                     "fields": "userEnteredValue,userEnteredFormat,textFormatRuns"}})

    # Tab 2: Top videos (best video per product; Kalo #1-#3 are in the lane file)
    tv = [{"values": [{"userEnteredValue": {"stringValue": h}, "userEnteredFormat": {"textFormat": {"bold": True}}} for h in
                      ("Product", "Tier", "Winning video", "Sales per 1K views", "Competitors using Kalo videos")]}]
    for p in ps:
        tv.append({"values": [{"userEnteredValue": {"stringValue": p["name"]}},
                              {"userEnteredValue": {"stringValue": p["tier"]}, "userEnteredFormat": {"backgroundColor": rgb(NAME_FILL[p["color"]])}},
                              link_cell(p.get("video"), "%s views · %s orders ↗" % (p.get("views"), p.get("orders"))),
                              {"userEnteredValue": {"stringValue": str(p.get("cvr") if p.get("cvr") is not None else "—")}},
                              {"userEnteredValue": {"stringValue": ", ".join("%s (%s)" % (x["name"], x.get("videos")) for x in p.get("competitors") or []) or "none found"}}]})
    reqs.append({"updateCells": {"rows": tv, "start": {"sheetId": 1001, "rowIndex": 0, "columnIndex": 0}, "fields": "userEnteredValue,userEnteredFormat"}})

    graded = [("Step", "What was checked", "Bar to pass"),
              ("1. Demand (Yellow)", "Kalo filter setup, 10 same-product videos", "AVD-36 filters, 10 valid videos"),
              ("2. No copycat (Orange)", "Meta Ad Library, 5 keywords, first frames of the top 10 Kalo videos", "All 5 keywords clear, no Kalo video matched"),
              ("3. Winning video (Green)", "Kalo orders/views of one video + TrendTrack appeal", "500+ orders, 0.6+ per 1K views, 300k+ views, a 100k+ appeal video"),
              ("Cost (flag)", "1688/Fabulk item cost, EXACT/CLOSE/SIMILAR", "Est. delivered = item + $5.00 until a real quote"),
              ("Launch math (rank)", "Margin, break-even ROAS at the CBO budget", "Break-even ROAS ≤ 3 or a watch-out with the fix"),
              ("Google Trends", "3-month US interest", "Shown, not scored")]
    reqs.append({"updateCells": {"rows": [{"values": [{"userEnteredValue": {"stringValue": v}, "userEnteredFormat": {"textFormat": {"bold": i == 0}, "wrapStrategy": "WRAP"}} for v in r]} for i, r in enumerate(graded)],
                                 "start": {"sheetId": 1002, "rowIndex": 0, "columnIndex": 0}, "fields": "userEnteredValue,userEnteredFormat"}})
    for sid, widths in ((1001, [240, 100, 220, 130, 360]), (1002, [200, 380, 380])):
        for i, w in enumerate(widths):
            reqs.append({"updateDimensionProperties": {"range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": i, "endIndex": i + 1},
                                                       "properties": {"pixelSize": w}, "fields": "pixelSize"}})
    # Split into parts of at most ~30 KB so each connector call stays small. Send them in order.
    parts, cur = [], []
    for r in reqs:
        if cur and len(json.dumps(cur + [r], ensure_ascii=False)) > 30000:
            parts.append(cur)
            cur = []
        cur.append(r)
    if cur:
        parts.append(cur)
    for old in os.listdir(a.out):
        if old.startswith("2-batch"):
            os.remove(os.path.join(a.out, old))
    for i, part in enumerate(parts, 1):
        json.dump({"requests": part}, open(os.path.join(a.out, "2-batch-%d.json" % i), "w", encoding="utf-8"), ensure_ascii=False)
    print("Wrote %s/1-create.json and %d batch parts 2-batch-1..%d.json (%d requests, %d product rows)" % (a.out, len(parts), len(parts), len(reqs), len(ps)))


if __name__ == "__main__":
    main()
