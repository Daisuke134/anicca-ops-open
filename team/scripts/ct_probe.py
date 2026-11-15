#!/usr/bin/env python3
"""Check App Store CTA ct parameters and Next.js client-side rewrites."""

import argparse
import http.client
import sys
import urllib.error
import urllib.parse
import urllib.request
from html.parser import HTMLParser

TIMEOUT = 15
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
_PAGE_ACCEPT = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
_CT_JS_PATTERN = 'URLSearchParams(window.location.search).get("ct")'
_APPSTORE_HOST = "apps.apple.com"


class _HTMLRefs(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.hrefs = []
        self.script_srcs = []
        self.inline_scripts = []
        self._script_buffer = None

    def _collect(self, tag, attrs):
        values = {}
        for name, value in attrs:
            if value is not None:
                values[name.lower()] = value
        if "href" in values:
            self.hrefs.append(values["href"])
        if tag == "script" and "src" in values:
            self.script_srcs.append(values["src"])

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "script" and self._script_buffer is None:
            self._script_buffer = []
        self._collect(tag, attrs)

    def handle_startendtag(self, tag, attrs):
        self._collect(tag.lower(), attrs)

    def handle_endtag(self, tag):
        if tag.lower() == "script" and self._script_buffer is not None:
            self.inline_scripts.append("".join(self._script_buffer))
            self._script_buffer = None

    def handle_data(self, data):
        if self._script_buffer is not None:
            self._script_buffer.append(data)


# Static export pages (the canonical marketing overlay: /, /en, /ja) carry no Next.js runtime,
# so their ct pass-through is an inline script in the page itself. Scan that text as well as the
# Next chunks: a page whose own script rewrites the CTA from ?ct= is a client rewrite too.
def inline_scripts(html_text):
    refs = _refs(html_text)
    refs.inline_scripts = [s for s in refs.inline_scripts if s.strip()]
    return refs.inline_scripts


def _refs(html_text):
    parser = _HTMLRefs()
    parser.feed(html_text)
    parser.close()
    return parser


def _hostname(url):
    try:
        return urllib.parse.urlsplit(url).hostname
    except ValueError:
        return None


def _is_appstore_href(href):
    host = _hostname(href)
    return bool(host) and (
        host == _APPSTORE_HOST or host.endswith("." + _APPSTORE_HOST)
    )


def _ct_value(href):
    try:
        query = urllib.parse.urlsplit(href).query
    except ValueError:
        return ""
    for key, value in urllib.parse.parse_qsl(query, keep_blank_values=True):
        if key == "ct":
            return value
    return ""


def appstore_cts(html):
    """Return the ct value for each href pointing at apps.apple.com."""
    values = []
    for raw_href in _refs(html).hrefs:
        href = raw_href.strip()
        if _is_appstore_href(href):
            values.append(_ct_value(href))
    return values


def passes(html, probe):
    """Return True when App Store hrefs exist and all carry the probe ct."""
    cts = appstore_cts(html)
    return bool(cts) and all(ct == probe for ct in cts)


def client_rewrite(js_text):
    """Return True when a JS chunk rewrites App Store CTAs from the query."""
    return _CT_JS_PATTERN in js_text and _APPSTORE_HOST in js_text


def _url_with_probe(url, probe):
    parts = urllib.parse.urlsplit(url)
    ct = "ct=" + urllib.parse.quote(probe, safe="")
    query = parts.query
    query = query + "&" + ct if query else ct
    return urllib.parse.urlunsplit(
        (parts.scheme, parts.netloc, parts.path, query, parts.fragment)
    )


def _fetch(url, accept=_PAGE_ACCEPT):
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": accept,
            "Accept-Encoding": "identity",
        },
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        text = response.read().decode("utf-8", errors="replace")
        return text, response.geturl()


def _chunk_urls(page_url, html_text):
    page_host = _hostname(page_url)
    if not page_host:
        return []
    page_host = page_host.lower()

    refs = _refs(html_text)
    urls = []
    seen = set()
    for candidate in refs.hrefs + refs.script_srcs:
        candidate = candidate.strip()
        if not candidate:
            continue
        absolute = urllib.parse.urldefrag(urllib.parse.urljoin(page_url, candidate))[0]
        host = _hostname(absolute)
        if not host or host.lower() != page_host:
            continue
        try:
            path = urllib.parse.urlsplit(absolute).path
        except ValueError:
            continue
        if not (path.startswith("/_next/static/chunks/") and path.endswith(".js")):
            continue
        if absolute not in seen:
            seen.add(absolute)
            urls.append(absolute)
    return urls


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("url", help="Page URL to fetch")
    parser.add_argument("probe", help="Expected ct query value")
    args = parser.parse_args(argv)

    try:
        page_html, final_url = _fetch(_url_with_probe(args.url, args.probe))
        chunks = []
        for chunk_url in _chunk_urls(final_url, page_html):
            chunk_text, _ = _fetch(chunk_url, accept="*/*")
            chunks.append(chunk_text)
    except (urllib.error.URLError, OSError, ValueError, http.client.HTTPException) as exc:
        print(f"ct_probe: {exc}", file=sys.stderr)
        return 2

    cts = appstore_cts(page_html)
    chunk_rewrite = any(client_rewrite(chunk) for chunk in chunks)
    inline_rewrite = any(client_rewrite(script) for script in inline_scripts(page_html))
    rewrite = chunk_rewrite or inline_rewrite
    ok = passes(page_html, args.probe) or rewrite
    ct_values = sorted(set(cts))
    source = "chunk" if chunk_rewrite else "inline" if inline_rewrite else "none"
    print(
        f"appstore_hrefs={len(cts)} ct_values={ct_values} "
        f"client_rewrite={str(rewrite).lower()} pass={str(ok).lower()} "
        f"rewrite_source={source}"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
