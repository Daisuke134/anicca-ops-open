#!/usr/bin/env python3
"""Build the public /open/oogiri.json feed from the latest dated Oogiri snapshot.

Input:  $OPEN_TEAM_DIR/metrics/oogiri/snapshots/oogiri-*.json (latest by name)
Output: a single public JSON file (usage: build_open_oogiri.py OUTFILE)

Publish rules (exit 1 = do not publish):
  * snapshot schema must be exactly "oogiri-snapshot/v1";
  * every site status must be in the known enum;
  * only allowlisted fields are published - anything else is stripped;
  * no private-looking strings (emails, keys) and none of the dashboard's
    FORBIDDEN words may appear in the output;
  * measured values only: fields absent in the snapshot stay absent in the
    feed. Nothing is estimated and nothing is zero-filled.
"""
import glob
import json
import os
import re
import sys
import datetime as dt

T = os.environ.get('OPEN_TEAM_DIR', '/workspace/team')
JST = dt.timezone(dt.timedelta(hours=9))

SCHEMA = 'oogiri-snapshot/v1'
STATUS_ENUM = {
    'registered-awaiting-permission',
    'active',
    'declined',
    'not-registered',
}
SITE_FIELDS = [
    'site', 'display_name', 'profile_url', 'status', 'operator_request',
    'reason', 'status_read_at', 'answers_total', 'votes_received_total',
    'best_rank', 'latest_round', 'per_post',
]
POST_FIELDS = [
    'site', 'round_id', 'posted_at', 'good_votes', 'bad_votes', 'rank',
    'field_size', 'read_at',
]
INT_FIELDS = {'answers_total', 'votes_received_total', 'good_votes',
              'bad_votes', 'rank', 'field_size'}
FORBIDDEN = re.compile(r'unverified|partial|未接続', re.I)
PRIVATE = re.compile(
    r'(?i)[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'
    r'|(api[_-]?key|secret|password|token)\s*[:=]'
    r'|\bsk-[A-Za-z0-9]'
)

fail = []


def check_strings(value, where):
    if isinstance(value, str):
        if FORBIDDEN.search(value):
            fail.append(f'forbidden word in {where}')
        if PRIVATE.search(value):
            fail.append(f'private-looking string in {where}')
    elif isinstance(value, dict):
        for k, v in value.items():
            check_strings(v, f'{where}.{k}')
    elif isinstance(value, list):
        for i, v in enumerate(value):
            check_strings(v, f'{where}[{i}]')


def clean_post(row, where):
    for req in ('site', 'round_id', 'posted_at'):
        if not row.get(req):
            fail.append(f'{where}: per_post row missing required {req}')
            return None
    out = {}
    for k in POST_FIELDS:
        if k not in row or row[k] is None:
            continue  # absent stays absent: no zero-fill
        v = row[k]
        if k in INT_FIELDS:
            if not isinstance(v, int) or isinstance(v, bool) or v < 0:
                fail.append(f'{where}: {k} must be a non-negative integer')
                continue
        out[k] = v
    return out


def clean_site(site, where):
    st = site.get('status')
    if st not in STATUS_ENUM:
        fail.append(f'{where}: unknown status {st!r}')
    out = {}
    for k in SITE_FIELDS:
        if k not in site:
            continue
        v = site[k]
        if k == 'per_post':
            rows = []
            for i, row in enumerate(v or []):
                cleaned = clean_post(row, f'{where}.per_post[{i}]')
                if cleaned:
                    rows.append(cleaned)
            out[k] = rows
            continue
        if v is None:
            continue  # null means unknown: omit, do not publish a placeholder
        if k in INT_FIELDS:
            if not isinstance(v, int) or isinstance(v, bool) or v < 0:
                fail.append(f'{where}: {k} must be a non-negative integer')
                continue
        out[k] = v
    if not out.get('site'):
        fail.append(f'{where}: site name missing')
    return out


def main():
    if len(sys.argv) != 2:
        sys.exit('usage: build_open_oogiri.py OUTFILE')
    snaps = sorted(glob.glob(f'{T}/metrics/oogiri/snapshots/oogiri-*.json'))
    if not snaps:
        sys.exit(f'no Oogiri snapshots under {T}/metrics/oogiri/snapshots/')
    path = snaps[-1]
    snap = json.load(open(path, encoding='utf-8'))
    if snap.get('schema') != SCHEMA:
        sys.exit(f'{path}: schema must be {SCHEMA!r}, got {snap.get("schema")!r}')
    if not snap.get('read_at'):
        sys.exit(f'{path}: read_at missing')
    if not isinstance(snap.get('sites'), list) or not snap['sites']:
        sys.exit(f'{path}: sites must be a non-empty list')

    sites = [clean_site(s, f'sites[{i}]') for i, s in enumerate(snap['sites'])]
    feed = {
        'schema': SCHEMA,
        'read_at': snap['read_at'],
        'built_at': dt.datetime.now(JST).isoformat(timespec='seconds'),
        'source': (f'Oogiri measurement snapshot {os.path.basename(path)} '
                   f'(team metrics tree); public result pages and operator '
                   f'decisions only'),
        'note': 'Measured values only. Unknown fields are omitted, never zero-filled.',
        'sites': sites,
    }
    check_strings(feed, 'feed')
    if fail:
        for f in fail:
            print(f'REFUSE: {f}', file=sys.stderr)
        sys.exit(1)
    with open(sys.argv[1], 'w', encoding='utf-8') as fh:
        json.dump(feed, fh, ensure_ascii=False, indent=2)
        fh.write('\n')
    print(f'wrote {sys.argv[1]} from {os.path.basename(path)} '
          f'(read_at {snap["read_at"]}, {len(sites)} sites)')


if __name__ == '__main__':
    main()
