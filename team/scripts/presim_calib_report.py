"""Pre-simulation calibration report: median abs log error by format."""

import csv
import json
import math
import statistics
import sys


def _as_positive_float(value):
    if value is None:
        return None
    try:
        number = float(value)
    except (TypeError, ValueError):
        return None
    if not math.isfinite(number) or number <= 0:
        return None
    return number


def _median_abs_ln_err(errors):
    if not errors:
        return None
    return float(statistics.median(errors))


def report(rows):
    overall_errors = []
    by_format_errors = {}

    for row in rows:
        pred = _as_positive_float(row.get("pred_impr"))
        actual = _as_positive_float(row.get("actual_impr"))
        if pred is None or actual is None:
            continue
        fmt = row.get("format")
        if fmt is None or str(fmt).strip() == "":
            fmt = "other"
        else:
            fmt = str(fmt).strip()
        error = abs(math.log(pred) - math.log(actual))
        overall_errors.append(error)
        by_format_errors.setdefault(fmt, []).append(error)

    return {
        "overall": {
            "n": len(overall_errors),
            "median_abs_ln_err": _median_abs_ln_err(overall_errors),
        },
        "by_format": {
            fmt: {"n": len(errors), "median_abs_ln_err": _median_abs_ln_err(errors)}
            for fmt, errors in by_format_errors.items()
        },
    }


def main(argv):
    if len(argv) != 2:
        print(f"usage: {argv[0]} <csv>", file=sys.stderr)
        return 2
    with open(argv[1], newline="") as fh:
        rows = list(csv.DictReader(fh))
    print(json.dumps(report(rows)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
