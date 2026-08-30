# ratios: loc_comments=156:118 imports_exports=17:28 calls_definitions=132:31
# GPT/Claude generated; context, prompt Erin Spencer
"""Research-only arity adapters and freeze artifact writer for PCEA v1.

This module is intentionally outside the runtime package. It gives the arity
protocol deterministic candidate adapters, matched PRF controls, fixture
generation, dependency graph emission, and receipt verification without
changing ``pcea/**``.
"""

# === MODULE_BUILD ===
# id: pcea_arity_candidate
#   module_name: arity candidate
#   module_kind: experiment
#   summary: research-only PCEA/PRF arity adapters plus deterministic freeze artifact generation
#   owner: Actor A / Codex
#   public_surface: evaluate_cell, pcea_encrypt_cell, prf_encrypt_cell, fixture_document, dependency_graph_document, freeze_document, write_freeze_artifacts
#   internal_surface: _git, _fixed_digits, _signed_fixture_value, _hmac_key_stream
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_arity_current_baseline.py, tests/test_arity_freeze.py
#   rollout: research_branch_only
#   rollback: remove pcea-ucns/arity generated candidate files and tests/test_arity_*.py
#   requires: pcea_cipher, pcea_codec, pcea_kdf, pcea_primes
#   since: 2026-08-30
#   unresolved: direct arity operationalization remains Boolean ANF microscope only
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: arity_a3_adapter_matches_runtime_pcea
#   given: PCEA-A3 adapter receives deterministic valid 7x7 seed and last_seed fixtures
#   then:  adapter output is byte-for-byte equal to pcea.cipher.encrypt_seed for the same inputs
#   class: regression
#
# id: arity_freeze_verifies_f0_runtime_identity
#   given: BASELINE_FREEZE_V1.json names frozen runtime blob ids and baseline commit
#   then:  verifier reports no mismatch for baseline commit and current runtime worktree content
#   class: evidence
#
# id: arity_fixtures_are_deterministic_and_versioned
#   given: fixture_document is called repeatedly without code changes
#   then:  it emits schema-versioned deterministic fixtures with frozen protocol parameters
#   class: reproducibility
#
# id: arity_dependency_graph_records_triadic_runtime_relation
#   given: current dependency graph is emitted for every encrypted cell
#   then:  every cell records plaintext, address, prime/base, hash/KDF, and exactly three prior-state contributors
#   class: evidence
#
# id: arity_phase3_gate_is_outcome_blind
#   given: PHASE3_GATE.json is emitted after Phase 1
#   then:  it contains only identity, receipt, authorization, criterion, and issuer fields without structural metrics
#   class: safety
# === END CONTRACTS ===

from __future__ import annotations

import argparse
import hashlib
import hmac
import json
import platform
import subprocess
import sys
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from pcea.cipher import CIRCLE_COUNT, TENSOR_COUNT, encrypt_seed  # noqa: E402
from pcea.codec import digit_count, from_fixed, mobius_encode, to_fixed  # noqa: E402
from pcea.kdf import key_stream  # noqa: E402
from pcea.primes import prime_at  # noqa: E402

ARITY_DIR = Path(__file__).resolve().parent
BASELINE_PATH = ARITY_DIR / "BASELINE_FREEZE_V1.json"
FIXTURES_PATH = ARITY_DIR / "fixtures.json"
GRAPH_PATH = ARITY_DIR / "current_dependency_graph.json"
FREEZE_PATH = ARITY_DIR / "freeze.json"
PHASE3_GATE_PATH = ARITY_DIR / "PHASE3_GATE.json"
STRUCTURAL_RESULTS_A_PATH = ARITY_DIR / "structural_results_A.json"
REPORT_A_PATH = ARITY_DIR / "REPORT_A.md"
LOCKS_DIR = ARITY_DIR / "locks"
ACTOR_A_LOCK_PATH = LOCKS_DIR / "ACTOR_A_LOCK.json"

SCHEMA = "pcea-arity-candidate-v1"
FIXTURE_SCHEMA = "pcea-arity-fixtures-v1"
DEPENDENCY_GRAPH_SCHEMA = "pcea-arity-current-dependency-graph-v1"
FREEZE_SCHEMA = "pcea-arity-freeze-v1"
PENDING_F1_SHA = "PENDING_F1_SHA_UNTIL_CANDIDATE_COMMIT"
PENDING_RESULT_SHA = "PENDING_ACTOR_A_RESULT_COMMIT"

OFFSETS: tuple[int, ...] = (0, -3, 3, -1, 1, -2, 2)
ARITIES: tuple[int, ...] = (2, 3, 5, 7)
VARIANTS: tuple[str, ...] = ("pcea", "prf")
PLAINTEXT_VALUES: tuple[int, ...] = (0, 1, -1, 2, 127)
WORD_BITS = 8
TARGET_CIRCLE = 0
TARGET_TENSOR = 0
SEED_INDEX = 0
NON_CONTRIBUTOR_VALUE = 0
CONTROL_SECRET = b"pcea-arity-v1|matched-prf-control"
SECRET_BITS: tuple[int, ...] = (8, 12)
SECRET_TRIALS = 16

STRUCTURAL_LABELS = frozenset(
    {
        "FALSIFIED_STRUCTURAL_ARITY",
        "SURVIVED_STRUCTURAL_ARITY",
        "BLOCKED",
    }
)
PCEA_LABELS = frozenset(
    {
        "FALSIFIED_PCEA_SPECIFIC_ARITY",
        "SURVIVED_PCEA_SPECIFIC_ARITY",
        "UNRESOLVED",
    }
)
HARDNESS_LABELS = frozenset(
    {
        "FALSIFIED_ARITY_HARDNESS_BENEFIT",
        "SURVIVED_CURRENT_HARNESS",
        "UNRESOLVED",
    }
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, document: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(document, indent=2, sort_keys=True)
    path.write_text(payload + "\n", encoding="utf-8")


def sha256_path(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def _git(args: Iterable[str]) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def git_blob_sha(commit: str, path: str) -> str | None:
    output = _git(["ls-tree", "-r", commit, "--", path])
    if not output:
        return None
    parts = output.split()
    return parts[2] if len(parts) >= 3 else None


def current_worktree_blob_sha(path: str) -> str:
    return _git(["hash-object", path])


def current_head_sha() -> str:
    return _git(["rev-parse", "HEAD"])


def baseline_receipt() -> dict[str, Any]:
    return read_json(BASELINE_PATH)


def verify_baseline_commit_blobs() -> dict[str, Any]:
    receipt = baseline_receipt()
    commit = receipt["baseline_commit"]
    checked: dict[str, str] = {}
    mismatches: list[dict[str, str | None]] = []
    for group_name in ("frozen_runtime_paths", "frozen_metadata_paths"):
        for path, expected in receipt[group_name].items():
            actual = git_blob_sha(commit, path)
            checked[path] = actual or ""
            if actual != expected:
                mismatches.append(
                    {
                        "path": path,
                        "group": group_name,
                        "expected": expected,
                        "actual": actual,
                    }
                )
    return {
        "schema": "pcea-arity-baseline-verification-v1",
        "baseline_commit": commit,
        "ok": not mismatches,
        "checked": checked,
        "mismatches": mismatches,
        "blocked_status": "" if not mismatches else "BLOCKED_FREEZE_DRIFT",
    }


def verify_current_runtime_blobs() -> dict[str, Any]:
    receipt = baseline_receipt()
    checked: dict[str, str] = {}
    mismatches: list[dict[str, str]] = []
    for path, expected in receipt["frozen_runtime_paths"].items():
        actual = current_worktree_blob_sha(path)
        checked[path] = actual
        if actual != expected:
            mismatches.append({"path": path, "expected": expected, "actual": actual})
    return {
        "schema": "pcea-arity-current-runtime-verification-v1",
        "baseline_commit": receipt["baseline_commit"],
        "ok": not mismatches,
        "checked": checked,
        "mismatches": mismatches,
        "blocked_status": "" if not mismatches else "BLOCKED_FREEZE_DRIFT",
    }


def validate_arity(arity: int) -> None:
    if arity not in ARITIES:
        raise ValueError(f"arity must be one of {ARITIES}")


def validate_variant(variant: str) -> None:
    if variant not in VARIANTS:
        raise ValueError(f"variant must be one of {VARIANTS}")


def offsets_for_arity(arity: int) -> tuple[int, ...]:
    validate_arity(arity)
    return OFFSETS[:arity]


def contributor_labels(arity: int) -> list[str]:
    return [f"circle{offset:+d}" for offset in offsets_for_arity(arity)]


def blank_seed(value: int = 0) -> list[list[int]]:
    return [[value for _ in range(TENSOR_COUNT)] for _ in range(CIRCLE_COUNT)]


def contributors_from_last_seed(
    last_seed: list[list[int]],
    arity: int,
    circle_idx: int,
    tensor_idx: int,
) -> list[int]:
    return [
        last_seed[(circle_idx + offset) % CIRCLE_COUNT][tensor_idx]
        for offset in offsets_for_arity(arity)
    ]


def last_seed_for_assignment(
    arity: int,
    assignment_mask: int,
    target_circle: int = TARGET_CIRCLE,
    target_tensor: int = TARGET_TENSOR,
    non_contributor_value: int = NON_CONTRIBUTOR_VALUE,
) -> list[list[int]]:
    validate_arity(arity)
    if assignment_mask < 0 or assignment_mask >= (1 << arity):
        raise ValueError("assignment_mask outside arity truth-table range")
    last_seed = blank_seed(non_contributor_value)
    for bit_index, offset in enumerate(offsets_for_arity(arity)):
        circle = (target_circle + offset) % CIRCLE_COUNT
        last_seed[circle][target_tensor] = (assignment_mask >> bit_index) & 1
    return last_seed


def _fixed_digits(value: int, circle_idx: int, tensor_idx: int, word_bits: int) -> tuple[int, int, list[int]]:
    p = prime_at(circle_idx * TENSOR_COUNT + tensor_idx)
    width = digit_count(p, word_bits)
    encoded = mobius_encode(value, word_bits)
    return p, width, to_fixed(encoded, p, width)


def pcea_encrypt_cell(
    value: int,
    last_seed: list[list[int]],
    arity: int,
    seed_idx: int = SEED_INDEX,
    circle_idx: int = TARGET_CIRCLE,
    tensor_idx: int = TARGET_TENSOR,
    word_bits: int = WORD_BITS,
) -> int:
    p, width, digits = _fixed_digits(value, circle_idx, tensor_idx, word_bits)
    contributors = contributors_from_last_seed(last_seed, arity, circle_idx, tensor_idx)
    stream = key_stream(contributors, seed_idx, circle_idx, tensor_idx, width, p)
    return from_fixed([(digit + key_digit) % p for digit, key_digit in zip(digits, stream)], p)


def _hmac_key_stream(
    contributors: list[int],
    seed_idx: int,
    circle_idx: int,
    tensor_idx: int,
    length: int,
    p: int,
) -> list[int]:
    raw = bytearray()
    counter = 0
    while len(raw) < length:
        payload = json.dumps(
            {
                "schema": SCHEMA,
                "variant": "prf-control",
                "contributors": contributors,
                "seed_idx": seed_idx,
                "circle_idx": circle_idx,
                "tensor_idx": tensor_idx,
                "counter": counter,
            },
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        raw.extend(hmac.new(CONTROL_SECRET, payload, hashlib.sha256).digest())
        counter += 1
    return [byte % p for byte in raw[:length]]


def prf_encrypt_cell(
    value: int,
    last_seed: list[list[int]],
    arity: int,
    seed_idx: int = SEED_INDEX,
    circle_idx: int = TARGET_CIRCLE,
    tensor_idx: int = TARGET_TENSOR,
    word_bits: int = WORD_BITS,
) -> int:
    p, width, digits = _fixed_digits(value, circle_idx, tensor_idx, word_bits)
    contributors = contributors_from_last_seed(last_seed, arity, circle_idx, tensor_idx)
    stream = _hmac_key_stream(contributors, seed_idx, circle_idx, tensor_idx, width, p)
    return from_fixed([(digit + key_digit) % p for digit, key_digit in zip(digits, stream)], p)


def evaluate_cell(
    variant: str,
    arity: int,
    plaintext: int,
    assignment_mask: int,
    seed_idx: int = SEED_INDEX,
    circle_idx: int = TARGET_CIRCLE,
    tensor_idx: int = TARGET_TENSOR,
    word_bits: int = WORD_BITS,
) -> int:
    validate_variant(variant)
    last_seed = last_seed_for_assignment(arity, assignment_mask, circle_idx, tensor_idx)
    if variant == "pcea":
        return pcea_encrypt_cell(plaintext, last_seed, arity, seed_idx, circle_idx, tensor_idx, word_bits)
    return prf_encrypt_cell(plaintext, last_seed, arity, seed_idx, circle_idx, tensor_idx, word_bits)


def pcea_encrypt_seed_adapter(
    seed: list[list[int]],
    last_seed: list[list[int]],
    arity: int,
    seed_idx: int = SEED_INDEX,
    word_bits: int = WORD_BITS,
) -> list[list[int]]:
    validate_arity(arity)
    return [
        [
            pcea_encrypt_cell(seed[c][t], last_seed, arity, seed_idx, c, t, word_bits)
            for t in range(TENSOR_COUNT)
        ]
        for c in range(CIRCLE_COUNT)
    ]


def _signed_fixture_value(label: str, word_bits: int) -> int:
    unsigned = int.from_bytes(hashlib.sha256(label.encode("utf-8")).digest(), "big")
    unsigned %= 1 << word_bits
    half = 1 << (word_bits - 1)
    return unsigned if unsigned < half else unsigned - (1 << word_bits)


def a3_regression_cases(count: int = 4, word_bits: int = WORD_BITS) -> list[dict[str, Any]]:
    cases = []
    for case_idx in range(count):
        seed = [
            [
                _signed_fixture_value(f"pcea-arity-v1|a3-regression|seed|{case_idx}|{c}|{t}", word_bits)
                for t in range(TENSOR_COUNT)
            ]
            for c in range(CIRCLE_COUNT)
        ]
        last_seed = [
            [
                _signed_fixture_value(f"pcea-arity-v1|a3-regression|last|{case_idx}|{c}|{t}", word_bits)
                for t in range(TENSOR_COUNT)
            ]
            for c in range(CIRCLE_COUNT)
        ]
        cases.append(
            {
                "case_id": f"a3_regression_{case_idx}",
                "seed_idx": case_idx,
                "word_bits": word_bits,
                "seed": seed,
                "last_seed": last_seed,
                "runtime_cipher": "pcea.cipher.encrypt_seed",
                "adapter": "PCEA-A3",
            }
        )
    return cases


def structural_assignments() -> dict[str, list[dict[str, Any]]]:
    assignments: dict[str, list[dict[str, Any]]] = {}
    for arity in ARITIES:
        labels = contributor_labels(arity)
        assignments[str(arity)] = [
            {
                "mask": mask,
                "values": {labels[i]: (mask >> i) & 1 for i in range(arity)},
            }
            for mask in range(1 << arity)
        ]
    return assignments


def secret_fixture_seed(secret_bits: int, trial: int) -> int:
    if secret_bits not in SECRET_BITS:
        raise ValueError(f"secret_bits must be one of {SECRET_BITS}")
    if trial < 0 or trial >= SECRET_TRIALS:
        raise ValueError("trial outside frozen range")
    digest = hashlib.sha256(f"pcea-arity-v1|secret-fixture|{secret_bits}|{trial}".encode("utf-8")).digest()
    return int.from_bytes(digest, "big") & ((1 << secret_bits) - 1)


def fixture_document() -> dict[str, Any]:
    return {
        "schema": FIXTURE_SCHEMA,
        "generator_version": "candidate.py:fixtures-v1",
        "parameters": frozen_parameters(),
        "variants": list(VARIANTS),
        "structural_assignments": structural_assignments(),
        "a3_regression_cases": a3_regression_cases(),
        "phase3_secret_fixtures": [
            {
                "secret_bits": bits,
                "trial": trial,
                "fixture_seed_derivation": f"SHA256('pcea-arity-v1|secret-fixture|{bits}|{trial}')",
                "secret_seed_int": secret_fixture_seed(bits, trial),
            }
            for bits in SECRET_BITS
            for trial in range(SECRET_TRIALS)
        ],
    }


def dependency_graph_document() -> dict[str, Any]:
    cells = []
    for circle in range(CIRCLE_COUNT):
        for tensor in range(TENSOR_COUNT):
            p = prime_at(circle * TENSOR_COUNT + tensor)
            cells.append(
                {
                    "seed_idx": "all",
                    "circle_idx": circle,
                    "tensor_idx": tensor,
                    "current_plaintext_dependency": {
                        "path": f"state[seed_idx][{circle}][{tensor}]",
                        "transform": "mobius_encode -> to_fixed -> additive digit shift",
                    },
                    "prior_state_contributor_dependency": [
                        {
                            "order": order,
                            "offset": offset,
                            "path": f"last_state[seed_idx][{(circle + offset) % CIRCLE_COUNT}][{tensor}]",
                        }
                        for order, offset in enumerate(offsets_for_arity(3))
                    ],
                    "address_dependency": {
                        "seed_idx": "included in key_stream payload",
                        "circle_idx": circle,
                        "tensor_idx": tensor,
                    },
                    "prime_base_dependency": {
                        "source": "pcea.primes.prime_at(circle_idx * TENSOR_COUNT + tensor_idx)",
                        "prime_index": circle * TENSOR_COUNT + tensor,
                        "prime": p,
                        "digit_count_at_word_bits_8": digit_count(p, WORD_BITS),
                    },
                    "hash_kdf_dependency": {
                        "source": "pcea.kdf.key_stream",
                        "payload_fields": [
                            "contributors",
                            "seed_idx",
                            "circle_idx",
                            "tensor_idx",
                            "counter",
                        ],
                    },
                }
            )
    return {
        "schema": DEPENDENCY_GRAPH_SCHEMA,
        "source": "pcea/cipher.py::_contributors + _encrypt_element",
        "verified_state_key_relation": {
            "state_key_direct_arity": 3,
            "contributors": ["circle", "circle-3 mod 7", "circle+3 mod 7"],
            "seven_circle_topology": "overlapping local triadic relations",
            "interpretation": "current PCEA is A3 state-key baseline, not direct A7",
        },
        "cells": cells,
    }


def frozen_parameters() -> dict[str, Any]:
    return {
        "offsets": list(OFFSETS),
        "arities": list(ARITIES),
        "plaintext_values": list(PLAINTEXT_VALUES),
        "word_bits": WORD_BITS,
        "target_circle": TARGET_CIRCLE,
        "target_tensor": TARGET_TENSOR,
        "seed_index": SEED_INDEX,
        "non_contributor_value": NON_CONTRIBUTOR_VALUE,
        "secret_bits": list(SECRET_BITS),
        "secret_trials": SECRET_TRIALS,
    }


def freeze_document(f1_sha: str = PENDING_F1_SHA) -> dict[str, Any]:
    receipt = baseline_receipt()
    return {
        "schema": FREEZE_SCHEMA,
        "status": "F1_CANDIDATE_FREEZE_PRE_EXECUTION",
        "repository": receipt["repository"],
        "F0": {
            "baseline_commit": receipt["baseline_commit"],
            "baseline_tree": receipt["baseline_tree"],
            "baseline_receipt_path": "pcea-ucns/arity/BASELINE_FREEZE_V1.json",
            "baseline_receipt_sha256": sha256_path(BASELINE_PATH),
            "frozen_runtime_paths": receipt["frozen_runtime_paths"],
        },
        "F1": {
            "candidate_commit": f1_sha,
            "candidate_commit_rule": "Initial freeze may use PENDING until immediate metadata-only correction records the F1 commit SHA.",
            "allowed_paths": [
                "pcea-ucns/arity/**",
                "tests/test_arity_*.py",
            ],
        },
        "environment": {
            "python_version": platform.python_version(),
            "platform": platform.platform(),
        },
        "research_code": {
            "candidate_py_sha256": sha256_path(ARITY_DIR / "candidate.py"),
            "structural_py_sha256": sha256_path(ARITY_DIR / "structural.py"),
        },
        "artifact_receipts": {
            "fixtures_json_sha256": sha256_path(FIXTURES_PATH),
            "current_dependency_graph_json_sha256": sha256_path(GRAPH_PATH),
        },
        "fixture_generator_version": "candidate.py:fixtures-v1",
        "parameters": frozen_parameters(),
        "candidate_adapters": {
            f"PCEA-A{arity}": {
                "variant": "pcea",
                "contributors": contributor_labels(arity),
                "notes": "A3 matches runtime PCEA; other arities are research-only adapter variants.",
            }
            for arity in ARITIES
        },
        "matched_controls": {
            f"PRF-A{arity}": {
                "variant": "prf",
                "contributors": contributor_labels(arity),
                "hash": "HMAC-SHA256",
                "domain": "same plaintext/address/output-width/base-p digit shift surface as PCEA adapter",
            }
            for arity in ARITIES
        },
        "metrics": [
            "maximum_algebraic_degree",
            "full_degree_output_bits",
            "output_bits_examined",
            "full_degree_fraction",
            "mismatches_after_deleting_degree_n",
            "mismatch_fraction",
        ],
        "outcome_label_vocabulary": {
            "H_STRUCT": sorted(STRUCTURAL_LABELS),
            "H_PCEA": sorted(PCEA_LABELS),
            "H_HARD": sorted(HARDNESS_LABELS),
        },
        "pcea_specific_equality_rules": [
            "Descriptive count/fraction differences alone are not material separation.",
            "For A5/A7, PCEA-specific separation requires PCEA full-degree presence when the matched PRF lacks it, or PCEA maximum degree at least two above the matched PRF.",
            "If PCEA and matched PRF both show full-degree presence for a high arity, the shared behavior is not classified as PCEA-specific.",
        ],
        "escalation_rules": {
            "phase2": "authorized only when H_STRUCT == SURVIVED_STRUCTURAL_ARITY and H_PCEA == SURVIVED_PCEA_SPECIFIC_ARITY",
            "phase3": "authorized only when H_STRUCT == SURVIVED_STRUCTURAL_ARITY and H_PCEA == SURVIVED_PCEA_SPECIFIC_ARITY",
        },
        "claim_rule": "No structural or attack survival result is a cryptographic security claim.",
        "hmmm": [
            "Boolean ANF full-degree residual is one exact operationalization of direct arity, not a universal definition.",
            "A PCEA-specific structural residual would still need an attack consequence before any hardness claim.",
        ],
    }


def write_freeze_artifacts(f1_sha: str = PENDING_F1_SHA) -> dict[str, str]:
    write_json(FIXTURES_PATH, fixture_document())
    write_json(GRAPH_PATH, dependency_graph_document())
    write_json(FREEZE_PATH, freeze_document(f1_sha))
    return {
        "fixtures": sha256_path(FIXTURES_PATH),
        "current_dependency_graph": sha256_path(GRAPH_PATH),
        "freeze": sha256_path(FREEZE_PATH),
    }


def runtime_encrypt_for_a3_fixture(case: dict[str, Any]) -> list[list[int]]:
    return encrypt_seed(case["seed"], case["last_seed"], case["seed_idx"], case["word_bits"])


def adapter_encrypt_for_a3_fixture(case: dict[str, Any]) -> list[list[int]]:
    return pcea_encrypt_seed_adapter(case["seed"], case["last_seed"], 3, case["seed_idx"], case["word_bits"])


def is_valid_sha_or_pending(value: str, pending: str = PENDING_F1_SHA) -> bool:
    return value == pending or (len(value) == 40 and all(ch in "0123456789abcdef" for ch in value))


def validate_outcome_labels(labels: dict[str, str]) -> list[str]:
    errors = []
    vocab = {
        "H_STRUCT": STRUCTURAL_LABELS,
        "H_PCEA": PCEA_LABELS,
        "H_HARD": HARDNESS_LABELS,
    }
    for key, value in labels.items():
        if key not in vocab:
            errors.append(f"unknown outcome key: {key}")
        elif value not in vocab[key]:
            errors.append(f"{key} label outside preregistered vocabulary: {value}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PCEA arity v1 candidate/freeze utility")
    sub = parser.add_subparsers(dest="command", required=True)
    write_freeze = sub.add_parser("write-freeze")
    write_freeze.add_argument("--f1-sha", default=PENDING_F1_SHA)
    sub.add_parser("verify-baseline")
    sub.add_parser("verify-current-runtime")
    args = parser.parse_args(argv)

    if args.command == "write-freeze":
        print(json.dumps(write_freeze_artifacts(args.f1_sha), indent=2, sort_keys=True))
        return 0
    if args.command == "verify-baseline":
        result = verify_baseline_commit_blobs()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["ok"] else 1
    if args.command == "verify-current-runtime":
        result = verify_current_runtime_blobs()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["ok"] else 1
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
# ratios: loc_comments=156:118 imports_exports=17:28 calls_definitions=132:31
