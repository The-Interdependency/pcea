# ratios: loc_comments=72:6 imports_exports=9:6 calls_definitions=27:9
# GPT/Claude generated; context, prompt Erin Spencer
"""Actor B replay tests for PCEA Arity v1.

These tests exercise only Actor B's own replay namespace and the frozen
baseline receipts. They do not import or inspect Actor A's implementation.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "pcea-ucns" / "arity" / "replay_b"))

from adapters import pcea_seed_a3  # noqa: E402
from anf import delete_full_degree_mismatches, mobius_transform  # noqa: E402

from pcea.cipher import encrypt_seed  # noqa: E402

ARITY_DIR = Path(__file__).resolve().parent.parent / "pcea-ucns" / "arity"


def _load_fixtures() -> dict:
    with (ARITY_DIR / "fixtures.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def _load_baseline_receipt() -> dict:
    with (ARITY_DIR / "BASELINE_FREEZE_V1.json").open(encoding="utf-8") as fh:
        return json.load(fh)


def _git_blob_sha1(data: bytes) -> str:
    header = b"blob " + str(len(data)).encode() + b"\0"
    return hashlib.sha1(header + data).hexdigest()


def test_frozen_runtime_blobs_match_baseline_receipt() -> None:
    receipt = _load_baseline_receipt()
    repo_root = ARITY_DIR.parent.parent
    for rel, expected in receipt["frozen_runtime_paths"].items():
        data = (repo_root / rel).read_bytes()
        actual = _git_blob_sha1(data)
        assert actual == expected, f"frozen runtime drift: {rel}"


def test_a3_adapter_matches_runtime_cipher_on_regression_fixtures() -> None:
    fixtures = _load_fixtures()
    for case in fixtures["a3_regression_cases"]:
        seed = case["seed"]
        last_seed = case["last_seed"]
        seed_idx = case["seed_idx"]
        word_bits = case["word_bits"]
        adapter = pcea_seed_a3(seed, last_seed, seed_idx, word_bits)
        runtime = encrypt_seed(seed, last_seed, seed_idx, word_bits)
        assert adapter == runtime, f"A3 adapter mismatch in {case['case_id']}"


def test_anf_transform_is_self_inverse() -> None:
    for n in range(1, 5):
        size = 1 << n
        table = [(i * 37 + n * 11) & 1 for i in range(size)]
        assert mobius_transform(mobius_transform(table)) == table


def test_full_degree_deletion_on_known_and_function() -> None:
    # f(x0, x1) = x0 AND x1; the single degree-2 coefficient is 1.
    table = [0, 0, 0, 1]
    mismatches = delete_full_degree_mismatches(table, 2)
    assert mismatches == 1


def test_structural_assignments_cover_all_masks() -> None:
    fixtures = _load_fixtures()
    for arity in (2, 3, 5, 7):
        entries = fixtures["structural_assignments"][str(arity)]
        masks = sorted(entry["mask"] for entry in entries)
        assert masks == list(range(1 << arity))


def test_phase1_runner_emits_rows_and_vocabulary_labels() -> None:
    from runner import run_phase1  # noqa: E402  (B namespace import)

    report = run_phase1()
    rows = report["rows"]
    assert len(rows) == 8
    for row in rows:
        assert set(row) >= {
            "variant", "arity", "maximum_algebraic_degree",
            "full_degree_output_bits", "output_bits_examined",
            "full_degree_fraction", "mismatches_after_deleting_degree_n",
            "mismatch_fraction",
        }
        assert row["output_bits_examined"] == 8 * len(report["parameters"]["plaintext_values"])
    labels = report["outcome_labels"]
    assert labels["H_STRUCT"] in {
        "FALSIFIED_STRUCTURAL_ARITY", "SURVIVED_STRUCTURAL_ARITY", "BLOCKED",
    }
    assert labels["H_PCEA"] in {
        "FALSIFIED_PCEA_SPECIFIC_ARITY", "SURVIVED_PCEA_SPECIFIC_ARITY", "UNRESOLVED",
    }
    assert labels["H_HARD"] == "UNRESOLVED"
# ratios: loc_comments=72:6 imports_exports=9:6 calls_definitions=27:9
