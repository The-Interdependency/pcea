# ratios: loc_comments=183:39 imports_exports=6:2 calls_definitions=44:9
# GPT/Claude generated; context, prompt Erin Spencer
"""Actor B Phase-1 exact structural microscope runner.

Reads the frozen deterministic fixtures, reconstructs the PCEA-A_n and PRF-A_n
truth tables for every plaintext value, computes exact Boolean ANF metrics per
output bit, and classifies H-STRUCT and H-PCEA with the frozen preregistered
rules. Writes ``replay_results_B.json`` next to the fixtures.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

_REPLAY_DIR = Path(__file__).resolve().parent
if str(_REPLAY_DIR) not in sys.path:
    sys.path.insert(0, str(_REPLAY_DIR))

from adapters import pcea_cell, prf_cell  # noqa: E402  (B namespace import)
from anf import (  # noqa: E402  (B namespace import)
    anf_degree,
    delete_full_degree_mismatches,
    full_degree_coefficient,
    mobius_transform,
)

# === MODULE_BUILD ===
# id: replay_b_runner
#   module_name: runner
#   module_kind: research
#   summary: Phase-1 exact structural microscope runner for Actor B; emits replay_results_B.json and outcome labels
#   owner: Actor B (DeepSeek) replay
#   public_surface: run_phase1, classify_outcomes
#   internal_surface: _load_fixtures, _load_freeze, _assignments, _last_seed_for_assignment, _offset_for_label, _bits, _row_for
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_arity_replay_b
#   rollout: research_only
#   rollback: remove module and its references
#   requires: pcea_ucns_arity_replay_b_adapters, pcea_ucns_arity_replay_b_anf
#   since: 2026-08-30
#   unresolved: PRF interpretation decisions are documented in adapters.py and REPORT_B.md
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: phase1_uses_frozen_parameters
#   given: run_phase1 executes
#   then:  every row uses the frozen parameters from fixtures.json, not runner-local overrides
#   class: correctness
# === END CONTRACTS ===

FIXTURES_PATH = Path(__file__).resolve().parent.parent / "fixtures.json"
FREEZE_PATH = Path(__file__).resolve().parent.parent / "freeze.json"
RESULTS_PATH = Path(__file__).resolve().parent.parent / "replay_results_B.json"

# Coordinator-provided F1 candidate-freeze identity. The on-disk freeze.json at
# the F1 commit itself still carries the PENDING marker by design; the
# metadata-only correction commit records the F1 SHA.
F1_CANDIDATE_COMMIT = "e5fb94defae29a4c1b6d3e796763d575b34e4c08"

ARITIES = (2, 3, 5, 7)
VARIANTS = ("pcea", "prf")


def _load_fixtures() -> dict:
    with FIXTURES_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _load_freeze() -> dict:
    with FREEZE_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def _assignments(fixtures: dict, arity: int) -> list[dict]:
    """Frozen structural assignments for one arity, sorted by mask."""
    entries = fixtures["structural_assignments"][str(arity)]
    return sorted(entries, key=lambda entry: entry["mask"])


def _last_seed_for_assignment(assignment: dict, fixtures: dict) -> list[list[int]]:
    """7x7 last_seed with contributor cells set and all others frozen at 0."""
    non_contributor = fixtures["parameters"]["non_contributor_value"]
    last_seed = [[non_contributor for _ in range(7)] for _ in range(7)]
    for label, value in assignment["values"].items():
        offset = _offset_for_label(label)
        circle = (0 + offset) % 7
        last_seed[circle][0] = value
    return last_seed


def _offset_for_label(label: str) -> int:
    label_to_offset = {
        "circle+0": 0,
        "circle-3": -3,
        "circle+3": 3,
        "circle-1": -1,
        "circle+1": 1,
        "circle-2": -2,
        "circle+2": 2,
    }
    if label not in label_to_offset:
        raise ValueError(f"unknown contributor label: {label}")
    return label_to_offset[label]


def _bits(value: int, word_bits: int) -> list[int]:
    return [(value >> j) & 1 for j in range(word_bits)]


def _row_for(
    variant: str,
    arity: int,
    fixtures: dict,
) -> dict:
    parameters = fixtures["parameters"]
    word_bits = parameters["word_bits"]
    plaintext_values = parameters["plaintext_values"]
    assignments = _assignments(fixtures, arity)
    n = arity
    expected = 1 << n
    if len(assignments) != expected or [a["mask"] for a in assignments] != list(range(expected)):
        raise ValueError(f"fixture assignments for arity {arity} do not cover all 2^n masks")

    full_degree_bits = 0
    examined_bits = 0
    mismatches = 0
    max_degree = 0
    per_plaintext: dict[int, dict] = {}

    for plaintext in plaintext_values:
        truth_tables: list[list[int]] = []
        for assignment in assignments:
            last_seed = _last_seed_for_assignment(assignment, fixtures)
            if variant == "pcea":
                output = pcea_cell(plaintext, last_seed, 0, 0, 0, word_bits, arity)
            else:
                output = prf_cell(plaintext, last_seed, 0, 0, 0, word_bits, arity)
            for j, bit in enumerate(_bits(output, word_bits)):
                if len(truth_tables) <= j:
                    truth_tables.append([])
                truth_tables[j].append(bit)

        plaintext_full_degree = 0
        plaintext_mismatches = 0
        plaintext_max_degree = 0
        for table in truth_tables:
            examined_bits += 1
            coeffs = mobius_transform(table)
            degree = anf_degree(coeffs)
            plaintext_max_degree = max(plaintext_max_degree, degree)
            if full_degree_coefficient(coeffs, n):
                full_degree_bits += 1
                plaintext_full_degree += 1
            plaintext_mismatches += delete_full_degree_mismatches(table, n)
        mismatches += plaintext_mismatches
        max_degree = max(max_degree, plaintext_max_degree)
        per_plaintext[plaintext] = {
            "full_degree_output_bits": plaintext_full_degree,
            "output_bits_examined": len(truth_tables),
            "mismatches_after_deleting_degree_n": plaintext_mismatches,
            "maximum_algebraic_degree": plaintext_max_degree,
        }

    total_cells = examined_bits * expected
    return {
        "variant": variant,
        "arity": arity,
        "maximum_algebraic_degree": max_degree,
        "full_degree_output_bits": full_degree_bits,
        "output_bits_examined": examined_bits,
        "full_degree_fraction": full_degree_bits / examined_bits if examined_bits else 0.0,
        "mismatches_after_deleting_degree_n": mismatches,
        "mismatch_fraction": mismatches / total_cells if total_cells else 0.0,
        "per_plaintext": per_plaintext,
    }


def classify_outcomes(rows: list[dict]) -> dict:
    """Apply the frozen preregistered classification rules mechanically."""
    by_key = {(row["variant"], row["arity"]): row for row in rows}

    structural_survived = False
    for arity in (5, 7):
        row = by_key.get(("pcea", arity))
        if row and row["full_degree_output_bits"] > 0:
            structural_survived = True

    pcea_separation = False
    comparison_valid = True
    for arity in (5, 7):
        pcea_row = by_key.get(("pcea", arity))
        prf_row = by_key.get(("prf", arity))
        if pcea_row is None or prf_row is None:
            comparison_valid = False
            continue
        pcea_has_full = pcea_row["full_degree_output_bits"] > 0
        prf_has_full = prf_row["full_degree_output_bits"] > 0
        if pcea_has_full and not prf_has_full:
            pcea_separation = True
        if pcea_row["maximum_algebraic_degree"] >= prf_row["maximum_algebraic_degree"] + 2:
            pcea_separation = True

    if structural_survived:
        h_struct = "SURVIVED_STRUCTURAL_ARITY"
    else:
        h_struct = "FALSIFIED_STRUCTURAL_ARITY"

    if not comparison_valid:
        h_pcea = "UNRESOLVED"
    elif pcea_separation:
        h_pcea = "SURVIVED_PCEA_SPECIFIC_ARITY"
    else:
        h_pcea = "FALSIFIED_PCEA_SPECIFIC_ARITY"

    return {
        "H_STRUCT": h_struct,
        "H_PCEA": h_pcea,
        "H_HARD": "UNRESOLVED",
        "phase2_authorized": h_struct == "SURVIVED_STRUCTURAL_ARITY" and h_pcea == "SURVIVED_PCEA_SPECIFIC_ARITY",
    }


def run_phase1() -> dict:
    fixtures = _load_fixtures()
    freeze = _load_freeze()
    rows = []
    for variant in VARIANTS:
        for arity in ARITIES:
            rows.append(_row_for(variant, arity, fixtures))
    outcomes = classify_outcomes(rows)
    report = {
        "schema": "pcea-arity-replay-results-B-v1",
        "actor": "DeepSeek",
        "role": "B",
        "phase_reached": "PHASE1_EXACT_STRUCTURAL_MICROSCOPE",
        "f0_baseline_commit": freeze["F0"]["baseline_commit"],
        "f1_candidate_commit": F1_CANDIDATE_COMMIT,
        "freeze_json_f1_field_at_f1_commit": freeze["F1"]["candidate_commit"],
        "parameters": fixtures["parameters"],
        "rows": rows,
        "outcome_labels": outcomes,
        "phase2_authorized": outcomes["phase2_authorized"],
        "hmmm": [
            "Boolean ANF full-degree residual is one exact operationalization of direct arity, not a universal definition.",
            "PRF reconstruction interpretation is documented in pcea-ucns/arity/replay_b/adapters.py and REPORT_B.md.",
            "Actor A result files were seen before this replay; independence is recorded as contaminated in ACTOR_B_LOCK.json.",
        ],
    }
    with RESULTS_PATH.open("w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2)
        fh.write("\n")
    return report


if __name__ == "__main__":
    run_phase1()
# ratios: loc_comments=183:39 imports_exports=6:2 calls_definitions=44:9
