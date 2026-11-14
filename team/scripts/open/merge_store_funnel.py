#!/usr/bin/env python3
"""Merge team/scripts/open/site/store_funnel.json (or argv1) into an open data.json (argv2, default site/data.json)."""
import json, sys, pathlib
src = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '/workspace/team/scripts/open/site/store_funnel.json')
dst = pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else '/workspace/team/scripts/open/site/data.json')
funnel = json.loads(src.read_text())
data = json.loads(dst.read_text())
data['store_funnel'] = funnel
data['store_funnel_updated_at'] = funnel.get('observed_at')
dst.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
print(f"merged store_funnel ({len(funnel.get('apps') or [])} apps) into {dst}")
