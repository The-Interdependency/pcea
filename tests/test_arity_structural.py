# ratios: loc_comments=50:15 imports_exports=5:5 calls_definitions=25:8
# GPT/Claude generated; context, prompt Erin Spencer
"""Exact ANF/Mobius analyzer checks for arity v1."""

from __future__ import annotations

import pathlib
import sys

ARITY_DIR = pathlib.Path(__file__).resolve().parent.parent / "pcea-ucns" / "arity"
if str(ARITY_DIR) not in sys.path:
    sys.path.insert(0, str(ARITY_DIR))

import candidate  # noqa: E402
import structural  # noqa: E402

# === CHECKS ===
# id: check_arity_anf_mobius_computes_exact_degree_terms
#   proves: arity_anf_mobius_computes_exact_degree_terms
#   call: self::test_anf_coefficients_roundtrip_and_find_full_degree_term
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_arity_structural_metrics_follow_frozen_protocol
#   proves: arity_structural_metrics_follow_frozen_protocol
#   call: self::test_structural_metrics_include_required_fields_for_low_arity
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_arity_outcome_labels_use_preregistered_vocabulary
#   proves: arity_outcome_labels_use_preregistered_vocabulary
#   call: self::test_outcome_label_validation_rejects_unknown_labels
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_anf_coefficients_roundtrip_and_find_full_degree_term() -> None:
    truth = [0, 0, 0, 1]
    coeffs = structural.anf_coefficients(truth)
    assert coeffs == [0, 0, 0, 1]
    assert structural.algebraic_degree(coeffs) == 2
    assert structural.reconstruct_truth(coeffs) == truth
    assert structural.reconstruct_truth(structural.remove_full_degree(coeffs)) == [0, 0, 0, 0]


def test_structural_metrics_include_required_fields_for_low_arity() -> None:
    result = structural.analyze_variant_arity("pcea", 2, plaintext_values=(0,), word_bits=8)
    metrics = result["metrics"]
    assert set(metrics) == {
        "maximum_algebraic_degree",
        "full_degree_output_bits",
        "output_bits_examined",
        "full_degree_fraction",
        "mismatches_after_deleting_degree_n",
        "mismatch_fraction",
    }
    assert metrics["output_bits_examined"] == 8
    assert 0 <= metrics["maximum_algebraic_degree"] <= 2


def test_outcome_label_validation_rejects_unknown_labels() -> None:
    assert not candidate.validate_outcome_labels(
        {
            "H_STRUCT": "SURVIVED_STRUCTURAL_ARITY",
            "H_PCEA": "FALSIFIED_PCEA_SPECIFIC_ARITY",
            "H_HARD": "UNRESOLVED",
        }
    )
    assert candidate.validate_outcome_labels({"H_STRUCT": "SECURE"})
# ratios: loc_comments=50:15 imports_exports=5:5 calls_definitions=25:8
