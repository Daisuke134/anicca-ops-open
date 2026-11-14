#!/usr/bin/env python3
"""Mercor public listings check for Fucker's lane. Prints newest 10 listings and any whose
title matches the allowed niche (superintelligence / behavior simulation, RULE 2026-11-01 09:32).
Usage: python3 mercor_niche_check.py   (read-only, no login)"""
import json, urllib.request
R=urllib.request.Request("https://aws.api.mercor.com/work/listings-explore-page",headers={"User-Agent":"curl/8"})
L=json.load(urllib.request.urlopen(R,timeout=30))
L=L if isinstance(L,list) else L.get("listings",[])
L.sort(key=lambda x:x.get("createdAt",""),reverse=True)
print(f"total={len(L)} newest:")
for x in L[:10]: print(" ",x.get("createdAt"),x.get("listingId"),x.get("title"))
kw=["superintell","behavior sim","behaviour sim","simulat","alignment"]
hits=[x for x in L if any(k in (x.get("title") or "").lower() for k in kw)]
print(f"niche_hits={len(hits)}")
for x in hits: print(" ",x.get("listingId"),x.get("title"),x.get("createdAt"))
