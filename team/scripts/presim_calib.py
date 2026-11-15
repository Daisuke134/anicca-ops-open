#!/usr/bin/env python3
"""presim_calib [CSV]: leave-one-out format calibration of x_presim impression predictions.

Reads team/metrics/presim-log.csv (read-only). Rows need pred_impr and actual_impr > 0.
Format from text_preview: connect (つながりたい / 繋がりたい / 'connect with'), question (ends ?/？), else other.
For each row, factor = geometric mean of actual/pred over the OTHER rows of the same format
(and backend when --by-backend); calibrated = pred * factor (factor 1 when no other rows).
Prints `format n median_abs_ln_err_raw median_abs_ln_err_calibrated`, plus `all`.
"""
import argparse
import csv
import math
import statistics
import sys

DEFAULT = "team/metrics/presim-log.csv"


def fmt(text):
    t = (text or "").strip()
    tl = t.lower()
    # EN connect markers added 2026-11-15 21:4x (2121608771445064174 "I want to meet more people shipping" was mis-bucketed as other)
    if "つながりたい" in t or "繋がりたい" in t or any(k in tl for k in ("connect with", "want to meet", "meet more people")):
        return "connect"
    if t.endswith("?") or t.endswith("？"):
        return "question"
    return "other"


def fmt_row(row):
    f = row.get("format")
    if f in ("connect", "question", "other"):
        return f
    return fmt(row.get("text_preview", ""))


def load(path, by_backend=False):
    rows = []
    with open(path, encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                p, a = float(r.get("pred_impr") or 0), float(r.get("actual_impr") or 0)
            except ValueError:
                continue
            if p > 0 and a > 0:
                key = fmt_row(r)
                if by_backend:
                    key = f"{key}/{r.get('backend') or '?'}"
                rows.append((key, p, a))
    return rows


def evaluate(rows):
    res = {}
    groups = {}
    for i, (k, _, _) in enumerate(rows):
        groups.setdefault(k, []).append(i)
    raw_all, cal_all = [], []
    for k, idx in sorted(groups.items()):
        raw, cal = [], []
        for i in idx:
            _, p, a = rows[i]
            others = [math.log(rows[j][2] / rows[j][1]) for j in idx if j != i]
            factor = math.exp(sum(others) / len(others)) if others else 1.0
            raw.append(abs(math.log(a / p)))
            cal.append(abs(math.log(a / (p * factor))))
        res[k] = (len(idx), statistics.median(raw), statistics.median(cal))
        raw_all += raw
        cal_all += cal
    if rows:
        res["all"] = (len(rows), statistics.median(raw_all), statistics.median(cal_all))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", nargs="?", default=DEFAULT)
    ap.add_argument("--by-backend", action="store_true")
    a = ap.parse_args(argv)
    res = evaluate(load(a.csv, a.by_backend))
    print("format n median_abs_ln_err_raw median_abs_ln_err_calibrated")
    for k, (n, r, c) in res.items():
        print(f"{k} {n} {r:.3f} {c:.3f}")
    return 0 if res else 1


if __name__ == "__main__":
    sys.exit(main())
