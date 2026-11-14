#!/usr/bin/env python3
"""Offline backtest of x_presim heuristic on @diceai0 originals (>=24h old at fetch).
Compares against the naive 'predict the account median' forecast (MASE-style skill check)
and a shrunk variant (geometric blend of simulator and median). No LLM, no network.
usage: x_presim_backtest.py <originals.json> <fetched_at_iso> [out.json]"""
import json, math, sys, statistics, datetime, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import x_presim as xp

def le(p, a): return abs(math.log((a + 1) / (p + 1)))

def spearman(x, y):
    def rk(v):
        o = sorted(range(len(v)), key=lambda i: v[i]); r = [0] * len(v)
        for k, i in enumerate(o): r[i] = k
        return r
    rx, ry = rk(x), rk(y); n = len(x)
    return 1 - 6 * sum((a - b) ** 2 for a, b in zip(rx, ry)) / (n * (n * n - 1))

def main(path, fetched, out=None):
    t0 = datetime.datetime.fromisoformat(fetched.replace('Z', '+00:00'))
    posts = [p for p in json.load(open(path, encoding='utf-8'))
             if (t0 - datetime.datetime.fromisoformat(p['created_at'].replace('Z', '+00:00'))).total_seconds() >= 86400
             and not p['text'].startswith('@')]
    base = xp.baseline('diceai0'); rows = []
    for p in posts:
        f = xp.feats(p['text'])
        pred = xp.aggregate(xp.heuristic_panel(p['text']), base, f['lang'])['pred_impr']
        act = p['public_metrics']['impression_count']
        rows.append(dict(id=p['id'], act=act, sim=pred, shrink=math.sqrt(pred * base), naive=base, lang=f['lang']))
    res = dict(n=len(rows), baseline_median_impr=base, fetched_at=fetched)
    for k in ('sim', 'shrink', 'naive'):
        res[k] = dict(median_abs_log_err=round(statistics.median(le(r[k], r['act']) for r in rows), 3),
                      spearman=None if k == 'naive' else round(spearman([r[k] for r in rows], [r['act'] for r in rows]), 3))
    res['skill_vs_naive'] = round(1 - res['sim']['median_abs_log_err'] / res['naive']['median_abs_log_err'], 3)
    res['rows'] = rows
    if out: json.dump(res, open(out, 'w'), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in res.items() if k != 'rows'}, ensure_ascii=False))

if __name__ == '__main__':
    main(*sys.argv[1:])
