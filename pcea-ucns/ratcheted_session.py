# ratios: loc_comments=223:97 imports_exports=7:4 calls_definitions=61:16
# GPT/Claude generated; context, prompt Erin Spencer
"""Authenticated ratcheted-session prototype around the PCEA transform.

This file belongs to the ``pcea-ucns`` proving ground. It is deliberately not
part of the shipped ``pcea`` package and makes no production-security claim.
It tests whether provisioned peers can add strict sequencing, transcript-bound
HMAC authentication, directional key separation, and verify-before-advance
state handling around the existing symmetric PCEA transform.

Usage guidance::

    alice = RatchetedSession(
        provisioned_secret=b"A" * 32,
        initial_state=[seed0],
        session_id="demo",
        role="initiator",
    )
    bob = RatchetedSession(
        provisioned_secret=b"A" * 32,
        initial_state=[seed0],
        session_id="demo",
        role="responder",
    )
    packet = alice.encrypt([seed1], aad=b"model-state")
    recovered = bob.decrypt(packet, aad=b"model-state")
    assert recovered == [seed1]

Limitations: strict in-order delivery only; no persistence, resynchronization
protocol, nonce-generation policy, multi-sender concurrency, or independent
cryptographic review. A passing harness means only that these local invariants
survive the tests named here.
"""

# === MODULE_BUILD ===
# id: pcea_ratcheted_authenticated_session_prototype
#   module_name: ratcheted_session
#   module_kind: experiment
#   summary: proving-ground wrapper adding strict sequencing, transcript HMAC authentication, directional key separation, and rollback-safe state advancement around PCEA
#   owner: Erin Spencer
#   public_surface: AuthenticationError, SequenceError, SessionPacket, RatchetedSession
#   internal_surface: _derive_direction_root, _message_keys, _diversify_state, _packet_material, _advance
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_ratcheted_session
#   rollout: proving_ground_only
#   rollback: delete this prototype and its test; do not alter shipped pcea runtime
#   requires: pcea_cipher
#   since: 2026-08-29
#   unresolved: independent cryptographic review; resynchronization protocol; nonce/session-id generation policy; multi-sender concurrency
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: pcea_session_round_trip
#   given: paired peers share the same provisioned secret, initial PCEA state, session id, and opposite roles
#   then:  authenticated packets decrypt exactly and each direction advances independently
#   class: correctness
#
# id: pcea_session_wrong_secret_rejected
#   given: a packet is checked by a peer with a different provisioned secret
#   then:  authentication fails before plaintext recovery or receive-state advancement
#   class: security
#
# id: pcea_session_transcript_binding
#   given: packet ciphertext, associated data, session id, direction, sequence, or prior transcript differs
#   then:  the packet authentication tag differs or verification fails
#   class: security
#
# id: pcea_session_replay_rejected
#   given: an already accepted packet is presented again
#   then:  strict sequence validation rejects it
#   class: security
#
# id: pcea_session_reordering_rejected
#   given: a later packet arrives before the next expected packet
#   then:  strict sequence validation rejects it without preventing later in-order recovery
#   class: security
#
# id: pcea_session_failure_does_not_advance
#   given: authentication or sequence validation fails
#   then:  the same receiver can still accept the untampered next packet
#   class: correctness
#
# id: pcea_session_key_separation
#   given: one directional chain key and message sequence
#   then:  distinct labeled encryption-diversification and authentication keys are derived and both affect packet output
#   class: security
#
# id: pcea_session_public_metadata_minimal
#   given: a packet is emitted
#   then:  public metadata contains only version, session id, direction, sequence, ciphertext, and tag; no ratchet or PCEA state is exported
#   class: security
# === END CONTRACTS ===

from __future__ import annotations

import copy
import hashlib
import hmac
import json
from typing import NamedTuple

from pcea.cipher import DEFAULT_WORD_BITS, decrypt_state, encrypt_state

State = list[list[list[int]]]

VERSION = "pcea-ratcheted-session-v0"
_INITIATOR = "initiator"
_RESPONDER = "responder"
_DIRECTION_FOR_ROLE = {
    _INITIATOR: ("i2r", "r2i"),
    _RESPONDER: ("r2i", "i2r"),
}


class AuthenticationError(ValueError):
    """Raised when a packet's transcript-bound authentication fails."""


class SequenceError(ValueError):
    """Raised when a packet is replayed, skipped ahead, or uses the wrong direction."""


class SessionPacket(NamedTuple):
    """Public wire-shaped record for the proving-ground session."""

    version: str
    session_id: str
    direction: str
    sequence: int
    ciphertext: State
    tag: str


def _hmac(key: bytes, payload: bytes) -> bytes:
    return hmac.new(key, payload, hashlib.sha256).digest()


def _derive_direction_root(secret: bytes, session_id: str, direction: str) -> bytes:
    context = f"{VERSION}|root|{session_id}|{direction}".encode("utf-8")
    return _hmac(secret, context)


def _message_keys(chain_key: bytes, sequence: int) -> tuple[bytes, bytes]:
    sequence_bytes = sequence.to_bytes(8, "big", signed=False)
    encryption_key = _hmac(chain_key, b"pcea-diversify|" + sequence_bytes)
    authentication_key = _hmac(chain_key, b"authenticate|" + sequence_bytes)
    return encryption_key, authentication_key


def _mask_for_cell(
    encryption_key: bytes,
    sequence: int,
    seed_idx: int,
    circle_idx: int,
    tensor_idx: int,
    word_bits: int,
) -> int:
    byte_count = (word_bits + 7) // 8
    material = bytearray()
    counter = 0
    prefix = (
        f"{VERSION}|cell|{sequence}|{seed_idx}|{circle_idx}|{tensor_idx}|".encode(
            "utf-8"
        )
    )
    while len(material) < byte_count:
        material.extend(_hmac(encryption_key, prefix + counter.to_bytes(4, "big")))
        counter += 1
    return int.from_bytes(material[:byte_count], "big") & ((1 << word_bits) - 1)


def _diversify_state(
    last_state: State,
    encryption_key: bytes,
    sequence: int,
    word_bits: int,
) -> State:
    modulus = 1 << word_bits
    diversified: State = []
    for seed_idx, seed in enumerate(last_state):
        diversified_seed: list[list[int]] = []
        for circle_idx, circle in enumerate(seed):
            diversified_circle: list[int] = []
            for tensor_idx, value in enumerate(circle):
                mask = _mask_for_cell(
                    encryption_key,
                    sequence,
                    seed_idx,
                    circle_idx,
                    tensor_idx,
                    word_bits,
                )
                diversified_circle.append((value % modulus) ^ mask)
            diversified_seed.append(diversified_circle)
        diversified.append(diversified_seed)
    return diversified


def _packet_material(
    session_id: str,
    direction: str,
    sequence: int,
    ciphertext: State,
    aad: bytes,
    transcript_hash: bytes,
) -> bytes:
    payload = {
        "aad": aad.hex(),
        "ciphertext": ciphertext,
        "direction": direction,
        "sequence": sequence,
        "session_id": session_id,
        "transcript": transcript_hash.hex(),
        "version": VERSION,
    }
    return json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    ).encode("utf-8")


def _advance(
    chain_key: bytes,
    transcript_hash: bytes,
    material: bytes,
    tag: bytes,
) -> tuple[bytes, bytes]:
    next_transcript = hashlib.sha256(transcript_hash + material + tag).digest()
    next_chain = _hmac(chain_key, b"ratchet|" + next_transcript)
    return next_chain, next_transcript


class RatchetedSession:
    """Strict in-order authenticated PCEA session for proving-ground use only."""

    def __init__(
        self,
        provisioned_secret: bytes,
        initial_state: State,
        session_id: str,
        role: str,
        word_bits: int = DEFAULT_WORD_BITS,
    ) -> None:
        if not isinstance(provisioned_secret, bytes) or len(provisioned_secret) < 16:
            raise ValueError("provisioned_secret must be at least 16 bytes")
        if not initial_state:
            raise ValueError("initial_state must be non-empty")
        if not session_id:
            raise ValueError("session_id must be non-empty")
        if role not in _DIRECTION_FOR_ROLE:
            raise ValueError("role must be 'initiator' or 'responder'")
        if word_bits <= 0:
            raise ValueError("word_bits must be positive")

        outbound, inbound = _DIRECTION_FOR_ROLE[role]
        self._session_id = session_id
        self._outbound_direction = outbound
        self._inbound_direction = inbound
        self._word_bits = word_bits

        self._send_chain = _derive_direction_root(
            provisioned_secret, session_id, outbound
        )
        self._recv_chain = _derive_direction_root(
            provisioned_secret, session_id, inbound
        )
        initial_transcript = hashlib.sha256(
            f"{VERSION}|transcript|{session_id}".encode("utf-8")
        ).digest()
        self._send_transcript = initial_transcript
        self._recv_transcript = initial_transcript
        self._send_last = copy.deepcopy(initial_state)
        self._recv_last = copy.deepcopy(initial_state)
        self._send_sequence = 0
        self._recv_sequence = 0

    @property
    def send_sequence(self) -> int:
        """Next outbound sequence number."""

        return self._send_sequence

    @property
    def receive_sequence(self) -> int:
        """Next inbound sequence number."""

        return self._recv_sequence

    def encrypt(self, state: State, aad: bytes = b"") -> SessionPacket:
        """Authenticate one outbound PCEA state and advance only after success."""

        sequence = self._send_sequence
        encryption_key, authentication_key = _message_keys(
            self._send_chain, sequence
        )
        effective_last = _diversify_state(
            self._send_last, encryption_key, sequence, self._word_bits
        )
        ciphertext = encrypt_state(state, effective_last, self._word_bits)
        material = _packet_material(
            self._session_id,
            self._outbound_direction,
            sequence,
            ciphertext,
            aad,
            self._send_transcript,
        )
        tag = _hmac(authentication_key, material)
        packet = SessionPacket(
            VERSION,
            self._session_id,
            self._outbound_direction,
            sequence,
            copy.deepcopy(ciphertext),
            tag.hex(),
        )

        next_chain, next_transcript = _advance(
            self._send_chain, self._send_transcript, material, tag
        )
        self._send_last = copy.deepcopy(state)
        self._send_chain = next_chain
        self._send_transcript = next_transcript
        self._send_sequence += 1
        return packet

    def decrypt(self, packet: SessionPacket, aad: bytes = b"") -> State:
        """Verify a packet before decrypting or advancing any receive state."""

        if packet.version != VERSION or packet.session_id != self._session_id:
            raise AuthenticationError("packet session binding failed")
        if packet.direction != self._inbound_direction:
            raise SequenceError("packet direction does not match this receiver")
        if packet.sequence != self._recv_sequence:
            raise SequenceError(
                f"expected sequence {self._recv_sequence}, got {packet.sequence}"
            )

        sequence = self._recv_sequence
        encryption_key, authentication_key = _message_keys(
            self._recv_chain, sequence
        )
        material = _packet_material(
            self._session_id,
            self._inbound_direction,
            sequence,
            packet.ciphertext,
            aad,
            self._recv_transcript,
        )
        expected_tag = _hmac(authentication_key, material)
        if not hmac.compare_digest(expected_tag.hex(), packet.tag):
            raise AuthenticationError("packet authentication failed")

        effective_last = _diversify_state(
            self._recv_last, encryption_key, sequence, self._word_bits
        )
        state = decrypt_state(packet.ciphertext, effective_last, self._word_bits)

        next_chain, next_transcript = _advance(
            self._recv_chain, self._recv_transcript, material, expected_tag
        )
        self._recv_last = copy.deepcopy(state)
        self._recv_chain = next_chain
        self._recv_transcript = next_transcript
        self._recv_sequence += 1
        return state
# ratios: loc_comments=223:97 imports_exports=7:4 calls_definitions=61:16
