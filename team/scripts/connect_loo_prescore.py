#!/usr/bin/env python3
"""Leave-one-POST-out median prescore for connect posts. CSV columns: post_id,impr[,segment].

Rows with the same post_id are collapsed to one value (their median) before LOO,
so a post never predicts itself (issue #503). Log error uses ln(v) - ln(pred) for
numerical stability on extreme finite values.

With --by-segment, the LOO median is computed only within the row's own segment;
segments with fewer than 2 posts fall back to all rows ("fallback": true).
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
                seg = (r.get("segment") or "").strip() or None
                rows.append((str(r.get("post_id") or ""), v, seg))
            else:
                skipped += 1
    return rows, skipped


def group(rows):
    by = {}
    for row in rows:
        pid, v = row[0], row[1]
        seg = row[2] if len(row) > 2 else None
        by.setdefault(pid, []).append((v, seg))
    posts, dup = [], 0
    for pid, vs in by.items():
        seg = next((s for _, s in vs if s is not None), None)
        posts.append((pid, statistics.median([v for v, _ in vs]), seg))
        dup += len(vs) - 1
    return posts, dup


def score(rows, skipped=0, by_segment=False):
    posts, dup = group(rows)
    n = len(posts)
    out = {"n": n, "prescore": statistics.median([v for _, v, _ in posts]) if n else None, "loo": [],
           "median_loo_err": None, "skipped_rows": skipped, "duplicate_rows_collapsed": dup}
    if n < 2:
        return out
    by_seg = {}
    for i, (_, _, seg) in enumerate(posts):
        by_seg.setdefault(seg, []).append(i)
    use_seg = by_segment and any(seg is not None for _, _, seg in posts)
    errs = {}
    for i, (pid, v, seg) in enumerate(posts):
        same = by_seg.get(seg, []) if use_seg else []
        pool = [j for j in same if j != i] if len(same) >= 2 else [j for j in range(n) if j != i]
        fallback = use_seg and len(same) < 2
        pred = statistics.median([posts[j][1] for j in pool])
        err = abs(math.log(v) - math.log(pred))
        entry = {"post_id": pid, "pred": pred, "abs_ln_err": err}
        if use_seg:
            entry["fallback"] = fallback
        out["loo"].append(entry)
        errs.setdefault(seg, []).append(err)
    out["median_loo_err"] = statistics.median([x["abs_ln_err"] for x in out["loo"]])
    if use_seg:
        out["segments"] = {str(seg): {"n": len(es), "median_loo_err": statistics.median(es)}
                           for seg, es in errs.items()}
    return out


def main(argv):
    args = [a for a in argv[1:] if a != "--by-segment"]
    by_segment = "--by-segment" in argv[1:]
    if len(args) != 1:
        print("usage: connect_loo_prescore.py <csv> [--by-segment]", file=sys.stderr)
        return 2
    rows, skipped = load(args[0])
    print(json.dumps(score(rows, skipped, by_segment)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
