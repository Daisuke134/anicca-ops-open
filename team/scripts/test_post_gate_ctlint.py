"""Tests for ct_link_check in post_gate.py (X create/schedule link lint)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pytest
from post_gate import Refused, ct_link_check


def test_direct_app_store_link_refused():
    with pytest.raises(Refused, match="ct-link"):
        ct_link_check("x", "create", "Get it: https://apps.apple.com/app/id123")


def test_anicca_go_link_with_ct_ok():
    assert ct_link_check("x", "schedule", "Download: https://aniccaai.com/go/anicca?ct=x-diceai0-20261121-test") is None


def test_go_link_without_ct_refused():
    with pytest.raises(Refused, match="ct-link"):
        ct_link_check("x", "create", "Try https://aniccaai.com/go/anicca now")


def test_text_without_links_ok():
    assert ct_link_check("x", "create", "just some plain text, no links here") is None


def test_non_x_platform_not_checked():
    assert ct_link_check("tiktok", "create", "https://apps.apple.com/app/id123") is None


def test_delete_action_ignored():
    assert ct_link_check("x", "delete", "https://apps.apple.com/app/id123") is None
