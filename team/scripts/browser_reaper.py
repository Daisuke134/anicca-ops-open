#!/usr/bin/env python3
"""Box browser reaper. Safe for other agents' live sessions.
Default = report only. --apply does:
 1. close DUPLICATE page tabs (same scheme+host+path) in each CDP browser, keeping the most recent one;
 2. kill chrome/headless/playwright roots whose parent is PID 1 or gone AND older than 2h AND whose DISPLAY has no Xvfb.
Never touches a browser's last tab, never kills a browser that still has a live Xvfb display.
Log: /workspace/team/health/browser-reaper.log"""
import json,os,re,subprocess,sys,time,urllib.request,urllib.parse as U
APPLY='--apply' in sys.argv; LOG='/workspace/team/health/browser-reaper.log'
def log(m):
    l=time.strftime('%Y-%m-%d %H:%M JST ')+m; print(l); open(LOG,'a').write(l+'\n')
def ps():
    out=subprocess.run(['ps','-eo','pid=,ppid=,etimes=,rss=,args='],capture_output=True,text=True).stdout
    for ln in out.splitlines():
        p=ln.split(None,4)
        if len(p)==5: yield int(p[0]),int(p[1]),int(p[2]),int(p[3]),p[4]
procs=list(ps()); pids={p[0] for p in procs}
displays={m.group(1) for *_,a in procs for m in [re.match(r'Xvfb (:\d+)',a)] if m}
closed=killed=0; done=set()
for pid,ppid,et,rss,a in procs:
    exe=a.split()[0]
    if not re.search(r'(chrome|chromium|headless_shell)$',exe) or 'type=' in a: continue
    m=re.search(r'remote-debugging-port=(\d+)',a)
    if m:
        port=m.group(1)
        if port in done: continue
        done.add(port)
        try: tabs=[t for t in json.load(urllib.request.urlopen(f'http://127.0.0.1:{port}/json/list',timeout=3)) if t['type']=='page']
        except Exception as e: log(f'port {port} unreadable {type(e).__name__}'); continue
        seen=set(); dup=[]
        for t in tabs:
            u=U.urlparse(t['url']); k=(u.scheme,u.netloc,u.path)
            (dup.append(t) if k in seen else seen.add(k))
        log(f'browser pid={pid} port={port} pages={len(tabs)} duplicates={len(dup)}')
        if APPLY:
            for t in dup:
                try: urllib.request.urlopen(f'http://127.0.0.1:{port}/json/close/{t["id"]}',timeout=3); closed+=1
                except Exception: pass
    disp=re.search(r'DISPLAY=(:\d+)',open(f'/proc/{pid}/environ','rb').read().decode(errors='ignore').replace('\0',' ')) if os.path.exists(f'/proc/{pid}/environ') else None
    orphan=(ppid==1 or ppid not in pids) and et>7200 and (disp is None or disp.group(1) not in displays)
    if orphan and ('headless' in a or 'playwright' in a or 'chrome' in a.split()[0]):
        log(f'orphan chrome pid={pid} age={et//60}m rss={rss//1024}MB')
        if APPLY:
            try: os.kill(pid,15); killed+=1
            except Exception: pass
av=int(open('/proc/meminfo').read().split('MemAvailable:')[1].split()[0])//1024
log(f'{"APPLY" if APPLY else "DRYRUN"} closed_dup_tabs={closed} killed_orphans={killed} mem_available={av}MB')
