#!/usr/bin/env python3
"""Exact two-sided binomial sign test (ties dropped). No network, stdlib only.
usage: sign_test.py WINS LOSSES"""
import math, sys

def sign_test(wins, losses):
    n = wins + losses
    if n == 0:
        return 1.0
    k = min(wins, losses)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (1 << n)
    return min(1.0, 2.0 * tail)

if __name__ == '__main__':
    w, l = int(sys.argv[1]), int(sys.argv[2])
    n = w + l
    p = sign_test(w, l)
    print(f"n={n} wins={w} p={p:.7f}")
