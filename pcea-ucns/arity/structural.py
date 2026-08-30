# ratios: loc_comments=117:87 imports_exports=9:14 calls_definitions=86:22
# GPT/Claude generated; context, prompt Erin Spencer
"""Exact Boolean ANF microscope and Actor A result writer.

The analyzer enumerates the frozen binary contributor cube exactly, computes
ANF/Mobius coefficients for each output bit, and writes only the preregistered
Actor A artifacts reached by the frozen escalation rule.
"""

# === MODULE_BUILD ===
# id: pcea_arity_structural
#   module_name: arity structural microscope
#   module_kind: experiment
#   summary: exact Boolean ANF analyzer and Actor A Phase 1 artifact writer for the frozen arity protocol
#   owner: Actor A / Codex
#   public_surface: anf_coefficients, analyze_variant_arity, run_phase1, write_actor_a_results
#   internal_surface: _variable_count, _bit_table, _classify_phase1, _artifact_hashes
#   auth_boundary: none
#   storage_boundary: write
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests/test_arity_structural.py, tests/test_arity_freeze.py
#   rollout: research_branch_only
#   rollback: remove pcea-ucns/arity generated structural files and tests/test_arity_*.py
#   requires: pcea_arity_candidate
#   since: 2026-08-30
#   unresolved: attack scaling is emitted only if the frozen Phase-3 gate opens
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: arity_anf_mobius_computes_exact_degree_terms
#   given: a complete Boolean truth table with power-of-two length
#   then:  anf_coefficients returns exact GF(2) coefficients and reconstruct_truth restores the table
#   class: correctness
#
# id: arity_structural_metrics_follow_frozen_protocol
#   given: PCEA/PRF variants are evaluated for a frozen arity and plaintext set
#   then:  metrics include maximum degree, full-degree count, examined bits, full-degree fraction, deletion mismatches, and mismatch fraction
#   class: evidence
#
# id: arity_outcome_labels_use_preregistered_vocabulary
#   given: Actor A Phase 1 classification is emitted
#   then:  each label is one of the vocabularies recorded in freeze.json
#   class: safety
#
# id: arity_actor_lock_hashes_reached_artifacts
#   given: Actor A result artifacts are written
#   then:  ACTOR_A_LOCK.json records F0/F1 receipts, PHASE3 gate hash, artifact hashes, labels, deviations, and hmmm
#   class: evidence
# === END CONTRACTS ===

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ARITY_DIR = Path(__file__).resolve().parent
if str(ARITY_DIR) not in sys.path:
    sys.path.insert(0, str(ARITY_DIR))

import candidate  # noqa: E402

STRUCTURAL_SCHEMA = "pcea-arity-structural-results-A-v1"
GATE_SCHEMA = "pcea-arity-phase3-gate-v1"
LOCK_SCHEMA = "pcea-arity-actor-lock-v1"


def _variable_count(table: list[int]) -> int:
    length = len(table)
    if length == 0 or length & (length - 1):
        raise ValueError("truth table length must be a non-zero power of two")
    return length.bit_length() - 1


def anf_coefficients(truth_table: list[int]) -> list[int]:
    variables = _variable_count(truth_table)
    coeffs = [value & 1 for value in truth_table]
    for bit in range(variables):
        step = 1 << bit
        for mask in range(1 << variables):
            if mask & step:
                coeffs[mask] ^= coeffs[mask ^ step]
    return coeffs


def reconstruct_truth(coefficients: list[int]) -> list[int]:
    variables = _variable_count(coefficients)
    table = [value & 1 for value in coefficients]
    for bit in range(variables):
        step = 1 << bit
        for mask in range(1 << variables):
            if mask & step:
                table[mask] ^= table[mask ^ step]
    return table


def algebraic_degree(coefficients: list[int]) -> int:
    return max((mask.bit_count() for mask, coeff in enumerate(coefficients) if coeff), default=0)


def remove_full_degree(coefficients: list[int]) -> list[int]:
    variables = _variable_count(coefficients)
    reduced = coefficients[:]
    reduced[(1 << variables) - 1] = 0
    return reduced


def _bit_table(words: list[int], bit: int) -> list[int]:
    return [(word >> bit) & 1 for word in words]


def _output_word(value: int, word_bits: int) -> int:
    return value & ((1 << word_bits) - 1)


def analyze_variant_arity(
    variant: str,
    arity: int,
    plaintext_values: tuple[int, ...] = candidate.PLAINTEXT_VALUES,
    word_bits: int = candidate.WORD_BITS,
    target_circle: int = candidate.TARGET_CIRCLE,
    target_tensor: int = candidate.TARGET_TENSOR,
    seed_idx: int = candidate.SEED_INDEX,
) -> dict[str, Any]:
    candidate.validate_variant(variant)
    candidate.validate_arity(arity)
    full_degree_bits: list[dict[str, int]] = []
    per_plaintext: list[dict[str, Any]] = []
    max_degree = 0
    full_degree_count = 0
    mismatches = 0
    assignments = 1 << arity

    for plaintext in plaintext_values:
        words = [
            _output_word(
                candidate.evaluate_cell(
                    variant,
                    arity,
                    plaintext,
                    mask,
                    seed_idx,
                    target_circle,
                    target_tensor,
                    word_bits,
                ),
                word_bits,
            )
            for mask in range(assignments)
        ]
        plaintext_full_degree = 0
        plaintext_max_degree = 0
        plaintext_mismatches = 0
        for bit in range(word_bits):
            truth = _bit_table(words, bit)
            coeffs = anf_coefficients(truth)
            degree = algebraic_degree(coeffs)
            max_degree = max(max_degree, degree)
            plaintext_max_degree = max(plaintext_max_degree, degree)
            if coeffs[-1]:
                full_degree_count += 1
                plaintext_full_degree += 1
                if len(full_degree_bits) < 50:
                    full_degree_bits.append({"plaintext": plaintext, "bit": bit})
            reconstructed = reconstruct_truth(remove_full_degree(coeffs))
            bit_mismatches = sum(1 for expected, actual in zip(truth, reconstructed) if expected != actual)
            mismatches += bit_mismatches
            plaintext_mismatches += bit_mismatches
        per_plaintext.append(
            {
                "plaintext": plaintext,
                "maximum_algebraic_degree": plaintext_max_degree,
                "full_degree_output_bits": plaintext_full_degree,
                "mismatches_after_deleting_degree_n": plaintext_mismatches,
            }
        )

    output_bits_examined = len(plaintext_values) * word_bits
    total_truth_bits = output_bits_examined * assignments
    return {
        "variant": variant,
        "arity": arity,
        "contributors": candidate.contributor_labels(arity),
        "metrics": {
            "maximum_algebraic_degree": max_degree,
            "full_degree_output_bits": full_degree_count,
            "output_bits_examined": output_bits_examined,
            "full_degree_fraction": full_degree_count / output_bits_examined,
            "mismatches_after_deleting_degree_n": mismatches,
            "mismatch_fraction": mismatches / total_truth_bits,
        },
        "per_plaintext": per_plaintext,
        "full_degree_bits_sample": full_degree_bits,
    }


def _classify_phase1(analyses: list[dict[str, Any]]) -> tuple[dict[str, str], list[str]]:
    by_key = {(item["variant"], item["arity"]): item for item in analyses}
    reasons: list[str] = []
    try:
        high_pcea_has_full = any(
            by_key[("pcea", arity)]["metrics"]["full_degree_output_bits"] > 0
            for arity in (5, 7)
        )
    except KeyError:
        return {"H_STRUCT": "BLOCKED", "H_PCEA": "UNRESOLVED", "H_HARD": "UNRESOLVED"}, [
            "missing required PCEA high-arity structural result"
        ]

    h_struct = "SURVIVED_STRUCTURAL_ARITY" if high_pcea_has_full else "FALSIFIED_STRUCTURAL_ARITY"
    pcea_specific = False
    for arity in (5, 7):
        pcea_metrics = by_key[("pcea", arity)]["metrics"]
        prf_metrics = by_key[("prf", arity)]["metrics"]
        pcea_full = pcea_metrics["full_degree_output_bits"] > 0
        prf_full = prf_metrics["full_degree_output_bits"] > 0
        if pcea_full and not prf_full:
            pcea_specific = True
            reasons.append(f"PCEA-A{arity} has full-degree presence while PRF-A{arity} lacks it")
        elif pcea_metrics["maximum_algebraic_degree"] >= prf_metrics["maximum_algebraic_degree"] + 2:
            pcea_specific = True
            reasons.append(f"PCEA-A{arity} maximum degree exceeds PRF-A{arity} by at least two")
        elif pcea_full and prf_full:
            reasons.append(f"PCEA-A{arity} and PRF-A{arity} both show full-degree presence")
        else:
            reasons.append(f"PCEA-A{arity} does not exceed matched PRF-A{arity} under frozen equality rules")

    h_pcea = "SURVIVED_PCEA_SPECIFIC_ARITY" if pcea_specific else "FALSIFIED_PCEA_SPECIFIC_ARITY"
    return {"H_STRUCT": h_struct, "H_PCEA": h_pcea, "H_HARD": "UNRESOLVED"}, reasons


def run_phase1() -> dict[str, Any]:
    analyses = [
        analyze_variant_arity(variant, arity)
        for variant in candidate.VARIANTS
        for arity in candidate.ARITIES
    ]
    labels, reasons = _classify_phase1(analyses)
    label_errors = candidate.validate_outcome_labels(labels)
    if label_errors:
        raise ValueError("; ".join(label_errors))
    return {
        "schema": STRUCTURAL_SCHEMA,
        "phase": "PHASE1_EXACT_STRUCTURAL_MICROSCOPE",
        "F0_baseline_commit": candidate.baseline_receipt()["baseline_commit"],
        "parameters": candidate.frozen_parameters(),
        "analyses": analyses,
        "classification_reasons": reasons,
        "outcome_labels": labels,
        "claim_rule": "ANF degree is a structural diagnostic, not a cryptographic security metric.",
    }


def phase3_authorized(labels: dict[str, str]) -> bool:
    return (
        labels.get("H_STRUCT") == "SURVIVED_STRUCTURAL_ARITY"
        and labels.get("H_PCEA") == "SURVIVED_PCEA_SPECIFIC_ARITY"
    )


def phase3_gate_document(f1_sha: str, structural_results: dict[str, Any]) -> dict[str, Any]:
    freeze = candidate.read_json(candidate.FREEZE_PATH)
    return {
        "schema": GATE_SCHEMA,
        "F0_baseline_commit": candidate.baseline_receipt()["baseline_commit"],
        "F1_candidate_commit": f1_sha,
        "freeze_json_sha256": candidate.sha256_path(candidate.FREEZE_PATH),
        "authorized": phase3_authorized(structural_results["outcome_labels"]),
        "criterion": freeze["escalation_rules"]["phase3"],
        "issuer": "Actor A / Codex",
    }


def report_markdown(structural_results: dict[str, Any], gate: dict[str, Any]) -> str:
    lines = [
        "# Actor A Report - PCEA Arity v1",
        "",
        "Role: Actor A / Codex.",
        "",
        "Boundary: this report records the preregistered structural microscope only. It is not a cryptographic security claim.",
        "",
        "## Phase Reached",
        "",
        "PHASE1_EXACT_STRUCTURAL_MICROSCOPE",
        "",
        "## Outcome Labels",
        "",
    ]
    for key, value in structural_results["outcome_labels"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Phase 3 Gate",
            "",
            f"- authorized: {str(gate['authorized']).lower()}",
            f"- criterion: {gate['criterion']}",
            "",
            "## Structural Metrics",
            "",
            "| variant | arity | max degree | full-degree bits | examined bits | mismatch fraction |",
            "|---|---:|---:|---:|---:|---:|",
        ]
    )
    for item in structural_results["analyses"]:
        m = item["metrics"]
        lines.append(
            f"| {item['variant']} | {item['arity']} | {m['maximum_algebraic_degree']} | "
            f"{m['full_degree_output_bits']} | {m['output_bits_examined']} | {m['mismatch_fraction']:.6f} |"
        )
    lines.extend(["", "## hmmm", ""])
    lines.append("- Direct arity may need richer operationalizations beyond this Boolean ANF microscope.")
    lines.append("- Shared behavior with the matched PRF control is not PCEA-specific evidence.")
    return "\n".join(lines) + "\n"


def _artifact_hashes(paths: list[Path]) -> dict[str, str]:
    return {
        str(path.relative_to(candidate.ROOT)): candidate.sha256_path(path)
        for path in paths
        if path.exists()
    }


def actor_a_lock_document(
    f1_sha: str,
    result_commit_sha: str,
    structural_results: dict[str, Any],
    gate: dict[str, Any],
) -> dict[str, Any]:
    artifacts = [
        candidate.STRUCTURAL_RESULTS_A_PATH,
        candidate.PHASE3_GATE_PATH,
        candidate.REPORT_A_PATH,
    ]
    return {
        "schema": LOCK_SCHEMA,
        "actor": "Codex",
        "role": "A",
        "F0": {
            "baseline_commit": candidate.baseline_receipt()["baseline_commit"],
            "BASELINE_FREEZE_V1_json_sha256": candidate.sha256_path(candidate.BASELINE_PATH),
        },
        "F1": {
            "candidate_commit": f1_sha,
            "freeze_json_sha256": candidate.sha256_path(candidate.FREEZE_PATH),
        },
        "PHASE3_GATE_json_sha256": candidate.sha256_path(candidate.PHASE3_GATE_PATH),
        "actor_result_commit": result_commit_sha,
        "artifact_hashes": _artifact_hashes(artifacts),
        "preregistered_outcome_labels": structural_results["outcome_labels"],
        "deviation_or_contamination": [],
        "hmmm": [
            "H_HARD remains UNRESOLVED unless Phase 3 is reached.",
            "No cryptographic security claim is made from this harness.",
        ],
        "phase_reached": "PHASE1_EXACT_STRUCTURAL_MICROSCOPE",
        "phase3_gate_authorized": gate["authorized"],
    }


def write_actor_a_results(f1_sha: str, result_commit_sha: str = candidate.PENDING_RESULT_SHA) -> dict[str, str]:
    structural_results = run_phase1()
    candidate.write_json(candidate.STRUCTURAL_RESULTS_A_PATH, structural_results)
    gate = phase3_gate_document(f1_sha, structural_results)
    candidate.write_json(candidate.PHASE3_GATE_PATH, gate)
    candidate.REPORT_A_PATH.write_text(report_markdown(structural_results, gate), encoding="utf-8")
    candidate.LOCKS_DIR.mkdir(parents=True, exist_ok=True)
    candidate.write_json(
        candidate.ACTOR_A_LOCK_PATH,
        actor_a_lock_document(f1_sha, result_commit_sha, structural_results, gate),
    )
    return {
        "structural_results_A": candidate.sha256_path(candidate.STRUCTURAL_RESULTS_A_PATH),
        "PHASE3_GATE": candidate.sha256_path(candidate.PHASE3_GATE_PATH),
        "REPORT_A": candidate.sha256_path(candidate.REPORT_A_PATH),
        "ACTOR_A_LOCK": candidate.sha256_path(candidate.ACTOR_A_LOCK_PATH),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="PCEA arity v1 structural utility")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("phase1")
    write_results = sub.add_parser("write-results")
    write_results.add_argument("--f1-sha", required=True)
    write_results.add_argument("--result-commit-sha", default=candidate.PENDING_RESULT_SHA)
    args = parser.parse_args(argv)

    if args.command == "phase1":
        print(json.dumps(run_phase1(), indent=2, sort_keys=True))
        return 0
    if args.command == "write-results":
        print(json.dumps(write_actor_a_results(args.f1_sha, args.result_commit_sha), indent=2, sort_keys=True))
        return 0
    raise AssertionError(args.command)


if __name__ == "__main__":
    raise SystemExit(main())
# ratios: loc_comments=117:87 imports_exports=9:14 calls_definitions=86:22
