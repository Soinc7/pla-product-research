#!/usr/bin/env python3
"""Merge the lane files into state/report.json (the host's step 6-8 in AGENTS.md).

Usage: python3 tools/report/merge_lanes.py --title "Product Research · Chapter 2 · Draft 1" [--state state] [--out state/report.json]

Reads state/intake.json, lane-L1-kalo.json, lane-L2-meta.json, lane-L3-pricing.json,
lane-L4-trendtrack.json and the optional host-overrides.json ({pid: {field: value}}).
Applies TIERS.md (v1.3) and the launch math, then writes report.json for build_report.py.
Missing evidence never counts as a pass. Standard library only.
"""
import argparse
import glob
import json
import math
import os
from urllib.parse import quote

GREEN_ORDERS = 500      # TIERS.md Step 3 (PROPOSED defaults)
GREEN_CVR = 0.6         # orders per 1,000 views
GREEN_VIEWS = 300_000
APPEAL_VIEWS = 100_000


def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def short(n):
    if n is None:
        return "—"
    n = float(n)
    if n >= 1e6:
        return ("%.2fM" % (n / 1e6)).replace(".00M", "M")
    if n >= 1e3:
        return ("%.1fk" % (n / 1e3)).replace(".0k", "k")
    return "%d" % n


def count_txt(r):
    if r is None:
        return "—"
    if isinstance(r, (int, float)):
        return "{:,}".format(int(r))
    return str(r).lstrip("~")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--title", required=True)
    ap.add_argument("--state", default="state")
    ap.add_argument("--out", default=None)
    ap.add_argument("--source", default="Kalodata · US · last 30 days")
    ap.add_argument("--top", type=int, default=10, help="keep the best N after ranking (0 = all)")
    a = ap.parse_args()
    st = a.state
    intake = load(os.path.join(st, "intake.json"), {}) or {}
    # Every round's lane files are read: lane-L1-kalo.json, lane-L1-kalo-r2.json, ... (same for L2-L4).
    def lane(prefix, key):
        out = {}
        for fn in sorted(glob.glob(os.path.join(st, prefix + "*.json"))):
            for r in (load(fn, {}) or {}).get(key, []) or []:
                out.setdefault(r.get("pid"), r)
        return out
    l1 = {"products": [], "observed_at_utc": None}
    seen = set()
    for fn in sorted(glob.glob(os.path.join(st, "lane-L1-kalo*.json"))):
        d = load(fn, {}) or {}
        l1["observed_at_utc"] = l1["observed_at_utc"] or d.get("observed_at_utc")
        for p in d.get("products", []) or []:
            if p.get("pid") and p["pid"] not in seen:
                seen.add(p["pid"])
                l1["products"].append(p)
    l2 = lane("lane-L2-meta", "meta_sweep")
    l3 = lane("lane-L3-pricing", "pricing")
    l4 = lane("lane-L4-trendtrack", "trendtrack")
    over = load(os.path.join(st, "host-overrides.json"), {}) or {}
    budget = intake.get("cbo_daily_budget_usd") or 150
    roas_max = intake.get("breakeven_roas_max") or 3

    rows = []
    for p in l1.get("products", []):
        pid = p["pid"]
        m, pr, tt, ov = l2.get(pid, {}), dict(l3.get(pid, {})), l4.get(pid, {}), over.get(pid, {})
        pr.update({k: v for k, v in ov.items() if k in ("item_usd", "match", "source_url", "note")})
        vids = p.get("videos") or []

        def wins(v):
            vw, od = v.get("views"), v.get("orders")
            return bool(vw and od and od >= GREEN_ORDERS and vw >= GREEN_VIEWS and od / vw * 1000 >= GREEN_CVR)
        # The winning video is the highest-revenue video that clears all three Kalo bars; else video #1.
        best = next((v for v in vids if wins(v)), vids[0] if vids else {})
        views, orders = best.get("views"), best.get("orders")
        cvr = round(orders / views * 1000, 2) if views and orders else None
        per = round(views / orders, -1) if views and orders else None
        item = pr.get("item_usd")
        est = round(item + 5.0, 2) if item is not None else None
        price = ov.get("price", p.get("price"))
        margin = round(price - est, 2) if (price is not None and est is not None) else None
        be = round(price / margin, 2) if margin and margin > 0 else None

        # --- tiers (TIERS.md v1.3) ---
        missing = []
        yellow = p.get("video_count_valid", 0) >= 10 and p.get("evidence") == "PROVEN"
        verdict = m.get("verdict")
        orange = yellow and verdict == "CLEAR"
        appeal = tt.get("best_appeal_views") if tt.get("appeal_100k") == "PROVEN" else None
        checks = {
            "500+ orders on the best video": orders is not None and orders >= GREEN_ORDERS,
            "0.6+ orders per 1K views": cvr is not None and cvr >= GREEN_CVR,
            "300k+ views on the best video": views is not None and views >= GREEN_VIEWS,
            "100k+ appeal video (TrendTrack)": appeal is not None and appeal >= APPEAL_VIEWS,
        }
        missing = [k for k, ok in checks.items() if not ok]
        green = orange and not missing
        color = "GREEN" if green else "ORANGE" if orange else "YELLOW" if yellow else "WHITE"

        comps = []
        for c in m.get("competitors_using_kalo", []) or []:
            nums = " ".join("#%s" % n for n in c.get("kalo_videos", []) or [])
            name = c.get("advertiser") or "Advertiser"
            if c.get("status") == "LIKELY":
                name += " (likely)"
            comps.append({"name": name, "ad": "https://www.facebook.com/ads/library/?id=%s" % c.get("library_id"), "videos": nums})
        kws = [{"q": k.get("q"), "url": k.get("url"),
                "results": "—" if (k.get("status") == "RECHECK" or k.get("results") is None) else count_txt(k.get("results"))}
               for k in (m.get("keywords") or [])]
        if color == "GREEN":
            why = "Clear on all 5 keywords · best video %s views, %s orders" % (short(views), short(orders))
        elif color == "ORANGE":
            why = "Clear on Meta · missing: " + "; ".join(missing)
        elif color == "YELLOW":
            if verdict in ("MATCH", "LIKELY"):
                why = "%d rival%s run%s its Kalo videos" % (len(comps), "" if len(comps) == 1 else "s", "s" if len(comps) == 1 else "")
            elif verdict == "RECHECK":
                why = "Meta keywords throttled · re-check before Orange"
            else:
                why = "Meta check not run yet"
        else:
            why = "Fewer than 10 proven Kalo videos"
        trend_q = ov.get("trend") or " ".join((p.get("name") or "").split()[:3]).lower()
        rows.append({
            "name": ov.get("name", p.get("name")), "variant": ov.get("variant", p.get("variant")) or "",
            "pid": pid, "img": p.get("main_image_url"), "image_file": None,
            "price": price, "rev": p.get("rev_30d"), "rating": p.get("rating"),
            "vid": best.get("vid"), "views": short(views), "orders": short(orders), "cvr": cvr,
            "topvid": short(appeal) if appeal else "—", "trend": trend_q, "sellers": m.get("sellers_count"),
            "item": item, "item_txt": ("$%.2f" % item) if item is not None else "—",
            "match": pr.get("match") if item is not None else "—", "item_url": pr.get("source_url") or "",
            "est_delivered": est, "why": why, "color": color,
            "kalo": p.get("kalo_url"),
            "video": "https://www.kalodata.com/video/detail?id=%s&region=US" % best.get("vid") if best.get("vid") else "",
            "trends": "https://trends.google.com/trends/explore?date=today%203-m&geo=US&q=" + quote(trend_q),
            "keywords": kws, "competitors": comps, "per": per, "competitor_file": "",
            "_be": be if be is not None else math.inf, "_margin": margin,
            "_watch": (margin is not None and margin <= 0) or (be is not None and be > roas_max),
        })

    order = {"GREEN": 0, "ORANGE": 1, "YELLOW": 2, "WHITE": 3}
    rows.sort(key=lambda r: (order[r["color"]], r["_be"]))
    if a.top:
        rows = rows[:a.top]
    counts = {}
    for i, r in enumerate(rows, 1):
        counts[r["color"]] = counts.get(r["color"], 0) + 1
        r["rank"] = i
        r["tier"] = "%s %d" % (r["color"], i)
        for k in ("_be", "_margin", "_watch"):
            r.pop(k)
    cats = intake.get("categories")
    report = {
        "title": a.title,
        "date": (l1.get("observed_at_utc") or "")[:10],
        "source": a.source,
        "intake": {
            "cbo_daily_budget_usd": budget,
            "cbo_setup": intake.get("cbo_setup"),
            "demographic": intake.get("demographic"),
            "price_band": intake.get("price_band"),
            "categories": ", ".join(cats) if isinstance(cats, list) else cats,
            "brief": intake.get("brief"),
        },
        "est_rule": "Est. delivered = 1688 item cost + $5.00 standard (shipping + fees) until a real supplier-agent quote replaces it.",
        "products": rows,
    }
    out = a.out or os.path.join(st, "report.json")
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(report, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print("Wrote %s: %d products · %s" % (out, len(rows), " / ".join("%s %d" % (k, v) for k, v in counts.items())))
    if counts.get("GREEN", 0) < 3:
        print("Fewer than 3 Greens: batch result is HOLD / NEEDS_MORE_CANDIDATES (TIERS.md).")


if __name__ == "__main__":
    main()
