"""Lint marketing copy for link problems."""

import re
import sys
from urllib.parse import parse_qs, urlparse

URL_RE = re.compile(r"https?://[^\s<>\"')\]]+")
CT_RE = re.compile(r"^[a-z0-9-]{6,80}$")
APP_STORE_HOSTS = {"apps.apple.com", "itunes.apple.com"}


def _problems_for_url(url: str) -> list[str]:
    parsed = urlparse(url)
    host = parsed.netloc.lower().split(":", 1)[0]
    if host in APP_STORE_HOSTS:
        return ["direct-app-store"]
    if host == "aniccaai.com" and parsed.path.startswith("/go/"):
        ct_values = parse_qs(parsed.query).get("ct", [])
        if not ct_values:
            return ["missing-ct"]
        if not CT_RE.fullmatch(ct_values[0]):
            return ["bad-ct"]
    return []


def lint(text: str) -> list[str]:
    problems: list[str] = []
    for match in URL_RE.finditer(text):
        problems.extend(_problems_for_url(match.group(0)))
    return problems


def main(argv: list[str]) -> int:
    text = argv[1] if len(argv) > 1 else ""
    problems = lint(text)
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
