# ratios: loc_comments=84:46 imports_exports=6:3 calls_definitions=27:6
# GPT/Claude generated; context, prompt Erin Spencer
"""Actor B independent PCEA-A_n and PRF-A_n cell adapters.

The PCEA-A_n adapter reconstructs the frozen arity relation directly from the
written protocol and the frozen baseline primitives (pcea.codec, pcea.kdf,
pcea.primes). The contributor order is frozen as OFFSETS =
[0, -3, +3, -1, +1, -2, +2] and each A_n uses the corresponding prefix as one
joint contributor list to the same hash/KDF relation.

The PRF-A_n control keeps the same contributor labels/order/count, the same
public address serialization, the same plaintext input, the same output width,
and the same base-p digit shift surface, but derives its key digits with
HMAC-SHA256 instead of PCEA's SHA-256 key stream, and omits PCEA's prime
selection (the 8-bit structural lane is binary, p=2), Mobius codec (the plain
word position is used directly), and PCEA state transform.
"""

from __future__ import annotations

import hashlib
import hmac

from pcea.codec import digit_count, from_fixed, to_fixed, mobius_encode
from pcea.kdf import key_stream
from pcea.primes import prime_at

# === MODULE_BUILD ===
# id: replay_b_adapters
#   module_name: adapters
#   module_kind: research
#   summary: independent PCEA-A_n and PRF-A_n cell adapters for the arity structural microscope
#   owner: Actor B (DeepSeek) replay
#   public_surface: OFFSETS, CONTRIBUTOR_LABELS, LABEL_TO_OFFSET, pcea_cell, prf_cell, pcea_seed_a3
#   internal_surface: _contributor_values, _prf_key_digits, _word_position
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_arity_replay_b
#   rollout: research_only
#   rollback: remove module and its references
#   requires: pcea_codec, pcea_kdf, pcea_primes
#   since: 2026-08-30
#   unresolved: PRF omits prime selection; p=2 is fixed for the 8-bit structural lane and coincides with prime_at(0) at the target cell
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: a3_matches_runtime_cipher
#   given: any 7x7 seed and last_seed pair from the frozen a3_regression fixtures
#   then:  pcea_seed_a3 equals pcea.cipher.encrypt_seed on every cell
#   class: correctness
# === END CONTRACTS ===

OFFSETS: tuple[int, ...] = (0, -3, 3, -1, 1, -2, 2)
CONTRIBUTOR_LABELS: tuple[str, ...] = (
    "circle+0", "circle-3", "circle+3", "circle-1", "circle+1", "circle-2", "circle+2",
)
LABEL_TO_OFFSET: dict[str, int] = dict(zip(CONTRIBUTOR_LABELS, OFFSETS))

PRF_KEY = b"pcea-arity-v1|prf-control"


def _contributor_values(
    last_seed: list[list[int]], circle_idx: int, tensor_idx: int, arity: int
) -> list[int]:
    """First ``arity`` contributor values under the frozen OFFSETS prefix."""
    if arity < 1 or arity > len(OFFSETS):
        raise ValueError(f"arity must be in [1, {len(OFFSETS)}]")
    values: list[int] = []
    for offset in OFFSETS[:arity]:
        circle = (circle_idx + offset) % 7
        values.append(last_seed[circle][tensor_idx])
    return values


def _word_position(value: int, word_bits: int) -> int:
    """Plain unsigned word position; no Mobius codec, no range guard."""
    return value & ((1 << word_bits) - 1)


def _prf_key_digits(
    contributors: list[int],
    seed_idx: int,
    circle_idx: int,
    tensor_idx: int,
    length: int,
    p: int,
) -> list[int]:
    """HMAC-SHA256 key digits over the same serialization as PCEA's KDF."""
    contrib_str = ":".join(str(c) for c in contributors)
    raw = bytearray()
    counter = 0
    while len(raw) < length:
        payload = f"{contrib_str}:{seed_idx}:{circle_idx}:{tensor_idx}:{counter}".encode()
        raw.extend(hmac.new(PRF_KEY, payload, hashlib.sha256).digest())
        counter += 1
    return [b % p for b in raw[:length]]


def pcea_cell(
    value: int,
    last_seed: list[list[int]],
    seed_idx: int,
    circle_idx: int,
    tensor_idx: int,
    word_bits: int,
    arity: int,
) -> int:
    """PCEA-A_n encrypted cell output under the frozen contributor prefix."""
    p = prime_at(circle_idx * 7 + tensor_idx)
    k = digit_count(p, word_bits)
    u = mobius_encode(value, word_bits)
    v_digits = to_fixed(u, p, k)
    contributors = _contributor_values(last_seed, circle_idx, tensor_idx, arity)
    key_digits = key_stream(contributors, seed_idx, circle_idx, tensor_idx, k, p)
    e_digits = [(vd + kd) % p for vd, kd in zip(v_digits, key_digits)]
    return from_fixed(e_digits, p)


def prf_cell(
    value: int,
    last_seed: list[list[int]],
    seed_idx: int,
    circle_idx: int,
    tensor_idx: int,
    word_bits: int,
    arity: int,
) -> int:
    """PRF-A_n control cell output: HMAC-SHA256 key stream, same digit surface."""
    p = 2  # frozen 8-bit structural lane is binary; omits PCEA prime selection
    k = digit_count(p, word_bits)
    u = _word_position(value, word_bits)
    v_digits = to_fixed(u, p, k)
    contributors = _contributor_values(last_seed, circle_idx, tensor_idx, arity)
    key_digits = _prf_key_digits(contributors, seed_idx, circle_idx, tensor_idx, k, p)
    e_digits = [(vd + kd) % p for vd, kd in zip(v_digits, key_digits)]
    return from_fixed(e_digits, p)


def pcea_seed_a3(
    seed: list[list[int]], last_seed: list[list[int]], seed_idx: int, word_bits: int
) -> list[list[int]]:
    """Full-seed A3 adapter; must equal pcea.cipher.encrypt_seed exactly."""
    return [
        [
            pcea_cell(seed[c][t], last_seed, seed_idx, c, t, word_bits, arity=3)
            for t in range(7)
        ]
        for c in range(7)
    ]
# ratios: loc_comments=84:46 imports_exports=6:3 calls_definitions=27:6
