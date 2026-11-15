#!/usr/bin/env python3
"""Public-safe team board JSON from NOW.json (no emails, no client names, no free text from cards).

Also attaches the owners roster (Grok bots + legacy contacts) via build_team_owners:
cadence = schedule only; current_task stays unknown; DAILY-LOG becomes latest_outcome.
"""
import json, os, re, sys
from pathlib import Path

ROOT = Path(os.environ.get('TEAM_DIR') or Path(__file__).resolve().parents[2])  # /workspace/team
sys.path.insert(0, str(Path(__file__).resolve().parent))
# Prefer products-repo builder when present on the box checkout path.
candidates = [
    Path('/workspace/wt-open-team/apps/landing/scripts/open/build_team_owners.py'),
    Path('/workspace/team/scripts/open/build_team_owners.py'),
    Path(__file__).resolve().parent / 'build_team_owners.py',
]
build_owners_mod = None
for c in candidates:
    if c.exists():
        import importlib.util
        spec = importlib.util.spec_from_file_location('build_team_owners', c)
        build_owners_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(build_owners_mod)
        break

d = json.load(open(ROOT / 'NOW.json'))

def clean(s, n=80):
    s = re.sub(r'[\w.+-]+@[\w-]+\.[\w.]+', '[email]', str(s))
    s = re.sub(r'(sk|rk|pk)_(live|test)_\w+|\b[0-9a-f]{32,}\b', '[redacted]', s)
    s = re.sub(r'\+?\d[\d -]{9,}\d', '[num]', s)
    s = re.sub(r'/(?:workspace|home|Users)/\S*', '[path]', s)
    return s[:n]

out = dict(
  built_at=d['built_at'],
  right_now=[dict(agent=r['agent'], last=r['last'][:16], source=r['source'].split('/')[0],
     task=(re.match(r'([\w\-]+)', r['task']).group(1) if r['source'].startswith('BOARD') else clean(r['task'].split(':')[0], 50)),
     blocked=bool(r['blockers']),
     age_hours=r.get('age_hours'), stale=r.get('stale')) for r in d['right_now']],
  loops=[dict(id=l['id'], loop=clean(l['loop'], 70), owner=clean(l['owner'], 40), schedule=clean(l['schedule'], 60), times=l['times']) for l in d['loops']],
  accounts=[dict(platform=a['platform'], account=clean(a['account'], 40), poster=clean(a['poster'], 30), followers=a['followers'],
     followers_7d=a['followers_delta'], posts_7d=a['posts_7d'], views_7d=a['views_7d'], er_7d=a['er_7d'], avg_views_last5=a.get('avg_views_last5','未取得'), last_post=str(a['last_post'])[:16],
     winner=(re.search(r'https://\S+', a['winner']) or [None])[0] if a['winner'] != '未取得' else '未取得') for a in d['accounts']],
  seo=[clean(x, 160) for x in d['seo']['lines'][:4]]
)

if build_owners_mod is not None:
    from datetime import datetime, timedelta, timezone
    JST = timezone(timedelta(hours=9))
    now = datetime.now(JST)
    owners = build_owners_mod.build_owners(ROOT, now)
    out = build_owners_mod.merge_public(out, owners, out['built_at'])

json.dump(out, open(sys.argv[1], 'w'), ensure_ascii=False, indent=1)
print('team public wrote', sys.argv[1], 'owners', len(out.get('owners', [])))
