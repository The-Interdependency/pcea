# ratios: loc_comments=103:51 imports_exports=4:8 calls_definitions=58:10
# GPT/Claude generated; context, prompt Erin Spencer
"""Regression harness for the non-runtime ratcheted authenticated-session prototype."""

from __future__ import annotations

import importlib.util
import pathlib

import pytest


# === CHECKS ===
# id: check_pcea_session_round_trip
#   proves: pcea_session_round_trip
#   call: self::test_bidirectional_round_trip_and_independent_sequences
#   mutates: none
#   cleanup: none
#
# id: check_pcea_session_wrong_secret_rejected
#   proves: pcea_session_wrong_secret_rejected
#   call: self::test_wrong_secret_fails_before_recovery
#   mutates: none
#   cleanup: none
#
# id: check_pcea_session_transcript_binding
#   proves: pcea_session_transcript_binding
#   call: self::test_associated_data_and_session_id_bind_packet
#   mutates: none
#   cleanup: none
#
# id: check_pcea_session_replay_rejected
#   proves: pcea_session_replay_rejected
#   call: self::test_replay_is_rejected
#   mutates: none
#   cleanup: none
#
# id: check_pcea_session_reordering_rejected
#   proves: pcea_session_reordering_rejected
#   call: self::test_reordering_is_rejected_without_poisoning_receiver
#   mutates: none
#   cleanup: none
#
# id: check_pcea_session_failure_does_not_advance
#   proves: pcea_session_failure_does_not_advance
#   call: self::test_authentication_failure_does_not_advance_receive_state
#   mutates: none
#   cleanup: none
#
# id: check_pcea_session_key_separation
#   proves: pcea_session_key_separation
#   call: self::test_labeled_keys_are_distinct_and_encryption_key_affects_ciphertext
#   mutates: none
#   cleanup: none
#
# id: check_pcea_session_public_metadata_minimal
#   proves: pcea_session_public_metadata_minimal
#   call: self::test_packet_exports_no_resynchronization_or_ratchet_state
#   mutates: none
#   cleanup: none
# === END CHECKS ===


ROOT = pathlib.Path(__file__).parent.parent
_spec = importlib.util.spec_from_file_location(
    "ratcheted_session", ROOT / "pcea-ucns" / "ratcheted_session.py"
)
ratchet = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ratchet)


def _seed(base: int) -> list[list[int]]:
    return [[base + circle * 7 + tensor for tensor in range(7)] for circle in range(7)]


def _pair(
    secret: bytes = b"S" * 32,
    session_id: str = "session-1",
) -> tuple[object, object]:
    initial = [_seed(0)]
    initiator = ratchet.RatchetedSession(
        secret, initial, session_id=session_id, role="initiator"
    )
    responder = ratchet.RatchetedSession(
        secret, initial, session_id=session_id, role="responder"
    )
    return initiator, responder


def test_bidirectional_round_trip_and_independent_sequences() -> None:
    alice, bob = _pair()

    a1 = [_seed(100)]
    packet_a1 = alice.encrypt(a1, aad=b"state")
    assert bob.decrypt(packet_a1, aad=b"state") == a1

    b1 = [_seed(200)]
    packet_b1 = bob.encrypt(b1, aad=b"reply")
    assert alice.decrypt(packet_b1, aad=b"reply") == b1

    a2 = [_seed(300)]
    packet_a2 = alice.encrypt(a2, aad=b"state")
    assert bob.decrypt(packet_a2, aad=b"state") == a2
    assert alice.send_sequence == 2
    assert alice.receive_sequence == 1
    assert bob.send_sequence == 1
    assert bob.receive_sequence == 2


def test_wrong_secret_fails_before_recovery() -> None:
    alice, _ = _pair(secret=b"A" * 32)
    _, wrong_bob = _pair(secret=b"B" * 32)
    packet = alice.encrypt([_seed(10)])

    with pytest.raises(ratchet.AuthenticationError):
        wrong_bob.decrypt(packet)
    assert wrong_bob.receive_sequence == 0


def test_associated_data_and_session_id_bind_packet() -> None:
    alice, bob = _pair()
    packet = alice.encrypt([_seed(20)], aad=b"context-a")

    with pytest.raises(ratchet.AuthenticationError):
        bob.decrypt(packet, aad=b"context-b")
    assert bob.decrypt(packet, aad=b"context-a") == [_seed(20)]

    other_alice, _ = _pair(session_id="session-2")
    other_packet = other_alice.encrypt([_seed(20)], aad=b"context-a")
    assert other_packet.ciphertext != packet.ciphertext
    assert other_packet.tag != packet.tag


def test_replay_is_rejected() -> None:
    alice, bob = _pair()
    packet = alice.encrypt([_seed(30)])
    assert bob.decrypt(packet) == [_seed(30)]

    with pytest.raises(ratchet.SequenceError):
        bob.decrypt(packet)


def test_reordering_is_rejected_without_poisoning_receiver() -> None:
    alice, bob = _pair()
    first = alice.encrypt([_seed(40)])
    second = alice.encrypt([_seed(50)])

    with pytest.raises(ratchet.SequenceError):
        bob.decrypt(second)

    assert bob.decrypt(first) == [_seed(40)]
    assert bob.decrypt(second) == [_seed(50)]


def test_authentication_failure_does_not_advance_receive_state() -> None:
    alice, bob = _pair()
    packet = alice.encrypt([_seed(60)], aad=b"bound")
    tampered = packet._replace(tag=("00" * 32))

    with pytest.raises(ratchet.AuthenticationError):
        bob.decrypt(tampered, aad=b"bound")

    assert bob.receive_sequence == 0
    assert bob.decrypt(packet, aad=b"bound") == [_seed(60)]
    assert bob.receive_sequence == 1


def test_labeled_keys_are_distinct_and_encryption_key_affects_ciphertext() -> None:
    chain = ratchet._derive_direction_root(b"K" * 32, "session-1", "i2r")
    encryption_key, authentication_key = ratchet._message_keys(chain, 0)
    assert encryption_key != authentication_key

    alice_a, _ = _pair(secret=b"A" * 32)
    alice_b, _ = _pair(secret=b"B" * 32)
    packet_a = alice_a.encrypt([_seed(70)])
    packet_b = alice_b.encrypt([_seed(70)])
    assert packet_a.ciphertext != packet_b.ciphertext
    assert packet_a.tag != packet_b.tag


def test_packet_exports_no_resynchronization_or_ratchet_state() -> None:
    alice, _ = _pair()
    packet = alice.encrypt([_seed(80)])

    assert packet._fields == (
        "version",
        "session_id",
        "direction",
        "sequence",
        "ciphertext",
        "tag",
    )
    forbidden = {"last_state", "chain_key", "ratchet", "traffic_secret", "resync"}
    assert not forbidden.intersection(packet._fields)
    assert len(packet.tag) == 64
# ratios: loc_comments=103:51 imports_exports=4:8 calls_definitions=58:10
