#!/usr/bin/env python3
"""Per-app iOS daily: RevenueCat v2 charts (revenue, transactions, trials_new, actives_new) per app_id
+ ASC Sales SUMMARY (downloads = product types 1/1F/1T/F1 units, by Title). Upserts metrics/ios-daily.csv."""
import json,urllib.request,urllib.parse,datetime,sys,gzip,io,csv
sys.path.insert(0,"/workspace/team/scripts/tracking"); from common import *
DAYS=int(sys.argv[1]) if len(sys.argv)>1 else 3
dates=[(datetime.date.today()-datetime.timedelta(days=i)).isoformat() for i in range(DAYS,0,-1)]
def rcget(key,path):
    r=urllib.request.Request("https://api.revenuecat.com/v2"+path,headers={"Authorization":"Bearer "+key})
    return json.load(urllib.request.urlopen(r,timeout=40))
env={l.split("=",1)[0]:l.strip().split("=",1)[1].strip('"') for l in open(f"{S}/revenuecat.env") if "=" in l}
targets=[]  # (key,project,app_id,name)
try:
    for a in rcget(env["RC_API_KEY"],f"/projects/{env['REVENUECAT_PROJECT_ID']}/apps")["items"]:
        if a["type"]=="app_store": targets.append((env["RC_API_KEY"],env["REVENUECAT_PROJECT_ID"],a["id"],a["name"]))
except Exception as e: print("RC apps list failed",err(e))
for f,name in [("macmini-revenuecat-thankful-existing-api-v2","Thankful"),("macmini-revenuecat-dhamma-existing-api-v2-ani","Dhamma"),("macmini-revenuecat-sleep-reset-metrics-read-v2","Sleep Reset")]:
    d=json.load(open(f"{S}/{f}")); targets.append((d["api_key"],d["project_id"],d["app_id"],name))
CH={"revenue":("Revenue","rc_revenue_usd"),"trials_new":("New Trials","rc_new_trials"),"actives_new":(None,"rc_new_paid_subs")}
rows=[]; t=now()
for key,proj,app,name in targets:
    vals={d:{} for d in dates}
    for ch,(meas,col) in CH.items():
        q=urllib.parse.urlencode({"resolution":"day","start_date":dates[0],"end_date":dates[-1],"filters":json.dumps([{"name":"app_id","values":[app]}])})
        try:
            j=rcget(key,f"/projects/{proj}/charts/{ch}?{q}"); names=[m["display_name"] for m in j["measures"]]
            mi=names.index(meas) if meas in names else 0
            for v in j["values"]:
                if v["measure"]!=mi or v.get("segment",0) not in (0,): continue
                d=datetime.datetime.fromtimestamp(v["cohort"],datetime.timezone.utc).date().isoformat()
                if d in vals: vals[d][col]=v["value"]
                if ch=="revenue":
                    ti=names.index("Transactions") if "Transactions" in names else None
            if ch=="revenue" and "Transactions" in names:
                ti=names.index("Transactions")
                for v in j["values"]:
                    d=datetime.datetime.fromtimestamp(v["cohort"],datetime.timezone.utc).date().isoformat()
                    if v["measure"]==ti and d in vals: vals[d]["rc_transactions"]=v["value"]
        except Exception as e:
            for d in dates: vals[d][col]=err(e)
    for d in dates:
        rows.append(dict(date=d,app=name,rc_app_id=app,rc_project=proj,**vals[d],asc_downloads="",asc_proceeds="",asc_currency="",read_at=t,source=f"RevenueCat v2 charts project {proj} app_id {app}"))
# ASC
asc={}
try:
    import jwt
    e={l.split("=",1)[0]:l.strip().split("=",1)[1].strip('"') for l in open(f"{S}/asc.env") if "=" in l}
    tok=jwt.encode({"iss":e["ASC_ISSUER_ID"],"iat":int(datetime.datetime.now().timestamp()),"exp":int(datetime.datetime.now().timestamp())+1200,"aud":"appstoreconnect-v1"},open(f"{S}/AuthKey_{e['ASC_KEY_ID']}.p8").read(),algorithm="ES256",headers={"kid":e["ASC_KEY_ID"]})
    for d in dates:
        u=f"https://api.appstoreconnect.apple.com/v1/salesReports?filter[frequency]=DAILY&filter[reportType]=SALES&filter[reportSubType]=SUMMARY&filter[vendorNumber]={e['ASC_VENDOR_NUMBER']}&filter[reportDate]={d}&filter[version]=1_1"
        try:
            raw=urllib.request.urlopen(urllib.request.Request(u,headers={"Authorization":"Bearer "+tok,"Accept":"application/a-gzip"}),timeout=40).read()
            for r in csv.DictReader(io.StringIO(gzip.decompress(raw).decode()),delimiter="\t"):
                a=asc.setdefault((d,r["Title"]),[0,0.0,r["Currency of Proceeds"]])
                if r["Product Type Identifier"] in ("1","1F","1T","F1"): a[0]+=int(r["Units"])
                a[1]+=float(r["Developer Proceeds"])*int(r["Units"])
        except urllib.error.HTTPError as x:
            body=x.read()[:200].decode(errors="ignore")
            asc[(d,"*")]=f"unknown (source error: HTTP {x.code} {'no sales report for this date (Apple: report not available / no sales)' if x.code==404 else body})"
except Exception as x: asc[("*","*")]=err(x)
for (d,title),v in asc.items():
    if isinstance(v,str):
        rows.append(dict(date=d,app="ASC (all apps)",asc_downloads=v,asc_proceeds=v,read_at=t,source="ASC Sales SUMMARY DAILY v1_1"))
    else:
        rows.append(dict(date=d,app=f"ASC: {title}",asc_downloads=v[0],asc_proceeds=round(v[1],2),asc_currency=v[2],read_at=t,source="ASC Sales SUMMARY DAILY v1_1"))
F=["date","app","rc_app_id","rc_project","rc_revenue_usd","rc_transactions","rc_new_trials","rc_new_paid_subs","asc_downloads","asc_proceeds","asc_currency","read_at","source"]
n=upsert(f"{M}/ios-daily.csv",F,rows,["date","app"])
num=lambda x: x if isinstance(x,(int,float)) else None
okd=[d for (d,ti),v in asc.items() if not isinstance(v,str)]
sd=max(okd) if okd else dates[-1]   # latest day Apple has a sales report for
per={}
for r in rows:
    if r["date"]!=sd: continue
    per[r["app"]]={k:r.get(k,"") for k in ("rc_revenue_usd","rc_new_trials","rc_new_paid_subs","asc_downloads","asc_proceeds")}
summary("ios",{"date":sd,"read_at":t,"per_app":per,"source":"RevenueCat v2 charts + ASC Sales"})
print("rows",n); [print(r["date"],r["app"],r.get("rc_revenue_usd"),r.get("rc_new_trials"),r.get("rc_new_paid_subs"),r.get("asc_downloads"),r.get("asc_proceeds")) for r in rows]
