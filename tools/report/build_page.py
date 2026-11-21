#!/usr/bin/env python3
"""Build the draft web page from a report.json.

Usage: python3 tools/report/build_page.py state/report.json --out reports/chapter2-draft1-page

Writes:
  <out>/index.html      the full page; opens locally with no server (photos sit next to it)
  <out>/page.html       the same page without the <html>/<head>/<body> wrapper, for publishing as
                        a Claude web page (artifact) together with img/1.jpg ... img/10.jpg
  <out>/img/<rank>.jpg  photos copied from each product's image_file (relative to the report),
                        or downloaded from its img URL

The page design lives in templates/draft-page.html. Launch math, proof checks and watch-outs use
the same bars and formulas as build_report.py (TIERS.md), with the budget and the break-even ROAS
limit taken from the intake (the report's own intake, then intake.json next to the report).
Standard library only. Runs on Python 3.8+.
"""
import argparse
import json
import math
import os
import re
import shutil
import sys
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build_report as br  # noqa: E402  (same folder: parse_num, launch_math and the tier bars)

TEMPLATE = os.path.join(HERE, "..", "..", "templates", "draft-page.html")
SPLIT = "<!--BODY-->"
TARGET_GREENS = 3


def num(v):
    return br.parse_num(v)


def usd(v):
    if v is None:
        return "MISSING"
    return ("-$%s" % format(-v, ",.2f")) if v < 0 else ("$%s" % format(v, ",.2f"))


def short_usd(v):
    if v is None:
        return "MISSING"
    if v >= 1e6:
        return "$%.2fM" % (v / 1e6)
    if v >= 1e3:
        return "$%.1fK" % (v / 1e3)
    return "$%.0f" % v


def text(v):
    """A display string with no em or en dashes; missing values read MISSING."""
    if v is None or str(v).strip() in ("", "—", "–", "-"):
        return "MISSING"
    return str(v).replace("—", "-").replace("–", "-")


def load_intake(rep, report_path):
    intake = dict(rep.get("intake") or {})
    side = os.path.join(os.path.dirname(os.path.abspath(report_path)), "intake.json")
    if os.path.exists(side):
        try:
            for k, v in json.load(open(side, encoding="utf-8")).items():
                intake.setdefault(k, v)
        except (OSError, ValueError):
            pass
    return intake


def launch(p, budget, roas_max):
    m = br.launch_math(p, budget)
    margin, roas = m["margin"], m["roas"]
    weak = None
    if margin is not None and margin <= 0:
        weak = "loss"
    elif roas is not None and roas > roas_max:
        weak = "thin"
    return {
        "margin": margin, "roas": roas, "price_2x": m["price_2x"],
        "sales_day": math.ceil(m["sales_day"] - 1e-9) if m["sales_day"] is not None else None,
        "weak": weak,
    }


def adlib_check(p):
    kws = p.get("keywords") or []
    counted = [k for k in kws if num(k.get("results")) is not None]
    comps = p.get("competitors") or []
    if comps:
        state = "no"
    elif kws and len(counted) == len(kws):
        state = "ok"
    else:
        state = "warn"
    return state, len(counted), len(kws)


def proof(p, adlib_state, counted, total):
    views, orders, cvr, top = num(p.get("views")), num(p.get("orders")), num(p.get("cvr")), num(p.get("topvid"))
    match = (p.get("match") or "").upper()
    comps = p.get("competitors") or []
    sellers = p.get("sellers")
    sell_txt = ("%s pages sell it" % sellers) if sellers not in (None, "") else "Sellers not counted"
    vid_ok = views is not None and orders is not None and views >= br.BAR_VIEWS and orders >= br.BAR_ORDERS
    k = lambda v: ("%gM" % (v / 1e6)) if v >= 1e6 else ("%gK" % (v / 1e3))  # noqa: E731
    rows = [
        {"key": "video", "state": "ok" if vid_ok else "no", "name": "Winning video",
         "value": "%s views, %s orders" % (text(p.get("views")), text(p.get("orders"))),
         "bar": "%s+ views and %d+ orders on one video" % (k(br.BAR_VIEWS), br.BAR_ORDERS)},
        {"key": "cvr", "state": "ok" if cvr is not None and cvr >= br.BAR_CVR else "no", "name": "Conversion",
         "value": ("%g sales per 1K views" % cvr) if cvr is not None else "MISSING",
         "bar": "%g+ sales per 1K views" % br.BAR_CVR},
        {"key": "appeal", "state": "ok" if top is not None and top >= br.BAR_APPEAL else "no", "name": "Appeal video",
         "value": ("%s views" % p.get("topvid")) if top is not None else "None found yet",
         "bar": "one video or ad with %s+ views" % k(br.BAR_APPEAL)},
    ]
    if adlib_state == "ok":
        mv = "%d of %d keywords clear, no one copying" % (counted, total)
    elif adlib_state == "no":
        mv = "%d competitor%s run%s its Kalo videos" % (len(comps), "" if len(comps) == 1 else "s", "s" if len(comps) == 1 else "")
    else:
        mv = "%d of %d keywords counted, re-check the rest" % (counted, total)
    rows.append({"key": "adlib", "state": adlib_state, "name": "Ad Library", "value": mv, "note": sell_txt})
    rows.append({"key": "match", "state": "ok" if match in ("EXACT", "CLOSE") else "warn", "name": "Factory match",
                 "value": "%s item at %s" % (match.title() if match else "No", text(p.get("item_txt"))),
                 "note": "Similar item, so confirm the cost" if match == "SIMILAR" else (
                     "Found on 1688 / Fabulk" if match in ("EXACT", "CLOSE") else "Not found yet")})
    rev = num(p.get("rev"))
    rows.append({"key": "demand", "state": "ok" if rev else "no", "name": "Kalo demand",
                 "value": "%s in 30 days" % short_usd(rev), "note": "Passed the Kalo demand filters"})
    return rows


def watchouts(p, m, roas_max):
    out = []
    if m["weak"] == "loss":
        out.append("Not profitable at the TikTok price: %s against %s delivered. Price it at %s+ or bundle."
                   % (usd(num(p.get("price"))), usd(num(p.get("est_delivered"))), usd(m["price_2x"])))
    elif m["weak"] == "thin":
        out.append("Thin margin: break-even ROAS %.2f is above %.2f. Price it at %s+ or bundle."
                   % (m["roas"], roas_max, usd(m["price_2x"])))
    if (p.get("match") or "").upper() == "SIMILAR":
        out.append("The cost comes from a similar item. Confirm the exact item before launch.")
    r = num(p.get("rating"))
    if r is not None and r < 4.0:
        out.append("Low rating (%g). Expect more refunds and complaints." % r)
    return out


def rivals(p):
    """Group the competitor ads by advertiser, keeping first-seen order."""
    groups = []
    for c in p.get("competitors") or []:
        raw = str(c.get("name") or "Unnamed advertiser")
        likely = bool(re.search(r"\(likely\)\s*$", raw, re.I))
        name = re.sub(r"\s*\(likely\)\s*$", "", raw, flags=re.I).strip() or raw
        g = next((x for x in groups if x["name"] == name), None)
        if g is None:
            g = {"name": name, "ads": []}
            groups.append(g)
        g["ads"].append({"url": c.get("ad") or "", "videos": text(c.get("videos")), "likely": likely})
    return groups


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report")
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    rep = json.load(open(a.report, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(a.report))
    intake = load_intake(rep, a.report)
    budget = num(intake.get("cbo_daily_budget_usd")) or br.DEFAULT_BUDGET
    roas_max = num(intake.get("breakeven_roas_max")) or br.WEAK_ROAS
    os.makedirs(os.path.join(a.out, "img"), exist_ok=True)

    data = []
    for p in sorted(rep["products"], key=lambda x: x["rank"]):
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
        color = p["color"] if p["color"] in ("GREEN", "ORANGE", "YELLOW") else "YELLOW"
        m = launch(p, budget, roas_max)
        adlib_state, counted, total = adlib_check(p)
        checks = proof(p, adlib_state, counted, total)
        data.append({
            "rank": p["rank"], "tier": text(p.get("tier")), "color": color,
            "name": text(p.get("name")), "variant": text(p.get("variant")) if p.get("variant") else "",
            "price": num(p.get("price")), "rev": num(p.get("rev")), "rating": num(p.get("rating")),
            "views": text(p.get("views")), "orders": text(p.get("orders")),
            "cvr": num(p.get("cvr")), "per": num(p.get("per")),
            "topvid": p.get("topvid") if num(p.get("topvid")) is not None else "",
            "sellers": p.get("sellers"), "item_txt": text(p.get("item_txt")),
            "match": (p.get("match") or "").upper() if p.get("match") not in (None, "—") else "",
            "item_url": p.get("item_url") or "", "est": num(p.get("est_delivered")),
            "why": text(p.get("why")) if p.get("why") else "",
            "kalo": p.get("kalo") or "", "video": p.get("video") or "", "trends": p.get("trends") or "",
            "comp_file": p.get("competitor_file") or "",
            "keywords": [{"q": k.get("q") or "", "url": k.get("url") or "",
                          "n": k.get("results") if num(k.get("results")) is not None else None}
                         for k in (p.get("keywords") or [])],
            "adlib_state": adlib_state, "n_comp": len(p.get("competitors") or []),
            "rivals": rivals(p), "math": m, "checks": checks,
            "missing": [c for c in checks if c["key"] in ("video", "cvr", "appeal") and c["state"] != "ok"],
            "watch": watchouts(p, m, roas_max),
        })

    counts = {t: sum(1 for d in data if d["color"] == t) for t in ("GREEN", "ORANGE", "YELLOW")}
    avoid = intake.get("avoid") or []
    if isinstance(avoid, str):
        avoid = [avoid]
    cats = intake.get("categories") or ""
    info = {
        "budget": budget, "roas_max": roas_max, "target": TARGET_GREENS, "counts": counts,
        "hold": counts["GREEN"] < TARGET_GREENS,
        "cbo": text(intake.get("cbo_setup")), "buyer": text(intake.get("demographic")),
        "price_band": text(intake.get("price_band")),
        "categories": ", ".join(cats) if isinstance(cats, list) else text(cats),
        "avoid": [re.sub(r"\s*\(.*\)\s*$", "", str(x)).strip() for x in avoid],
        "brief": text(intake.get("brief")),
        "est_rule": text(rep.get("est_rule") or "Est. delivered = item cost + $5.00 standard (shipping + fees)."),
        "bars": {"views": br.BAR_VIEWS, "orders": br.BAR_ORDERS, "cvr": br.BAR_CVR, "appeal": br.BAR_APPEAL},
    }

    tpl = open(TEMPLATE, encoding="utf-8").read()
    page = (tpl.replace("__DATA__", json.dumps(data, ensure_ascii=False))
               .replace("__INFO__", json.dumps(info, ensure_ascii=False))
               .replace("__TITLE__", br.esc(text(rep["title"])))
               .replace("__DATE__", br.esc(text(rep.get("date", ""))))
               .replace("__SOURCE__", br.esc(text(rep.get("source", "")))))
    head, body = page.split(SPLIT, 1)
    full = ('<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            + head.strip() + "\n</head>\n<body>\n" + body.strip() + "\n</body>\n</html>\n")
    with open(os.path.join(a.out, "index.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(full)
    with open(os.path.join(a.out, "page.html"), "w", encoding="utf-8", newline="\n") as f:
        f.write(head.strip() + "\n" + body.strip() + "\n")
    print("Wrote %s/index.html, %s/page.html and %d photos (Green %d, Orange %d, Yellow %d%s)"
          % (a.out, a.out, len(os.listdir(os.path.join(a.out, "img"))), counts["GREEN"], counts["ORANGE"],
             counts["YELLOW"], ", HOLD" if info["hold"] else ""))


if __name__ == "__main__":
    main()
