#!/usr/bin/env python3
"""The only writer for team/metrics/applications.csv (2026-11-01).
Every row carries a stable row_id = 'a-' + sha1(date|platform|agent|evidence)[:12], computed once at append time.
row_id never changes afterwards, even if status/evidence is edited later (sync.py keys CSV rows on it).
  append:   applications_ledger.py append --platform Upwork --agent dr-eggbot --evidence "proposal sent ... job:..." [--date YYYY-MM-DD] [--count 1] [--kind apply]
  backfill: applications_ledger.py backfill     (adds row_id column / fills empty row_id; idempotent)
Off-box agents without this script: compute the same hash, or leave row_id empty and the next backfill fills it.
  check:    applications_ledger.py check        (exit 1 on empty row_id, missing job:<id> token, duplicate row_id)
Evidence must carry a job:<platform>:<id> token; 'job ~0221…' is normalised to 'job:upwork:~0221…' on append/backfill."""
import csv, hashlib, os, sys, argparse, datetime as dt, io, re
ROOT = os.environ.get('ANICCA_ROOT', '/workspace'); P = ROOT + '/team/metrics/applications.csv'
COLS = ['date', 'platform', 'agent', 'count', 'evidence', 'kind', 'row_id']
def rid(r): return 'a-' + hashlib.sha1('|'.join((r.get('date') or '', r.get('platform') or '', r.get('agent') or '', r.get('evidence') or '')).encode()).hexdigest()[:12]
def load():
    if not os.path.exists(P): return []
    return list(csv.DictReader(open(P, encoding='utf-8')))
def save(rows):
    f = io.StringIO(); w = csv.DictWriter(f, COLS, extrasaction='ignore', lineterminator='\n'); w.writeheader()
    for r in rows: w.writerow({c: r.get(c, '') or '' for c in COLS})
    tmp = P + '.tmp'; open(tmp, 'w', encoding='utf-8').write(f.getvalue()); os.replace(tmp, P)
JOBTOK = re.compile(r"job:[^\s,;\"'()\[\]<>]+")   # same token sync.py keys on
LOOSE = re.compile(r"\bjob\s+(~[0-9A-Za-z]+)")      # 'job ~0221…' (Upwork ciphertext) -> 'job:upwork:~0221…'
def norm_evidence(platform, ev):
    ev = ev or ''
    if JOBTOK.search(ev): return ev
    return LOOSE.sub(lambda m: 'job:' + re.sub(r'[^a-z0-9.]+', '-', (platform or 'x').lower()).strip('-') + ':' + m.group(1), ev, count=1)
def problems(rows):
    out = []
    for i, r in enumerate(rows, 2):
        if not (r.get('row_id') or '').strip():
            out.append(f'line {i}: empty row_id')
            if not JOBTOK.search(r.get('evidence') or ''): out.append(f'line {i}: no job:<id> token either (sync would fall back to full text)')
    ids = [r.get('row_id') for r in rows if r.get('row_id')]
    out += [f'duplicate row_id {k}' for k in sorted({k for k in ids if ids.count(k) > 1})]
    return out
def backfill():
    rows = load(); seen = set(); n = 0
    for r in rows:
        if not (r.get('row_id') or '').strip():
            r['evidence'] = norm_evidence(r.get('platform'), r.get('evidence'))   # only rows without an id yet; existing ids/evidence untouched
        if not (r.get('row_id') or '').strip():
            base = rid(r); k = base; i = 2
            while k in seen: k = f'{base}-{i}'; i += 1   # identical duplicate rows get -2, -3 in file order (deterministic)
            r['row_id'] = k; n += 1
        seen.add(r['row_id'])
    save(rows); return n
def append(a):
    rows = load(); r = dict(date=a.date or dt.datetime.now(dt.timezone(dt.timedelta(hours=9))).date().isoformat(), platform=a.platform, agent=a.agent, count=str(a.count), evidence=norm_evidence(a.platform, a.evidence), kind=a.kind)
    ids = {x.get('row_id') for x in rows}; k = rid(r); i = 2; base = k
    while k in ids: k = f'{base}-{i}'; i += 1
    r['row_id'] = k; rows.append(r); save(rows); return k
if __name__ == '__main__':
    ap = argparse.ArgumentParser(); sp = ap.add_subparsers(dest='cmd', required=True)
    sp.add_parser('backfill'); sp.add_parser('check')
    x = sp.add_parser('append'); x.add_argument('--platform', required=True); x.add_argument('--agent', required=True); x.add_argument('--evidence', required=True)
    x.add_argument('--date'); x.add_argument('--count', type=int, default=1); x.add_argument('--kind', default='apply')
    a = ap.parse_args()
    if a.cmd == 'check':
        pr = problems(load()); print('\n'.join(pr) or 'ok'); sys.exit(1 if pr else 0)
    print(('backfilled ' + str(backfill())) if a.cmd == 'backfill' else append(a))
