"""Rankings + money + winner gaps. Imported by collect_all.py (adds keys to snap). No secrets printed."""
import json, os, csv, urllib.request, urllib.error, urllib.parse, datetime as dt
S='/workspace/.secrets'
def _get(url, data=None, headers=None):
    r=urllib.request.Request(url, data=data, headers=headers or {'User-Agent':'collect_all'})
    return json.load(urllib.request.urlopen(r, timeout=25))
APPS={'Anicca':dict(id=6755129214,kw={'us':['affirmations','daily affirmations','affirmation app'],'jp':['アファメーション','アファメーション アプリ']}),
      'Honne':dict(id=6759667221,kw={'jp':['本音翻訳','LINE 相性','本音']}),
      'Thankful':dict(bundle='app.rork.thankful-gratitude-app',kw={'us':['gratitude journal','gratitude'],'jp':['感謝日記']})}
def app_ranks(gap):
    out={}
    for name,a in APPS.items():
        row=dict(keywords={})
        try:
            q=f"id={a['id']}" if 'id' in a else f"bundleId={a['bundle']}"
            res=_get(f'https://itunes.apple.com/lookup?{q}&country=jp').get('results') or _get(f'https://itunes.apple.com/lookup?{q}&country=us').get('results')
            if res:
                r=res[0]; a['id']=r['trackId']; row.update(id=r['trackId'],genre=r.get('primaryGenreName'),ratings=r.get('userRatingCount'),rating=r.get('averageUserRating'),version=r.get('version'))
        except Exception as e: gap(f'App Store lookup {name}',type(e).__name__)
        for cc,kws in a['kw'].items():
            for k in kws:
                try:
                    ids=[x['trackId'] for x in _get(f'https://itunes.apple.com/search?term={urllib.parse.quote(k)}&country={cc}&entity=software&limit=200')['results']]
                    row['keywords'][f'{cc}:{k}']=(ids.index(a.get('id'))+1) if a.get('id') in ids else '圏外(>200)'
                except Exception as e: gap(f'App Store search {name} {k}',type(e).__name__)
        out[name]=row
    gap('App Store category rank','Apple top-charts RSS only lists top 100-200 per genre; not in chart = no rank number')
    return out
def gsc(gap):
    try:
        c=json.load(open(f'{S}/gsc-adc.json'))
        tok=_get('https://oauth2.googleapis.com/token',data=urllib.parse.urlencode(dict(client_id=c['client_id'],client_secret=c['client_secret'],refresh_token=c['refresh_token'],grant_type='refresh_token')).encode())['access_token']
        H={'Authorization':f'Bearer {tok}','Content-Type':'application/json'}
        if c.get('quota_project_id'): H['x-goog-user-project']=c['quota_project_id']  # fix 2026-10-30: ADC user creds need the quota project header
        sites=[s['siteUrl'] for s in _get('https://www.googleapis.com/webmasters/v3/sites',headers=H).get('siteEntry',[])]
        end=dt.date.today()-dt.timedelta(days=2); out={}
        for s in sites:
            q=lambda dims,start: _get(f'https://www.googleapis.com/webmasters/v3/sites/{urllib.parse.quote(s,safe="")}/searchAnalytics/query',
                data=json.dumps(dict(startDate=str(start),endDate=str(end),dimensions=dims,rowLimit=15)).encode(),headers=H).get('rows',[])
            tot=q([],end-dt.timedelta(days=6)); prev=q([],end-dt.timedelta(days=13))
            out[s]=dict(d7=tot[0] if tot else None, top_queries=[dict(q=r['keys'][0],pos=round(r['position'],1),impr=r['impressions'],clicks=r['clicks']) for r in q(['query'],end-dt.timedelta(days=27))])
        return out
    except urllib.error.HTTPError as e: gap('GSC',f'HTTP {e.code}: {e.read()[:200].decode("utf-8","replace")}'); return None
    except Exception as e: gap('GSC',f'{type(e).__name__}'); return None
def capafy_rank(cap_list, gap):
    ranked=sorted([a for a in cap_list if a.get('uses') is not None], key=lambda a:-a['uses'])
    try:
        w=_get('https://api.capafy.ai/public/developer/agents?slug=saya&pageSize=100')['data']['list']
        wu=sorted([(x.get('salesVolume') or 0, x['title']) for x in w], reverse=True)[:3]
    except Exception as e: wu=None; gap('Capafy winner saya',type(e).__name__)
    gap('Capafy category/search position','no public search-rank endpoint found; only per-seller uses are public')
    return dict(our_top=[dict(rank=i+1,title=a['title'],uses=a['uses']) for i,a in enumerate(ranked[:5])], winner_saya_top=wu)
def money(T, snap, gap):
    c=json.load(open(f'{T}/cfo/costs_verified.json'))
    costs={i['name']:i['monthly_usd'] for i in c['items']}
    rev={}; now=dt.date.today(); ym=now.strftime('%Y-%m')
    for r in csv.DictReader(open(f'{T}/cfo/history.csv')):
        if r['kind']=='revenue' and r['date'].startswith(ym): rev[r['source']]=round(rev.get(r['source'],0)+float(r['amount_usd'] or 0),2)
    cap_oct=(snap['revenue'].get('capafy_orders_by_month_usd') or {}).get(ym,0)
    if cap_oct and not any('capafy' in k.lower() for k in rev): rev['capafy (orders)']=cap_oct
    fees={'Capafy 20%':round(sum(v for k,v in rev.items() if 'capafy' in k.lower())*0.2,2),'Apple 15% (RC MRR)':round((snap['mrr'].get('revenuecat') or 0)*0.15,2)}
    tr=round(sum(rev.values()),2); tf=round(sum(fees.values()),2); tc=round(sum(costs.values()),2)
    gap('Costs not in total', c.get('unknown',''))
    gap('Per-product cost split','vendor costs (Grok/ChatGPT/Postiz) are shared; not allocated per product')
    return dict(month=ym, revenue_by_source=rev, revenue_total=tr, platform_fees=fees, gross_profit=round(tr-tf,2),
        opex_monthly=costs, opex_total=tc, net=round(tr-tf-tc,2), burn=round(tc+tf-tr,2))
WINNERS=[ # product, winner, metric -> (ours, winner)  sources: team/gaps/*.md
 ('Anicca iOS','Daily Affirmations and Widgets (id6758928040)','US ratings','gaps/GAP-appstore-anicca.md'),
 ('Honne','めろとーく (id6757545135)','JP ranking/ratings','gaps/GAP-honne-merotalk.md'),
 ('Capafy','saya CloneCut (5133292529)','uses / daily demo video','gaps/GAP-capafy-Anicca.md'),
 ('PromptBase','@shandra (Rank #1)','sales / rank','gaps/GAP-promptbase-keipanda.md'),
 ('PDF Insight','ChatPDF','traffic / price','gaps/GAP-pdfinsight-chatpdf.md'),
 ('note','@yuusan_juusyoku','followers / daily posts','gaps/GAP-note-anicca123.md'),
 ('Upwork','vivek s. (Top Rated, 258 reviews)','reviews / catalog','gaps/GAP-upwork-daisukenarita.md')]
def winners(T):
    out=[]
    for p,w,m,f in WINNERS:
        txt=open(f'{T}/{f}').read() if os.path.exists(f'{T}/{f}') else ''
        rows=[l for l in txt.splitlines() if l.startswith('|') and not l.startswith('|-') and not l.startswith('|#')]
        out.append(dict(product=p,winner=w,metric=m,gap_rows=max(len(rows)-1,0),open=sum(1 for l in rows if 'open' in l.lower() or '未' in l),file=f))
    return out
def extend(T, snap, gap, cap_list):
    snap['rank']=dict(app_store=app_ranks(gap), gsc=gsc(gap), capafy=capafy_rank(cap_list,gap))
    gap('PromptBase rank/sales','no public API; dashboard login only (last read 10/27: 11 live, 0 sales)')
    gap('Google SERP for non-GSC sites','no SERP API key on box')
    snap['money']=money(T,snap,gap); snap['winners']=winners(T)
