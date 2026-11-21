#!/usr/bin/env python3
"""Leave-one-POST-out median prescore for connect posts. CSV columns: post_id,impr.

Rows with the same post_id are collapsed to one value (their median) before LOO,
so a post never predicts itself (issue #503). Log error uses ln(v) - ln(pred) for
numerical stability on extreme finite values.
"""
import csv, json, math, statistics, sys


def load(path):
    rows, skipped = [], 0
    with open(path, newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            try:
                v = float((r.get("impr") or "").strip())
            except (ValueError, AttributeError):
                skipped += 1
                continue
            if math.isfinite(v) and v > 0:
                rows.append((str(r.get("post_id") or ""), v))
            else:
                skipped += 1
    return rows, skipped


def group(rows):
    by = {}
    for pid, v in rows:
        by.setdefault(pid, []).append(v)
    return [(pid, statistics.median(vs)) for pid, vs in by.items()], sum(len(vs) - 1 for vs in by.values())


def score(rows, skipped=0):
    posts, dup = group(rows)
    n = len(posts)
    out = {"n": n, "prescore": statistics.median([v for _, v in posts]) if n else None, "loo": [],
           "median_loo_err": None, "skipped_rows": skipped, "duplicate_rows_collapsed": dup}
    if n < 2:
        return out
    for i, (pid, v) in enumerate(posts):
        pred = statistics.median([w for j, (_, w) in enumerate(posts) if j != i])
        out["loo"].append({"post_id": pid, "pred": pred, "abs_ln_err": abs(math.log(v) - math.log(pred))})
    out["median_loo_err"] = statistics.median([x["abs_ln_err"] for x in out["loo"]])
    return out


def main(argv):
    if len(argv) != 2:
        print("usage: connect_loo_prescore.py <csv>", file=sys.stderr)
        return 2
    rows, skipped = load(argv[1])
    print(json.dumps(score(rows, skipped)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
