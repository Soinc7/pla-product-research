#!/usr/bin/env python3
"""Turn a filled preflight result into GO / GO_LIMITED / STOP.

Usage: python3 preflight/evaluate.py path/to/result.json
Exit code: 0 = GO or GO_LIMITED, 2 = STOP, 3 = PENDING (checks not run yet), 1 = bad input.
Standard library only. Reads files; changes nothing.
"""
import json
import os
import sys

STATES = ("PROVEN", "PARTIAL", "MISSING", "PENDING")


def main(argv):
    if len(argv) != 2:
        print("Usage: python3 preflight/evaluate.py path/to/result.json")
        return 1
    here = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(here, "checklist.json"), encoding="utf-8") as f:
            checklist = json.load(f)
        with open(argv[1], encoding="utf-8") as f:
            result = json.load(f)
    except (OSError, ValueError) as err:
        print("Cannot read input: %s" % err)
        return 1

    filled = result.get("checks", {})
    by_id = {c["id"]: c for c in checklist["checks"]}
    stop = False
    limited = False
    pending = False

    for check_id in checklist["run_order"]:
        check = by_id[check_id]
        state = str(filled.get(check_id, {}).get("state", "")).upper()
        if state not in STATES:
            state = "MISSING"
            shown = "MISSING (no valid state recorded)"
        else:
            shown = state
        print("%-28s %s" % (check["label"][:28], shown))
        if state == "PROVEN":
            continue
        if state == "PENDING":
            pending = True
            print("    Not run yet. Run this check before research (it is not a failure).")
            continue
        if state == "MISSING":
            if check["required"] and check.get("missing_blocks", True):
                stop = True
                print("    STOP. Fix: %s" % check["fix"])
            else:
                limited = True
                print("    %s" % check["on_missing"])
                print("    Fix: %s" % check["fix"])
        elif check.get("partial_blocks"):
            stop = True
            print("    STOP. %s" % check["on_partial"])
            print("    Fix: %s" % check["fix"])
        else:
            limited = True
            print("    Limit: %s" % check["on_partial"])

    if stop:
        verdict = "STOP"
    elif pending:
        verdict = "PENDING"
    elif limited:
        verdict = "GO_LIMITED"
    else:
        verdict = "GO"
    message = checklist["verdicts"].get(verdict, "Run the PENDING checks, then evaluate again.")
    print("\nVERDICT: %s - %s" % (verdict, message))
    return 2 if stop else 3 if pending else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
