#!/usr/bin/env python3
from pathlib import Path
import sys
p = Path(sys.argv[1] if len(sys.argv) > 1 else 'apps/landing/public/open/index.html')
html = p.read_text()
if 'id="card-store-funnel"' in html and 'function renderStoreFunnel' in html:
    print('index already has store funnel card')
    raise SystemExit(0)

FUNNEL_CARD = '''<div class="c" id="card-store-funnel"><h2>Store funnel, six iOS apps <span class="scope ">APPS · APP STORE + REVENUECAT</span></h2>
<div class="m" id="store-funnel-meta">Loading…</div>
<div style="overflow-x:auto"><table class="asc-apps" id="store-funnel-table" style="margin-top:6px"></table></div>
<div class="m" id="store-funnel-notes" style="margin-top:8px"></div>
</div>
'''

inserted = False
for needle in [
    '<section class="grpwrap" id="grp-apps">\n<div class="grp">Apps <small>App Store · subscriptions</small></div>\n',
    '<section class="grpwrap" id="grp-apps">\n<div class="grp">Apps <small>App Store · subscriptions</small></div>',
    'id="grp-apps">',
]:
    if needle in html:
        html = html.replace(needle, needle + '\n' + FUNNEL_CARD, 1)
        inserted = True
        break
if not inserted:
    raise SystemExit('grp-apps not found')

old = "['status','card-team','card-apps','card-anicca-product-analytics','card-soc','card-svw','card-rank'].forEach(id=>$(id).style.display='');"
new = "['status','card-team','card-store-funnel','card-apps','card-anicca-product-analytics','card-soc','card-svw','card-rank'].forEach(id=>$(id).style.display='');"
if old in html:
    html = html.replace(old, new, 1)
else:
    print('display-reset list not in expected shape; card will still render')

JS = r'''
 function renderStoreFunnel(d){
  const root=$('store-funnel-table'), meta=$('store-funnel-meta'), notes=$('store-funnel-notes');
  if(!root)return;
  const F=d.store_funnel;
  const n=v=>v==null||v===''?'<span class="m">not reported</span>':(typeof v==='number'?Number(v).toLocaleString('en-US'):esc(String(v)));
  const money=v=>v==null?'<span class="m">not reported</span>':U(Number(v));
  const pct=v=>v==null?'<span class="m">n/a</span>':`${Number(v).toLocaleString('en-US')}%`;
  if(!F||!Array.isArray(F.apps)||!F.apps.length){
    if(meta)meta.textContent='End-to-end store funnel has not been written into this snapshot yet. App Store impressions, page views and first-time downloads still appear in the table below, and RevenueCat stock metrics stay in the RevenueCat section.';
    root.innerHTML='';
    if(notes)notes.textContent='';
    return;
  }
  if(meta)meta.innerHTML=`Measured ${esc(F.observed_at||'')} · App Store window ${esc(F.windows?.asc?.period||'')} · RevenueCat window ${esc(F.windows?.revenuecat?.period||'')}. First-time downloads are Apple units. RevenueCat new customers are not installs.`;
  root.innerHTML='<tr><th>App</th><th class="r">Impressions</th><th class="r">Page views</th><th class="r">First-time downloads</th><th class="r">Trial starts (28d)</th><th class="r">Active trials</th><th class="r">Paid subs (stock)</th><th class="r">MRR</th><th class="r">Proceeds (28d)</th><th class="r">Churn (last complete)</th></tr>'+F.apps.map(app=>{
    const A=app.asc||{}, R=app.revenuecat||{};
    const churn=R.churn_rate_latest_complete_pct==null?pct(null):(pct(R.churn_rate_latest_complete_pct)+(R.churned_actives_latest_complete!=null?`<div class="m" style="font-size:10px">${n(R.churned_actives_latest_complete)} churned</div>`:''));
    return `<tr><td><b>${esc(app.app)}</b><div class="m" style="font-size:10px">${A.status==='measured'?'App Store measured':esc(A.note||'App Store not in this snapshot')}</div></td><td class="r">${n(A.impressions)}</td><td class="r">${n(A.page_views)}</td><td class="r">${n(A.first_time_downloads)}</td><td class="r">${n(R.trial_starts_28d)}</td><td class="r">${n(R.active_trials)}</td><td class="r">${n(R.active_subscriptions)}</td><td class="r">${money(R.mrr_usd)}</td><td class="r">${money(R.revenue_28d_usd)}</td><td class="r">${churn}${R.churn_note?`<div class="m" style="font-size:10px">${esc(R.churn_note)}</div>`:''}</td></tr>`;
  }).join('');
  if(notes)notes.innerHTML=(F.notes||[]).map(x=>esc(x)).join(' ');
 }
'''

if 'const loadData=()=>fetch(' not in html:
    raise SystemExit('loadData not found')
html = html.replace('const loadData=()=>fetch(', JS + '\nconst loadData=()=>fetch(', 1)

old_call = ' renderAniccaProductAnalytics(d.product_analytics?.anicca_ios);'
new_call = ' renderAniccaProductAnalytics(d.product_analytics?.anicca_ios);\n renderStoreFunnel(d);'
if old_call in html:
    html = html.replace(old_call, new_call, 1)
elif 'renderStoreFunnel(d);' not in html:
    raise SystemExit('could not hook renderStoreFunnel into loadData')

if 'id="card-store-funnel"' not in html or 'function renderStoreFunnel' not in html:
    raise SystemExit('patch failed')
p.write_text(html)
print('patched', p)
