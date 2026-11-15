#!/usr/bin/env python3
"""Leave-one-out scaled close analysis for presim-log.csv.

For closed rows (pred_impr > 0 and actual_impr > 0) compute, per row, a
leave-one-out scale ratio: the median of actual/pred over the OTHER closed
rows sharing the same presim_calib.fmt(text_preview) format, used only when
there are at least 3 such others (otherwise ratio = 1). Reports the median
absolute log error raw vs scaled, per format and overall.
"""

import csv
import math
import statistics
import sys
from collections import defaultdict
from pathlib import Path

try:
    from presim_calib import fmt
except Exception:  # presim_calib not present: local fallback
    _FMT_KEYWORDS = (
        ("connect", "connect"),
        ("inmail", "inmail"),
        ("message", "dm"),
        ("dm ", "dm"),
        ("comment", "comment"),
        ("follow", "follow"),
        ("like", "like"),
        ("view", "view"),
    )

    def fmt(text_preview):
        t = (text_preview or "").strip().lower()
        for needle, name in _FMT_KEYWORDS:
            if needle in t:
                return name
        return "other"


DEFAULT_CSV = Path(__file__).resolve().parent.parent / "presim-log.csv"


def _norm(name):
    return name.strip().lower().replace("-", "_").replace(" ", "_")


def load_rows(path):
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        rows = []
        for rec in reader:
            norm = {_norm(k): v for k, v in rec.items() if k is not None}
            try:
                pred = float(norm["pred_impr"])
                actual = float(norm["actual_impr"])
            except (KeyError, TypeError, ValueError):
                continue
            if pred <= 0 or actual <= 0:
                continue
            rows.append(
                {
                    "fmt": fmt(norm.get("text_preview") or ""),
                    "pred": pred,
                    "actual": actual,
                }
            )
        return rows


def compute(rows):
    """Return {fmt: {"n": int, "raw": float, "scaled": float}} plus "ALL"."""
    by_fmt = defaultdict(list)
    for r in rows:
        by_fmt[r["fmt"]].append(r)

    stats = {}
    all_raw = []
    all_scaled = []
    for name in sorted(by_fmt):
        group = by_fmt[name]
        raw_errs = []
        scaled_errs = []
        for r in group:
            raw = abs(math.log(r["actual"] / r["pred"]))
            others = [o for o in group if o is not r]
            if len(others) >= 3:
                ratio = statistics.median(o["actual"] / o["pred"] for o in others)
            else:
                ratio = 1.0
            scaled = abs(math.log(r["actual"] / (r["pred"] * ratio)))
            raw_errs.append(raw)
            scaled_errs.append(scaled)
        stats[name] = {
            "n": len(group),
            "raw": statistics.median(raw_errs),
            "scaled": statistics.median(scaled_errs),
        }
        all_raw.extend(raw_errs)
        all_scaled.extend(scaled_errs)

    stats["ALL"] = {
        "n": len(rows),
        "raw": statistics.median(all_raw) if all_raw else 0.0,
        "scaled": statistics.median(all_scaled) if all_scaled else 0.0,
    }
    return stats


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    path = Path(argv[0]) if argv else DEFAULT_CSV
    stats = compute(load_rows(path))
    for name in sorted(k for k in stats if k != "ALL"):
        s = stats[name]
        print(f"{name} n={s['n']} raw={s['raw']:.2f} scaled={s['scaled']:.2f}")
    s = stats["ALL"]
    print(f"ALL n={s['n']} raw={s['raw']:.2f} scaled={s['scaled']:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
