# ratios: loc_comments=69:18 imports_exports=7:8 calls_definitions=38:10
# GPT/Claude generated; context, prompt Erin Spencer
"""Freeze artifact checks for the arity v1 protocol."""

from __future__ import annotations

import pathlib
import sys

ARITY_DIR = pathlib.Path(__file__).resolve().parent.parent / "pcea-ucns" / "arity"
if str(ARITY_DIR) not in sys.path:
    sys.path.insert(0, str(ARITY_DIR))

import candidate  # noqa: E402
import structural  # noqa: E402

# === CHECKS ===
# id: check_arity_fixtures_are_deterministic_and_versioned
#   proves: arity_fixtures_are_deterministic_and_versioned
#   call: self::test_fixture_document_is_deterministic_and_schema_versioned
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_arity_freeze_artifacts_point_to_receipts
#   proves: arity_freeze_verifies_f0_runtime_identity, arity_fixtures_are_deterministic_and_versioned
#   call: self::test_freeze_artifacts_exist_and_match_receipts
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_arity_phase3_gate_is_outcome_blind
#   proves: arity_phase3_gate_is_outcome_blind
#   call: self::test_phase3_gate_is_outcome_blind_when_present
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
#
# id: check_arity_actor_lock_hashes_reached_artifacts
#   proves: arity_actor_lock_hashes_reached_artifacts
#   call: self::test_actor_lock_hashes_reached_artifacts_when_present
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_fixture_document_is_deterministic_and_schema_versioned() -> None:
    first = candidate.fixture_document()
    second = candidate.fixture_document()
    assert first == second
    assert first["schema"] == "pcea-arity-fixtures-v1"
    assert first["parameters"]["plaintext_values"] == [0, 1, -1, 2, 127]
    assert len(first["phase3_secret_fixtures"]) == len(candidate.SECRET_BITS) * candidate.SECRET_TRIALS


def test_freeze_artifacts_exist_and_match_receipts() -> None:
    assert candidate.FIXTURES_PATH.exists()
    assert candidate.GRAPH_PATH.exists()
    assert candidate.FREEZE_PATH.exists()

    freeze = candidate.read_json(candidate.FREEZE_PATH)
    assert freeze["schema"] == "pcea-arity-freeze-v1"
    assert freeze["F0"]["baseline_commit"] == candidate.baseline_receipt()["baseline_commit"]
    assert freeze["F0"]["baseline_receipt_sha256"] == candidate.sha256_path(candidate.BASELINE_PATH)
    assert freeze["artifact_receipts"]["fixtures_json_sha256"] == candidate.sha256_path(candidate.FIXTURES_PATH)
    assert freeze["artifact_receipts"]["current_dependency_graph_json_sha256"] == candidate.sha256_path(candidate.GRAPH_PATH)
    assert candidate.is_valid_sha_or_pending(freeze["F1"]["candidate_commit"])


def test_phase3_gate_is_outcome_blind_when_present() -> None:
    if not candidate.PHASE3_GATE_PATH.exists():
        return
    gate = candidate.read_json(candidate.PHASE3_GATE_PATH)
    assert set(gate) == {
        "schema",
        "F0_baseline_commit",
        "F1_candidate_commit",
        "freeze_json_sha256",
        "authorized",
        "criterion",
        "issuer",
    }
    assert gate["schema"] == structural.GATE_SCHEMA
    forbidden = {"metrics", "effect_sizes", "outcome_labels", "classification_reasons", "analyses"}
    assert not (set(gate) & forbidden)


def test_actor_lock_hashes_reached_artifacts_when_present() -> None:
    if not candidate.ACTOR_A_LOCK_PATH.exists():
        return
    lock = candidate.read_json(candidate.ACTOR_A_LOCK_PATH)
    assert lock["schema"] == structural.LOCK_SCHEMA
    assert lock["F0"]["BASELINE_FREEZE_V1_json_sha256"] == candidate.sha256_path(candidate.BASELINE_PATH)
    assert lock["F1"]["freeze_json_sha256"] == candidate.sha256_path(candidate.FREEZE_PATH)
    assert lock["PHASE3_GATE_json_sha256"] == candidate.sha256_path(candidate.PHASE3_GATE_PATH)
    assert not candidate.validate_outcome_labels(lock["preregistered_outcome_labels"])
    for relative_path, digest in lock["artifact_hashes"].items():
        assert candidate.sha256_path(candidate.ROOT / relative_path) == digest
# ratios: loc_comments=69:18 imports_exports=7:8 calls_definitions=38:10
