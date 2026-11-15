import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import ct_probe


PROBE = "probe_value"


def test_all_appstore_hrefs_pass():
    html = """
    <a href="https://apps.apple.com/us/app/alpha/id1?ct=probe_value&mt=8">Alpha</a>
    <a href='https://apps.apple.com/jp/app/beta/id2?mt=8&ct=probe_value'>Beta</a>
    """
    assert ct_probe.appstore_cts(html) == [PROBE, PROBE]
    assert ct_probe.passes(html, PROBE) is True


def test_hardcoded_ct_fails():
    html = (
        '<a href="https://apps.apple.com/us/app/alpha/id1'
        '?ct=affirmation_app_en">Alpha</a>'
    )
    assert ct_probe.appstore_cts(html) == ["affirmation_app_en"]
    assert ct_probe.passes(html, PROBE) is False


def test_mixed_ct_values_fail():
    html = """
    <a href="https://apps.apple.com/us/app/alpha/id1?ct=probe_value">Alpha</a>
    <a href="https://apps.apple.com/us/app/beta/id2?ct=affirmation_app_en">Beta</a>
    """
    assert ct_probe.passes(html, PROBE) is False


def test_no_appstore_href_fails():
    html = """
    <a href="https://example.com/?ct=probe_value">Example</a>
    <a href="https://play.google.com/store/apps/details?id=x&ct=probe_value">Android</a>
    """
    assert ct_probe.appstore_cts(html) == []
    assert ct_probe.passes(html, PROBE) is False


def test_ampersand_entity_query_is_parsed():
    html = (
        '<a href="https://apps.apple.com/app?id=1&amp;ct=probe_value'
        '&amp;mt=8">App</a>'
    )
    assert ct_probe.appstore_cts(html) == [PROBE]
    assert ct_probe.passes(html, PROBE) is True


def test_non_appstore_links_are_ignored():
    html = """
    <a href="https://apps.apple.com.evil.example/?ct=bad">Lookalike</a>
    <a href="https://example.com/?ct=bad">Example</a>
    <a href="https://apps.apple.com/app?id=1&ct=probe_value">App</a>
    """
    assert ct_probe.appstore_cts(html) == [PROBE]
    assert ct_probe.passes(html, PROBE) is True


def test_appstore_href_without_ct_gives_empty_value():
    html = '<a href="https://apps.apple.com/app/id123">App</a>'
    assert ct_probe.appstore_cts(html) == [""]
    assert ct_probe.passes(html, PROBE) is False


def test_client_rewrite_detects_ct_pattern():
    js = (
        'const ct = new URLSearchParams(window.location.search).get("ct");'
        'const url = "https://apps.apple.com/app";'
    )
    assert ct_probe.client_rewrite(js) is True
    assert ct_probe.client_rewrite(
        'URLSearchParams(window.location.search).get("ct")'
    ) is False
    assert ct_probe.client_rewrite("apps.apple.com") is False
