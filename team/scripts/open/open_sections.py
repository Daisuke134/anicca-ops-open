"""Public /open sections: businesses (real status, no fake $0), contract work by platform, team.
Counts come only from explicit records; unknown = None ('not tracked yet')."""
import csv, re, os, datetime as dt
PLATFORMS=[ # (key, label, owner, regex for BOARD lines)
 ('coconala','Coconala','dr eggbot',r'ココナラ|coconala'),
 ('lancers','Lancers','dr eggbot',r'ランサーズ|lancers'),
 ('upwork','Upwork','dr eggbot',r'upwork'),
 ('skima','SKIMA','dr eggbot',r'skima|スキマ'),
 ('crowdworks','CrowdWorks','Dots',r'クラウドワークス|crowdworks'),
 ('contra','Contra','Dots',r'contra\b'),
 ('freelancer','Freelancer.com','Dots',r'freelancer(\.com)?\b'),
 ('malt','Malt','Dots',r'\bmalt\b'),
 ('workana','Workana','Dots',r'workana'),
 ('guru','Guru','Dots',r'\bguru\b'),
 ('mercor','Mercor','Fucker',r'mercor'),
 ('fiverr','Fiverr','Fucker',r'fiverr'),
 ('capafy','Capafy (our agents)','Fucker',r'capafy'),
 ('promptbase','PromptBase (our prompts)','Fucker',r'promptbase'),
]
STATUS={'coconala':'active; trial order in progress (10/30)','lancers':'active','upwork':'contract active (Labelbox, 10/30); ID check due 11/6','skima':'status not tracked yet','crowdworks':'active; 3 client replies waiting (login needed)','contra':'status not tracked yet','freelancer':'status not tracked yet','malt':'status not tracked yet','workana':'account in review (10/26)','guru':'signup retry assigned to Dots','mercor':'applied, awaiting offers','fiverr':'status not tracked yet','capafy':'71 agents live','promptbase':'live, no sales yet'}
SELL_ONLY={'capafy','promptbase'}  # marketplaces where we list products; no applications
AUTHORS=[('参謀','参謀'),('dr eggbot','dr eggbot'),('fucker','Fucker'),('dots','Dots'),('muse','Muse'),('codex','Codex')]
NEW=re.compile(r'^[^、。／;]{0,30}?新規(?:応募|提案)?\s*(\d+)\s*件(?:の)?(?:提案|応募)?(?:完了|確定)')
def _date(l):
    m=re.match(r'^- (\d{4}-\d{2}-\d{2})',l); return dt.date.fromisoformat(m.group(1)) if m else None
def applications(T,today):
    """dict platform -> {date: count}; ledger metrics/applications.csv wins per (platform,date)."""
    days=[today-dt.timedelta(days=i) for i in range(6,-1,-1)]
    board={}; 
    try: lines=open(f'{T}/BOARD.md',encoding='utf-8').read().splitlines()
    except Exception: lines=[]
    seen=set()
    for l in lines:
        d=_date(l)
        if not d or d not in days or l in seen: continue
        seen.add(l); low=l.lower()
        for key,_,_,rx in PLATFORMS:
            if key in SELL_ONLY: continue
            for pm in re.finditer(rx,low):
                seg=l[pm.start():pm.start()+60]
                m=NEW.search(seg)
                if m:
                    board.setdefault(key,{}).setdefault(d,0); board[key][d]+=int(m.group(1)); break
            else:
                if key=='mercor' and re.search(r'｜\s*mercor\s*｜\s*applied',low): board.setdefault(key,{}).setdefault(d,0); board[key][d]+=1
    led={}
    p=f'{T}/metrics/applications.csv'
    if os.path.exists(p):
        for r in csv.DictReader(open(p,encoding='utf-8')):
            try: d=dt.date.fromisoformat(r['date'][:10]); k=r['platform'].strip().lower(); c=int(r['count'])
            except Exception: continue
            if d in days: led.setdefault(k,{}).setdefault(d,0); led[k][d]+=c
    out={}
    for k,_,_,_ in PLATFORMS:
        m=dict(board.get(k,{})); m.update(led.get(k,{}))
        out[k]=m
    return days,out
def revenue_by_platform(T):
    tot={}; seen=set()
    try:
        for r in csv.DictReader(open(f'{T}/cfo/history.csv',encoding='utf-8')):
            if r['kind']!='revenue': continue
            sig=(r['date'],r['source'],r['amount_usd'])
            if sig in seen: continue  # exact duplicate rows in history.csv
            seen.add(sig); src=r['source'].split(':')[0]
            tot[src]=tot.get(src,0)+float(r['amount_usd'] or 0)
    except Exception: pass
    return tot
def contract_work(T,today,x):
    days,apps=applications(T,today); rev=revenue_by_platform(T)
    rows=[]; tday=0; t7=0
    for key,label,owner,_ in PLATFORMS:
        a=apps[key]; sell=key in SELL_ONLY
        by={d.isoformat():a.get(d,0) for d in days} if (a and not sell) else None
        at=a.get(today,0) if by is not None else None
        if by: tday+=at; t7+=sum(by.values())
        r=dict(platform=label,owner=owner,applications_today=at,applications_by_day=by,
               applications_7d=sum(by.values()) if by else None,status=STATUS.get(key,''))
        if key=='coconala': r['revenue_lifetime_usd']=round(rev.get('coconala',0),2)
        elif key=='capafy' and x.get('capafy_lifetime') is not None: r['revenue_lifetime_usd']=x['capafy_lifetime']
        else: r['revenue_lifetime_usd']=None
        if sell: r['note']='we list our own products here; no applications'+(f'; {x["capafy_installs"]:,} installs' if key=='capafy' and x.get('capafy_installs') else '')+(f'; {x["pb"]} views in 7 days' if key=='promptbase' and x.get('pb') is not None else '')
        elif by is None: r['note']='no applications recorded in the last 7 days (not tracked yet)'
        rows.append(r)
    return dict(applications_today=tday,applications_7d=t7,days=[d.isoformat() for d in days],platforms=rows,
        source='Counted from dated team-board entries that state how many proposals were sent, plus metrics/applications.csv. Applications are proposals, not orders.')
def manager_lab(T):
    import json
    d=f'{T}/research/manager-lab'
    try: arts=json.load(open(f'{d}/manifest.json')).get('articles',[])
    except Exception: arts=[]
    exps=[e for e in os.listdir(d) if os.path.isdir(f'{d}/{e}') and re.match(r'\d{4}-\d{2}-\d{2}-',e)] if os.path.isdir(d) else []
    arts=sorted(arts,key=lambda a:a.get('date',''))
    return dict(articles=len(arts),experiments=len(exps),latest=arts[-1]['url'] if arts else None)

def build_sections(T,today,now,x):
    ml=manager_lab(T)
    rv=x['rev_by_src']; xf=x['xf']
    def money(v): return round(v,2) if v else None   # never publish a meaningless $0
    B=[
     dict(name='Contract work (freelance platforms)',owner='dr eggbot, Dots, Fucker',revenue_mtd=money(rv.get('coconala',0)),mrr=None,metric='paid Upwork contract (Labelbox) active since 10/30; Coconala trial order in progress',status='live',next='first Upwork payout; more Coconala repeat orders'),
     dict(name='Anicca iOS (affirmation app)',owner='Codex (build), Anicca Marketer (growth)',revenue_mtd=money(rv.get('revenuecat',0)),mrr=x['mrr_anicca'],metric='paying subscribers',metric_value=x['subs'],status='live, update 1.9.6 in review',next='1.9.6 approval'),
     dict(name='Honne family apps (Honne, Thankful, Daily Dhamma, Sleep Reset)',owner='Codex / Fucker',revenue_mtd=None,mrr=x['mrr_honne'],metric='live on the App Store',status='live',next='Honne 1.0.5 release'),
     dict(name='Capafy agents (Clip Map, Hook Lab and others)',owner='Fucker',revenue_mtd=None,revenue_lifetime=x['capafy_lifetime'],mrr=None,metric='installs (cumulative)',metric_value=x['capafy_installs'],status='live; 4 fixed agents resubmitted 10/30, in review',next='paid tier'),
     dict(name='Monk e-book / Anicca Reset',owner='Muse',revenue_mtd=None,mrr=None,metric='social views, 7d (monk + app accounts)',metric_value=x['social_views_7d'],status='live; Whop store created 10/30, listing next',next='first e-book sale'),
     dict(name='AI Monk Factory / Monk Database (web)',owner='参謀',revenue_mtd=None,mrr=None,metric='site pageviews (cumulative)',metric_value=x['site_pv'],status='live',next='search traffic (SEO loop)'),
     dict(name='PromptBase prompts',owner='Fucker',revenue_mtd=None,mrr=None,metric='listing views, 7d',metric_value=x['pb'],status='live, no sales yet',next='first sale'),
     dict(name='LINE stickers',owner='Digital products',revenue_mtd=None,mrr=None,metric='38 sets on sale',status='live, no sales yet',next='first sale'),
     dict(name='Life Manager Cloud',owner='Codex (CTO)',revenue_mtd=None,mrr=None,metric='shipped: aniccaai.com/maritime live; billing in test mode',status='building; no paying users yet',next='first paid signup end to end'),
     dict(name='The Manager (AI that ends suffering)',owner='Codex (Head of Research)',revenue_mtd=None,mrr=None,metric='published research articles / experiments run (team/research/manager-lab)',metric_value=f"{ml['articles']} articles / {ml['experiments']} experiments",research_articles=ml['articles'],experiments_run=ml['experiments'],latest_article_url=ml['latest'],status='research (Manager Lab, daily 09:00 JST)',next='next daily research note'),
     dict(name='Accelerators, hackathons, grants',owner='参謀 / Codex',revenue_mtd=None,mrr=None,metric='accepted: Meta Global AI Developer Hackathon, Vultr Agent Rush; applied: YC Haunted Hacks; in progress: YC W27',status='applying',next='YC W27 due 11/3 12:00 JST; Meta build due 11/5'),
    ]
    try: tl=[l for l in open(f'{T}/BOARD.md',encoding='utf-8').read().splitlines() if today.isoformat() in l[:30]]
    except Exception: tl=[]
    def cnt(*p): return sum(1 for l in tl if any(s.lower() in l.lower() for s in p))
    A=[
     dict(agent='参謀 (CEO)',today='Priorities, delegation, YC W27, this page, SEO writing',platforms='X @diceai0 / @selawmqt, note, Substack, dev.to, Life Manager Bluesky/Mastodon/Tumblr',board_updates_today=cnt('参謀')),
     dict(agent='Codex (CTO, Head of Research)',today='Product builds and releases, Life Manager Cloud, Manager Lab, hackathon PM',platforms='GitHub, App Store Connect',board_updates_today=cnt('codex')),
     dict(agent='Dots (COO)',today='Contract work on its platforms, one new platform signup a day, chasing open items, daily summary',platforms='CrowdWorks, Contra, Freelancer.com, Malt, Workana, Guru',board_updates_today=cnt('dots')),
     dict(agent='Muse (CMO)',today='Monk reels, e-book funnel, Whop store, Naïve push',platforms='Instagram, Threads, TikTok, YouTube, Whop',board_updates_today=cnt('muse (','muse｜','｜muse')),
     dict(agent='dr eggbot',today='Proposals and client work; designs new agents',platforms='Coconala, Lancers, Upwork, SKIMA',board_updates_today=cnt('dr eggbot')),
     dict(agent='Fucker',today='Our own marketplace products: Capafy agents, PromptBase, Mercor/Fiverr',platforms='Capafy, PromptBase, Mercor, Fiverr, dev.to agentworkshop',board_updates_today=cnt('fucker')),
     dict(agent='Anicca Marketer',today='Anicca iOS growth: daily posts, directories, metrics',platforms='TikTok @aniccaaffirmation, Bluesky, Mastodon, Nostr, Telegraph',board_updates_today=cnt('anicca marketer')),
     dict(agent='Muse Relay',today="Turns Muse's winning reels into X / note / TikTok material",platforms='none (hands drafts to account owners)',board_updates_today=cnt('muse relay')),
     dict(agent='Forensic Writing',today='Viral-hook analysis for X (drafts only)',platforms='none (drafts only)',board_updates_today=cnt('forensic')),
     dict(agent='Manus (trial)',today='New external teammate, first trial task starting 10/30',platforms='none yet',board_updates_today=cnt('manus')),
    ]
    return B,A,contract_work(T,today,x)
