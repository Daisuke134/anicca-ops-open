#!/usr/bin/env python3
"""End-to-end: post -> engagement -> taps -> installs -> paid -> revenue. Read-only.
usage: python3 e2e.py [START END]   (default: 7 days ending yesterday + today)
in : Postiz analytics, POST-LOG.csv, ASC Sales SUMMARY (daily), RevenueCat v2 overview,
     connector-pulls/*.json (PostHog utm/ct, Stripe, X) written by the routine via connectors.
out: e2e-YYYY-MM-DD.csv (one row per date x account/product x metric), CHANGES.csv (appended), E2E.md"""
import jwt,time,urllib.request,urllib.parse,gzip,json,csv,os,sys,datetime,collections,subprocess,re
D='/workspace/team/metrics/attribution'; S='/workspace/.secrets'
JST=datetime.timezone(datetime.timedelta(hours=9)); today=datetime.datetime.now(JST).date()
if len(sys.argv)==3: start,end=[datetime.date.fromisoformat(x) for x in sys.argv[1:]]
else: start,end=today-datetime.timedelta(days=7),today
days=[start+datetime.timedelta(n) for n in range((end-start).days+1)]
rows=[]; gaps=[]
def add(d,product,layer,source,key,metric,val,note=''): rows.append(dict(date=str(d),product=product,layer=layer,source=source,key=key,metric=metric,value=val,note=note))
PROD={'6755129214':'Anicca','6757726663':'Daily Dhamma','6759514159':'Thankful','6762143790':'Sleep Reset','6759667221':'Honne'}
# ---- installs / paid / proceeds: ASC
def asc():
    e=dict(l.strip().split('=',1) for l in open(S+'/asc.env') if '=' in l)
    k=open(S+'/AuthKey_%s.p8'%e['ASC_KEY_ID']).read()
    t=jwt.encode({'iss':e['ASC_ISSUER_ID'],'exp':int(time.time())+1000,'aud':'appstoreconnect-v1'},k,algorithm='ES256',headers={'kid':e['ASC_KEY_ID']})
    for d in days:
        u='https://api.appstoreconnect.apple.com/v1/salesReports?'+urllib.parse.urlencode({'filter[frequency]':'DAILY','filter[reportType]':'SALES','filter[reportSubType]':'SUMMARY','filter[vendorNumber]':e['ASC_VENDOR_NUMBER'],'filter[reportDate]':str(d)})
        try: txt=gzip.decompress(urllib.request.urlopen(urllib.request.Request(u,headers={'Authorization':'Bearer '+t,'Accept':'application/a-gzip'}),timeout=60).read()).decode()
        except Exception as x:
            add(d,'ALL','installs','ASC','-','report_status','n/a','not published yet' if '404' in str(x) else str(x)[:60]); continue
        agg=collections.Counter()
        for r in csv.DictReader(txt.splitlines(),delimiter='\t'):
            pid=r['Parent Identifier'].strip() or r['Apple Identifier']; app=r['Title'] if pid==r['Apple Identifier'] else None
            ty=r['Product Type Identifier']; u_=int(r['Units'] or 0)
            name=PROD.get(r['Apple Identifier'],r['Title']) if not r['Parent Identifier'].strip() else 'sub:'+r['Parent Identifier'].strip()
            if ty in('1','1F','1T','F1'): agg[(name,'installs','new_downloads')]+=u_
            elif ty in('3','3F','3T','F3'): agg[(name,'installs','redownloads')]+=u_
            elif ty.startswith('IA') or ty.startswith('FI'):
                agg[(name,'paid','iap_units')]+=u_
                try: agg[(name,'revenue','proceeds_'+r['Currency of Proceeds'])]+=float(r['Developer Proceeds'])*u_
                except: pass
        for (n,l,m),v in agg.items(): add(d,n,l,'ASC','app',m,round(v,2))
# ---- engagement: Postiz daily series per account
def postiz():
    PZ=open(S+'/postiz').read().split()[0]; g=lambda p: json.load(urllib.request.urlopen(urllib.request.Request('https://api.postiz.com/public/v1'+p,headers={'Authorization':PZ}),timeout=60))
    n=(today-start).days+1
    ints=g('/integrations'); idm={i['id']:i.get('profile') for i in ints}
    for i in ints:
        try: an=g(f"/analytics/{i['id']}?date={min(max(n,7),30)}")
        except Exception as x: gaps.append(f"Postiz analytics {i.get('profile')}: {str(x)[:50]}"); continue
        for a in an:
            for p in a.get('data') or []:
                ds=(p.get('date') or '')[:10]
                if ds and start<=datetime.date.fromisoformat(ds)<=end:
                    add(ds,'acct:'+str(i.get('profile')),'engagement','Postiz',i.get('identifier'),a['label'].lower().replace(' ','_'),p.get('total'))
    try:
        s=datetime.datetime.combine(start,datetime.time(),JST).astimezone(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'); e_=datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
        ps=g('/posts?'+urllib.parse.urlencode({'startDate':s,'endDate':e_})); ps=ps.get('posts',ps) if isinstance(ps,dict) else ps
        for p in ps:
            if (p.get('state') or '')=='ERROR': continue
            d=datetime.datetime.fromisoformat(p['publishDate'].replace('Z','+00:00')).astimezone(JST).date()
            txt=re.sub(r'<[^>]+>','',p.get('content') or '')[:60].replace('\n',' ')
            ct=';'.join(re.findall(r'(?:ct|utm_campaign)=([\w\-.]+)',p.get('content') or ''))
            add(d,'acct:'+str(idm.get((p.get('integration') or {}).get('id'),(p.get('integration') or {}).get('profile'))),'post','Postiz',p.get('releaseURL') or p.get('id'),'posted',1,(txt+(' |ct='+ct if ct else '')))
    except Exception as x: gaps.append('Postiz posts: '+str(x)[:60])
# ---- POST-LOG.csv (non-Postiz posts)
def postlog():
    for r in csv.DictReader(open('/workspace/marketing/POST-LOG.csv')):
        try: d=datetime.date.fromisoformat(r['date_jst'][:10])
        except: continue
        if start<=d<=end:
            add(d,'acct:'+r['platform']+'/'+r['account'],'post','POST-LOG',r['post_url'],'posted',1,r['topic'][:60])
            for m in('impr_24h','likes','reposts','replies','follows'):
                if r.get(m): add(d,'acct:'+r['platform']+'/'+r['account'],'engagement','POST-LOG',r['post_url'],m,r[m])
# ---- RevenueCat v2 overview (snapshot, today only)
def rc():
    e=dict(l.strip().split('=',1) for l in open(S+'/revenuecat.env') if '=' in l)
    try:
        o=json.load(urllib.request.urlopen(urllib.request.Request(f"https://api.revenuecat.com/v2/projects/{e['REVENUECAT_PROJECT_ID']}/metrics/overview",headers={'Authorization':'Bearer '+e['RC_API_KEY']}),timeout=60))
        for m in o.get('metrics',[]): add(today,'RevenueCat project','revenue','RevenueCat',m.get('id'),m.get('name'),m.get('value'),m.get('unit',''))
    except Exception as x: gaps.append('RevenueCat overview: '+str(x)[:60])
# ---- connector pulls (PostHog taps by utm/ct, Stripe, X) dropped as JSON rows by the routine
def pulls():
    for f in sorted(os.listdir(D+'/connector-pulls')) if os.path.isdir(D+'/connector-pulls') else []:
        for r in json.load(open(D+'/connector-pulls/'+f)):
            if start<=datetime.date.fromisoformat(r['date'][:10])<=end: rows.append({**dict(note=''),**r,'date':r['date'][:10]})
# ---- CHANGES.csv: auto from BOARD.md + git merges (dedup); other loops append manually
NOISE=r'coordinator|チーム収益ループ|team revenue loop|hourly status|日次レポート|受託=|提案|Reason inbox|Reason受信箱|LM Cloud|REASSIGN|#agents-hq|追記\)|終了扱い|審査提出をhome|Reporter｜/open|runbook|ループ引き継ぎ|実行中|新着0|seo_daily'
def changes():
    p=D+'/CHANGES.csv'; old=list(csv.DictReader(open(p))) if os.path.exists(p) else []
    seen={(r['date_jst'],r['description']) for r in old}; new=[]
    rj=D+'/CHANGES-REJECTED.csv'  # rows a cleanup dropped; never re-import them
    if os.path.exists(rj): seen|={(r['date_jst'],r['description']) for r in csv.DictReader(open(rj))}
    kw={'release':r'リリース|release|審査通過|配信開始|販売開始','pricing':r'価格|pricing|トライアル|trial|買い切り','paywall':'paywall|ペイウォール','onboarding':'onboarding|オンボーディング','ASO':'ASO|スクショ|キーワード','SEO':r'SEO|サイトマップ|sitemap|title','listing':r'出品|listing','channel':r'新チャネル|アカウント開設|停止|再開'}
    for l in open('/workspace/team/BOARD.md',encoding='utf-8',errors='ignore'):
        m=re.search(r'(2026-\d\d-\d\d)[ T]?(\d\d:\d\d)?',l)
        if not m or not re.search(r'done|完了|マージ|merged|公開|販売開始',l): continue
        if re.search(NOISE,l): continue
        for t,rx in kw.items():
            if re.search(rx,l,re.I):
                prod=next((x for x in['Anicca','Life Manager','Capafy','Honne','Sleep Reset','LINE','PromptBase','ebook','CHERIE'] if x.lower() in l.lower()),'?')
                new.append(dict(date_jst=m.group(1)+' '+(m.group(2) or ''),product=prod,type=t,description=l.strip()[:160],source='BOARD.md')); break
    for repo in['/workspace/life-manager','/workspace/anicca','/workspace/repos/life-manager','/workspace/repos/anicca']:
        if os.path.isdir(repo+'/.git'):
            out=subprocess.run(['git','-C',repo,'log','--merges','--since=30 days ago','--date=format-local:%Y-%m-%d %H:%M','--pretty=%ad\t%s'],capture_output=True,text=True,env={**os.environ,'TZ':'Asia/Tokyo'}).stdout
            for ln in out.splitlines():
                d_,s_=ln.split('\t',1); new.append(dict(date_jst=d_,product=os.path.basename(repo),type='release',description=s_[:160],source='git merge '+os.path.basename(repo)))
    add_=[r for r in new if (r['date_jst'],r['description']) not in seen]
    with open(p,'a' if old else 'w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=['date_jst','product','type','description','source'])
        if not old: w.writeheader()
        w.writerows(add_)
    return old+add_
for fn in(asc,postiz,postlog,rc,pulls):
    try: fn()
    except Exception as x: gaps.append(fn.__name__+': '+str(x)[:80])
chg=changes()
out=f'{D}/e2e-{today}.csv'
with open(out,'w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['date','product','layer','source','key','metric','value','note']); w.writeheader(); w.writerows(rows)
# ---- summary
def tot(layer,metric=None,prod=None,ds=None):
    s=0
    for r in rows:
        if r['layer']==layer and (metric is None or r['metric']==metric) and (prod is None or prod in r['product']) and (ds is None or r['date'] in ds):
            try: s+=float(r['value'] or 0)
            except: pass
    return round(s,2)
y=str(today-datetime.timedelta(1)); wk=[str(today-datetime.timedelta(n)) for n in range(1,8)]
L=[f'# E2E 投稿→収益 ({start}〜{end}, 生成 {datetime.datetime.now(JST):%Y-%m-%d %H:%M} JST)','','正直な前提: タップ→インストールを投稿単位で結ぶ ct/utm はまだ無い。下の投稿↔インストールは**相関（同時期）であって帰属ではない**。','',
   '## 鎖（アプリ別, ASC実数）','ASCは前日分が翌日JST午後に出るため、朝の実行では「昨日」が0/未公開になる。','| 製品 | 新規DL 昨日 | 新規DL 7日 | 課金件数 7日 | 収益(proceeds) 7日 |','|---|---|---|---|---|']
apps=sorted({r['product'] for r in rows if r['source']=='ASC' and r['product']!='ALL'})
for a in apps: L.append(f"| {a} | {tot('installs','new_downloads',a,[y])} | {tot('installs','new_downloads',a,wk)} | {tot('paid',None,a,wk)} | {tot('revenue',None,a,wk)} |")
L+=['','## 投稿・エンゲージメント（アカウント別 7日）','| アカウント | 投稿 | 指標合計 |','|---|---|---|']
accs=sorted({r['product'] for r in rows if r['product'].startswith('acct:')})
for a in accs:
    em=collections.Counter()
    for r in rows:
        if r['product']==a and r['layer']=='engagement' and r['date'] in wk:
            try: em[r['metric']]+=float(r['value'] or 0)
            except: pass
    L.append(f"| {a[5:]} | {sum(1 for r in rows if r['product']==a and r['layer']=='post' and r['date'] in wk)} | {', '.join(f'{k}={int(v)}' for k,v in em.most_common(5))} |")
L+=['','## タップ（PostHog utm/ct, connector-pulls）']
tp=[r for r in rows if r['layer']=='taps']
L+=[f"- {r['date']} {r['key']} {r['metric']}={r['value']} {r['note']}" for r in sorted(tp,key=lambda r:-float(r['value'] or 0))[:15]] or ['- データ無し = GAP']
L+=['','## 変更→前後比較（before/after 比較であり証明ではない; Anicca新規DL）','| 日時 | 製品 | 種別 | 内容 | 前7日DL | 後DL(〜7日) |','|---|---|---|---|---|---|']
for c in sorted([c for c in chg if c['source']=='BOARD.md'],key=lambda c:c['date_jst'])[-20:]+sorted([c for c in chg if c['source']!='BOARD.md'],key=lambda c:c['date_jst'])[-5:]:
    try: cd=datetime.date.fromisoformat(c['date_jst'][:10])
    except: continue
    b=[str(cd-datetime.timedelta(n)) for n in range(1,8)]; a_=[str(cd+datetime.timedelta(n)) for n in range(0,7) if cd+datetime.timedelta(n)<today]
    L.append(f"| {c['date_jst']} | {c['product']} | {c['type']} | {c['description'][:70]} | {tot('installs','new_downloads','Anicca',b)} | {tot('installs','new_downloads','Anicca',a_)} ({len(a_)}日) |")
L+=['','※前日比は範囲内データのみ。範囲外は空=0扱いになるので 30日で回すと正確（`e2e.py 開始 終了`）。','','## GAP']+[f'- {g}' for g in gaps]
open(D+'/E2E.md','w').write('\n'.join(L)+'\n'); print(out, len(rows),'rows', len(chg),'changes', 'gaps:',gaps)
