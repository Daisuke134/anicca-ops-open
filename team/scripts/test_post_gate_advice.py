"""Tests for the advisory checks that come from X-ADVICE-LOG (never refuse a post)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from post_gate import advice_warnings


def test_bare_percentage_warns():
    assert advice_warnings("Only 4% of people opened the page.")


def test_percentage_with_denominator_ok():
    assert advice_warnings("14 of 334 opened the page (4%).") == []
    assert advice_warnings("334回表示→14人がページを開いた（4%）") == []
    assert advice_warnings("14/334 = 4%") == []


def test_no_percentage_ok():
    assert advice_warnings("5 paying users, 0 trials.") == []
    assert advice_warnings("") == []


CONNECT_MSG = "connect request must be line 1 (X-STYLE 11/22)"


def test_connect_request_not_on_line1_warns():
    assert CONNECT_MSG in advice_warnings("今日の学びを共有します\nつながりたい方はぜひ")
    assert CONNECT_MSG in advice_warnings("Sharing today's lesson.\nI'd love to connect with builders.")


def test_connect_request_on_line1_ok():
    assert advice_warnings("つながりたい方はぜひ\n今日の学びを共有します") == []
    assert advice_warnings("Love to connect!\n\nSharing today's lesson.") == []


def test_no_connect_request_ok():
    assert advice_warnings("Hello everyone, nice to meet you.") == []
    assert advice_warnings("") == []
