#!/usr/bin/env python3
"""x402scan_register.py — register an x402 origin (or one resource) on x402scan
with SIWX wallet auth. Free (no payment); the read APIs are paid so this never
calls them. Used by team/loops/AGENT-RAILS.md (weekly re-check).

Usage:
  python3 team/scripts/x402scan_register.py --origin https://x402-agents-production.up.railway.app
  python3 team/scripts/x402scan_register.py --url https://host/route

Signs with the Base wallet in credentials.json (service=bountybook). The key is
never printed. Registration is idempotent on the origin side; do not loop it.

Needs: pip package `eth-account`.
"""
import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request

from eth_account import Account
from eth_account.messages import encode_defunct

SCAN = "https://www.x402scan.com"
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def call(path, body, headers=None):
    req = urllib.request.Request(SCAN + path, data=json.dumps(body).encode(),
                                 headers={"content-type": "application/json", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, r.read().decode()
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def wallet():
    creds = json.load(open(os.path.join(REPO, "credentials.json")))["credentials"]
    for c in creds:
        if isinstance(c, dict) and c.get("service") == "bountybook" and c.get("private_key"):
            return c["private_key"]
    sys.exit("no bountybook private_key in credentials.json")


def register(path, payload_key, target, priv):
    """One challenge -> one signature -> one send. Nonce is single-use."""
    st, body = call(path, {payload_key: target})
    if st != 402:
        return st, body
    info = json.loads(body)["extensions"]["sign-in-with-x"]["info"]
    acct = Account.from_key(priv)
    # Chain ID must be the numeric chain id (8453), NOT the CAIP form (eip155:8453).
    msg = (f"{info['domain']} wants you to sign in with your Ethereum account:\n{acct.address}\n\n"
           f"{info['statement']}\n\nURI: {info['uri']}\nVersion: {info['version']}\n"
           f"Chain ID: 8453\nNonce: {info['nonce']}\nIssued At: {info['issuedAt']}\n"
           f"Expiration Time: {info['expirationTime']}")
    sig = "0x" + Account.sign_message(encode_defunct(text=msg), private_key=priv).signature.hex().replace("0x", "")
    signed = {**info, "address": acct.address, "type": "eip191", "signature": sig}
    header = base64.b64encode(json.dumps(signed).encode()).decode()  # raw JSON -> siwx_malformed
    return call(path, {payload_key: target}, {"SIGN-IN-WITH-X": header})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--origin", help="register every x402 resource discovered from this origin")
    ap.add_argument("--url", help="register a single resource URL")
    a = ap.parse_args()
    priv = wallet()
    if a.origin:
        st, body = register("/api/x402/registry/register-origin", "origin", a.origin, priv)
        print("origin", st, body[:600])
    if a.url:
        st, body = register("/api/x402/registry/register", "url", a.url, priv)
        print("url", st, body[:400])


if __name__ == "__main__":
    main()
