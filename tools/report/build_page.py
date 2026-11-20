#!/usr/bin/env python3
"""Build the draft web page (the Chapter 1 · Draft 2 design) from state/report.json.

Usage: python3 tools/report/build_page.py state/report.json --out reports/chapter2-draft1-page

Writes <out>/index.html plus <out>/img/<rank>.jpg (photos copied from the report's image_file or
downloaded from its img URL), ready to publish as a web page or open locally.
Standard library only (Pillow optional, not needed).
"""
import argparse
import json
import os
import shutil
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "..", "templates", "draft-page.html")


def num(v):
    try:
        return float(str(v).replace(",", "").replace("$", ""))
    except (TypeError, ValueError):
        return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rep = json.load(open(a.report, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(a.report))
    os.makedirs(os.path.join(a.out, "img"), exist_ok=True)
    data = []
    for p in rep["products"]:
        dest = os.path.join(a.out, "img", "%d.jpg" % p["rank"])
        src = os.path.join(base, p["image_file"]) if p.get("image_file") else None
        try:
            if src and os.path.exists(src):
                shutil.copyfile(src, dest)
            elif p.get("img"):
                req = urllib.request.Request(p["img"], headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=30) as r, open(dest, "wb") as f:
                    f.write(r.read())
        except Exception as err:  # the page shows "No photo" for a missing file
            print("photo #%d not saved: %s" % (p["rank"], err))
        data.append({
            "name": p.get("name"), "variant": p.get("variant") or "", "img": p.get("img"),
            "price": num(p.get("price")) or 0, "rev": num(p.get("rev")) or 0, "rating": num(p.get("rating")) or 0,
            "views": p.get("views"), "orders": p.get("orders"), "cvr": p.get("cvr") if p.get("cvr") is not None else "—",
            "topvid": p.get("topvid") or "—", "sellers": p.get("sellers"),
            "item_txt": p.get("item_txt") or "—", "match": p.get("match") or "—", "item_url": p.get("item_url") or "",
            "why": p.get("why") or "", "rank": p["rank"], "tier": p["tier"], "color": p["color"] if p["color"] != "WHITE" else "YELLOW",
            "kalo": p.get("kalo") or "", "video": p.get("video") or "", "trends": p.get("trends") or "",
            "comp_file": p.get("competitor_file") or "", "keywords": p.get("keywords") or [],
            "competitors": p.get("competitors") or [], "per": p.get("per") or 0,
            "est": p.get("est_delivered") if p.get("est_delivered") is not None else 0,
        })
    html = open(TEMPLATE, encoding="utf-8").read()
    html = (html.replace("__DATA__", json.dumps(data, ensure_ascii=False))
                .replace("__TITLE__", rep["title"])
                .replace("__DATE__", rep.get("date", ""))
                .replace("__SOURCE__", rep.get("source", "")))
    with open(os.path.join(a.out, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(html)
    print("Wrote %s/index.html and %d photos" % (a.out, len(os.listdir(os.path.join(a.out, "img")))))


if __name__ == "__main__":
    main()
