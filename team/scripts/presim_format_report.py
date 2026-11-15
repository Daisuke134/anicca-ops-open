#!/usr/bin/env python3
"""Per-format summary of the presim log CSV.

Usage: presim_format_report.py [CSV]

Groups rows by presim_calib.fmt(text_preview) and prints one line per
format plus an ``all`` line:

    <format> scored=<rows> posted=<all-digit post_id> closed=<actual_impr>0>
             median_pred=<x> median_actual=<y> ratio=<y/x 2dp>
"""

import csv
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

try:
    from presim_calib import fmt
except ImportError:  # presim_calib not present in this checkout

    def fmt(text):
        t = (text or "").lower()
        if "connect" in t:
            return "connect"
        if "?" in t:
            return "question"
        return "other"


DEFAULT_CSV = Path(__file__).resolve().parents[1] / "metrics" / "presim-log.csv"

TEXT_KEYS = ("text_preview", "text", "preview")
POST_KEYS = ("post_id", "post")
PRED_KEYS = ("predicted_impr", "pred_impr", "predicted", "prediction", "pred")
ACTUAL_KEYS = ("actual_impr", "actual_impressions", "actual")


def _first(row, names):
    for name in names:
        value = row.get(name)
        if value is not None and str(value).strip() != "":
            return str(value).strip()
    return ""


def _num(value):
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def _records(path):
    with open(path, newline="", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle):
            post_id = _first(row, POST_KEYS)
            yield {
                "format": fmt(_first(row, TEXT_KEYS)),
                "posted": post_id.isdigit(),
                "pred": _num(_first(row, PRED_KEYS)),
                "actual": _num(_first(row, ACTUAL_KEYS)),
            }


def _fmt_num(value):
    number = float(value)
    return str(int(number)) if number.is_integer() else str(number)


def _stats(records):
    scored = len(records)
    posted = sum(1 for r in records if r["posted"])
    closed = [
        (r["pred"], r["actual"])
        for r in records
        if r["actual"] is not None and r["actual"] > 0
    ]
    preds = [p for p, _ in closed if p is not None]
    actuals = [a for _, a in closed]
    if preds and actuals:
        median_pred = statistics.median(preds)
        median_actual = statistics.median(actuals)
        median_pred_s = _fmt_num(median_pred)
        median_actual_s = _fmt_num(median_actual)
        ratio = f"{median_actual / median_pred:.2f}"
    else:
        median_pred_s = median_actual_s = ratio = "-"
    return scored, posted, len(closed), median_pred_s, median_actual_s, ratio


def _line(name, stats):
    scored, posted, closed, median_pred, median_actual, ratio = stats
    return (
        f"{name} scored={scored} posted={posted} closed={closed} "
        f"median_pred={median_pred} median_actual={median_actual} ratio={ratio}"
    )


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = Path(argv[0]) if argv else DEFAULT_CSV
    records = list(_records(path))
    groups = {}
    for record in records:
        groups.setdefault(record["format"], []).append(record)
    for name in sorted(groups):
        print(_line(name, _stats(groups[name])))
    print(_line("all", _stats(records)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
