"""English one-screen summary for /open (成田さん 2026-11-02). Every figure comes from cfo/revenue_facts.py,
finance/REVENUE-BY-SOURCE.csv, metrics/*.json, cfo/notices.csv; missing = None (page shows 'no data')."""
import csv, json, sys, datetime as dt
T = '/workspace/team'; sys.path.insert(0, f'{T}/cfo')
import revenue_facts as RF, fx_basis as FB
TYPE = {'Coconala': 'Contract work', 'Upwork': 'Contract work', 'Lancers': 'Contract work', 'CrowdWorks': 'Contract work', 'Mercor': 'Contract work',
        'Fiverr': 'Contract work', 'Contra': 'Contract work', 'Guru': 'Contract work', 'Truelancer': 'Contract work', 'SKIMA': 'Contract work',
        'Freelancer.com': 'Contract work', 'Malt': 'Contract work', 'Workana': 'Contract work', 'Alignerr': 'Contract work',
        'App Store (RevenueCat)': 'iOS apps', 'Stripe': 'Web payments', 'x402 (Base USDC)': 'API (crypto)', 'Apify': 'API marketplace', 'RapidAPI': 'API marketplace',
        'Capafy': 'AI skill marketplace', 'PromptBase': 'Digital marketplace', 'LINE Creators Market': 'Digital marketplace',
        'note / Substack': 'Digital marketplace', 'Whop / Gumroad': 'Digital marketplace'}
NAME = {'App Store (RevenueCat)': 'App Store (iOS)', 'x402 (Base USDC)': 'x402 (USDC on Base)', 'LINE Creators Market': 'LINE Stickers'}
def j(p):
    try: return json.load(open(p))
    except Exception: return None
def r2(v): return None if v is None else (round(v + 0.0, 3) if 0 < abs(v) < 0.01 else round(v + 0.0, 2))
def summary(ym, lm):
    rows = RF.rows(); csvrows = list(csv.DictReader(open(f'{T}/finance/REVENUE-BY-SOURCE.csv', encoding='utf-8')))
    P = {}
    def p(name):
        return P.setdefault(name, dict(platform=NAME.get(name, name), type=TYPE.get(name, 'Other'), this_month=0.0, last_month=0.0, all_time=0.0, pending=0.0, status='', note=''))
    for r in rows:
        x = p(r['platform']); x['all_time'] += r['usd']
        if r['date'][:7] == ym: x['this_month'] += r['usd']
        if r['date'][:7] == lm: x['last_month'] += r['usd']
        if r['status'] != 'paid': x['pending'] += r['usd']
    # App Store lifetime gross (RevenueCat all-time rows, Oct 2026 = 0 per the row source)
    for r in csvrows:
        if r['platform'] == 'App Store (RevenueCat)' and 'all-time' in (r['status'] or '') and r['amount_jpy']:
            u, _ = FB.usd_of(dict(amount=float(r['amount_jpy']), currency='JPY'), r['date']); x = p(r['platform'])
            x['all_time'] += u; x['note'] = 'lifetime gross from RevenueCat'
    rc = j(f'{T}/metrics/revenuecat-all-projects.json') or {}
    a = p('App Store (RevenueCat)'); a['this_month'] = None
    a['note'] = f"lifetime gross (RevenueCat); {sum(1 for q in rc.get('projects', []) if q.get('active_subscriptions'))} apps with paying subs"
    a['last_month'] = 0.0  # RevenueCat rows: 'Oct 2026 = ¥0'
    # Capafy: order notices without payout -> pending, not revenue
    cp = p('Capafy'); cp['this_month'] = 0.0; cp['last_month'] = 0.0
    try:
        n = [r for r in csv.DictReader(open(f'{T}/cfo/notices.csv', encoding='utf-8')) if r['source'] == 'capafy' and r['amount_usd']]
        cp['pending'] = r2(sum(float(r['amount_usd']) for r in n)); cp['note'] = f"{len(n)} orders (gross), payout not received yet"
    except Exception: cp['note'] = 'no data'
    ap = j(f'{T}/metrics/apify-latest.json') or {}
    x = p('Apify'); x.update(this_month=None, last_month=None, all_time=None,
        note=f"{ap.get('users_total','no data')} users, {ap.get('runs_total','no data')} runs; paid pricing starts 2026-11-16; earnings unknown (source error)")
    ra = j(f'{T}/metrics/rapidapi-latest.json') or {}
    x = p('RapidAPI'); x.update(this_month=None, last_month=None, all_time=None,
        note=f"App Store Top Charts JP & Global API; subscribers {ra.get('subscribers','unknown (source error)')}, calls {ra.get('calls_total','unknown (source error)')}; earnings unknown (source error)")
    seen = set(P)
    for r in csvrows:
        pl = r['platform']
        if pl in seen or pl in ('—', 'Others') or pl not in TYPE: continue
        seen.add(pl); y = p(pl); y.update(this_month=None, last_month=None, all_time=None, note='no revenue recorded')
    out = []
    for k, x in P.items():
        for f in ('this_month', 'last_month', 'all_time', 'pending'): x[f] = r2(x[f])
        x['status'] = 'pending payout' if x['pending'] and x['pending'] > 0 else ('paid' if x['all_time'] else ('—'))
        out.append(x)
    out.sort(key=lambda x: (-(x['all_time'] or 0), x['platform']))
    # monthly trend, stacked by platform (confirmed rows only)
    months = sorted({r['date'][:7] for r in rows})
    m0 = months[0]; y0, mo0 = map(int, m0.split('-')); allm = []
    while f'{y0}-{mo0:02d}' <= ym:
        allm.append(f'{y0}-{mo0:02d}'); mo0 += 1
        if mo0 > 12: y0, mo0 = y0 + 1, 1
    trend = []
    for m in allm:
        seg = {}
        for r in rows:
            if r['date'][:7] == m: seg[NAME.get(r['platform'], r['platform'])] = r2(seg.get(NAME.get(r['platform'], r['platform']), 0) + r['usd'])
        trend.append(dict(month=m, total=RF.month(m)['usd'], by_platform=seg))
    # products
    prod = {}
    for r in rows:
        src = next((c for c in csvrows if c['date'] == r['date'] and c['platform'] == r['platform']), {})
        k = src.get('product') or r['platform']; k = 'Web subscriptions (product not labelled)' if r['platform'] == 'Stripe' else k
        z = prod.setdefault(k, dict(product=k, platform=NAME.get(r['platform'], r['platform']), all_time=0.0, this_month=0.0))
        z['all_time'] += r['usd']; z['this_month'] += r['usd'] if r['date'][:7] == ym else 0
    for r in csvrows:
        if r['platform'] == 'App Store (RevenueCat)' and 'all-time' in (r['status'] or '') and r['amount_jpy']:
            u, _ = FB.usd_of(dict(amount=float(r['amount_jpy']), currency='JPY'), r['date'])
            name = 'Anicca (iOS)' if 'Anicca' in r['product'] else r['product'] + ' (iOS)'
            prod[name] = dict(product=name, platform='App Store (iOS)', all_time=u, this_month=None)
    prod['Capafy skills'] = dict(product='Capafy skills', platform='Capafy', all_time=0.0, this_month=0.0, note=f"${cp['pending']} pending payout")
    prod['Apify actor'] = dict(product='Apify actor (S7JAoTNiztat9Qwuq)', platform='Apify', all_time=None, this_month=None, note='pricing starts 2026-11-16')
    pl = sorted(prod.values(), key=lambda z: -(z['all_time'] or 0))
    for z in pl:
        z['all_time'] = r2(z['all_time']); z['this_month'] = r2(z['this_month'])
    return dict(platforms=out, trend=trend, products=pl, mrr_split={k: v for k, v in ((j(f'{T}/metrics/snapshots/latest.json') or {}).get('mrr') or {}).items() if isinstance(v, (int, float))})
