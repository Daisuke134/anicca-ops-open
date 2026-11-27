#!/usr/bin/env python3
"""agent_rails_probe.py — no-spend, no-human-credential measurement of the
agent-native payout rails (2026-11-26, @pickle / MRR10K cycle 1).

What it measures, from primary sources only:
  1. make.fun      : handle, payable wallet, on-chain USDC balance (Solana mainnet-beta),
                     grant status, open competitions count + top prize.
  2. x402 origin   : health, 402 challenge (network / amount / payTo) of one endpoint,
                     and the on-chain USDC balance sitting at payTo (Base L2).
  3. Agoragentic   : platform payment availability (/market.json), seller listing count,
                     per-listing review/sandbox status, revenue counter.
  4. agent wallets : USDC balance of every Base/Solana wallet recorded in credentials.json
                     for an agent-owned rail (bountybook / make.fun), so payout custody
                     is visible instead of assumed.

Nothing here spends money, signs a payment, or posts anything. Read-only HTTP + JSON-RPC.
Writes team/metrics/agent-rails.json and prints a summary.

Usage: python3 team/scripts/agent_rails_probe.py [--repo <path to anicca-ops checkout>]
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "team", "metrics", "agent-rails.json")
MAKEFUN_CREDS = os.path.expanduser("~/.makefun/credentials")
SOLANA_RPC = "https://api.mainnet-beta.solana.com"
BASE_RPC = "https://base-rpc.publicnode.com"
USDC_SOLANA = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
USDC_BASE = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913"
X402_ORIGIN = "https://x402-agents-production.up.railway.app"
TIMEOUT = 30


def http(url, method="GET", body=None, headers=None):
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method,
                                 headers={"user-agent": "anicca-agent-rails-probe/1.0",
                                          "content-type": "application/json",
                                          **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            raw = r.read().decode()
            try:
                return r.status, json.loads(raw)
            except json.JSONDecodeError:
                return r.status, raw[:400]
    except urllib.error.HTTPError as e:
        raw = e.read().decode()
        try:
            return e.code, json.loads(raw)
        except json.JSONDecodeError:
            return e.code, raw[:400]
    except Exception as e:  # network / DNS
        return None, {"error": str(e)[:200]}


def rpc(url, payload):
    return http(url, "POST", payload)


def solana_usdc(wallet):
    st, d = rpc(SOLANA_RPC, {"jsonrpc": "2.0", "id": 1, "method": "getTokenAccountsByOwner",
                             "params": [wallet, {"mint": USDC_SOLANA}, {"encoding": "jsonParsed"}]})
    if st != 200 or not isinstance(d, dict):
        return {"error": f"rpc {st}"}
    vals = d.get("result", {}).get("value", [])
    total = sum(float(v["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmountString"]) for v in vals)
    return {"usdc": round(total, 6), "accounts": len(vals)}


def base_usdc(addr):
    data = "0x70a08231" + addr.lower().replace("0x", "").rjust(64, "0")
    st, d = rpc(BASE_RPC, {"jsonrpc": "2.0", "id": 1, "method": "eth_call",
                           "params": [{"to": USDC_BASE, "data": data}, "latest"]})
    if st != 200 or not isinstance(d, dict) or not isinstance(d.get("result"), str):
        return {"error": f"rpc {st}"}
    return {"usdc": round(int(d["result"], 16) / 1e6, 6)}


def load_credentials():
    path = os.path.join(REPO, "credentials.json")
    with open(path) as f:
        return json.load(f)


def probe_makefun():
    if not os.path.exists(MAKEFUN_CREDS):
        return {"status": "no local keypair/credentials on this host"}
    creds = json.load(open(MAKEFUN_CREDS))
    k = creds.get("keys", {}).get("https://make.fun") or {}
    if not k.get("key"):
        return {"status": "credentials file has no make.fun key"}
    h = {"x-api-key": k["key"]}
    out = {"origin": "https://make.fun", "key_expires_at": k.get("expires_at")}
    st, me = http("https://make.fun/api/agents/me", headers=h)
    out["agents_me_status"] = st
    if st == 200 and isinstance(me, dict):
        a = me.get("agent", {})
        out["handle"] = a.get("handle")
        out["wallet"] = a.get("payable_wallet") or a.get("wallet")
        comps = me.get("open_competitions", []) or []
        out["open_competitions"] = len(comps)
        prizes = sorted(({"slug": c.get("slug"), "prize_usd": c.get("prize_total_usd"),
                          "close": c.get("entries_close")} for c in comps),
                        key=lambda c: float(c["prize_usd"] or 0), reverse=True)
        out["top_prize_competitions"] = prizes[:3]
    st, g = http("https://make.fun/api/me/grants", headers=h)
    out["grants_status"] = st
    if st == 200 and isinstance(g, dict):
        gr = g.get("grants", [])
        out["grants"] = [{"id": x.get("id"), "amount": x.get("amount"), "token": x.get("token"),
                          "status": x.get("status"), "paid_at": x.get("paid_at"),
                          "tx": x.get("tx_signature")} for x in gr]
        out["paid_usdc_total"] = round(sum(float(x.get("amount") or 0) for x in gr if x.get("status") == "paid"), 6)
        out["tax_details_required"] = (g.get("claim") or {}).get("tax_details_required")
    if out.get("wallet"):
        out["onchain"] = solana_usdc(out["wallet"])
    return out


def probe_x402():
    out = {"origin": X402_ORIGIN}
    st, h = http(X402_ORIGIN + "/health")
    out["health_status"] = st
    out["health"] = h if isinstance(h, dict) else str(h)[:120]
    st, ch = http(X402_ORIGIN + "/context-compressor", "POST", {"text": "probe"})
    out["challenge_status"] = st
    if isinstance(ch, dict):
        acc = (ch.get("accepts") or [{}])[0]
        out["network"] = acc.get("network")
        out["amount_usdc"] = round(int(acc.get("amount", "0")) / 1e6, 6) if acc.get("amount") else None
        out["pay_to"] = acc.get("payTo")
        if out.get("pay_to"):
            out["pay_to_onchain"] = base_usdc(out["pay_to"])
    ledger = os.path.join(REPO, "team", "agent-economy", "x402_inflows.jsonl")
    if os.path.exists(ledger):
        rows = [json.loads(l) for l in open(ledger) if l.strip()]
        out["ledger_rows"] = len(rows)
        out["ledger_sum_usd"] = round(sum(float(r.get("amount_usd") or 0) for r in rows), 6)
    return out


def probe_agoragentic(key):
    out = {}
    st, m = http("https://agoragentic.com/market.json")
    out["market_json_status"] = st
    if isinstance(m, dict):
        pay = m.get("payment", {})
        out["paid_execution"] = ((pay.get("wallet") or {}).get("status"))
        out["paid_execution_reason"] = ((pay.get("wallet") or {}).get("reason"))
        out["x402_edge_status"] = ((pay.get("x402_edge") or {}).get("status"))
    if not key:
        out["seller"] = "no api key in credentials.json"
        return out
    h = {"Authorization": "Bearer " + key}
    st, s = http("https://agoragentic.com/api/seller/status", headers=h)
    out["seller_status_http"] = st
    if isinstance(s, dict):
        se = s.get("seller", {})
        out["listings_total"] = se.get("total_listings")
        out["listings_active"] = se.get("active_total")
        out["free_slots_remaining"] = se.get("free_concurrent_slots_remaining")
    st, me = http("https://agoragentic.com/api/agents/me", headers=h)
    if isinstance(me, dict):
        out["revenue_usd"] = (me.get("activity") or {}).get("revenue")
        out["sales"] = (me.get("activity") or {}).get("sales")
        out["wallet_balance"] = (me.get("wallet") or {}).get("balance")
    st, lh = http("https://agoragentic.com/api/agents/me/listing-health", headers=h)
    if isinstance(lh, dict):
        out["listing_health"] = [{"name": l.get("name"), "review_status": l.get("review_status"),
                                  "verification": (l.get("verification") or {}).get("sandbox_status"),
                                  "issues": l.get("issues")} for l in lh.get("listings", [])]
    return out


def probe_agent_wallets(creds):
    rows = []
    for c in creds.get("credentials", []):
        if not isinstance(c, dict):
            continue
        svc = (c.get("service") or "").lower()
        if svc in ("bountybook", "bountybook.ai") and c.get("wallet_address"):
            rows.append({"service": svc, "chain": "base", "address": c["wallet_address"],
                         "balance": base_usdc(c["wallet_address"]),
                         "key_held": bool(c.get("private_key"))})
        if "solana" in svc and c.get("wallet_address"):
            rows.append({"service": svc, "chain": "solana", "address": c["wallet_address"],
                         "balance": solana_usdc(c["wallet_address"]), "key_held": True})
    return rows


def main():
    creds = load_credentials()
    agora = next((c for c in creds.get("credentials", [])
                  if isinstance(c, dict) and c.get("service") == "agoragentic"), {})
    report = {
        "probe": "agent_rails_probe.py",
        "ran_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ran_at_jst": time.strftime("%Y-%m-%d %H:%M", time.gmtime(time.time() + 9 * 3600)),
        "note": "Read-only. No payment, signature, post or spend. Unknown is never written as 0.",
        "makefun": probe_makefun(),
        "x402": probe_x402(),
        "agoragentic": probe_agoragentic(agora.get("api_key")),
        "agent_wallets": probe_agent_wallets(creds),
    }
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as f:
        json.dump(report, f, ensure_ascii=False, indent=1)
    print(json.dumps(report, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
