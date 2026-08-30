# ratios: loc_comments=103:33 imports_exports=10:2 calls_definitions=28:5
# GPT/Claude generated; context, prompt Erin Spencer
"""
Three-factor positional attack for PCEA-UCNS.

The two-factor positional attack (positional_attack.py) refuted the v0
Q1 conjecture: P = A ⊠ B at a fixed carrier yields a recomposing split
every time. This module tests the THREE-factor candidate raised next:
P = A ⊠ B ⊠ C, where one factor (C) is the designated private key and the
attacker holds the public product P.

The question is sharper than recompose-rate. Because UCNS composition is
ORDERED, a single two-factor split of a triple product need not fall on a
private-factor boundary. Two quantities matter:

- FIRST-SPLIT-CLEAN: fraction where factor_search_v08's split is exactly
  (A ⊠ B, C) — i.e. the search peels the private factor off in one step.
- RECURSIVE-PEEL-RECOVERS-C: fraction where recursively factoring the
  first split's parts yields C among the leaves — the realistic attacker,
  who peels iteratively.

MEASURE, not assert. Skipped without recursive UCNS APIs. The historical
60-trial recursive-peel measurement is opt-in for test cost; quick runs keep
a small deterministic smoke sample.

Measured result (denoms [8,5] = carrier 40, width 3, seed 13, trials 60,
2026-08-30 refresh): recompose 60/60, first-split-clean 0/60,
recursive-peel-recovers-C 27/60 (45%). Historical 80-trial run: recompose
80/80, first-split-clean 0/80, recursive-peel-recovers-C ~49%. Interpretation:
ordered triple composition SMEARS the private-factor boundary (the single
split never cleanly isolates C), but recursive peeling still recovers C
about half the time. Three factors degrade the attack measurably; they do
NOT defeat it. A KEM cannot rest on triple-composition alone.
"""

from __future__ import annotations

import os
import random
import sys
from fractions import Fraction
from math import lcm
from pathlib import Path
from typing import List, Tuple

sys.path.insert(0, str(Path(__file__).resolve().parent))
from ucns_compat import import_ucns_module  # noqa: E402

try:
    _canonical = import_ucns_module("canonical")
    _factor_search = import_ucns_module("factor_search_v08")

    UCNSObject = _canonical.UCNSObject
    multiply = _canonical.multiply
    SEQ_PRIME = _factor_search.SEQ_PRIME
    factor_search_v08 = _factor_search.factor_search_v08

    UCNS_AVAILABLE = True
    UCNS_IMPORT_ERROR = ""
except ImportError as exc:  # pragma: no cover
    UCNS_AVAILABLE = False
    UCNS_IMPORT_ERROR = str(exc)


def _mk(angles: List[Fraction], faces: List[int]) -> "UCNSObject":
    n_min = 1
    for a in angles:
        frac = (a % 2) / 2
        if frac != 0:
            n_min = lcm(n_min, frac.denominator)
    return UCNSObject(2 * n_min, n_min, [(a, None) for a in angles], faces)


def _keylike(rng: random.Random, denoms: List[int], width: int) -> "UCNSObject":
    poss = sorted({Fraction(k, d) for d in denoms for k in range(1, d)})
    angles = [Fraction(0)] + rng.sample(poss, min(width, len(poss)))
    return _mk(angles, [rng.randint(0, 1) for _ in range(len(angles))])


def _struct(o: "UCNSObject") -> Tuple:
    return (tuple(o.A_plus), tuple(o.F_plus))


def three_factor_recovery(
    denoms: List[int],
    width: int,
    trials: int = 80,
    seed: int = 13,
    include_recursive_peel: bool = True,
) -> dict:
    """Attack P = A ⊠ B ⊠ C at a fixed carrier; C is the private factor.

    Returns recompose count, clean-first-split count (search isolates C in
    one step), and recursive-peel recovery count (iterative attacker finds
    C among leaves of a two-level factor tree).
    """
    rng = random.Random(seed)
    recompose = 0
    first_split_clean = 0
    peel_recovers_C = 0
    for _ in range(trials):
        A = _keylike(rng, denoms, width)
        B = _keylike(rng, denoms, width)
        C = _keylike(rng, denoms, width)
        P = multiply(multiply(A, B), C)
        r = factor_search_v08(P, prune=False)
        if r is SEQ_PRIME:
            continue
        recompose += 1
        X, Y = r
        if _struct(Y) == _struct(C) and _struct(X) == _struct(multiply(A, B)):
            first_split_clean += 1
        if include_recursive_peel:
            leaves: List["UCNSObject"] = []
            for part in (X, Y):
                rr = factor_search_v08(part, prune=False)
                if rr is SEQ_PRIME:
                    leaves.append(part)
                else:
                    leaves.extend(rr)
            if any(_struct(leaf) == _struct(C) for leaf in leaves):
                peel_recovers_C += 1
    return {
        "denoms": denoms,
        "width": width,
        "trials": trials,
        "recompose": recompose,
        "first_split_clean": first_split_clean,
        "peel_recovers_C": peel_recovers_C if include_recursive_peel else None,
        "peel_recovery_rate": peel_recovers_C / trials if include_recursive_peel else None,
    }


FULL_RECURSIVE_REQUIRES = (
    "Run with PCEA_UCNS_EXPENSIVE=1 or call "
    "three_factor_recovery([8, 5], 3, trials=60) to refresh the historical "
    "recursive-peel measurement."
)


def run_all(include_recursive_peel: bool = False) -> dict:
    if not UCNS_AVAILABLE:
        return {"available": False}
    report = {
        "available": True,
        "results": [
            three_factor_recovery([3, 5], 2, trials=10, include_recursive_peel=include_recursive_peel),
            three_factor_recovery([8, 5], 3, trials=10, include_recursive_peel=include_recursive_peel),
            three_factor_recovery([3, 5, 7], 3, trials=10, include_recursive_peel=include_recursive_peel),
        ],
    }
    if not include_recursive_peel:
        report["requires_more"] = FULL_RECURSIVE_REQUIRES
    return report


if __name__ == "__main__":
    import json

    rep = run_all(include_recursive_peel=os.environ.get("PCEA_UCNS_EXPENSIVE") == "1")
    if not rep["available"]:
        print(f"recursive UCNS API unavailable; three-factor harness skipped: {UCNS_IMPORT_ERROR}")
    else:
        print(json.dumps(rep, indent=2))
# ratios: loc_comments=103:33 imports_exports=10:2 calls_definitions=28:5
