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
