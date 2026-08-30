# ratios: loc_comments=34:39 imports_exports=1:4 calls_definitions=19:5
# GPT/Claude generated; context, prompt Erin Spencer
"""Exact GF(2) algebraic normal form (ANF) tools for Actor B.

This is an independent implementation of the Boolean Mobius transform used by
the Phase-1 exact structural microscope. Truth tables are indexed by
little-endian assignment masks: bit ``i`` of ``mask`` is variable ``x_i``.

The fast subset-zeta transform computes every ANF coefficient ``a_S`` in
place. Over GF(2) the same transform is its own inverse, which gives exact
full-degree deletion and reconstruction without floating point.
"""

from __future__ import annotations

# === MODULE_BUILD ===
# id: replay_b_anf
#   module_name: anf
#   module_kind: research
#   summary: exact GF(2) Mobius/ANF transform, degree extraction, and full-degree deletion for the arity structural microscope
#   owner: Actor B (DeepSeek) replay
#   public_surface: mobius_transform, anf_degree, full_degree_coefficient, delete_full_degree_mismatches
#   internal_surface: _validate_truth_table
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_arity_replay_b
#   rollout: research_only
#   rollback: remove module and its references
#   requires: none
#   since: 2026-08-30
#   unresolved: Boolean ANF degree is one exact operationalization of direct arity, not a universal definition
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: anf_transform_self_inverse
#   given: any truth table of length 2**n over GF(2)
#   then:  applying mobius_transform twice returns the original table exactly
#   class: correctness
# === END CONTRACTS ===


def _validate_truth_table(table: list[int]) -> int:
    length = len(table)
    if length < 1 or (length & (length - 1)) != 0:
        raise ValueError("truth table length must be a power of two")
    if any(v not in (0, 1) for v in table):
        raise ValueError("truth table values must be bits in {0,1}")
    return length.bit_length() - 1


def mobius_transform(table: list[int]) -> list[int]:
    """Return ANF coefficients indexed by subset mask over GF(2)."""
    n = _validate_truth_table(table)
    coeffs = list(table)
    for i in range(n):
        bit = 1 << i
        for mask in range(1 << n):
            if mask & bit:
                coeffs[mask] ^= coeffs[mask ^ bit]
    return coeffs


def anf_degree(coeffs: list[int]) -> int:
    """Maximum |S| over nonzero ANF coefficients; constants are degree 0."""
    n = len(coeffs).bit_length() - 1
    degree = 0
    for mask in range(1, 1 << n):
        if coeffs[mask]:
            degree = max(degree, mask.bit_count())
    return degree


def full_degree_coefficient(coeffs: list[int], n: int) -> int:
    """The unique degree-n ANF coefficient for an n-variable function."""
    return coeffs[(1 << n) - 1]


def delete_full_degree_mismatches(table: list[int], n: int) -> int:
    """Delete the degree-n term and count exact reconstruction mismatches."""
    _validate_truth_table(table)
    if len(table) != (1 << n):
        raise ValueError("table length must match variable count n")
    coeffs = mobius_transform(table)
    coeffs[(1 << n) - 1] = 0
    reconstructed = mobius_transform(coeffs)
    return sum(1 for mask, bit in enumerate(table) if reconstructed[mask] != bit)
# ratios: loc_comments=34:39 imports_exports=1:4 calls_definitions=19:5
