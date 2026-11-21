#!/usr/bin/env python3
"""Build a self-contained HTML report (+ PDF) from a product-research report.json.

Usage:
    python3 tools/report/build_report.py examples/chapter1/report.json --out reports/chapter1-draft3

Standard library only. Pillow is used to shrink large photos if it is installed.
The PDF is printed with headless Chrome/Chromium/Edge, or Playwright as a fallback.
"""
import argparse
import base64
import html
import io
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from pathlib import Path

try:  # optional
    from PIL import Image  # type: ignore
except Exception:  # pragma: no cover
    Image = None

DEFAULT_BUDGET = 150.0
BAR_CVR, BAR_ORDERS, BAR_VIEWS, BAR_APPEAL = 0.6, 500, 300_000, 100_000
WEAK_ROAS = 3.0
MAX_IMG_PX = 640

PLACEHOLDER_SVG = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 300 300">'
    '<rect width="300" height="300" fill="#eceff1"/>'
    '<rect x="95" y="105" width="110" height="80" rx="8" fill="none" stroke="#b0b8bf" stroke-width="6"/>'
    '<circle cx="128" cy="132" r="9" fill="#b0b8bf"/>'
    '<path d="M103 178l32-30 22 20 16-12 26 22z" fill="#b0b8bf"/>'
    '<text x="150" y="222" font-family="sans-serif" font-size="15" fill="#8a949c" text-anchor="middle">No photo</text>'
    '</svg>'
)


# ----------------------------------------------------------------- helpers
def esc(v):
    return html.escape("" if v is None else str(v), quote=True)


def parse_num(v):
    """'2.25M' -> 2250000, '1.4k' -> 1400, '2,300' -> 2300, '—'/None -> None."""
    if v is None:
        return None
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).strip().replace(",", "").replace("$", "")
    m = re.match(r"^([0-9]*\.?[0-9]+)\s*([kKmMbB]?)\+?$", s)
    if not m:
        return None
    return float(m.group(1)) * {"": 1, "k": 1e3, "m": 1e6, "b": 1e9}[m.group(2).lower()]


def money(v, cents=True):
    if v is None:
        return "—"
    return f"${v:,.2f}" if cents else f"${v:,.0f}"


def short_money(v):
    if v is None:
        return "—"
    if v >= 1e6:
        return f"${v / 1e6:.2f}M"
    if v >= 1e3:
        return f"${v / 1e3:.1f}K"
    return f"${v:,.0f}"


def safe_url(u):
    u = (u or "").strip()
    return u if re.match(r"^https?://", u, re.I) else ""


def link(url, label, cls=""):
    url = safe_url(url)
    if not url:
        return f'<span class="lnk off {cls}">{esc(label)}</span>'
    return f'<a class="lnk {cls}" href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>'


# ------------------------------------------------------------------ images
def _mime(data):
    if data[:3] == b"\xff\xd8\xff":
        return "image/jpeg"
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        return "image/png"
    if data[:6] in (b"GIF87a", b"GIF89a"):
        return "image/gif"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    return None


def _shrink(data, mime):
    if Image is None:
        return data, mime
    try:
        im = Image.open(io.BytesIO(data))
        if max(im.size) <= MAX_IMG_PX and mime == "image/jpeg":
            return data, mime
        im = im.convert("RGB")
        im.thumbnail((MAX_IMG_PX, MAX_IMG_PX))
        buf = io.BytesIO()
        im.save(buf, "JPEG", quality=86, optimize=True)
        return buf.getvalue(), "image/jpeg"
    except Exception:
        return data, mime


def image_data_uri(product, base_dir, notes):
    """Local image_file -> download img URL -> neutral placeholder. Always a data: URI."""
    data = None
    f = product.get("image_file")
    if f:
        p = Path(f)
        p = p if p.is_absolute() else base_dir / p
        try:
            data = p.read_bytes()
        except OSError:
            notes.append(f"#{product.get('rank')}: image_file not found ({f})")
    if data is None and safe_url(product.get("img")):
        try:
            req = urllib.request.Request(product["img"], headers={"User-Agent": "Mozilla/5.0 (report-builder)"})
            with urllib.request.urlopen(req, timeout=15) as r:
                data = r.read(8_000_000)
            notes.append(f"#{product.get('rank')}: photo downloaded from img URL")
        except Exception as e:
            notes.append(f"#{product.get('rank')}: img download failed ({type(e).__name__})")
            data = None
    if data:
        mime = _mime(data)
        if mime:
            data, mime = _shrink(data, mime)
            return f"data:{mime};base64,{base64.b64encode(data).decode()}"
        notes.append(f"#{product.get('rank')}: unrecognised image format")
    notes.append(f"#{product.get('rank')}: placeholder used")
    return "data:image/svg+xml;base64," + base64.b64encode(PLACEHOLDER_SVG.encode()).decode()


# ------------------------------------------------------------- launch math
def launch_math(p, budget):
    price = parse_num(p.get("price"))
    deliv = parse_num(p.get("est_delivered"))
    rev = parse_num(p.get("rev"))
    m = {"price": price, "deliv": deliv, "rev": rev, "budget": budget, "margin": None, "roas": None,
         "sales_day": None, "price_2x": None, "kalo_orders": None, "share": None, "weak": None, "ok": False}
    if price and rev:
        m["kalo_orders"] = rev / price
    if deliv is not None:
        m["price_2x"] = 2 * deliv
    if price is not None and deliv is not None:
        m["margin"] = price - deliv
        if m["margin"] > 0:
            m["ok"] = True
            m["roas"] = price / m["margin"]
            m["sales_day"] = budget / m["margin"]
            if m["kalo_orders"]:
                m["share"] = m["sales_day"] / (m["kalo_orders"] / 30) * 100
            if m["roas"] > WEAK_ROAS:
                m["weak"] = "thin"
        else:
            m["weak"] = "loss"
    return m


def need_sales(m):
    return f"~{math.ceil(m['sales_day'] - 1e-9)}" if m["sales_day"] is not None else "—"


def gates(p, m):
    """Each gate: (state, label). state: ok | no | warn | info. Derived from data, never from the tier."""
    views, orders, cvr = parse_num(p.get("views")), parse_num(p.get("orders")), parse_num(p.get("cvr"))
    top = parse_num(p.get("topvid"))
    comps = p.get("competitors") or []
    kws = p.get("keywords") or []
    counted = [k for k in kws if parse_num(k.get("results")) is not None]
    sellers = p.get("sellers")
    match = (p.get("match") or "").upper()
    g = {}
    g["demand"] = ("ok" if m["rev"] else "no",
                   f"Kalo demand {money(m['rev'], False)}/30d" + (f" · ≈{m['kalo_orders']:,.0f} orders/mo" if m["kalo_orders"] else ""))
    vid_ok = views is not None and orders is not None and views >= BAR_VIEWS and orders >= BAR_ORDERS
    g["video"] = ("ok" if vid_ok else "no",
                  f"Winning video {p.get('views') or '—'} views · {p.get('orders') or '—'} orders (bar 300K+ / 500+)")
    g["cvr"] = ("ok" if cvr is not None and cvr >= BAR_CVR else "no",
                f"Conversion {cvr if cvr is not None else '—'} sales per 1K views (bar {BAR_CVR})")
    g["appeal"] = ("ok" if top is not None and top >= BAR_APPEAL else "no",
                   f"Appeal video {p.get('topvid') or '—'} views (bar 100K+)"
                   if top is not None else "Appeal video not proven (need one 100K+ video)")
    seller_txt = f"{sellers} sellers" if sellers not in (None, "") else "sellers not counted"
    if comps:
        g["meta"] = ("no", f"Copied on Meta: {len(comps)} competitor{'s' if len(comps) != 1 else ''} running its Kalo videos · {seller_txt}")
    elif kws and len(counted) == len(kws):
        g["meta"] = ("ok", f"{len(counted)}/{len(kws)} Meta keywords clear · {seller_txt}, none copying")
    else:
        g["meta"] = ("warn", f"Meta check incomplete: {len(counted)}/{len(kws)} keywords counted · {seller_txt}")
    g["match"] = ({"EXACT": "ok", "CLOSE": "ok"}.get(match, "warn"),
                  f"Factory match {match or '—'} · item {p.get('item_txt') or '—'}"
                  + (" (similar item, confirm the cost)" if match == "SIMILAR" else ""))
    g["cost"] = ("info", f"Est. delivered {money(m['deliv'])}" + (f" · {money(m['margin'])} left per sale at TikTok price" if m["margin"] is not None else ""))
    return g


def missing_reasons(g):
    out = []
    if g["video"][0] != "ok":
        out.append("winning video not proven (needs 500+ orders and 300K+ views)")
    if g["cvr"][0] != "ok":
        out.append("conversion under the 0.6 bar")
    if g["appeal"][0] != "ok":
        out.append("no 100K+ appeal video yet")
    return out


def watchouts(p, m):
    out = []
    if m["weak"] == "loss":
        out.append(f"Not profitable at the TikTok price ({money(m['price'])} vs {money(m['deliv'])} delivered) — "
                   f"price it at {money(m['price_2x'])}+ or bundle.")
    elif m["weak"] == "thin":
        out.append(f"Thin margin at TikTok price — break-even ROAS {m['roas']:.2f}. "
                   f"Price it at {money(m['price_2x'])}+ or bundle.")
    if (p.get("match") or "").upper() == "SIMILAR":
        out.append("Cost comes from a similar item, not the exact one — confirm before launch.")
    r = parse_num(p.get("rating"))
    if r is not None and r < 4.0:
        out.append(f"Low rating ({r:g}) — expect more refunds and complaints.")
    return out


# ------------------------------------------------------------------ pieces
MARK = {"ok": "✓", "no": "✗", "warn": "!", "info": "•"}


def checklist(g, keys=("demand", "video", "cvr", "appeal", "meta", "match", "cost")):
    rows = "".join(f'<li class="g-{g[k][0]}"><span class="mk">{MARK[g[k][0]]}</span><span>{esc(g[k][1])}</span></li>' for k in keys)
    return f'<ul class="proof">{rows}</ul>'


def keyword_block(p, g):
    kws = p.get("keywords") or []
    chips = "".join(
        f'<a class="kw" href="{esc(safe_url(k.get("url")) or "#")}" target="_blank" rel="noopener">'
        f'<span class="kq">{esc(k.get("q"))}</span><span class="kn">{esc(k.get("results") or "—")}</span></a>'
        for k in kws)
    state = g["meta"][0]
    verdict = {"ok": "CLEAR — no competitor uses its Kalo videos",
               "no": "COPIED — competitors run its Kalo videos",
               "warn": "RECHECK — keyword counts missing"}[state]
    return (f'<div class="kwbox"><div class="kwhead"><span class="lbl">Meta Ad Library · {len(kws)} keywords (video ads found)</span>'
            f'<span class="verdict v-{state}">{MARK[state]} {esc(verdict)}</span></div><div class="kws">{chips}</div></div>')


def cost_block(p, m):
    match = (p.get("match") or "—").upper()
    item = link(p.get("item_url"), p.get("item_txt") or "—", "plain")
    margin = money(m["margin"]) if m["margin"] is not None else "—"
    mcls = "neg" if (m["margin"] is not None and m["margin"] <= 0) else ""
    return (f'<div class="costs">'
            f'<div class="cost"><div class="lbl">Item cost <span class="tag t-{esc(match.lower())}">{esc(match)}</span></div><div class="val">{item}</div></div>'
            f'<div class="cost"><div class="lbl">Est. delivered</div><div class="val">{money(m["deliv"])}</div></div>'
            f'<div class="cost"><div class="lbl">TikTok price</div><div class="val">{money(m["price"])}</div></div>'
            f'<div class="cost {mcls}"><div class="lbl">Margin / sale</div><div class="val">{margin}</div></div>'
            f'</div>')


def math_block(m, compact=False):
    b = money(m["budget"], False)
    if m["margin"] is None:
        body = '<div class="mline">Launch math not available (price or est. delivered missing).</div>'
    elif not m["ok"]:
        body = (f'<div class="mline bad"><b>Not profitable at this price.</b> Every sale loses {money(-m["margin"])} at the TikTok price. '
                f'Price needed for a 2.0 break-even ROAS: <b>{money(m["price_2x"])}</b>.</div>')
    else:
        share = f' That is about {m["share"]:.0f}% of what it already sells per day on TikTok Shop.' if m["share"] else ""
        tiles = (f'<div class="mt"><div class="mv">{need_sales(m)}</div><div class="ml">sales/day to break even at {b}/day</div></div>'
                 f'<div class="mt"><div class="mv">{m["roas"]:.2f}</div><div class="ml">break-even ROAS</div></div>'
                 f'<div class="mt"><div class="mv">{money(m["price_2x"])}</div><div class="ml">price for a 2.0 break-even ROAS</div></div>'
                 f'<div class="mt"><div class="mv">{m["kalo_orders"]:,.0f}</div><div class="ml">Kalo orders / month (≈)</div></div>'
                 if m["kalo_orders"] else "")
        if compact:
            body = (f'<div class="mline">At {b}/day: <b>{need_sales(m)} sales/day</b> to break even · break-even ROAS <b>{m["roas"]:.2f}</b> · '
                    f'2.0-ROAS price <b>{money(m["price_2x"])}</b>'
                    + (f' · Kalo ≈ <b>{m["kalo_orders"]:,.0f}</b> orders/mo' if m["kalo_orders"] else "") + '</div>')
        else:
            body = (f'<div class="mtiles">{tiles}</div>'
                    f'<div class="mline">At {b}/day you need {need_sales(m)} sales/day to break even ({money(m["margin"])} margin per sale).{share}</div>')
    return (f'<div class="math{" compact" if compact else ""}"><div class="lbl">Launch math at {b}/day CBO '
            f'<span class="ref">· uses TikTok price as reference; your store price/bundles change this</span></div>{body}</div>')


def links_block(p):
    return ('<div class="links">' + link(p.get("kalo"), "Open Kalo") + link(p.get("video"), "Winning video")
            + link(p.get("competitor_file"), "Competitor file") + link(p.get("trends"), "Google Trends") + '</div>')


def watch_block(p, m):
    w = watchouts(p, m)
    if not w:
        return ""
    return '<div class="watch"><b>Watch-outs:</b> ' + " ".join(esc(x) for x in w) + '</div>'


def copied_block(p):
    comps = p.get("competitors") or []
    if not comps:
        return ""
    rows = "".join(f'<li>{link(c.get("ad"), c.get("name") or "competitor", "plain")}'
                   f'<span class="cv">Kalo video {esc(c.get("videos") or "—")}</span></li>' for c in comps)
    return (f'<div class="copied"><div class="chead">⚠ Copied on Meta — {len(comps)} competitor{"s" if len(comps) != 1 else ""} '
            f'already run its Kalo videos</div><ul>{rows}</ul></div>')


def stats_block(p, m):
    def t(v, l):
        return f'<div class="st"><div class="sv">{esc(v)}</div><div class="sl">{esc(l)}</div></div>'
    return ('<div class="stats">' + t(short_money(m["rev"]), "30-day revenue") + t(money(m["price"]), "TikTok price")
            + t(f'{p.get("rating", "—")}★', "rating") + t(p.get("views") or "—", "video views")
            + t(p.get("orders") or "—", "video orders") + t(p.get("cvr", "—"), "sales / 1K views") + '</div>')


def title_block(p):
    var = f'<span class="variant">{esc(p.get("variant"))}</span>' if p.get("variant") else ""
    return f'<h3>{esc(p.get("name"))} {var}</h3><div class="why">{esc(p.get("why"))}</div>'


def short_watch(m):
    if m["weak"] == "loss":
        return f"Loses money at the TikTok price — price it at {money(m['price_2x'])}+"
    if m["weak"] == "thin":
        return f"Thin margin — price it at {money(m['price_2x'])}+ or bundle"
    return ""


def card(p, m, g, img):
    color = (p.get("color") or "YELLOW").upper()
    c = color.lower()
    pid = f'p{esc(p.get("rank"))}'
    pill = f'<span class="pill p-{c}">{esc(p.get("tier") or color)}</span>'
    photo = f'<div class="photo"><img src="{img}" alt="{esc(p.get("name"))}"></div>'
    head = f'<div class="chd">{pill}<span class="rk">#{esc(p.get("rank"))}</span>'
    if color == "YELLOW" or color not in ("GREEN", "ORANGE"):
        reason = "Do not launch — copied" if p.get("competitors") else "Not proven"
        return (f'<article class="card c-yellow" id="{pid}">{head}<span class="hold red">{reason}</span></div>'
                f'<div class="ybody"><div class="y1"><div class="yt">{photo}<div>{title_block(p)}</div></div>{stats_block(p, m)}{links_block(p)}</div>'
                f'<div class="y2">{copied_block(p)}{watch_block(p, m)}</div>'
                f'<div class="y3">{math_block(m, compact=True)}{cost_block(p, m)}{keyword_block(p, g)}</div></div></article>')
    if color == "GREEN":
        proven = all(g[k][0] == "ok" for k in ("demand", "video", "cvr", "appeal", "meta"))
        if proven and not m["weak"]:
            extra = '<div class="seal">✓ Launch-ready<small>all proof gates passed</small></div>'
        elif proven:
            extra = '<div class="seal priced">✓ Launch-ready<small>proof passed · fix the price first</small></div>'
        else:
            extra = ""
        mid, compact = "", False
    else:
        extra = '<span class="hold">Hold — not proven yet</span>'
        miss = missing_reasons(g) or ["winning video not proven"]
        mid = '<div class="missing"><b>What is missing for Green:</b> ' + esc("; ".join(miss)) + '.</div>'
        compact = True
    return (f'<article class="card c-{c}" id="{pid}">{head}{extra}</div>'
            f'<div class="cbody"><div class="cside">{photo}{cost_block(p, m)}{links_block(p)}</div>'
            f'<div class="cmain">{title_block(p)}{mid}{stats_block(p, m)}{checklist(g)}'
            f'{math_block(m, compact=compact)}{keyword_block(p, g)}</div></div>{watch_block(p, m)}</article>')


def hero(p, m, g, img):
    b = money(m["budget"], False)
    if m["ok"]:
        share = f'<div class="hshare">That is about <b>{m["share"]:.0f}%</b> of the ≈{m["kalo_orders"] / 30:,.0f} orders/day it already gets on TikTok Shop.</div>' if m["share"] else ""
        big = (f'<div class="hmath"><div class="hm"><div class="hv">{need_sales(m)}</div><div class="hl">sales/day to break even at {b}/day</div></div>'
               f'<div class="hm"><div class="hv">{m["roas"]:.2f}</div><div class="hl">break-even ROAS</div></div>'
               f'<div class="hm"><div class="hv">{money(m["margin"])}</div><div class="hl">margin per sale</div></div>'
               f'<div class="hm"><div class="hv">{m["kalo_orders"]:,.0f}</div><div class="hl">Kalo orders / month (≈)</div></div></div>'
               f'<div class="hline">At {b}/day you need {need_sales(m)} sales/day to break even; break-even ROAS {m["roas"]:.2f}. '
               f'Price for a 2.0 break-even ROAS: {money(m["price_2x"])}.</div>{share}')
    else:
        big = math_block(m)
    return (f'<section class="hero" id="p{esc(p.get("rank"))}"><div class="ribbon">WINNER</div>'
            f'<div class="hkick">Pick this first · {esc(p.get("tier"))}</div>'
            f'<div class="hgrid"><div class="hphoto"><img src="{img}" alt="{esc(p.get("name"))}"></div>'
            f'<div class="hmain"><h2>{esc(p.get("name"))}</h2><div class="hvar">{esc(p.get("variant"))}</div>'
            f'<div class="hwhy">{esc(p.get("why"))}</div>{checklist(g)}</div></div>'
            f'<div class="hbox"><div class="lbl">Launch math at {b}/day CBO</div>{big}'
            f'<div class="fine">Uses TikTok price as reference; your store price/bundles change this.</div></div>'
            f'{watch_block(p, m)}{cost_block(p, m)}{keyword_block(p, g)}{links_block(p)}</section>')


def podium(items):
    if not items:
        return ""
    cols = []
    for p, m, g, img in items:
        if m["ok"]:
            line = f'<b>{need_sales(m)} sales/day</b> to break even · ROAS <b>{m["roas"]:.2f}</b>'
            cls = "weak" if m["weak"] else ""
        else:
            line, cls = "<b>Not profitable at this price</b>", "weak"
        note = f'<div class="pnote">{esc(short_watch(m))}</div>' if m["weak"] else ""
        cols.append(f'<a class="pod" href="#p{esc(p.get("rank"))}"><img src="{img}" alt="">'
                    f'<div class="pinfo"><span class="pill p-green sm">{esc(p.get("tier"))}</span>'
                    f'<div class="pname">{esc(p.get("name"))}</div>'
                    f'<div class="pnum">{short_money(m["rev"])}/30d · {esc(p.get("views"))} views · {esc(p.get("orders"))} orders · {esc(p.get("cvr"))}/1K</div>'
                    f'<div class="pmath {cls}">{line}</div>{note}</div></a>')
    return ('<section class="podium avoid"><div class="sech small">Next in line — the other Greens</div>'
            f'<div class="pods">{"".join(cols)}</div></section>')


def scoreboard(rows, budget):
    def cell(state, txt=""):
        return f'<td class="s-{state}">{MARK[state] if state != "info" else ""}{(" " + esc(txt)) if txt else ""}</td>'
    trs = []
    for p, m, g, _ in rows:
        c = (p.get("color") or "").lower()
        if m["ok"]:
            roas = f'<td class="{"s-no" if m["weak"] else "s-ok"}">{m["roas"]:.2f}</td>'
            need = f'<td>{need_sales(m)}</td>'
        else:
            roas, need = '<td class="s-no">loss</td>', '<td class="s-no">—</td>'
        passed = sum(1 for k in ("demand", "meta", "video", "cvr", "appeal") if g[k][0] == "ok")
        trs.append(f'<tr class="r-{c}"><td class="nm"><span class="dot d-{c}"></span><a href="#p{esc(p.get("rank"))}">{esc(p.get("rank"))}. {esc(p.get("name"))}</a></td>'
                   + cell(g["demand"][0], short_money(m["rev"])) + cell(g["meta"][0]) + cell(g["video"][0], str(p.get("orders") or "—"))
                   + cell(g["cvr"][0], str(p.get("cvr", "—"))) + cell(g["appeal"][0], str(p.get("topvid") or "—"))
                   + f'<td class="s-{g["match"][0]}">{esc((p.get("match") or "—").title())}</td>' + roas + need
                   + f'<td class="tot t{passed}">{passed}/5</td></tr>')
    return ('<section class="score avoid"><div class="sech">The mountain of data — every product against every gate</div>'
            '<table><thead><tr><th>Product</th><th>Kalo demand</th><th>Meta clear</th><th>Video orders 500+</th><th>Conv. 0.6+</th>'
            f'<th>Appeal 100K+</th><th>Factory</th><th>Break-even ROAS</th><th>Sales/day at {money(budget, False)}</th><th>Proof</th></tr></thead>'
            f'<tbody>{"".join(trs)}</tbody></table>'
            '<div class="fine">Proof = the five tier gates (demand, Meta clear, video orders + views, conversion, appeal). '
            'Factory match and break-even ROAS are shown for choosing between products; red numbers are weak at the TikTok price.</div></section>')


CSS = r"""
*{box-sizing:border-box}
html{-webkit-print-color-adjust:exact;print-color-adjust:exact}
body{margin:0;background:#f4f6f8;color:#1c2430;font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:#0b57d0;text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:980px;margin:0 auto;padding:22px 18px 40px}
.top{background:#12261a;color:#fff;border-radius:16px;padding:20px 24px;display:flex;justify-content:space-between;align-items:flex-end;gap:16px;flex-wrap:wrap}
.top h1{margin:0;font-size:25px;letter-spacing:-.3px}.top .meta{font-size:12.5px;opacity:.85;text-align:right}
.top .bud{display:inline-block;margin-top:8px;background:#1E8E3E;border-radius:999px;padding:4px 12px;font-weight:700;font-size:13px}
.panel{background:#fff;border:1px solid #e1e5ea;border-radius:16px;padding:18px 20px;margin-top:16px}
.sech{font-size:17px;font-weight:800;margin:0 0 10px;letter-spacing:-.2px}.sech.small{font-size:14px}
.lbl{font-size:10.5px;font-weight:700;text-transform:uppercase;letter-spacing:.7px;color:#647080;margin-bottom:5px}
.fine{font-size:11px;color:#6b7684;margin-top:6px}
.igrid{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.ibox{background:#f6f8fa;border-radius:10px;padding:10px 12px}.ibox .v{font-weight:700;font-size:13.5px}
.ibox.b{background:#e6f4ea}.ibox.b .v{font-size:20px;color:#14672c}
.brief{margin-top:12px;border-left:4px solid #1E8E3E;padding:4px 0 4px 14px}.brief p{margin:0;color:#333d49}
.legend{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}
.leg{border-radius:12px;padding:12px 14px;border:1px solid}.leg p{margin:8px 0 0;font-size:13px}
.leg.g{background:#e6f4ea;border-color:#a8d5b5}.leg.o{background:#fff4e5;border-color:#f5cf9b}.leg.y{background:#f7f3df;border-color:#e3d79a;color:#5d5a48}
.pill{display:inline-block;border-radius:999px;color:#fff;font-weight:800;letter-spacing:.6px;padding:6px 16px;font-size:14px}
.pill.sm{padding:2px 9px;font-size:10.5px}.pill.big{font-size:17px;padding:7px 20px}
.p-green{background:#1E8E3E}.p-orange{background:#E37400}.p-yellow{background:#B08800}
.why3{display:grid;grid-template-columns:1.25fr 1fr 1fr;gap:10px;margin-top:12px}
.w3{border-radius:10px;padding:10px 12px;font-size:12.5px}.w3 b{display:block;font-size:22px;line-height:1.1}
.w3.g{background:#1E8E3E;color:#fff}.w3.o{background:#fff4e5;color:#7a4300}.w3.y{background:#eeeade;color:#6f6a55}
/* hero */
.hero{position:relative;overflow:hidden;margin-top:16px;border-radius:18px;padding:22px 24px;background:linear-gradient(135deg,#0f5c27,#1E8E3E 60%,#2aa652);color:#fff;border:2px solid #0f5c27}
.ribbon{position:absolute;top:22px;right:-44px;transform:rotate(45deg);background:#ffd54a;color:#3a2c00;font-weight:900;letter-spacing:2px;padding:6px 56px;font-size:14px;box-shadow:0 2px 6px rgba(0,0,0,.25)}
.hkick{font-weight:800;text-transform:uppercase;letter-spacing:1.4px;font-size:12.5px;color:#d5f5dd}
.hgrid{display:grid;grid-template-columns:250px 1fr;gap:20px;margin-top:10px;align-items:start}
.hphoto img{width:250px;height:250px;object-fit:cover;border-radius:14px;border:4px solid #fff;display:block;background:#fff}
.hero h2{margin:0;font-size:30px;line-height:1.1;letter-spacing:-.5px;padding-right:70px}
.hvar{opacity:.9;font-size:14px;margin-top:3px}.hwhy{margin:8px 0 10px;font-weight:700;font-size:15px;color:#fff6c9}
.proof{list-style:none;margin:0;padding:0}.proof li{display:flex;gap:8px;align-items:flex-start;padding:2.5px 0;font-size:13px}
.mk{flex:0 0 19px;height:19px;border-radius:50%;display:inline-flex;align-items:center;justify-content:center;font-weight:900;font-size:12px;color:#fff;margin-top:1px}
.g-ok .mk{background:#1E8E3E}.g-no .mk{background:#c5221f}.g-warn .mk{background:#E37400}.g-info .mk{background:#8a949c}
.g-no{color:#a11512;font-weight:600}
.hero .proof li{font-size:14px;padding:3.5px 0;color:#fff}.hero .g-ok .mk{background:#fff;color:#14672c}.hero .g-info .mk{background:rgba(255,255,255,.4)}
.hbox{background:#fff;color:#1c2430;border-radius:14px;padding:14px 16px;margin-top:16px}
.hmath{display:grid;grid-template-columns:repeat(4,1fr);gap:10px}
.hm{background:#e6f4ea;border-radius:10px;padding:10px 8px;text-align:center}.hv{font-size:28px;font-weight:900;color:#14672c;line-height:1.1}.hl{font-size:11px;color:#3c4a57;margin-top:3px}
.hline{margin-top:10px;font-weight:700;font-size:14.5px}.hshare{font-size:13px;color:#3c4a57;margin-top:2px}
.hero .costs,.hero .kwbox{background:#fff;color:#1c2430;border-radius:12px;padding:10px 12px;margin-top:10px;border:0}
.hero .links{margin-top:12px}.hero .lnk{background:#fff;color:#14672c;border-color:#fff}
.hero .watch{background:#fff8e1;color:#5c3b00}
/* podium */
.podium{margin-top:14px}.pods{display:grid;grid-template-columns:repeat(3,1fr);gap:10px}
.pod{display:flex;gap:10px;background:#fff;border:2px solid #1E8E3E;border-radius:12px;padding:10px;color:inherit}.pod:hover{text-decoration:none}
.pod img{width:72px;height:72px;border-radius:8px;object-fit:cover;flex:0 0 72px}
.pname{font-weight:800;font-size:13.5px;line-height:1.2;margin:4px 0 2px}.pnum{font-size:11px;color:#55606d}
.pmath{font-size:12px;margin-top:4px;color:#14672c}.pmath.weak{color:#a11512}.pnote{font-size:10.5px;color:#8a4b00;margin-top:2px}
/* scoreboard */
.score table{width:100%;border-collapse:collapse;font-size:12px}
.score th{font-size:10px;text-transform:uppercase;letter-spacing:.4px;color:#647080;text-align:center;padding:5px 4px;border-bottom:2px solid #dfe3e8;line-height:1.2}
.score th:first-child,.score td.nm{text-align:left}
.score td{padding:6px 4px;text-align:center;border-bottom:1px solid #edf0f3;white-space:nowrap}
.score td.nm{white-space:normal;font-weight:700}.score td.nm a{color:inherit}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:6px}.d-green{background:#1E8E3E}.d-orange{background:#E37400}.d-yellow{background:#B08800}
.s-ok{color:#14672c;font-weight:700}.s-no{color:#c5221f;font-weight:700}.s-warn{color:#b35c00;font-weight:700}
.r-green td{background:#eef8f1}.r-orange td{background:#fff9f0}.r-yellow td{background:#f8f7f1;color:#6f6a55}.r-yellow td.nm{font-weight:500}
.tot{font-weight:900}.r-green .tot{color:#fff;background:#1E8E3E!important}
/* tier sections + cards */
.tierhead{display:flex;align-items:center;gap:12px;margin:20px 0 8px}.tierhead p{margin:0;font-size:13.5px;color:#3c4a57}
.card{background:#fff;border-radius:16px;margin-top:12px;padding:12px 16px;border:1px solid #e1e5ea}
.chd{display:flex;align-items:center;gap:10px;margin-bottom:7px}.rk{font-weight:800;color:#647080}
.cbody{display:grid;gap:16px;align-items:start}
.photo img{display:block;width:100%;aspect-ratio:1/1;object-fit:cover;border-radius:12px;background:#f1f3f5}
.card h3{margin:0;font-size:20px;line-height:1.15;letter-spacing:-.2px}.variant{font-weight:500;font-size:13px;color:#647080}
.why{font-size:13px;color:#3c4a57;margin:4px 0 8px;font-weight:600}
.stats{display:grid;grid-template-columns:repeat(6,1fr);gap:6px;margin:6px 0}
.st{background:#f6f8fa;border-radius:8px;padding:6px 4px;text-align:center}.sv{font-weight:800;font-size:14.5px}.sl{font-size:9.5px;color:#647080;text-transform:uppercase;letter-spacing:.3px}
.cside .costs{grid-template-columns:1fr 1fr;gap:5px;margin-top:8px}.cside .cost{padding:5px 7px}.cside .cost .val{font-size:14px}.cside .cost .lbl{font-size:9px;letter-spacing:.3px;margin-bottom:2px}
.cside .links{display:grid;grid-template-columns:1fr 1fr;gap:5px;margin-top:8px}.cside .lnk{font-size:10.5px;padding:4px 2px;text-align:center}.cside .lnk.plain{padding:0;text-align:left;font-size:inherit}
.cmain .proof{columns:2;column-gap:14px;margin-top:6px}.cmain .proof li{break-inside:avoid;font-size:12px;padding:2px 0}
.c-green{border:2.5px solid #1E8E3E;border-left-width:10px;background:linear-gradient(180deg,#e3f4e8,#fff 200px);box-shadow:0 3px 12px rgba(30,142,62,.16)}
.c-green .cbody{grid-template-columns:180px 1fr}.c-green h3{font-size:23px}.c-green .st{background:#d3ecda}.c-green .sv{color:#14672c}
.seal{margin-left:auto;background:#1E8E3E;color:#fff;font-weight:900;border-radius:10px;padding:6px 14px;font-size:14px;text-align:center;line-height:1.15;box-shadow:0 0 0 3px #bfe5c9}
.seal small{display:block;font-weight:600;font-size:9.5px;opacity:.95;text-transform:uppercase;letter-spacing:.5px}
.seal.priced{box-shadow:0 0 0 3px #f3c26b}
.c-orange{border:2px solid #E37400;border-left-width:8px;background:#fffaf3}
.c-orange .cbody{grid-template-columns:150px 1fr}.c-orange h3{font-size:18px}.c-orange .st{background:#fdeed9}.c-orange .sv{font-size:13px}
.hold{margin-left:auto;font-weight:800;font-size:12px;color:#a85600;border:1.5px dashed #E37400;border-radius:8px;padding:3px 10px}
.hold.red{color:#c5221f;border-color:#c5221f}
.missing{background:#ffe9cc;border-radius:8px;padding:6px 10px;font-size:12.5px;color:#6b3a00;margin-bottom:4px}
.c-yellow{border:1px solid #d9d2ad;border-left:6px solid #B08800;background:#f7f6f0;color:#5a5a55;padding:9px 13px;font-size:11.5px;margin-top:9px}
.c-yellow .chd{margin-bottom:6px}
.ybody{display:grid;grid-template-columns:1fr 1.05fr 1.5fr;gap:12px;align-items:start}
.yt{display:grid;grid-template-columns:62px 1fr;gap:9px;align-items:start}
.c-yellow h3{font-size:14px;color:#4a4a45}.c-yellow .variant{font-size:11px}.c-yellow .why{font-size:11px;margin:3px 0 0;font-weight:500}
.c-yellow .photo img{filter:grayscale(.75) opacity(.8);border-radius:8px}
.c-yellow .stats{grid-template-columns:repeat(3,1fr);gap:4px;margin:7px 0 0}.c-yellow .st{background:#eeece1;padding:3px}.c-yellow .sv{font-size:11.5px;font-weight:700}.c-yellow .sl{font-size:8px}
.c-yellow .pill{font-size:10.5px;padding:3px 10px}.c-yellow .hold{font-size:10.5px}
.c-yellow .copied,.c-yellow .math{margin-top:0}.c-yellow .watch{font-size:11px;padding:6px 9px;margin-top:7px}
.c-yellow .costs{gap:4px;margin-top:6px}.c-yellow .kwbox{margin-top:6px}.c-yellow .links{margin-top:7px;gap:4px;display:grid;grid-template-columns:1fr 1fr}.c-yellow .links .lnk{text-align:center}.c-yellow .verdict{font-size:10.5px}
.copied{background:#fdecea;border:1.5px solid #c5221f;border-radius:10px;padding:8px 10px;margin-top:8px;color:#7a1512}
.chead{font-weight:800;color:#c5221f;font-size:12.5px}.copied ul{margin:5px 0 0;padding:0;list-style:none}
.copied li{font-size:11.5px;padding:1px 0;display:inline-block;margin-right:12px}.copied .cv{color:#7a1512;margin-left:5px;font-weight:700}.copied a{color:#7a1512;text-decoration:underline}
.math{background:#f1f8f3;border:1px solid #cfe8d6;border-radius:12px;padding:8px 11px;margin-top:8px}
.mtiles{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}.mt{background:#fff;border-radius:8px;padding:5px 6px;text-align:center;border:1px solid #d9eedf}
.mv{font-size:20px;font-weight:900;color:#14672c;line-height:1.1}.ml{font-size:10px;color:#55606d;margin-top:2px}
.mline{font-size:13px;margin-top:6px}.math.compact .mline{margin-top:0}.mline.bad{color:#a11512;margin-top:0}
.c-orange .math{background:#fff;border-color:#f1d5ae}.c-yellow .math{background:#fff;border-color:#e3dfcc;padding:7px 9px}.c-yellow .mline{font-size:11.5px}
.watch{background:#fff3cd;border-left:5px solid #c5221f;border-radius:8px;padding:6px 11px;margin-top:8px;font-size:12.5px;color:#5c3b00}
.costs{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:10px}
.cost{background:#f6f8fa;border-radius:8px;padding:7px 10px}.cost .val{font-weight:800;font-size:16px}.cost.neg .val{color:#c5221f}
.c-yellow .cost{padding:4px 6px;background:#eeece1}.c-yellow .cost .val{font-size:12px}.c-yellow .cost .lbl,.c-yellow .lbl{font-size:8.5px;letter-spacing:.3px}
.tag{display:inline-block;border-radius:4px;color:#fff;font-size:9px;padding:1px 5px;letter-spacing:.4px;vertical-align:1px}
.t-exact{background:#1E8E3E}.t-close{background:#3b78c4}.t-similar{background:#E37400}.t--{background:#8a949c}
.kwbox{margin-top:8px}.kws{display:flex;flex-wrap:wrap;gap:6px}
.kw{display:inline-flex;border:1px solid #cfd6de;border-radius:999px;overflow:hidden;font-size:11.5px;background:#fff;color:#1c2430}
.kq{padding:3px 8px}.kn{padding:3px 8px;background:#eef1f4;font-weight:800}
.c-yellow .kw{font-size:10px}.c-yellow .kq,.c-yellow .kn{padding:2px 6px}
.verdict{font-weight:800;font-size:12px}.kwhead{display:flex;flex-wrap:wrap;gap:4px 12px;align-items:baseline;margin-bottom:5px}.kwhead .lbl{margin:0}.ref{text-transform:none;letter-spacing:0;font-weight:500}.v-ok{color:#14672c}.v-no{color:#c5221f}.v-warn{color:#b35c00}
.links{display:flex;flex-wrap:wrap;gap:7px;margin-top:11px}
.lnk{border:1.5px solid #c3ccd6;border-radius:8px;padding:4px 11px;font-weight:700;font-size:12px;background:#fff}
.lnk.off{color:#9aa3ad}.lnk.plain{border:0;padding:0;background:none;font-size:inherit;font-weight:inherit;text-decoration:underline}
.c-yellow .lnk{font-size:9.5px;padding:3px 6px}.c-yellow .lnk.plain{padding:0;font-size:inherit}
.foot{font-size:12px;color:#3c4a57;padding:12px 18px}.foot ul{margin:6px 0 0;padding-left:18px}.foot li{margin:3px 0}
.avoid,.card,.hero,.panel,.yrow,.pod,tr{break-inside:avoid;page-break-inside:avoid}
.tierhead,.sech{break-after:avoid;page-break-after:avoid}
@page{size:Letter;margin:.42in .4in}
@media print{
  body{background:#fff}.wrap{max-width:none;padding:0;zoom:.8}
  .c-green{box-shadow:none}.ribbon{box-shadow:none}
  .newpage{break-before:page;page-break-before:always;margin-top:0}
  a{text-decoration:none}
}
@media screen and (max-width:760px){
  .igrid,.legend,.pods,.why3{grid-template-columns:1fr}.hgrid,.c-green .cbody,.c-orange .cbody,.ybody{grid-template-columns:1fr}.cmain .proof{columns:1}
  .hphoto img{width:100%;height:auto}.stats,.hmath,.mtiles,.costs{grid-template-columns:repeat(2,1fr)}.yrow{flex-direction:column}.score{overflow-x:auto}
}
"""


def build_html(data, base_dir, notes):
    intake = data.get("intake") or {}
    try:
        budget = float(intake.get("cbo_daily_budget_usd") or DEFAULT_BUDGET)
    except (TypeError, ValueError):
        budget = DEFAULT_BUDGET
    products = sorted(data.get("products") or [], key=lambda p: (parse_num(p.get("rank")) or 999))
    rows = []
    for p in products:
        m = launch_math(p, budget)
        rows.append((p, m, gates(p, m), image_data_uri(p, base_dir, notes)))
    by = {c: [r for r in rows if (r[0].get("color") or "").upper() == c] for c in ("GREEN", "ORANGE", "YELLOW")}
    other = [r for r in rows if (r[0].get("color") or "").upper() not in by]
    by["YELLOW"] += other
    b = money(budget, False)
    setup = intake.get("cbo_setup") or "CBO"

    top = (f'<header class="top"><div><h1>{esc(data.get("title") or "Product Research")}</h1>'
           f'<span class="bud">{b}/day · {esc(setup)}</span></div>'
           f'<div class="meta">{esc(data.get("date"))}<br>{esc(data.get("source"))}<br>{len(rows)} products ranked</div></header>')
    intake_html = (
        '<section class="panel"><div class="sech">Intake</div><div class="igrid">'
        f'<div class="ibox b"><div class="lbl">Budget</div><div class="v">{b}/day</div><div class="fine">{esc(setup)}</div></div>'
        f'<div class="ibox"><div class="lbl">Demographic</div><div class="v">{esc(intake.get("demographic") or "—")}</div></div>'
        f'<div class="ibox"><div class="lbl">Price band</div><div class="v">{esc(intake.get("price_band") or "—")}</div></div>'
        f'<div class="ibox"><div class="lbl">Categories</div><div class="v">{esc(intake.get("categories") or "—")}</div></div></div>'
        f'<div class="brief"><div class="lbl">What we set out to find</div><p>{esc(intake.get("brief") or "—")}</p></div></section>')
    ng, no, ny = len(by["GREEN"]), len(by["ORANGE"]), len(by["YELLOW"])
    copied_total = sum(len(r[0].get("competitors") or []) for r in by["YELLOW"])
    legend = (
        '<section class="panel avoid"><div class="sech">How to read this</div><div class="legend">'
        '<div class="leg g"><span class="pill big p-green">GREEN</span><p><b>Launch first.</b> Demand, a clear Meta field and a proven winning video — every gate passed.</p></div>'
        '<div class="leg o"><span class="pill big p-orange">ORANGE</span><p><b>Hold.</b> Nobody is copying it on Meta, but the winning video is not proven yet.</p></div>'
        '<div class="leg y"><span class="pill big p-yellow">YELLOW</span><p><b>Skip for now.</b> It sells on TikTok, but competitors already run its videos on Meta.</p></div></div>'
        '<div class="why3">'
        f'<div class="w3 g"><b>{ng} Green</b>Proof is complete. At {b}/day, three days of testing is {money(budget * 3, False)} — spend it where every gate is already passed.</div>'
        f'<div class="w3 o"><b>{no} Orange</b>One gate short. The same {money(budget * 3, False)}, but on an unproven video.</div>'
        f'<div class="w3 y"><b>{ny} Yellow</b>{copied_total} competitor ads already use these videos. You would pay to enter a copied market.</div>'
        '</div></section>')

    greens = by["GREEN"]
    hero_html = hero(*greens[0]) if greens else ""
    podium_html = podium(greens[1:4])
    green_cards = "".join(card(*r) for r in greens[1:])
    orange_cards = "".join(card(*r) for r in by["ORANGE"])
    ys = by["YELLOW"]
    yellow_rows = "".join(card(*r) for r in ys)

    def tierhead(c, label, text, cls=""):
        return f'<div class="tierhead {cls}"><span class="pill big p-{c}">{label}</span><p>{text}</p></div>'

    sections = hero_html + podium_html + scoreboard(rows, budget)
    if green_cards:
        sections += tierhead("green", "GREEN", "<b>Launch-ready.</b> Full proof on each one — compare the launch math to choose the order.") + green_cards
    if orange_cards:
        sections += tierhead("orange", "ORANGE", "<b>Hold.</b> Clear on Meta, but one proof is still missing. Re-check when the video numbers move.") + orange_cards
    if yellow_rows:
        sections += tierhead("yellow", "YELLOW", "<b>Skip for now.</b> Competitors are already running these Kalo videos on Meta.") + yellow_rows

    foot = (
        '<section class="panel foot avoid"><div class="sech">Grading rules</div><ul>'
        '<li><b>Yellow → Orange:</b> all 5 Meta keywords show no competitor using its Kalo top-10 videos.</li>'
        '<li><b>Orange → Green:</b> winning video proven — 500+ orders, 0.6+ sales per 1K views, 300K+ views, plus a 100K+ appeal video.</li>'
        f'<li>{esc(data.get("est_rule") or "Est. delivered = item cost + standard shipping and fees.")}</li>'
        '<li>Sales per 1K views is a TikTok conversion signal, not ROAS.</li>'
        f'<li><b>Launch math:</b> margin = TikTok price − est. delivered · break-even ROAS = price ÷ margin · sales/day = {b} ÷ margin (rounded up) · '
        '2.0-ROAS price = 2 × est. delivered · Kalo orders/month ≈ 30-day revenue ÷ price. Uses TikTok price as reference; your store price/bundles change this.</li>'
        '<li>Costs are estimates until a supplier quote replaces them. Ad fees, refunds and payment fees are not included.</li>'
        '</ul></section>')

    return ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            f'<title>{esc(data.get("title") or "Product Research")}</title><style>{CSS}</style></head>'
            f'<body><div class="wrap">{top}{intake_html}{legend}{sections}{foot}</div></body></html>')


# --------------------------------------------------------------------- pdf
def find_browser():
    custom = os.environ.get("PLA_CHROME")  # any Chrome/Edge/Chromium binary outside the usual places
    if custom and os.path.isfile(custom):
        return custom
    names = ["google-chrome", "google-chrome-stable", "chromium", "chromium-browser", "msedge", "microsoft-edge"]
    for n in names:
        p = shutil.which(n)
        if p:
            return p
    home = os.path.expanduser("~")
    paths = [
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        os.path.join(home, "Applications", "Google Chrome.app", "Contents", "MacOS", "Google Chrome"),
        os.path.join(home, "Desktop", "Google Chrome.app", "Contents", "MacOS", "Google Chrome"),
    ]
    for env in ("PROGRAMFILES", "PROGRAMFILES(X86)", "LOCALAPPDATA"):
        root = os.environ.get(env)
        if root:
            paths += [os.path.join(root, "Google", "Chrome", "Application", "chrome.exe"),
                      os.path.join(root, "Microsoft", "Edge", "Application", "msedge.exe")]
    for p in paths:
        if os.path.isfile(p):
            return p
    return None


def print_pdf(html_path, pdf_path):
    """Returns the name of the engine used, or None."""
    url = html_path.resolve().as_uri()
    browser = find_browser()
    if browser:
        if pdf_path.exists():
            pdf_path.unlink()
        # The throwaway browser profile sits next to the output, not in the system temp folder:
        # sandboxed agents (Claude Code, Codex) often may not write there, and the print then fails silently.
        prof = tempfile.mkdtemp(prefix=".chrome-profile-", dir=str(pdf_path.resolve().parent))
        try:
            cmd = [browser, "--headless=new", "--no-sandbox", "--disable-gpu", "--no-pdf-header-footer",
                   f"--user-data-dir={prof}", f"--print-to-pdf={pdf_path.resolve()}", url]
            try:
                subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=180)
            except Exception as e:
                print(f"  browser print failed: {e}")
        finally:
            shutil.rmtree(prof, ignore_errors=True)
        if pdf_path.exists() and pdf_path.stat().st_size > 1000:
            return os.path.basename(browser)
        print(f"  {browser} was found but printed no PDF.")
    try:
        from playwright.sync_api import sync_playwright  # type: ignore
        with sync_playwright() as pw:
            br = pw.chromium.launch()
            pg = br.new_page()
            pg.goto(url)
            pg.pdf(path=str(pdf_path), format="Letter", print_background=True, prefer_css_page_size=True)
            br.close()
        if pdf_path.exists():
            return "playwright"
    except Exception:
        pass
    return None


def pdf_pages(pdf_path):
    try:
        return len(re.findall(rb"/Type\s*/Page(?![s\w])", pdf_path.read_bytes())) or None
    except OSError:
        return None


def main(argv=None):
    ap = argparse.ArgumentParser(description="Build the product-research HTML + PDF report.")
    ap.add_argument("json", help="path to report.json")
    ap.add_argument("--out", help="output path without extension (default: reports/<json folder name>)")
    ap.add_argument("--no-pdf", action="store_true", help="write the HTML only")
    a = ap.parse_args(argv)

    src = Path(a.json)
    data = json.loads(src.read_text(encoding="utf-8"))
    out = Path(a.out) if a.out else Path("reports") / src.resolve().parent.name
    if out.suffix.lower() in (".html", ".pdf"):
        out = out.with_suffix("")
    out.parent.mkdir(parents=True, exist_ok=True)
    html_path, pdf_path = Path(str(out) + ".html"), Path(str(out) + ".pdf")

    notes = []
    html_path.write_text(build_html(data, src.resolve().parent, notes), encoding="utf-8")
    print(f"HTML: {html_path}  ({html_path.stat().st_size / 1024:.0f} KB, {len(data.get('products') or [])} products)")
    for n in notes:
        print(f"  image note: {n}")
    if a.no_pdf:
        return 0
    engine = print_pdf(html_path, pdf_path)
    if engine:
        pages = pdf_pages(pdf_path)
        print(f"PDF:  {pdf_path}  ({pdf_path.stat().st_size / 1024:.0f} KB" + (f", {pages} pages" if pages else "") + f", via {engine})")
    else:
        print("PDF:  NOT written. No working Chrome, Chromium, Edge or Playwright. If Chrome is installed somewhere "
              "unusual, set PLA_CHROME to its binary and run again; or open the HTML in any browser and use "
              "Print → Save as PDF (Letter, background graphics on).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
