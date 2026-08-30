# ratios: loc_comments=29:12 imports_exports=4:3 calls_definitions=11:3
# GPT/Claude generated; context, prompt Erin Spencer
"""
Tests for the three-factor positional attack harness.

Pins the MEASURED partial result: ordered triple composition smears the
private-factor boundary (first split never cleanly isolates C), yet
recursive peeling still recovers C roughly half the time. Three factors
degrade but do not defeat the attack. Skipped without ucns.
"""

import importlib.util
import os
import pathlib

import pytest

_spec = importlib.util.spec_from_file_location(
    "three_factor_attack",
    pathlib.Path(__file__).parent.parent / "pcea-ucns" / "three_factor_attack.py",
)
tfa = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(tfa)

RUN_EXPENSIVE = os.environ.get("PCEA_UCNS_EXPENSIVE") == "1"

pytestmark = pytest.mark.skipif(
    not tfa.UCNS_AVAILABLE,
    reason=getattr(tfa, "UCNS_IMPORT_ERROR", "recursive UCNS API unavailable"),
)


def test_first_split_does_not_cleanly_isolate_private_factor():
    # Ordered composition smears the boundary: the single split essentially
    # never equals (A ⊠ B, C).
    r = tfa.three_factor_recovery([8, 5], 3, trials=10, include_recursive_peel=False)
    assert r["first_split_clean"] <= r["trials"] * 0.1
    assert r["peel_recovery_rate"] is None


def test_recursive_peel_smoke_still_recovers_but_not_fully():
    r = tfa.three_factor_recovery([8, 5], 3, trials=5)
    assert 0 < r["peel_recovery_rate"] < 1


@pytest.mark.skipif(
    not RUN_EXPENSIVE,
    reason="set PCEA_UCNS_EXPENSIVE=1 for the historical 60-trial recursive-peel measurement",
)
def test_recursive_peel_historical_measurement():
    # The partial-protection finding: recovery is materially above zero and
    # materially below one. Both bounds matter — neither safe nor trivial.
    r = tfa.three_factor_recovery([8, 5], 3, trials=60)
    assert 0.2 < r["peel_recovery_rate"] < 0.85
# ratios: loc_comments=29:12 imports_exports=4:3 calls_definitions=11:3
