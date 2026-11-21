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


def _loo_bias(rows):
    residuals = []
    for row in rows:
        pred = _as_positive_float(row.get("pred_impr"))
        actual = _as_positive_float(row.get("actual_impr"))
        if pred is None or actual is None:
            continue
        residuals.append(math.log(actual) - math.log(pred))

    n = len(residuals)
    result = {
        "n": n,
        "multiplier": None,
        "median_abs_ln_err_raw": None,
        "median_abs_ln_err_loo": None,
    }
    if n < 2:
        return result

    center = statistics.median(residuals)
    result["multiplier"] = float(math.exp(center))
    result["median_abs_ln_err_raw"] = float(statistics.median(abs(r) for r in residuals))
    loo_errors = []
    for i, r in enumerate(residuals):
        others = residuals[:i] + residuals[i + 1:]
        loo_errors.append(abs(r - statistics.median(others)))
    result["median_abs_ln_err_loo"] = float(statistics.median(loo_errors))
    return result


def report(rows, bias=False):
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

    out = {
        "overall": {
            "n": len(overall_errors),
            "median_abs_ln_err": _median_abs_ln_err(overall_errors),
        },
        "by_format": {
            fmt: {"n": len(errors), "median_abs_ln_err": _median_abs_ln_err(errors)}
            for fmt, errors in by_format_errors.items()
        },
    }
    if bias:
        out["loo_bias"] = _loo_bias(rows)
    return out


def main(argv):
    if len(argv) not in (2, 3) or (len(argv) == 3 and argv[2] != "--bias"):
        print(f"usage: {argv[0]} <csv> [--bias]", file=sys.stderr)
        return 2
    bias = len(argv) == 3
    with open(argv[1], newline="") as fh:
        rows = list(csv.DictReader(fh))
    print(json.dumps(report(rows, bias=bias)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
