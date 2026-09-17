# ratios: loc_comments=18:45 imports_exports=2:1 calls_definitions=5:1
# GPT/Claude generated; context, prompt Erin Spencer
"""
Hash-based key derivation for PCEA.

Key stream is derived from a versioned binary transcript containing the
hierarchical address (seed, circle, tensor), stream parameters, and the values
at that position plus its heptagram neighbors in the circle dimension (±3 mod
7, the PTCA adjacency rule). This means each tensor's encryption depends on
its own last_state value AND the last_state of the two circles it interlocks
with — implementing the circular interlocking property of the seven-disk
structure.
"""

# === MODULE_BUILD ===
# id: pcea_kdf
#   module_name: kdf
#   module_kind: engine
#   summary: hash-based key-stream derivation keyed by hierarchical address plus heptagram neighbors
#   owner: Erin Spencer
#   public_surface: key_stream
#   internal_surface: typed length-delimited integer transcript encoding
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_kdf
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: none
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: kdf_transcript_is_typed_canonical_integer_bytes
#   given: key_stream receives contributor values and address parameters
#   then: every value is an exact int and the hash transcript is schema-prefixed and length-delimited without implicit object stringification
#   class: correctness
# === END CONTRACTS ===

from __future__ import annotations

import hashlib


_TRANSCRIPT_SCHEMA = b"PCEA-KDF-INT-v1\x00"


def _encode_integer(value: int, name: str) -> bytes:
    """Encode one exact integer without text conversion or width ambiguity."""
    if type(value) is not int:
        raise ValueError(f"{name} must be an exact integer")
    magnitude = abs(value)
    width = max(1, (magnitude.bit_length() + 7) // 8)
    return (
        (b"\x01" if value < 0 else b"\x00")
        + width.to_bytes(8, "big")
        + magnitude.to_bytes(width, "big")
    )


def _canonical_transcript(
    contributors: list[int],
    seed_idx: int,
    circle_idx: int,
    tensor_idx: int,
    length: int,
    p: int,
    counter: int,
) -> bytes:
    """Build the versioned, typed transcript hashed for one stream block."""
    if type(contributors) is not list:
        raise ValueError("contributors must be a list of exact integers")
    if type(length) is not int or length < 0:
        raise ValueError("length must be a non-negative integer")
    if type(p) is not int or p < 2:
        raise ValueError("p must be an integer base >= 2")

    payload = bytearray(_TRANSCRIPT_SCHEMA)
    payload.extend(len(contributors).to_bytes(8, "big"))
    for index, value in enumerate(contributors):
        payload.extend(_encode_integer(value, f"contributors[{index}]"))
    for name, value in (
        ("seed_idx", seed_idx),
        ("circle_idx", circle_idx),
        ("tensor_idx", tensor_idx),
        ("length", length),
        ("p", p),
        ("counter", counter),
    ):
        payload.extend(_encode_integer(value, name))
    return bytes(payload)


def key_stream(
    contributors: list[int],
    seed_idx: int,
    circle_idx: int,
    tensor_idx: int,
    length: int,
    p: int,
) -> list[int]:
    """
    Derive `length` key digits in [0, p-1] via SHA-256.

    Args:
        contributors: [own_val, left_neighbor_val, right_neighbor_val] —
                      the last_state values at (circle_idx, tensor_idx),
                      ((circle_idx - 3) % 7, tensor_idx), and
                      ((circle_idx + 3) % 7, tensor_idx).
        seed_idx:     index of the seed in the architecture.
        circle_idx:   index of the circle within the seed (0..6).
        tensor_idx:   index of the tensor within the circle (0..6).
        length:       number of key digits to produce.
        p:            prime base; digits are reduced mod p. Both length and p
                      are bound into the transcript.

    Returns:
        List of `length` integers, each in [0, p-1].
    """
    # Validate the complete input before deriving even the first key byte.
    _canonical_transcript(contributors, seed_idx, circle_idx, tensor_idx, length, p, 0)
    raw = bytearray()
    counter = 0
    while len(raw) < length:
        payload = _canonical_transcript(
            contributors, seed_idx, circle_idx, tensor_idx, length, p, counter
        )
        raw.extend(hashlib.sha256(payload).digest())
        counter += 1
    return [b % p for b in raw[:length]]
# ratios: loc_comments=18:45 imports_exports=2:1 calls_definitions=5:1
