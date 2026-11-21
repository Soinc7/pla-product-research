#!/usr/bin/env python3
"""Build the Competitor Files workbook tabs (templates/sheet-layout.md, "Companion workbook") as Sheets API bodies.

Usage:
  python3 tools/sheets/build_competitor_tabs.py state/report.json --out state/compfiles \
      [--spreadsheet-id <id>] [--new-workbook "Competitor Files — Chapter 2"] [--pids a,b] [--first-number 11]

Reads (all from the report's folder, normally state/):
  report.json                 tiers, ranks and short names of the draft's products
  lane-L1-kalo*.json          Kalo link, price, revenue, main photo per product
  lane-L4-trendtrack*.json    TrendTrack: top_tiktok, plus competitor_stores / running_ads when the worker saved them
  lane-L5-compfiles*.json     TrendTrack competitor data (older runs kept it in its own file)
  lane-L2-meta*.json          Meta competitors running the Kalo videos (later files win)
  host-overrides.json         short names and variants
Writes to --out:
  0-create.json   only with --new-workbook: Drive create body (add "parents": ["<folder id>"] before sending)
  1-add.json      spreadsheets/<id>:batchUpdate, adds one tab per product (sheetId = 2000 + tab number)
  2-values.json   spreadsheets/<id>/values:batchUpdate (USER_ENTERED, one range per tab; send one range per call if large)
  3-format.json   spreadsheets/<id>:batchUpdate, banner, headers, widths, wrapping
  tabs.json       [{rank, pid, title, sheetId, gid_url}] to save as state/competitor-files-<chapter>.json ("tabs": [...])
Tabs are named "T<n> · <short name>", n = the product's rank in the draft (or --first-number onward for extra tabs).
A product with nothing found gets a "none found" line, never a blank section. Standard library only.
"""
import argparse
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "report"))
from merge_lanes import lane_files  # noqa: E402  (base lane file first, re-checks after, later wins)

TIER_FILL = {"GREEN": "#1E8E3E", "ORANGE": "#E37400", "YELLOW": "#B08800", "WHITE": "#5F6368"}


def load(path, default=None):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return default


def by_pid(folder, pattern, key):
    out = {}
    for fn in lane_files(folder, pattern):
        for r in (load(fn, {}) or {}).get(key, []) or []:
            if r.get("pid"):
                out.setdefault(r["pid"], {}).update({k: v for k, v in r.items() if v not in (None, [], "")})
    return out


def q(s):
    return str(s).replace('"', '""')


def link(url, label):
    return '=HYPERLINK("%s","%s")' % (q(url), q(label)) if url else label


def money(v):
    if v is None or v == "":
        return ""
    return "$%s" % format(v, ",.2f") if isinstance(v, (int, float)) else str(v)


def num(v):
    if v is None or v == "":
        return ""
    return format(v, ",") if isinstance(v, int) else str(v)


def rgb(h):
    return {"red": int(h[1:3], 16) / 255, "green": int(h[3:5], 16) / 255, "blue": int(h[5:7], 16) / 255}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--out", required=True)
    ap.add_argument("--spreadsheet-id", default="", help="existing workbook id, to fill gid_url in tabs.json")
    ap.add_argument("--new-workbook", default="", help="name for a new workbook; also writes 0-create.json and drops the default Sheet1")
    ap.add_argument("--pids", default="", help="comma list of product IDs (default: every product in the report)")
    ap.add_argument("--first-number", type=int, default=0, help="number tabs from N onward instead of by report rank")
    a = ap.parse_args()

    st = os.path.dirname(os.path.abspath(a.report))
    rep = load(a.report, {}) or {}
    rprods = {p["pid"]: p for p in rep.get("products", [])}
    l1 = {}
    for fn in lane_files(st, "lane-L1-kalo*.json"):
        for p in (load(fn, {}) or {}).get("products", []) or []:
            l1.setdefault(p.get("pid"), p)
    tt = by_pid(st, "lane-L4-trendtrack*.json", "trendtrack")
    for pid, v in by_pid(st, "lane-L5-compfiles*.json", "products").items():
        tt.setdefault(pid, {}).update(v)
    meta = {}
    for fn in lane_files(st, "lane-L2-meta*.json"):
        for m in (load(fn, {}) or {}).get("meta_sweep", []) or []:
            meta[m.get("pid")] = m  # later files win
    ov = load(os.path.join(st, "host-overrides.json"), {}) or {}

    pids = [x.strip() for x in a.pids.split(",") if x.strip()] or [p["pid"] for p in sorted(rprods.values(), key=lambda p: p["rank"])]
    os.makedirs(a.out, exist_ok=True)
    adds, fmts, data, tabs = [], [], [], []
    for i, pid in enumerate(pids):
        k, c, o, m, rp = l1.get(pid, {}), tt.get(pid, {}), ov.get(pid, {}), meta.get(pid, {}), rprods.get(pid)
        n = (a.first_number + i) if a.first_number else (rp["rank"] if rp else 90 + i)
        sid = 2000 + n
        name = o.get("name") or (rp or {}).get("name") or (k.get("name") or pid)[:40]
        variant = o.get("variant") or (rp or {}).get("variant") or ""
        tier = (rp or {}).get("color") or "YELLOW"
        title = ("T%d · %s" % (n, name))[:100]
        status = ("%s %d" % (tier, rp["rank"])) if rp else "%s (not in this draft's top 10)" % tier
        adds.append({"addSheet": {"properties": {"sheetId": sid, "title": title, "gridProperties": {"rowCount": 80, "columnCount": 8}}}})
        rows, heads, titles = [], [], []
        rows.append([" · ".join(x for x in (status, name, variant) if x)])
        rows.append([link(k.get("kalo_url") or (rp or {}).get("kalo"), "Open Kalo ↗"),
                     "Kalo list price %s · 30-day revenue %s" % (money(k.get("price", (rp or {}).get("price"))), money(k.get("rev_30d", (rp or {}).get("rev"))))])
        rows.append([])
        qy = c.get("queries", {}) if isinstance(c.get("queries"), dict) else {}
        rows.append(["1. Competitor stores (TrendTrack%s)" % ((", AND query: " + qy["stores"]) if qy.get("stores") else "")]); titles.append(len(rows))
        rows.append(["Store", "Product page", "Price", "Est. 30-day revenue", "Active Meta ads", "Note"]); heads.append(len(rows))
        st_rows = c.get("competitor_stores") or []
        for s in st_rows:
            rows.append([s.get("store") or "", link(s.get("product_url"), "Product page ↗"), money(s.get("price")),
                         money(s.get("est_rev_30d")), num(s.get("active_meta_ads")), s.get("note") or ""])
        if not st_rows:
            rows.append(["none found" + ((": " + c["notes"][:280]) if c.get("notes") else " in TrendTrack search_products")])
        rows.append([])
        rows.append(["2. Their running Meta ads (TrendTrack)"]); titles.append(len(rows))
        rows.append(["Preview", "Advertiser", "Days running", "Reach / est. spend", "Hook text (script idea)", "Watch video", "Ad Library", "Landing page"]); heads.append(len(rows))
        ads = c.get("running_ads") or []
        for ad in ads:
            lib = ad.get("library_id")
            rows.append([('=IMAGE("%s",1)' % q(ad["thumbnail_url"])) if ad.get("thumbnail_url") else "", ad.get("advertiser") or "",
                         num(ad.get("days_running")), str(ad.get("reach_or_spend") or ""), ad.get("hook") or "", link(ad.get("video_url"), "Watch ↗"),
                         link("https://www.facebook.com/ads/library/?id=%s" % lib if lib else "", "Ad Library ↗ %s" % (lib or "")),
                         link(ad.get("landing_page"), "Landing ↗")])
        if not ads:
            rows.append(["none found in TrendTrack search_ads (US, video)"])
        rows.append([])
        rows.append(["Meta competitors using the Kalo videos (from the Meta sweep)"]); titles.append(len(rows))
        rows.append(["Advertiser", "Ad Library link", "Kalo video", "Status"]); heads.append(len(rows))
        comps = m.get("competitors_using_kalo") or []
        for cc in comps:
            lib = cc.get("library_id")
            rows.append([cc.get("advertiser") or "", link("https://www.facebook.com/ads/library/?id=%s" % lib if lib else "", "Ad Library ↗ %s" % (lib or "")),
                         " ".join("#%s" % x for x in cc.get("kalo_videos") or []), cc.get("status") or "MATCHED"])
        if not comps:
            rows.append([{"CLEAR": "none: all 5 keywords clear, none of the 10 Kalo videos found in Meta ads",
                          "RECHECK": "not checked yet: Meta was throttled, re-check pending (never read as 'no competitor')"}.get(m.get("verdict"), "Meta check not run yet")])
        rows.append([])
        rows.append(["3. TrendTrack top TikTok videos (caption search, US, by views)"]); titles.append(len(rows))
        rows.append(["Preview", "Creator", "Views", "Likes", "Hook / caption", "Match", "Open"]); heads.append(len(rows))
        vids = c.get("top_tiktok") or []
        for t in vids[:10]:
            rows.append([('=IMAGE("%s",1)' % q(t["url"])) if t.get("url") else "", t.get("creator") or "", num(t.get("views")), num(t.get("likes")),
                         (t.get("hook") or "")[:200], t.get("match") or "", link(t.get("video_link"), "Open ↗")])
        if not vids:
            rows.append(["none found: the TrendTrack caption search returned no videos of this product"])
        same = [t.get("views") or 0 for t in vids if "SAME" in str(t.get("match") or "")]
        if same and max(same) < 100000:
            rows.append(["No same-product video reaches 100K views."])
        rows.append([])
        rows.append(["4. Reference photo (Kalo main product image)"]); titles.append(len(rows))
        img = k.get("main_image_url") or (rp or {}).get("img")
        rows.append(['=IMAGE("%s",1)' % q(img)] if img else ["MISSING"])
        photo = len(rows)
        data.append({"range": "'%s'!A1:H%d" % (title.replace("'", "''"), len(rows)), "values": rows})

        fill = rgb(TIER_FILL.get(tier, TIER_FILL["YELLOW"]))
        fmts += [
            {"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 8},
                            "cell": {"userEnteredFormat": {"backgroundColor": fill, "textFormat": {"bold": True, "fontSize": 13, "foregroundColor": {"red": 1, "green": 1, "blue": 1}}}},
                            "fields": "userEnteredFormat(backgroundColor,textFormat)"}},
            {"mergeCells": {"range": {"sheetId": sid, "startRowIndex": 0, "endRowIndex": 1, "startColumnIndex": 0, "endColumnIndex": 8}, "mergeType": "MERGE_ALL"}},
            {"updateDimensionProperties": {"range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": 0, "endIndex": 8}, "properties": {"pixelSize": 170}, "fields": "pixelSize"}},
            {"updateDimensionProperties": {"range": {"sheetId": sid, "dimension": "COLUMNS", "startIndex": 4, "endIndex": 5}, "properties": {"pixelSize": 320}, "fields": "pixelSize"}},
            {"repeatCell": {"range": {"sheetId": sid, "startRowIndex": 1, "endRowIndex": 80, "startColumnIndex": 0, "endColumnIndex": 8},
                            "cell": {"userEnteredFormat": {"wrapStrategy": "WRAP", "verticalAlignment": "MIDDLE"}}, "fields": "userEnteredFormat(wrapStrategy,verticalAlignment)"}},
            {"updateDimensionProperties": {"range": {"sheetId": sid, "dimension": "ROWS", "startIndex": photo - 1, "endIndex": photo}, "properties": {"pixelSize": 220}, "fields": "pixelSize"}},
        ]
        for r in heads:
            fmts.append({"repeatCell": {"range": {"sheetId": sid, "startRowIndex": r - 1, "endRowIndex": r, "startColumnIndex": 0, "endColumnIndex": 8},
                                        "cell": {"userEnteredFormat": {"backgroundColor": {"red": 0.93, "green": 0.94, "blue": 0.96}, "textFormat": {"bold": True}}},
                                        "fields": "userEnteredFormat(backgroundColor,textFormat)"}})
        for r in titles:
            fmts.append({"repeatCell": {"range": {"sheetId": sid, "startRowIndex": r - 1, "endRowIndex": r, "startColumnIndex": 0, "endColumnIndex": 1},
                                        "cell": {"userEnteredFormat": {"textFormat": {"bold": True, "fontSize": 11}}}, "fields": "userEnteredFormat.textFormat"}})
        gid = ("https://docs.google.com/spreadsheets/d/%s/edit#gid=%d" % (a.spreadsheet_id, sid)) if a.spreadsheet_id else ""
        tabs.append({"rank": n, "pid": pid, "title": title, "sheetId": sid, "gid_url": gid})
        print("%-44s stores %d · ads %d · Meta rivals %d · TikTok %d" % (title, len(st_rows), len(ads), len(comps), len(vids)))

    if a.new_workbook:
        adds.append({"deleteSheet": {"sheetId": 0}})  # the default "Sheet1" of a new workbook
        with open(os.path.join(a.out, "0-create.json"), "w", encoding="utf-8") as f:
            json.dump({"name": a.new_workbook, "mimeType": "application/vnd.google-apps.spreadsheet"}, f, ensure_ascii=False)
    for fn, body in (("1-add.json", {"requests": adds}), ("2-values.json", {"valueInputOption": "USER_ENTERED", "data": data}),
                     ("3-format.json", {"requests": fmts}), ("tabs.json", tabs)):
        with open(os.path.join(a.out, fn), "w", encoding="utf-8") as f:
            json.dump(body, f, ensure_ascii=False, indent=1 if fn == "tabs.json" else None)
    print("Wrote %d tabs to %s (1-add, 2-values, 3-format, tabs.json%s)." % (len(tabs), a.out, ", 0-create" if a.new_workbook else ""))
    if not a.spreadsheet_id:
        print("No --spreadsheet-id given: fill gid_url in tabs.json once the workbook id is known (https://docs.google.com/spreadsheets/d/<id>/edit#gid=<sheetId>).")


if __name__ == "__main__":
    main()
