#!/usr/bin/env python3
# Commission Math oracle - mirrors engine.js.
import json, math

MAXM = 100000000

def _c(x, msg, hi, allow_zero):
    if isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x < 0 or x > hi or (not allow_zero and x == 0):
        raise ValueError(msg)
    return math.floor(x * 100 + 0.5)

def _fmt(h):
    whole, frac = divmod(h, 100)
    if frac == 0:
        return str(whole)
    f = f"{frac:02d}"
    if f[1] == "0":
        f = f[0]
    return f"{whole}.{f}"

def _money(c):
    whole, frac = divmod(c, 100)
    return f"{whole:,}.{frac:02d}"

def _part(cents, rate):
    return (2 * cents * rate + 10000) // 20000

def flat_truth(sales, rate):
    s = _c(sales, "sales must be between 0 and 100000000", MAXM, True)
    r = _c(rate, "rate must be between 0 and 100", 100, True)
    return f"Commission on {_money(s)} of sales at {_fmt(r)}%: {_money(_part(s, r))}."

def tier_truth(sales, threshold, low_rate, high_rate):
    s = _c(sales, "sales must be between 0 and 100000000", MAXM, True)
    t = _c(threshold, "threshold must be above 0 and at most 100000000", MAXM, False)
    lo = _c(low_rate, "rate below the threshold must be between 0 and 100", 100, True)
    hi = _c(high_rate, "rate above the threshold must be between 0 and 100", 100, True)
    if s <= t:
        return f"All {_money(s)} is at or under the {_money(t)} threshold: {_fmt(lo)}% gives {_money(_part(s, lo))}."
    a = _part(t, lo); b = _part(s - t, hi)
    return f"{_fmt(lo)}% on the first {_money(t)} is {_money(a)}; {_fmt(hi)}% on the other {_money(s - t)} is {_money(b)}; total {_money(a + b)}."

def target_truth(target, rate):
    g = _c(target, "target commission must be between 0 and 100000000", MAXM, True)
    r = _c(rate, "rate must be above 0 and at most 100", 100, False)
    s = 0
    if g > 0:
        n = 10000 * g
        s = n // r + (1 if n % r > 0 else 0)
    return f"To earn {_money(g)} at {_fmt(r)}%, sales of {_money(s)} are needed."

FNS = {"flatTruth": flat_truth, "tierTruth": tier_truth, "targetTruth": target_truth}

CASES = [
    ("flatTruth", [50000, 5]), ("flatTruth", [0, 5]), ("flatTruth", [1234.56, 7.5]), ("flatTruth", [100000000, 100]),
    ("flatTruth", [1, 0.5]), ("flatTruth", [0.01, 5]), ("flatTruth", [1000, 0]), ("flatTruth", [999.99, 3.33]),
    ("flatTruth", [-1, 5]), ("flatTruth", [100000001, 5]), ("flatTruth", [100, 101]), ("flatTruth", [100, -1]),
    ("tierTruth", [60000, 50000, 3, 5]), ("tierTruth", [30000, 50000, 3, 5]), ("tierTruth", [50000, 50000, 3, 5]),
    ("tierTruth", [50000.01, 50000, 3, 5]), ("tierTruth", [0, 50000, 3, 5]), ("tierTruth", [123456.78, 40000, 2.5, 6.25]),
    ("tierTruth", [100000000, 1, 0, 100]), ("tierTruth", [60000, 0, 3, 5]), ("tierTruth", [60000, 100000001, 3, 5]),
    ("tierTruth", [-1, 50000, 3, 5]), ("tierTruth", [60000, 50000, 101, 5]), ("tierTruth", [60000, 50000, 3, -1]),
    ("tierTruth", [1234567.89, 1000, 1, 2]),
    ("targetTruth", [2500, 5]), ("targetTruth", [0, 5]), ("targetTruth", [1000, 3]), ("targetTruth", [0.01, 5]),
    ("targetTruth", [100, 100]), ("targetTruth", [500, 7.25]), ("targetTruth", [1, 0.01]), ("targetTruth", [100000000, 0.01]),
    ("targetTruth", [100, 0]), ("targetTruth", [-1, 5]), ("targetTruth", [100000001, 5]), ("targetTruth", [100, 101]),
    ("targetTruth", [1234.56, 3.33]),
]

out = []
for fn, args in CASES:
    try:
        exp = FNS[fn](*args)
    except ValueError as e:
        exp = "ERR:" + str(e)
    out.append({"fn": fn, "args": args, "expected": exp})
with open("expected.json", "w") as f:
    json.dump(out, f, indent=1)
    f.write("\n")
print(len(out), "cases")
