#!/usr/bin/env python3
"""Rebuild team/NOW.md, NOW.json, metrics/ACCOUNTS-BOARD.md from existing files only. Unknown = 未取得.

Paths come from $TEAM_DIR / $MARKETING_DIR so the hourly health check and a local
test run can rebuild the board from a checkout instead of only the box's /workspace.
"""
import csv, glob, json, os, re, datetime as dt
T = os.environ.get('TEAM_DIR') or '/workspace/team'; M = os.environ.get('MARKETING_DIR') or '/workspace/marketing'; U = '未取得'
JST = dt.timezone(dt.timedelta(hours=9))
now = dt.datetime.now(JST).strftime('%Y-%m-%d %H:%M JST')
STALE_HOURS = 24  # a "last activity" older than this is shown as an old record, not current work
AG = ['参謀', 'Muse', 'Dots', 'Codex', 'Fucker', 'Anicca Marketer', 'dr eggbot', 'Forensic Writing', 'Muse Relay']
ALIAS = {'dr-eggbot': 'dr eggbot', 'dr eggbot': 'dr eggbot', 'Forensic': 'Forensic Writing', 'Marketer': 'Anicca Marketer',
         'Muse Relay': 'Muse Relay', 'muse-relay': 'Muse Relay', 'Fucker': 'Fucker', 'Dots': 'Dots', 'dots': 'Dots',
         'Codex': 'Codex', '参謀': '参謀', 'watcher (参謀)': '参謀', 'Muse': 'Muse'}
def rd(p):
    try: return open(p, encoding='utf-8').read()
    except Exception: return ''
def agents_in(s):
    out = []
    for k in sorted(ALIAS, key=len, reverse=True):
        if k in s:
            a = ALIAS[k]
            if a == 'Muse' and re.sub(r'Muse Relay|muse-relay', '', s).find('Muse') < 0: continue
            if a == 'Codex' and 'Codex' not in s.replace('box Codex', 'Codex'): continue
            if a not in out: out.append(a)
    return out
def mtime(p):
    try: return dt.datetime.fromtimestamp(os.path.getmtime(p), JST).strftime('%m/%d %H:%M')
    except Exception: return U
missing = []

# ---- loops
loops = []
lt = rd(f'{T}/LOOPS.md')
sec = lt.split('## 2.')[0]
for line in sec.splitlines():
    if not line.startswith('| ') or line.startswith('| #') or line.startswith('|---'): continue
    c = [x.strip() for x in line.strip().strip('|').split('|')]
    if len(c) < 5: continue
    c += [''] * (7 - len(c))
    sched = c[4]
    times = sorted(set(f'{int(h):02d}:{m}' for h, m in re.findall(r'(?<!\d)(\d{1,2}):(\d{2})', sched) if int(h) < 24))
    loops.append(dict(id=c[0], loop=re.sub(r'\*\*', '', c[1])[:120], owner=re.sub(r'\*\*', '', c[2])[:80],
                      owners=agents_in(c[2]) or ['Mac mini' if 'Mac mini' in c[2] else c[2][:20]], host=c[3][:40],
                      schedule=sched[:120], times=times, writes=c[5][:160], status=(c[6] or U)[:200]))
# §Muse loops
mu = lt.split('## §Muse')[1] if '## §Muse' in lt else ''
for name, t in re.findall(r'([a-z][a-z\-/ と]+?) (\d{2}:\d{2})', mu.split('毎日のループ')[1].split('\n')[0] if '毎日のループ' in mu else ''):
    loops.append(dict(id='M', loop='Muse ' + name.strip('、 '), owner='Muse', owners=['Muse'], host='Muse VM', schedule='毎日 ' + t,
                      times=[t], writes='§Muse', status=U))
for freq, names in re.findall(r'(3時間ごと|1時間ごと|6時間ごと|30分ごと|15分ごと)：([^。]+)', mu):
    for n in re.split(r'、', names):
        n = re.sub(r'（.*', '', n).strip()
        if n: loops.append(dict(id='M', loop='Muse ' + n, owner='Muse', owners=['Muse'], host='Muse VM', schedule=freq, times=[], writes='§Muse', status=U))

# ---- activity sources
acts = {a: [] for a in AG}
def add(a, t, what, src):
    if a in acts: acts[a].append((t, what[:180], src))
for line in rd(f'{T}/LIVE-STATE.md').splitlines()[-60:]:
    p = [x.strip() for x in line.strip('| ').split('|')]
    if len(p) >= 4:
        m = re.search(r'20\d\d-\d\d-\d\d \d\d:\d\d', line)
        for a in agents_in(p[0])[:1]: add(a, m.group(0) if m else '', p[1] + ': ' + p[2], 'LIVE-STATE.md')
cards = []
for f in sorted(glob.glob(f'{T}/BOARD/*.md')):
    if os.path.basename(f).startswith('_'): continue
    s = rd(f); g = lambda k: (re.search(rf'^- {k}:\s*(.*)$', s, re.M) or [None, ''])[1].strip()
    st = re.findall(r'^STATE:.*$', s, re.M)
    card = dict(card=os.path.basename(f)[:-3], owner=g('owner') or U, status=g('status') or U, last=g('last_activity') or U,
                next=g('next_action') or U, deadline=g('deadline') or U, state=(st[-1] if st else U)[:200])
    cards.append(card)
    for a in agents_in(card['owner'])[:1]:
        add(a, card['last'] if card['last'] != U else '', f"{card['card']} [{card['status']}] next: {card['next']}", f'BOARD/{card["card"]}.md')
for line in rd(f'{T}/health/failures.md').splitlines():
    p = [x.strip() for x in line.split('|')]
    if len(p) >= 4:
        for a in agents_in(p[1])[:1]: add(a, p[0], 'FAILURE: ' + p[3], 'health/failures.md')
for l in loops:
    m = re.search(r'(1\d)/(\d\d)\s*(\d\d):(\d)(\d|x)', l['status'])
    if m:
        for a in l['owners'][:1]:
            add(a, f"2026-{int(m.group(1)):02d}-{m.group(2)} {m.group(3)}:{m.group(4)}{m.group(5).replace('x','0')}", f"loop #{l['id']} {l['loop'][:50]}: {l['status'][:100]}", 'LOOPS.md')
# wake
wl = [l for l in rd(f'{T}/wake/WAKE_LOG.md').splitlines() if l.strip()]
wake_last = wl[-1][:220] if wl else U

# ---- live reports (the team's own 15-minute channel) ----
# BOARD/LIVE-STATE stop being written for days at a time; ACTIVITY.md and LIVE-NOW.md are
# where agents actually post START/DONE/FIX. Report them separately so a days-old board row
# is never read as current work (STALLED-NOW #30).
STAMP_RE = re.compile(r'\[?(20\d\d-\d\d-\d\d)[ T](\d{1,2})(x?):(\d{1,2})(x?)(?::\d{2})?\s*(?:JST)?\]?')
KIND_RE = re.compile(r'\|\s*(START|DONE|FIX|SYNC|SHARE|BLOCKED|GO|UPDATE|NOTE)[^|]*', re.I)
NAME_MAP = {'dr-eggbot': 'dr eggbot', 'dr eggbot': 'dr eggbot', 'forensic': 'Forensic Writing',
            'marketer': 'Anicca Marketer', 'anicca marketer': 'Anicca Marketer', '参謀': '参謀',
            'muse': 'Muse', 'dots': 'Dots', 'codex': 'Codex', 'fucker': 'Fucker',
            'muse relay': 'Muse Relay', 'pickle': 'Pickle', 'x operator': 'X Operator',
            'applications': 'Applications', 'reporter': 'Reporter', 'chatgpt': 'ChatGPT', 'devin': 'Devin'}

def live_reports():
    newest = {}
    for fname in ('ACTIVITY.md', 'LIVE-NOW.md'):
        for raw in rd(f'{T}/{fname}').splitlines():
            line = raw.strip()
            m = STAMP_RE.search(line)
            if not m or len(line) < 16:
                continue
            try:
                hh, mm = int(m.group(2)), int(m.group(4))
                if m.group(3):
                    hh *= 10
                if m.group(5):
                    mm *= 10
                when = dt.datetime.strptime(f'{m.group(1)} {hh:02d}:{mm:02d}', '%Y-%m-%d %H:%M').replace(tzinfo=JST)
            except ValueError:
                continue
            rest = re.sub(r'^\s*[|｜]\s*', '', line[m.end():].lstrip(' ]'))
            cand = re.split(r'[|｜→]', rest)[0].strip()
            cand = re.sub(r'^[@\s]+', '', cand).strip().lower()
            cand = re.sub(r'\s*\(.*?\)\s*', '', cand).strip()
            agent = NAME_MAP.get(cand)
            if not agent:
                continue
            prev = newest.get(agent)
            if prev and prev['when'] >= when:
                continue
            k = KIND_RE.search(line)
            newest[agent] = dict(agent=agent, when=when, kind=(k.group(1).upper() if k else 'NOTE'),
                                 text=re.sub(r'^[-\s]*\[?20\d\d-\d\d-\d\d[^|｜→]*[|｜]?\s*', '', line)[:200],
                                 source=fname)
    out = []
    for agent, s in newest.items():
        ah = (dt.datetime.now(JST) - s['when']).total_seconds() / 3600
        out.append(dict(agent=agent, at=s['when'].strftime('%Y-%m-%d %H:%M'), kind=s['kind'],
                        text=(s['text'] or '').replace(chr(10), ' '), source=s['source'],
                        age_hours=round(ah, 1), stale=(ah > STALE_HOURS)))
    return sorted(out, key=lambda x: x['at'], reverse=True)

live = live_reports()

def tkey(t):
    m = re.search(r'(20\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d)', t or '')
    return m.groups() if m else ('0',)

def age_hours(t):
    """Hours since the recorded stamp, or None when the stamp is unusable."""
    m = re.search(r'(20\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d)', t or '')
    if not m:
        return None
    try:
        return (dt.datetime.now(JST) - dt.datetime(*[int(x) for x in m.groups()], tzinfo=JST)).total_seconds() / 3600
    except ValueError:
        return None

right = []
for a in AG:
    xs = sorted(acts[a], key=lambda x: tkey(x[0]))
    nonfail = [x for x in xs if not x[1].startswith('FAILURE')]
    cur = (nonfail or xs or [(U, U, U)])[-1]
    ah = age_hours(cur[0])
    right.append(dict(agent=a, task=cur[1], last=cur[0] or U, source=cur[2],
                      age_hours=(round(ah, 1) if ah is not None else None),
                      stale=(ah is None or ah > STALE_HOURS),
                      blockers=[x[1] for x in xs if 'FAILURE' in x[1] or 'block' in x[1].lower() or '待ち' in x[1]][-3:]))
    if cur[1] == U: missing.append(f'{a}: 現在タスクの記録なし（LIVE-STATE/BOARD に行がない）')

# ---- posts & accounts
posts = []
try:
    with open(f'{M}/POST-LOG.csv', encoding='utf-8') as fh:
        posts = list(csv.DictReader(fh))
except Exception: missing.append('marketing/POST-LOG.csv 読めず')
snapf = sorted(glob.glob(f'{T}/metrics/accounts-snapshot-*.json'))
snap = json.load(open(snapf[-1])) if snapf else {}
prev = json.load(open(snapf[-2])) if len(snapf) > 1 else {}
latest = {}
try: latest = json.load(open(f'{T}/metrics/latest.json'))
except Exception: missing.append('metrics/latest.json 読めず')
def key(p, a): return (p.lower(), re.sub(r'^@', '', a).lower())
prevf = {key(x.get('platform', ''), x.get('account', '')): x.get('followers') for x in (prev.get('accounts') or [])}
gaps = {}
for f in glob.glob(f'{T}/gaps/GAP-*.md'):
    s = rd(f); w = re.search(r'^Winner[^:]*:\s*(.*)$', s, re.M)
    nxt = [l for l in s.splitlines() if l.startswith('|') and '|open|' in l.replace(' ', '')]
    gaps[os.path.basename(f)[4:-3].lower()] = dict(winner=(w.group(1)[:220] if w else U),
        next=(re.sub(r'\s+', ' ', nxt[0])[:200] if nxt else U), file='gaps/' + os.path.basename(f))
def gap_for(plat, acct):
    a = re.sub(r'^@', '', acct).lower(); p = plat.lower().replace('instagram', 'instagram')
    for k, v in gaps.items():
        if a and a in k and (p[:4] in k or p in ('ig',) and 'instagram' in k): return v
    for k, v in gaps.items():
        if a and a in k: return v
    return None
accts = []
seen = set()
for x in (snap.get('accounts') or []):
    k = key(x.get('platform', ''), x.get('account', '')); seen.add(k)
    pl = [p for p in posts if key(p.get('platform', ''), p.get('account', ''))[1].endswith(k[1]) and k[1]]
    f0, f1 = x.get('followers'), prevf.get(k)
    g = gap_for(x.get('platform', ''), x.get('account', ''))
    accts.append(dict(platform=x.get('platform'), account=x.get('account'), poster=x.get('owner') or U,
        followers=f0 if f0 is not None else U, followers_delta=(round(f0 - f1) if f0 is not None and f1 is not None else U),
        posts_7d=x.get('posts_7d', U), views_7d=x.get('views_7d', U), likes_7d=x.get('recent_likes_7d', U),
        comments_7d=x.get('recent_comments_7d', U), shares_7d=x.get('recent_shares_7d', U),
        er_7d=(f"{(x.get('recent_likes_7d') or 0)+(x.get('recent_comments_7d') or 0)+(x.get('recent_shares_7d') or 0)}/{x['views_7d']:.0f}=" +
               f"{100*((x.get('recent_likes_7d') or 0)+(x.get('recent_comments_7d') or 0)+(x.get('recent_shares_7d') or 0))/x['views_7d']:.1f}%") if x.get('views_7d') else U,
        last_post=x.get('last_post') or U, recent=[dict(t=p['date_jst'], url=p['post_url'], views=p.get('impr_24h') or U, likes=p.get('likes') or U,
            reposts=p.get('reposts') or U, replies=p.get('replies') or U) for p in pl[-5:]],
        winner=(g or {}).get('winner', U), next_copy=(g or {}).get('next', U), gap_file=(g or {}).get('file', U), src=os.path.basename(snapf[-1]) if snapf else U))
# accounts only in POST-LOG / latest.json
xf = ((latest.get('distribution') or {}).get('x_followers') or {})
for p in posts:
    k = key(p.get('platform', ''), p.get('account', ''))
    if k in seen: continue
    seen.add(k)
    pl = [q for q in posts if key(q.get('platform', ''), q.get('account', '')) == k]
    h = k[1].lstrip('@'); g = gap_for(k[0], h)
    fol = (xf.get(h) or {}).get('followers', U) if k[0] == 'x' else U
    accts.append(dict(platform=k[0], account=p.get('account'), poster=U, followers=fol, followers_delta=U, posts_7d=U, views_7d=U, likes_7d=U,
        comments_7d=U, shares_7d=U, er_7d=U, last_post=pl[-1]['date_jst'],
        recent=[dict(t=q['date_jst'], url=q['post_url'], views=q.get('impr_24h') or U, likes=q.get('likes') or U, reposts=q.get('reposts') or U,
                     replies=q.get('replies') or U) for q in pl[-5:]],
        winner=(g or {}).get('winner', U), next_copy=(g or {}).get('next', U), gap_file=(g or {}).get('file', U), src='POST-LOG.csv'))
# sole poster from ACCOUNT-OWNERS
ao = rd(f'{T}/ACCOUNT-OWNERS.md')
for a in accts:
    if a['poster'] not in (U, None, ''): continue
    h = str(a['account']).lstrip('@').lower()
    for line in ao.splitlines():
        if line.startswith('|') and h and h in line.lower():
            a['poster'] = line.split('|')[3].strip()[:60]; break
# per-post metrics from fill_post_metrics.py (Postiz) when POST-LOG has none
try: _pm = json.load(open(f'{T}/metrics/post-metrics.json')).get('posts', {})
except Exception: _pm = {}
for a in accts:
    if any(re.fullmatch(r'[\d.]+', str(r['views'])) for r in a['recent']): continue
    h = str(a['account']).lstrip('@').lower()
    L = sorted([v for v in _pm.values() if str(v.get('account', '')).lower() == h and str(v.get('platform', '')).lower() == str(a['platform']).lower()], key=lambda v: v['t'])[-5:]
    if L: a['recent'] = [dict(t=v['t'][:16], url=v['url'], views=v.get('views') if v.get('views') is not None else U, likes=v.get('likes', U), reposts=v.get('reposts', U), replies=v.get('replies', U)) for v in L]
for a in accts:
    vs = [float(r['views']) for r in a['recent'] if re.fullmatch(r'[\d.]+', str(r['views']))]
    a['avg_views_last5'] = round(sum(vs) / len(vs)) if vs else U
for k in ['followers', 'views_7d']:
    n = sum(1 for a in accts if a[k] == U)
    if n: missing.append(f'アカウント {n}/{len(accts)} 件で {k} が未取得')
missing.append(f"直近5本平均views 未取得: {sum(1 for a in accts if a['avg_views_last5']==U)}/{len(accts)} アカウント（fill_post_metrics.py で毎時書き戻し）")
missing.append('Threads・note・LinkedIn・Muse の IG 投稿別数字：ファイルに記録なし')

# SEO
seo = rd(f'{T}/marketing/SEO-GSC.md') or rd(f'{M}/SEO-GSC.md')
seo_lines = [l for l in seo.splitlines() if re.search(r'click|imp|indexed|Sitemap|28d|90d', l, re.I)][:6]
seo_upd = (re.findall(r'^#+ .*?(20\d\d-\d\d-\d\d[^)]*)', seo, re.M) or [U])[-1]

# overlaps
ov = []
plat_owners = {}
for l in loops:
    for pf in ['Lancers', 'lancers', 'Coconala', 'ココナラ', 'coconala', 'CrowdWorks', 'crowdworks', 'Mercor', 'mercor', 'Capafy', 'capafy', 'Upwork', '@selawmqt', '@diceai0', 'contra', 'Contra']:
        if pf in l['loop'] + l['writes']:
            nm = pf.lower().replace('ココナラ', 'coconala')
            st = l['status']
            if 'PAUSED' in st or 'STOPPED' in st or '停止' in st[:10]: continue
            for o in l['owners']: plat_owners.setdefault(nm, set()).add(f"{o}(#{l['id']} {l['loop'][:30]})")
roles = rd(f'{T}/ROLES.md')
for nm, os_ in sorted(plat_owners.items()):
    ags = {x.split('(')[0] for x in os_}
    if len(ags) > 1: ov.append(f'{nm}: ' + ' / '.join(sorted(os_)))
if re.search(r'Lancers', roles) and '参謀' in roles:
    ln = [l for l in roles.splitlines() if 'Lancers' in l][:1]
    if ln: ov.append('lancers: ROLES.md にも記載 → ' + ln[0][:140])
for line in ao.splitlines():
    if line.startswith('|') and ('全員本番' in line.split('|')[3] if len(line.split('|')) > 3 else False):
        ov.append('1垢1投稿者ルール違反の恐れ: ' + line.split('|')[1].strip()[:50] + ' owner欄=' + line.split('|')[3].strip()[:60])

# ---- write
data = dict(built_at=now, right_now=right, live=live, loops=loops, cards=cards, accounts=accts, seo=dict(updated=seo_upd, lines=seo_lines),
            wake_last=wake_last, overlaps=ov, missing=missing)
json.dump(data, open(f'{T}/NOW.json', 'w'), ensure_ascii=False, indent=1)

def acct_md():
    o = [f'# ACCOUNTS-BOARD（SNS スコアボード）{now}', '> 自動生成 scripts/build_now.py。数字は既存ファイルのみ。空欄＝未取得。', '',
         '| platform | account | 投稿者(1人) | followers | 7d増減 | 7d投稿 | 7d views | 7d いいね/コメ/シェア | ER 7d | 直近5本 平均views | 最終投稿 | Copy the winners | 次にコピーする型 |', '|' + '---|' * 13]
    for a in sorted(accts, key=lambda a: (str(a['platform']), str(a['account']))):
        o.append('| ' + ' | '.join(str(v).replace('|', '/').replace('\n', ' ') for v in [a['platform'], a['account'], a['poster'], a['followers'], a['followers_delta'],
            a['posts_7d'], a['views_7d'], f"{a['likes_7d']}/{a['comments_7d']}/{a['shares_7d']}", a['er_7d'], a['avg_views_last5'], a['last_post'],
            a['winner'][:120], a['next_copy'][:120]]) + ' |')
    o += ['', '## 直近5投稿（POST-LOG.csv）']
    for a in accts:
        if a['recent']:
            o.append(f"- **{a['platform']} {a['account']}**")
            o += [f"  - {r['t']} views {r['views']} いいね {r['likes']} RP {r['reposts']} 返信 {r['replies']} {r['url']}" for r in a['recent']]
    return '\n'.join(o) + '\n'
open(f'{T}/metrics/ACCOUNTS-BOARD.md', 'w').write(acct_md())

o = [f'# NOW — Anicca live team board',
     f'Built {now} by scripts/build_now.py。生成経路: hourly health check（team/scripts/health_check.sh の board ステップ、毎時）／手動 `TEAM_DIR=team python3 team/scripts/build_now.py`。正本: LOOPS.md / ACCOUNT-OWNERS.md / BOARD/。空欄＝{U}。',
     '「最終活動」は出典ファイルに書かれた時刻であって、稼働中の証明ではない。{0}h 以上前の行は ⚠{0}h を付け、古い記録として扱う。'.format(STALE_HOURS), '',
     '## ライブ報告（正本: ACTIVITY.md / LIVE-NOW.md の最新行、15分更新ルール）', '| agent | 最終報告 | 種別 | 何を | 出典 |', '|---|---|---|---|---|']
o += [f"| {r['agent']} | {r['at']}（{r['age_hours']:.0f}h前）{' ⚠' + str(STALE_HOURS) + 'h超' if r['stale'] else ''} | {r['kind']} | {r['text'][:160].replace('|', '/')} | {r['source']} |" for r in live]
if not live: o += ['| — | 記録なし | — | ACTIVITY.md に日付付きの行がない | — |']
o += ['',
     '## Right now（旧 BOARD / LIVE-STATE の最終記録。稼働中の証明ではない）', '| agent | 今のタスク | 最終活動 | 出典 | 詰まり |', '|---|---|---|---|---|']
def _last_cell(r):
    if r['age_hours'] is None:
        return f"{r['last']}（経過不明）" + (f" ⚠{STALE_HOURS}h超" if r['stale'] else '')
    cell = f"{r['last']}（{r['age_hours']:.0f}h前）"
    return cell + (f" ⚠{STALE_HOURS}h超" if r['stale'] else '')
for r in right: o.append(f"| {r['agent']} | {r['task'].replace('|','/')} | {_last_cell(r)} | {r['source']} | {'; '.join(b[:60] for b in r['blockers']) or '-'} |")
o += ['', f'Wake 最終: {wake_last}', '', '## Daily schedule（JST 24h、時刻指定のあるループ）', '| JST | loop | owner |', '|---|---|---|']
tl = sorted((t, l['loop'], l['owner']) for l in loops for t in l['times'])
o += [f'| {t} | {n} | {w} |' for t, n, w in tl]
o += ['', '### 時刻なし・周期ループ', '| 周期 | loop | owner |', '|---|---|---|']
o += [f"| {l['schedule']} | {l['loop']} | {l['owner']} |" for l in loops if not l['times']]
o += ['', '## エージェント別']
for a in AG:
    o.append(f'### {a}')
    o += [f"- #{l['id']} {l['loop']} — {l['schedule']} — 状態: {l['status'][:120]}" for l in loops if a in l['owners']]
    o += [f"- card {c['card']} [{c['status']}] last {c['last']} next: {c['next'][:100]}" for c in cards if a in agents_in(c['owner'])]
o += ['', '## SNS スコアボード（詳細 metrics/ACCOUNTS-BOARD.md）', acct_md().split('\n', 3)[3].split('## 直近5投稿')[0]]
o += ['## SEO（marketing/SEO-GSC.md, 最終 ' + seo_upd + '）'] + ['- ' + l.strip('- ')[:200] for l in seo_lines]
o += ['', '## 重なり（担当が2人以上）'] + ['- ⚠ ' + x for x in ov]
o += ['', '## 未取得データ'] + ['- ' + x for x in missing]
# Preserve hand-maintained tail (open to-dos + long-term thinking). These are the
# canonical live lists; this script must not wipe them. Search the live tree and
# the repo copy next to this script so a just-committed section survives the next hourly run.
HAND_MARKS = ('## Open to-dos (canonical', '### Long-term thinking actions')
def extract_hand():
    candidates = [f'{T}/NOW.md', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'NOW.md')]
    best = ''
    for path in candidates:
        s = rd(path)
        idxs = [s.find(m) for m in HAND_MARKS if s.find(m) >= 0]
        if idxs:
            chunk = s[min(idxs):].rstrip()
            if len(chunk) > len(best):
                best = chunk
    return best
hand = extract_hand()
body = '\n'.join(o) + '\n'
if hand:
    body = body.rstrip() + '\n\n' + hand + '\n'
open(f'{T}/NOW.md', 'w').write(body)
print('ok', len(loops), 'loops', len(accts), 'accounts', len(ov), 'overlaps', 'hand', bool(hand))
