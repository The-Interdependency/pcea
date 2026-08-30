# ratios: loc_comments=45:17 imports_exports=6:5 calls_definitions=29:7
# GPT/Claude generated; context, prompt Erin Spencer
"""Current-baseline checks for the arity v1 research adapter."""

from __future__ import annotations

import pathlib
import sys

ARITY_DIR = pathlib.Path(__file__).resolve().parent.parent / "pcea-ucns" / "arity"
if str(ARITY_DIR) not in sys.path:
    sys.path.insert(0, str(ARITY_DIR))

import candidate  # noqa: E402

# === CHECKS ===
# id: check_arity_a3_adapter_matches_runtime_pcea
#   proves: arity_a3_adapter_matches_runtime_pcea
#   call: self::test_a3_adapter_matches_runtime_for_deterministic_fixtures
#   requires: python3
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_arity_freeze_verifies_f0_runtime_identity
#   proves: arity_freeze_verifies_f0_runtime_identity
#   call: self::test_f0_and_current_runtime_blob_identity_hold
#   requires: python3, git
#   timeout: 10
#   mutates: none
#   cleanup: none
#
# id: check_arity_dependency_graph_records_triadic_runtime_relation
#   proves: arity_dependency_graph_records_triadic_runtime_relation
#   call: self::test_dependency_graph_records_every_cell_as_triadic
#   requires: python3
#   timeout: 5
#   mutates: none
#   cleanup: none
# === END CHECKS ===


def test_a3_adapter_matches_runtime_for_deterministic_fixtures() -> None:
    for case in candidate.fixture_document()["a3_regression_cases"]:
        assert candidate.adapter_encrypt_for_a3_fixture(case) == candidate.runtime_encrypt_for_a3_fixture(case)


def test_f0_and_current_runtime_blob_identity_hold() -> None:
    assert candidate.verify_baseline_commit_blobs()["ok"]
    assert candidate.verify_current_runtime_blobs()["ok"]


def test_dependency_graph_records_every_cell_as_triadic() -> None:
    graph = candidate.dependency_graph_document()
    assert graph["verified_state_key_relation"]["state_key_direct_arity"] == 3
    assert len(graph["cells"]) == candidate.CIRCLE_COUNT * candidate.TENSOR_COUNT
    for cell in graph["cells"]:
        assert len(cell["prior_state_contributor_dependency"]) == 3
        assert cell["current_plaintext_dependency"]
        assert cell["address_dependency"]
        assert cell["prime_base_dependency"]["prime"] >= 2
        assert cell["hash_kdf_dependency"]["source"] == "pcea.kdf.key_stream"
# ratios: loc_comments=45:17 imports_exports=6:5 calls_definitions=29:7
