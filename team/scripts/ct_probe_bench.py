#!/usr/bin/env python3
"""ct_probe_bench FILE PROBE: run ct_probe.main over every URL in FILE.

FILE: one URL per line; blank lines and '#' lines skipped.
Per URL prints `<url> pass|fail|na|err`, then `bench pass=<k>/<n> na=<m> err=<e>`.
na = zero App Store hrefs and no client rewrite; err = fetch error (rc 2);
n = pass + fail. Exit 0 only when n > 0 and every probed URL passes.
"""
import contextlib
import io
import os
import re
import sys
from datetime import datetime
from zoneinfo import ZoneInfo

import ct_probe


def read_urls(path):
    with open(path, encoding="utf-8") as f:
        return [s for s in (line.strip() for line in f) if s and not s.startswith("#")]


def classify(url, probe):
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(io.StringIO()):
        rc = ct_probe.main([url, probe])
    out = buf.getvalue()
    if rc == 2:
        return "err"
    hrefs = re.search(r"appstore_hrefs=(\d+)", out)
    rewrite = "client_rewrite=true" in out
    if rc == 0:
        return "pass"
    if hrefs and int(hrefs.group(1)) == 0 and not rewrite:
        return "na"
    return "fail"


CSV_HEADER = "ts_jst,probe,pass,n,na,err"


def append_csv(path, probe, counts, n):
    ts = datetime.now(ZoneInfo("Asia/Tokyo")).strftime("%Y-%m-%d %H:%M")
    row = f"{ts},{probe},{counts['pass']},{n},{counts['na']},{counts['err']}\n"
    new = not os.path.exists(path) or os.path.getsize(path) == 0
    with open(path, "a", encoding="utf-8") as f:
        if new:
            f.write(CSV_HEADER + "\n")
        f.write(row)


def main(argv=None):
    args = list(sys.argv[1:] if argv is None else argv)
    csv_path = None
    if "--csv" in args:
        i = args.index("--csv")
        if i + 1 >= len(args):
            print("usage: ct_probe_bench.py FILE PROBE [--csv OUT]", file=sys.stderr)
            return 2
        csv_path = args[i + 1]
        del args[i:i + 2]
    if len(args) != 2:
        print("usage: ct_probe_bench.py FILE PROBE [--csv OUT]", file=sys.stderr)
        return 2
    counts = {"pass": 0, "fail": 0, "na": 0, "err": 0}
    for url in read_urls(args[0]):
        status = classify(url, args[1])
        counts[status] += 1
        print(f"{url} {status}")
    n = counts["pass"] + counts["fail"]
    print(f"bench pass={counts['pass']}/{n} na={counts['na']} err={counts['err']}")
    if csv_path is not None:
        append_csv(csv_path, args[1], counts, n)
    return 0 if n and counts["pass"] == n else 1


if __name__ == "__main__":
    sys.exit(main())
