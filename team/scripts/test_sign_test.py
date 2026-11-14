import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sign_test import sign_test


def test_known_values():
    assert round(sign_test(9, 0), 7) == 0.0039062
    assert sign_test(8, 0) == 0.0078125
    assert sign_test(6, 2) == 0.2890625
    assert sign_test(7, 1) == 0.0703125
    assert sign_test(6, 1) == 0.125
    assert sign_test(0, 0) == 1.0


def test_symmetric():
    assert sign_test(2, 6) == sign_test(6, 2)


def test_capped_at_one():
    assert sign_test(5, 5) == 1.0
