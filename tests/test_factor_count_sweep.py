# ratios: loc_comments=32:11 imports_exports=4:3 calls_definitions=11:3
# GPT/Claude generated; context, prompt Erin Spencer
"""
Tests for the factor-count sweep and non-uniqueness diagnosis.

Pins two measured findings: (1) private-factor recovery does NOT decay
with factor count, and (2) the public product admits many ordered
factorizations (the structural defeater). Skipped without ucns.
"""

import importlib.util
import os
import pathlib

import pytest

_spec = importlib.util.spec_from_file_location(
    "factor_count_sweep",
    pathlib.Path(__file__).parent.parent / "pcea-ucns" / "factor_count_sweep.py",
)
fcs = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(fcs)

RUN_EXPENSIVE = os.environ.get("PCEA_UCNS_EXPENSIVE") == "1"

pytestmark = pytest.mark.skipif(
    not fcs.UCNS_AVAILABLE,
    reason=getattr(fcs, "UCNS_IMPORT_ERROR", "recursive UCNS API unavailable"),
)


def test_default_run_reports_factor_count_work_still_required():
    r = fcs.run_all()
    assert r["available"]
    assert "nonuniqueness" in r
    assert "decay" not in r
    assert "requires_more" in r


@pytest.mark.skipif(
    not RUN_EXPENSIVE,
    reason="set PCEA_UCNS_EXPENSIVE=1 for the legacy exhaustive factor-count decay sweep",
)
def test_recovery_does_not_decay_with_factor_count():
    d = fcs.decay_sweep([8, 5], 2, counts=(2, 4, 6), trials=40)
    # No monotone downward trend: the 6-factor rate is not materially
    # below the 2-factor rate. More factors do not hide the key.
    assert d[6]["rate"] >= d[2]["rate"] - 0.2


def test_product_has_many_ordered_factorizations():
    r = fcs.nonuniqueness([8, 5], 2, nfac=5, trials=50)
    # The search essentially never returns the true ordered split; the
    # product is massively non-unique. This is the structural barrier.
    assert r["true_split"] <= r["recompose"] * 0.1
    assert r["other_split"] >= r["recompose"] * 0.9
# ratios: loc_comments=32:11 imports_exports=4:3 calls_definitions=11:3
