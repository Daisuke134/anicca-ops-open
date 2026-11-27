#!/usr/bin/env python3
"""Fill per-post views/likes/replies/reposts in marketing/POST-LOG.csv (rows >24h old, impr_24h empty)
and write metrics/post-metrics.json (last 5 published Postiz posts per account, >24h old, with per-post analytics).
Sources: X = metrics/x-post-metrics.json (X connector public_metrics cache, written by the agent) else public syndication (likes/replies, no views);
Bluesky/Mastodon/Telegraph/dev.to public APIs; Postiz /analytics/post/{id}. Never prints secrets.
usage: fill_post_metrics.py [--no-postiz]"""
import csv, json, os, random, re, sys, time, datetime, urllib.request, urllib.parse
T = os.environ.get('OPEN_TEAM_DIR', '/workspace/team')
PL = os.path.join(os.environ.get('OPEN_MARKETING_DIR', '/workspace/marketing'), 'POST-LOG.csv')
OUT = f'{T}/metrics/post-metrics.json'
SECRETS = os.environ.get('OPEN_SECRETS_DIR', '/workspace/.secrets')
JST = datetime.timezone(datetime.timedelta(hours=9)); now = datetime.datetime.now(JST)
POSTIZ_CACHE_TTL = datetime.timedelta(hours=24)
def get(u, h=None):
    return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=h or {'User-Agent': 'anicca-metrics'}), timeout=40))
def pzkey():
    key = os.environ.get('POSTIZ_API_KEY', '').strip()
    if key: return key
    for f in (f'{SECRETS}/postiz', f'{SECRETS}/postiz.key'):
        try:
            with open(f, encoding='utf-8') as fh: return fh.read().split()[0]
        except Exception: pass
PZ = pzkey()
def pz(p): return get('https://api.postiz.com/public/v1' + p, {'Authorization': PZ, 'User-Agent': 'anicca-metrics'})
def pz_post(pid):
    d = {}; periods = {}; series = {}
    for x in pz('/analytics/post/' + pid):
        points = x.get('data') or []
        if not points: continue
        label = x['label'].lower(); point = points[-1]
        d[label] = int(float(point['total'])) if point.get('total') is not None else None
        if point.get('date'): periods[label] = point['date']
        series[label] = [dict(date=p['date'], value=int(float(p['total']))) for p in points
                         if p.get('date') and p.get('total') is not None]
    return dict(views=d.get('views', d.get('impressions')), likes=d.get('likes'),
                replies=d.get('comments', d.get('replies')), reposts=d.get('shares', d.get('reposts')),
                metric_periods=dict(views=periods.get('views', periods.get('impressions')),
                                    likes=periods.get('likes'), replies=periods.get('comments', periods.get('replies')),
                                    reposts=periods.get('shares', periods.get('reposts'))),
                metric_series=dict(views=series.get('views') or series.get('impressions') or [],
                                   likes=series.get('likes') or [], replies=series.get('comments') or series.get('replies') or [],
                                   reposts=series.get('shares') or series.get('reposts') or []))
def age_ok(s):
    m = re.match(r'(\d{4}-\d\d-\d\d)[ T]?(\d\d)?', s or '')
    if not m: return False
    t = datetime.datetime.fromisoformat(m.group(1) + ' ' + (m.group(2) or '00') + ':00').replace(tzinfo=JST)
    return now - t > datetime.timedelta(hours=24)
def cache_fresh(post):
    if not post or not post.get('metric_periods') or not post.get('metric_series') or not post.get('fetched_at'): return False
    try:
        fetched = datetime.datetime.fromisoformat(post['fetched_at'].replace('Z', '+00:00'))
        if fetched.tzinfo is None: fetched = fetched.replace(tzinfo=JST)
        age = now - fetched.astimezone(JST)
        return datetime.timedelta(0) <= age < POSTIZ_CACHE_TTL
    except (TypeError, ValueError):
        return False
xc = {}
try:
    with open(f'{T}/metrics/x-post-metrics.json', encoding='utf-8') as fh: xc = json.load(fh)['posts']
except Exception: pass
def fetch(r):
    u, p = r['post_url'], r['platform'].lower()
    if (u or '').startswith('postiz:') and PZ: return pz_post(u[7:])
    if p == 'x':
        m = re.search(r'status/(\d+)', u or '')
        if not m: return None
        i = m.group(1)
        if i in xc: return xc[i]
        d = get(f'https://cdn.syndication.twimg.com/tweet-result?id={i}&token=a')
        return dict(views=None, likes=d.get('favorite_count'), replies=d.get('conversation_count'), reposts=None)
    if p == 'bluesky':
        m = re.search(r'profile/([^/]+)/post/(\w+)', u)
        h = m.group(1); h = h if h.startswith('did:') else get('https://public.api.bsky.app/xrpc/com.atproto.identity.resolveHandle?handle=' + h)['did']  # handle URIs return 500
        d = get('https://public.api.bsky.app/xrpc/app.bsky.feed.getPosts?uris=' + urllib.parse.quote(f'at://{h}/app.bsky.feed.post/{m.group(2)}'))['posts'][0]
        return dict(views=None, likes=d.get('likeCount'), replies=d.get('replyCount'), reposts=d.get('repostCount'))
    if p == 'mastodon':
        m = re.search(r'https://([^/]+)/@[^/]+/(\d+)', u); d = get(f'https://{m.group(1)}/api/v1/statuses/{m.group(2)}')
        return dict(views=None, likes=d.get('favourites_count'), replies=d.get('replies_count'), reposts=d.get('reblogs_count'))
    if p == 'telegraph':
        d = get('https://api.telegra.ph/getViews/' + u.rstrip('/').split('/')[-1])
        return dict(views=d['result']['views'], likes=None, replies=None, reposts=None)
    if p == 'devto':
        path = u.split('dev.to/')[1].strip('/'); d = get('https://dev.to/api/articles/' + path)
        return dict(views=None, likes=d.get('public_reactions_count'), replies=d.get('comments_count'), reposts=None)
    return None
with open(PL, encoding='utf-8') as fh: rows = list(csv.DictReader(fh))
for r in rows: r.pop(None, None)  # drop overflow cols from unquoted commas
cols = [c for c in rows[0].keys() if c is not None]
filled = skipped = 0; why = {}
for r in rows:
    if r.get('impr_24h') or r.get('likes') or not age_ok(r['date_jst']): continue
    try: m = fetch(r)
    except Exception as e: m = None; why[r['platform']] = str(e)[:80]
    if not m: skipped += 1; why.setdefault(r['platform'], 'no public source'); continue
    if m.get('views') is not None: r['impr_24h'] = str(m['views'])
    for k in ('likes', 'replies', 'reposts'):
        if m.get(k) is not None: r[k] = str(m[k])
    filled += 1; time.sleep(0.2)
tmp = PL + '.tmp'
with open(tmp, 'w', encoding='utf-8', newline='') as fh:
    w = csv.DictWriter(fh, fieldnames=cols); w.writeheader(); w.writerows(rows)
os.replace(tmp, PL)
print(f'POST-LOG: filled {filled}, no source {skipped}', {k: v for k, v in why.items()})
# Postiz: last 5 published posts per account
if PZ and '--no-postiz' not in sys.argv:
    old = {}
    try:
        with open(OUT, encoding='utf-8') as fh: old = json.load(fh).get('posts', {})
    except Exception: pass
    s = (now - datetime.timedelta(days=10)).astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    e = (now - datetime.timedelta(hours=24)).astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    ps = pz('/posts?' + urllib.parse.urlencode({'startDate': s, 'endDate': e})); ps = ps.get('posts', ps) if isinstance(ps, dict) else ps
    ints = {i['id']: i for i in pz('/integrations')}
    by = {}
    for p in sorted(ps, key=lambda p: p.get('publishDate') or '', reverse=True):
        if p.get('state') != 'PUBLISHED': continue
        iid = (p.get('integration') or {}).get('id'); by.setdefault(iid, [])
        if len(by[iid]) < 5: by[iid].append(p)
    out, n, errs = {}, 0, 0
    for iid, L in by.items():
        i = ints.get(iid) or {}; acct = i.get('profile') or (p.get('integration') or {}).get('name')
        plat = {'instagram-standalone': 'Instagram', 'instagram': 'Instagram', 'tiktok': 'TikTok', 'youtube': 'YouTube', 'x': 'X', 'threads': 'Threads'}.get(i.get('identifier') or i.get('providerIdentifier'), i.get('identifier'))
        for p in L:
            c = old.get(p['id'])
            if not cache_fresh(c):
                try: c = dict(pz_post(p['id']), fetched_at=now.isoformat()); n += 1
                except Exception as ex:
                    errs += 1; c = c or {}
                    if '429' in str(ex): break
                time.sleep(0.5)
            out[p['id']] = dict(c, platform=plat, account=acct, t=p['publishDate'], url=p.get('releaseURL') or '')
    with open(OUT, 'w', encoding='utf-8') as fh:
        json.dump(dict(built_at=now.isoformat(), window_start=s, window_end=e,
                       selection='up to 5 most recent published posts per connected account; posts older than 24 hours',
                       posts=out), fh, ensure_ascii=False, indent=1)
    print(f'Postiz: {len(out)} posts across {len(by)} accounts, {n} fetched, {errs} errors')

def opener_effect(rows, n_boot=2000, seed=0):
    """Ratio of total impressions for opener='request' vs opener='number' rows,
    with a 95% bootstrap CI over resampled rows. Deterministic for a given seed."""
    def totals(sample):
        req = num = 0.0
        for r in sample:
            v = float(r.get('impressions') or 0)
            if r.get('opener') == 'request': req += v
            elif r.get('opener') == 'number': num += v
        return req, num
    req, num = totals(rows)
    mean = req / num if num else float('nan')
    n = len(rows)
    rng = random.Random(seed)
    boots = []
    for _ in range(n_boot):
        req_b, num_b = totals(rows[rng.randrange(n)] for _ in range(n)) if n else (0, 0)
        if num_b:
            boots.append(req_b / num_b)
    boots.sort()
    def quantile(p):
        if not boots:
            return float('nan')
        return boots[min(len(boots) - 1, max(0, int(p * len(boots))))]
    return dict(ratio=mean, ci=(quantile(0.025), quantile(0.975)), n_boot=n_boot, seed=seed, n_rows=n)
