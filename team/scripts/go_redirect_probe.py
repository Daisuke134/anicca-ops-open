#!/usr/bin/env python3
"""Probe /go/anicca?ct=<ct> redirects to apps.apple.com with the ct echoed."""
import sys
import urllib.request
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlparse

BASE_URL = "https://aniccaai.com/go/anicca?ct="
REDIRECT_STATUSES = {301, 302, 307, 308}
TIMEOUT = 15


def check(ct, fetch):
    """Return (True, "") if fetch redirects correctly for ct, else (False, reason)."""
    url = BASE_URL + ct
    status, location = fetch(url)
    if status not in REDIRECT_STATUSES:
        return False, f"status {status}"
    if not location:
        return False, "no location header"
    parsed = urlparse(location)
    if parsed.hostname != "apps.apple.com":
        return False, f"host {parsed.hostname}"
    values = parse_qs(parsed.query).get("ct", [])
    if values != [ct]:
        return False, f"ct mismatch {values}"
    return True, ""


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def fetch(url):
    """Return (status, location) without following redirects."""
    opener = urllib.request.build_opener(_NoRedirect)
    try:
        resp = opener.open(url, timeout=TIMEOUT)
        status, location = resp.status, resp.headers.get("Location", "")
    except HTTPError as e:
        status, location = e.code, e.headers.get("Location", "")
    return status, location or ""


def main(argv):
    passes = 0
    total = 0
    for ct in argv:
        total += 1
        ok, reason = check(ct, fetch)
        if ok:
            passes += 1
            print(f"PASS {ct}")
        else:
            print(f"FAIL {ct} {reason}")
    print(f"go pass={passes}/{total}")
    return 1 if passes != total else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
