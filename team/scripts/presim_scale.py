"""Scale predicted impressions by per-format calibration ratios.

Reads the presim-log CSV, groups rows by message format, computes the median
actual/predicted ratio per format, and either reports those ratios (CLI) or
applies them to new predictions via scaled_pred().
"""

import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from statistics import median

try:
    from presim_calib import fmt
except ImportError:  # presim_calib.py may not be present in all checkouts
    def fmt(text_preview):
        t = (text_preview or "").lower()
        if "connect" in t:
            return "connect"
        return "other"

DEFAULT_CSV = Path(__file__).resolve().parents[1] / "metrics" / "presim-log.csv"


def _num(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def ratios(csv_path):
    """Return {format: (median(actual/pred), n)} for valid rows in csv_path."""
    grouped = {}
    with open(csv_path, newline="") as fh:
        for row in csv.DictReader(fh):
            pred = _num(row.get("pred_impr"))
            actual = _num(row.get("actual_impr"))
            if pred is None or actual is None or pred <= 0 or actual <= 0:
                continue
            grouped.setdefault(fmt(row.get("text_preview", "")), []).append(
                actual / pred
            )
    return {
        name: (median(vals), len(vals)) for name, vals in grouped.items()
    }


def scaled_pred(fmt_name, pred, ratios_map, min_n=3):
    """Scale pred by the format's median ratio when n >= min_n, else unchanged."""
    entry = ratios_map.get(fmt_name)
    if entry is not None and entry[1] >= min_n:
        return pred * entry[0]
    return pred


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    csv_path = Path(args[0]) if args else DEFAULT_CSV
    r = ratios(csv_path)
    for name in sorted(r):
        ratio, n = r[name]
        print(f"{name} ratio={ratio:.2f} n={n}")


if __name__ == "__main__":
    main()
