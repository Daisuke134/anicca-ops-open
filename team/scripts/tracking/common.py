import csv,os,datetime,json
M="/workspace/team/metrics"; S="/workspace/.secrets"
def now(): return datetime.datetime.now().strftime("%Y-%m-%d %H:%M JST")
def upsert(path,fields,rows,key):
    """Idempotent: rows keyed by `key` cols replace earlier rows with same key."""
    old=[]
    if os.path.exists(path): old=list(csv.DictReader(open(path)))
    k=lambda r:tuple(r.get(c,"") for c in key)
    new={k(r):r for r in rows}
    out=[r for r in old if k(r) not in new]+list(new.values())
    with open(path,"w",newline="") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore"); w.writeheader(); w.writerows(out)
    return len(rows)
def summary(section,data):
    p=f"{M}/tracking-summary.json"; d=json.load(open(p)) if os.path.exists(p) else {}
    d[section]=data; d["updated_at"]=now(); json.dump(d,open(p,"w"),ensure_ascii=False,indent=1)
def err(e): return f"unknown (source error: {type(e).__name__}: {str(e)[:160]})"
