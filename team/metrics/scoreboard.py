#!/usr/bin/env python3
"""accounts-snapshot-*.json -> /workspace/team/ACCOUNTS-SCOREBOARD.md + metrics/snapshots/scoreboard-YYYY-MM-DD.md"""
import json,glob,os,datetime
M='/workspace/team/metrics'; JST=datetime.timezone(datetime.timedelta(hours=9)); now=datetime.datetime.now(JST)
fs=sorted(glob.glob(f'{M}/accounts-snapshot-20??-??-??.json')); cur=json.load(open(fs[-1]))
prev={(r['platform'],r['account']):r for r in json.load(open(fs[-2]))['accounts']} if len(fs)>1 else {}
def n(x):
    try: return float(x)
    except Exception: return None
def views(r):
    for k in ('views_7d','impression_7d','impressions_7d','reach_7d'):
        if n(r.get(k)) is not None: return n(r[k])
def eng(r): return sum(n(r.get(k)) or 0 for k in r if k.endswith('_7d') and any(w in k for w in ('like','comment','share','save','repl','retweet','quote','bookmark')))
def d(a,b): return '—' if a is None or b is None else f'{a-b:+g}'
L=[f'# ACCOUNTS-SCOREBOARD — {now:%Y-%m-%d %H:%M} JST','比較: '+(os.path.basename(fs[-2]) if len(fs)>1 else 'なし')+'。views=7日表示/インプ。24h表示はPostizが日別しか返さないため7日値のみ。','',
 '|媒体|アカウント|担当|フォロワー|Δ|7d表示|Δ|7d反応|24h投稿|7d投稿|旗|','|---|---|---|---|---|---|---|---|---|---|---|']
flags=[];mv=[]
for r in cur['accounts']:
    p=prev.get((r['platform'],r['account']),{}); f=n(r.get('followers')); v=views(r); pv=views(p) if p else None
    p7=r.get('posts_7d'); fl=[]
    if r.get('disabled'): fl.append('無効')
    elif p7==0: fl.append('🔴投稿なし')
    if r.get('posts_24h')==0 and not r.get('disabled') and p7: fl.append('🟠24h投稿なし')
    if v is not None and pv and v<pv*0.7: fl.append('🔻表示-30%超')
    if f is not None and n(p.get('followers')) is not None and f<n(p['followers']): fl.append('🔻フォロワー減')
    if v is not None and v<=10 and p7: fl.append('⚫表示ほぼ0')
    if r.get('error') or r.get('analytics_error'): fl.append('読めず')
    if v is not None and pv is not None: mv.append((v-pv,r['platform'],r['account']))
    if fl: flags.append(f"- {r['platform']} {r['account']}（{r.get('owner','')[:6]}）: {' '.join(fl)}")
    L.append('|'+'|'.join(map(str,[r['platform'],r['account'],(r.get('owner') or '')[:8],'' if f is None else f'{f:g}',d(f,n(p.get('followers'))),'' if v is None else f'{v:g}',d(v,pv),f'{eng(r):g}',r.get('posts_24h','—'),'' if p7 is None else p7,' '.join(fl)]))+'|')
mv.sort()
L+=['','## 大きく動いた（7d表示、前回比）']+[f'- {a} {b}: {x:+g}' for x,a,b in mv[-5:][::-1]+mv[:5]]+['','## 旗']+flags
out='\n'.join(L)+'\n'; os.makedirs(f'{M}/snapshots',exist_ok=True)
open('/workspace/team/ACCOUNTS-SCOREBOARD.md','w').write(out); open(f'{M}/snapshots/scoreboard-{now:%Y-%m-%d}.md','w').write(out); print(out)
