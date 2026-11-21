#!/usr/bin/env python3
"""Find the sub-agents and skills this machine already has, and pick one worker per lane.

Usage: python3 tools/check_agents.py [--out state/agents.json] [--dir <extra folder> ...]

Looks in (Claude Code locations; add others with --dir):
  <repo>/.claude/agents/*.md            this repo's bundled workers (pla-*)
  ~/.claude/agents/*.md                 the owner's own sub-agents
  <repo>/.claude/skills/*/SKILL.md, ~/.claude/skills/*/SKILL.md
  ~/.claude/plugins/**/agents/*.md and ~/.claude/plugins/**/skills/*/SKILL.md   (installed plugins)
Each agent or skill is matched to the lanes by the words in its name and description.

Per lane it picks, in this order:
  1. "owner"    the owner's own agent that covers the lane (ask the owner once before using it)
  2. "bundled"  the repo's pla-* worker (.claude/agents/), when Claude Code loaded it
  3. "builtin"  Claude Code's general-purpose agent, briefed with the bundled worker file as its prompt
A product-research *skill* the owner already has is reported separately (see FOR-YOUR-AGENT.md,
"If your owner already has a product researcher"): never replace it; offer side by side or second opinion.
Whether the agent can start sub-agents at all is for the host to say; if it cannot, every lane runs in
the host ("single" mode). Writes state/agents.json and prints a short summary. Reads only; changes nothing else.
Standard library only.
"""
import argparse
import glob
import json
import os
import re
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HOME = os.path.expanduser("~")

LANES = {
    "L1": ("Kalo discovery and video IDs", "pla-kalo-worker",
           [r"kalo", r"kalodata", r"tiktok shop", r"product (discovery|hunt|finder)", r"winning product"]),
    "L2": ("Meta Ad Library competitor check", "pla-meta-worker",
           [r"meta ad ?library", r"facebook ad ?library", r"ads? library", r"competitor ads?", r"ad spy"]),
    "L3": ("1688 / Fabulk pricing", "pla-pricing-worker",
           [r"1688", r"fabulk", r"factory price", r"(supplier|sourcing) (price|cost)", r"\bcogs\b"]),
    "L4": ("TrendTrack appeal + Competitor Files data", "pla-trendtrack-worker",
           [r"trendtrack", r"tiktok (library|videos?)", r"competitor stores?", r"winning (ads|videos)"]),
    "L5": ("Google Sheets writes", "pla-sheets-worker",
           [r"google ?sheets?", r"\bsheets? (writer|builder)"]),
}
RESEARCHER = [r"product research", r"product[- ]research", r"research (a )?batch", r"find(ing)? products"]


def frontmatter(path):
    try:
        text = open(path, encoding="utf-8", errors="replace").read(20000)
    except OSError:
        return {}
    m = re.match(r"^---\s*\n(.*?)\n---", text, re.S)
    if not m:
        return {}
    out, key = {}, None
    for line in m.group(1).splitlines():
        km = re.match(r"^([A-Za-z_-]+):\s*(.*)$", line)
        if km:
            key, val = km.group(1).lower(), km.group(2).strip()
            out[key] = val.strip("'\"") if val not in (">", "|", ">-", "|-") else ""
        elif key and line.startswith((" ", "\t")):
            out[key] = (out[key] + " " + line.strip()).strip()
    return out


def scan(extra):
    found = []
    def add(kind, scope, path):
        fm = frontmatter(path)
        name = fm.get("name") or (os.path.basename(os.path.dirname(path)) if kind == "skill" else os.path.basename(path)[:-3])
        desc = fm.get("description", "")
        hay = (name + " " + desc).lower()
        lanes = [lid for lid, (_, _, pats) in LANES.items() if any(re.search(p, hay) for p in pats)]
        found.append({"kind": kind, "scope": scope, "name": name, "path": path, "model": fm.get("model", ""),
                      "description": desc[:300], "lanes": lanes,
                      "researcher": kind == "skill" and not name.startswith("pla-") and any(re.search(p, hay) for p in RESEARCHER)})
    places = [
        ("agent", "bundled", os.path.join(ROOT, ".claude", "agents", "*.md")),
        ("agent", "owner", os.path.join(HOME, ".claude", "agents", "*.md")),
        ("skill", "project", os.path.join(ROOT, ".claude", "skills", "*", "SKILL.md")),
        ("skill", "owner", os.path.join(HOME, ".claude", "skills", "*", "SKILL.md")),
        ("agent", "plugin", os.path.join(HOME, ".claude", "plugins", "**", "agents", "*.md")),
        ("skill", "plugin", os.path.join(HOME, ".claude", "plugins", "**", "skills", "*", "SKILL.md")),
    ]
    for d in extra:
        places += [("agent", "extra", os.path.join(d, "**", "agents", "*.md")), ("skill", "extra", os.path.join(d, "**", "SKILL.md"))]
    seen = set()
    for kind, scope, pattern in places:
        for path in sorted(glob.glob(pattern, recursive=True))[:500]:
            real = os.path.realpath(path)
            if real in seen:
                continue
            seen.add(real)
            add(kind, scope, path)
    return found


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "state", "agents.json"))
    ap.add_argument("--dir", action="append", default=[], help="extra folder to search for agents/ and SKILL.md")
    a = ap.parse_args()
    found = scan(a.dir)
    plan = {}
    for lid, (label, bundled, _) in LANES.items():
        own = [f for f in found if f["kind"] == "agent" and f["scope"] in ("owner", "plugin", "extra")
               and lid in f["lanes"] and not f["name"].startswith("pla-")]
        has_bundled = any(f["name"] == bundled for f in found if f["kind"] == "agent")
        if own:
            pick = {"use": own[0]["name"], "source": "owner", "path": own[0]["path"], "ask_owner_first": True,
                    "fallback": bundled if has_bundled else "general-purpose + .claude/agents/%s.md" % bundled}
        elif has_bundled:
            pick = {"use": bundled, "source": "bundled", "path": os.path.join(".claude", "agents", bundled + ".md")}
        else:
            pick = {"use": "general-purpose", "source": "builtin", "brief": os.path.join(".claude", "agents", bundled + ".md")}
        pick["lane"] = label
        if own[1:]:
            pick["other_matches"] = [f["name"] for f in own[1:5]]
        plan[lid] = pick
    researchers = [{"name": f["name"], "path": f["path"]} for f in found if f["researcher"]]
    result = {"checked_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
              "lanes": plan, "owner_researcher_skills": researchers,
              "found": [{k: f[k] for k in ("kind", "scope", "name", "lanes")} for f in found if f["lanes"] or f["researcher"]],
              "scanned": len(found),
              "note": "The host confirms it can start sub-agents (else run_mode = single) and asks the owner once before using an owner agent."}
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print("Scanned %d agents and skills. Lane plan (%s):" % (len(found), os.path.relpath(a.out, ROOT) if a.out.startswith(ROOT) else a.out))
    for lid, p in plan.items():
        extra = " (owner's own; ask first, fallback %s)" % p["fallback"] if p["source"] == "owner" else ""
        print("  %s %-44s -> %s [%s]%s" % (lid, p["lane"], p["use"], p["source"], extra))
    if researchers:
        print("Owner already has product-research skills: %s. Keep them; offer side by side or second opinion (FOR-YOUR-AGENT.md)."
              % ", ".join(r["name"] for r in researchers[:5]))


if __name__ == "__main__":
    main()
