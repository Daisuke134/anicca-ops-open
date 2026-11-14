#!/usr/bin/env python3
"""Box port of Mac mini com.anicca.daily-report (automaton wallet/shelter report). Prints a JSON + text snapshot.
Used by the box 'Daily Anicca report' routine; Mac mini copy disabled 2026-10-27."""
import json, urllib.request, datetime
BASE="0xB9dd3B67921B354c656523d6851537988F31DD56"
USDC_HOLDER="0xa3CDd4Ec6b94F01826Aaf90a6d5538A2Aa8C4C21"
AKASH="akash18utu7e2reaa0uazlvju7mv5y4cu24kk95pcs6m"
def rpc(m,p):
    r=urllib.request.Request("https://mainnet.base.org",json.dumps({"jsonrpc":"2.0","id":1,"method":m,"params":p}).encode(),{"Content-Type":"application/json","User-Agent":"anicca"})
    return int(json.load(urllib.request.urlopen(r,timeout=10)).get("result","0x0"),16)
def get(u): return json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"User-Agent":"anicca"}),timeout=15))
out={"at":datetime.datetime.now().strftime("%Y-%m-%d %H:%M JST")}
try: out["base_eth"]=round(rpc("eth_getBalance",[BASE,"latest"])/1e18,6)
except Exception as e: out["base_eth"]=f"err {e}"
try: out["base_usdc"]=round(rpc("eth_call",[{"to":"0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913","data":"0x70a08231"+USDC_HOLDER[2:].lower().rjust(64,"0")},"latest"])/1e6,4)
except Exception as e: out["base_usdc"]=f"err {e}"
try:
    b=get(f"https://rest.cosmos.directory/akash/cosmos/bank/v1beta1/balances/{AKASH}").get("balances",[])
    out["akash_akt"]=next((int(x["amount"]) for x in b if x["denom"]=="uakt"),0)/1e6
    out["akash_act"]=next((int(x["amount"]) for x in b if x["denom"]=="uact"),0)/1e6
except Exception as e: out["akash"]=f"err {e}"
try:
    d=get(f"https://rest.cosmos.directory/akash/akash/deployment/v1beta4/deployments/list?filters.owner={AKASH}&filters.state=active")
    out["akash_active_deployments"]=len(d.get("deployments",[]))
except Exception as e: out["akash_active_deployments"]=f"err {e}"
print(json.dumps(out,ensure_ascii=False))
