"""Synthetic toy re-creation inspired by Li, Mintz, Carpenter, Buman (arXiv:2511.02944).
ALL DATA ARE SYNTHETIC. Not a reproduction of the paper's ROGUE-TS; a small stationary-TS vs clipped-TS check
under habituation (effect shrinks when nudged) and recovery (effect returns when rested)."""
import numpy as np, json
P0, E0, DECAY, RECOVER = 0.30, 0.20, 0.80, 0.15   # base prob, max nudge effect, habituation, recovery
T, N, SIMS = 60, 40, 200                          # decision points/user, users/trial, simulated trials

def run_user(policy, rng, lo=0.0, hi=1.0):
    h=1.0; a_s=np.ones(2); b_s=np.ones(2); rew=0; ipw=[]
    for t in range(T):
        if policy=='always': p=1.0
        elif policy=='mrt50': p=0.5
        else:
            p=float(np.mean(rng.beta(a_s[1],b_s[1],200)>rng.beta(a_s[0],b_s[0],200)))
            p=min(max(p,lo),hi)
        a=int(rng.random()<p)
        y=int(rng.random()< P0 + a*E0*h)
        rew+=y; a_s[a]+=y; b_s[a]+=1-y
        if p>0 and p<1: ipw.append(y*(a/p-(1-a)/(1-p)))   # IPW estimate of excursion effect
        h = h*DECAY if a else h+RECOVER*(1-h)
    return rew, (np.mean(ipw) if ipw else np.nan)

def trial(policy, rng, **kw):
    r=[run_user(policy,rng,**kw) for _ in range(N)]
    rew=np.mean([x[0] for x in r]); eff=np.array([x[1] for x in r]); eff=eff[~np.isnan(eff)]
    # two-sided one-sample t-test, df=N-1=39, critical |t|=2.0227 (alpha=0.05)
    pval=(0.0 if abs(eff.mean()/(eff.std(ddof=1)/np.sqrt(len(eff))))>2.0227 else 1.0) if len(eff)==N else np.nan
    return rew, pval, (float(np.mean(eff)) if len(eff) else np.nan)

rng=np.random.default_rng(20261031); out={}
for name,pol,kw in [('always_send','always',{}),('mrt_p0.5','mrt50',{}),('ts_unclipped','ts',{}),('ts_clipped_0.2_0.8','ts',dict(lo=0.2,hi=0.8))]:
    res=[trial(pol,rng,**kw) for _ in range(SIMS)]
    rw=np.array([x[0] for x in res]); pv=np.array([x[1] for x in res]); ef=np.array([x[2] for x in res])
    out[name]=dict(mean_successes_per_user=round(float(rw.mean()),2),sd=round(float(rw.std()),2),
        power_p_lt_005=None if np.all(np.isnan(pv)) else round(float(np.mean(pv[~np.isnan(pv)]<0.05)),3),
        mean_ipw_effect=None if np.all(np.isnan(ef)) else round(float(np.nanmean(ef)),3))
out['params']=dict(P0=P0,E0=E0,DECAY=DECAY,RECOVER=RECOVER,T=T,N=N,SIMS=SIMS,seed=20261031,data='synthetic')
print(json.dumps(out,indent=1))
