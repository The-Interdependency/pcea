import { defineMsdmdCollection } from "./.agents/skills/msdmd/collection";

export default defineMsdmdCollection({
  "declarations": [
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "authentication or sequence validation fails",
        "then": "the same receiver can still accept the untampered next packet"
      },
      "file": "pcea-ucns/ratcheted_session.py",
      "id": "pcea_session_failure_does_not_advance"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "security",
        "given": "one directional chain key and message sequence",
        "then": "distinct labeled encryption-diversification and authentication keys are derived and both affect packet output"
      },
      "file": "pcea-ucns/ratcheted_session.py",
      "id": "pcea_session_key_separation"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "security",
        "given": "a packet is emitted",
        "then": "public metadata contains only version, session id, direction, sequence, ciphertext, and tag; no ratchet or PCEA state is exported"
      },
      "file": "pcea-ucns/ratcheted_session.py",
      "id": "pcea_session_public_metadata_minimal"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "security",
        "given": "a later packet arrives before the next expected packet",
        "then": "strict sequence validation rejects it without preventing later in-order recovery"
      },
      "file": "pcea-ucns/ratcheted_session.py",
      "id": "pcea_session_reordering_rejected"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "security",
        "given": "an already accepted packet is presented again",
        "then": "strict sequence validation rejects it"
      },
      "file": "pcea-ucns/ratcheted_session.py",
      "id": "pcea_session_replay_rejected"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "correctness",
        "given": "paired peers share the same provisioned secret, initial PCEA state, session id, and opposite roles",
        "then": "authenticated packets decrypt exactly and each direction advances independently"
      },
      "file": "pcea-ucns/ratcheted_session.py",
      "id": "pcea_session_round_trip"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "security",
        "given": "packet ciphertext, associated data, session id, direction, sequence, or prior transcript differs",
        "then": "the packet authentication tag differs or verification fails"
      },
      "file": "pcea-ucns/ratcheted_session.py",
      "id": "pcea_session_transcript_binding"
    },
    {
      "block": "CONTRACTS",
      "fields": {
        "class": "security",
        "given": "a packet is checked by a peer with a different provisioned secret",
        "then": "authentication fails before plaintext recovery or receive-state advancement"
      },
      "file": "pcea-ucns/ratcheted_session.py",
      "id": "pcea_session_wrong_secret_rejected"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_derive_direction_root, _message_keys, _diversify_state, _packet_material, _advance",
        "module_kind": "experiment",
        "module_name": "ratcheted_session",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "AuthenticationError, SequenceError, SessionPacket, RatchetedSession",
        "requires": "pcea_cipher",
        "rollback": "delete this prototype and its test; do not alter shipped pcea runtime",
        "rollout": "proving_ground_only",
        "since": "2026-08-29",
        "storage_boundary": "none",
        "summary": "proving-ground wrapper adding strict sequencing, transcript HMAC authentication, directional key separation, and rollback-safe state advancement around PCEA",
        "tests": "tests.test_ratcheted_session",
        "unresolved": "independent cryptographic review; resynchronization protocol; nonce/session-id generation policy; multi-sender concurrency",
        "user_data_boundary": "none"
      },
      "file": "pcea-ucns/ratcheted_session.py",
      "id": "pcea_ratcheted_authenticated_session_prototype"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_validate_seed, _contributors, _encrypt_element, _decrypt_element",
        "module_kind": "engine",
        "module_name": "cipher",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "encrypt_seed, decrypt_seed, encrypt_state, decrypt_state, CIRCLE_COUNT, TENSOR_COUNT, DEFAULT_WORD_BITS",
        "requires": "pcea_codec, pcea_kdf, pcea_primes",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "prime-circular Mobius disk cipher: fixed-width base-p digit encode with SHA-256 keyed additive shift",
        "tests": "tests.test_cipher",
        "unresolved": "security-critical module; changes require independent crypto review",
        "user_data_boundary": "none"
      },
      "file": "pcea/cipher.py",
      "id": "pcea_cipher"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "adapter",
        "module_name": "codec",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "mobius_encode, mobius_decode, digit_count, to_fixed, from_fixed",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "Mobius disk codec: signed<->unsigned position mapping and fixed-width base-p digit encoding",
        "tests": "tests.test_codec",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "pcea/codec.py",
      "id": "pcea_codec"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "schema",
        "module_name": "contract",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "DECISION, SECURITY_INVARIANT, FORBIDDEN_UCNS_SYMBOLS, RUNTIME_MODULES, contract_statement",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "PCEA<->UCNS interface-contract constants and guardrails (single source of truth)",
        "tests": "tests.test_contract_spec",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "pcea/contract.py",
      "id": "pcea_contract"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_zero_seed",
        "module_kind": "service",
        "module_name": "instance",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "PCEAInstance",
        "requires": "pcea_cipher",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "stateful PCEA session that auto-advances last_state so sender/receiver stay synchronized",
        "tests": "tests.test_instance",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "pcea/instance.py",
      "id": "pcea_instance"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "none",
        "module_kind": "engine",
        "module_name": "kdf",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "key_stream",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "hash-based key-stream derivation keyed by hierarchical address plus heptagram neighbors",
        "tests": "tests.test_kdf",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "pcea/kdf.py",
      "id": "pcea_kdf"
    },
    {
      "block": "MODULE_BUILD",
      "fields": {
        "admin_only": "false",
        "auth_boundary": "none",
        "internal_surface": "_sieve",
        "module_kind": "schema",
        "module_name": "primes",
        "network_boundary": "none",
        "owner": "Erin Spencer",
        "public_surface": "prime_at, PRIME_CIRCLE, CIRCLE_SIZE",
        "requires": "none",
        "rollback": "remove module and its references",
        "rollout": "default_enabled",
        "since": "2026-06-02",
        "storage_boundary": "none",
        "summary": "fixed 53-prime circle used as the circular bases for prime-circular base encryption",
        "tests": "tests.test_primes",
        "unresolved": "none",
        "user_data_boundary": "none"
      },
      "file": "pcea/primes.py",
      "id": "pcea_primes"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_authentication_failure_does_not_advance_receive_state",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pcea_session_failure_does_not_advance"
      },
      "file": "tests/test_ratcheted_session.py",
      "id": "check_pcea_session_failure_does_not_advance"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_labeled_keys_are_distinct_and_encryption_key_affects_ciphertext",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pcea_session_key_separation"
      },
      "file": "tests/test_ratcheted_session.py",
      "id": "check_pcea_session_key_separation"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_packet_exports_no_resynchronization_or_ratchet_state",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pcea_session_public_metadata_minimal"
      },
      "file": "tests/test_ratcheted_session.py",
      "id": "check_pcea_session_public_metadata_minimal"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_reordering_is_rejected_without_poisoning_receiver",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pcea_session_reordering_rejected"
      },
      "file": "tests/test_ratcheted_session.py",
      "id": "check_pcea_session_reordering_rejected"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_replay_is_rejected",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pcea_session_replay_rejected"
      },
      "file": "tests/test_ratcheted_session.py",
      "id": "check_pcea_session_replay_rejected"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_bidirectional_round_trip_and_independent_sequences",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pcea_session_round_trip"
      },
      "file": "tests/test_ratcheted_session.py",
      "id": "check_pcea_session_round_trip"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_associated_data_and_session_id_bind_packet",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pcea_session_transcript_binding"
      },
      "file": "tests/test_ratcheted_session.py",
      "id": "check_pcea_session_transcript_binding"
    },
    {
      "block": "CHECKS",
      "fields": {
        "call": "self::test_wrong_secret_fails_before_recovery",
        "cleanup": "none",
        "mutates": "none",
        "proves": "pcea_session_wrong_secret_rejected"
      },
      "file": "tests/test_ratcheted_session.py",
      "id": "check_pcea_session_wrong_secret_rejected"
    }
  ],
  "edges": [
    {
      "from": "check_pcea_session_failure_does_not_advance",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_failure_does_not_advance",
      "to": "self::test_authentication_failure_does_not_advance_receive_state"
    },
    {
      "from": "check_pcea_session_failure_does_not_advance",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_failure_does_not_advance",
      "to": "pcea_session_failure_does_not_advance"
    },
    {
      "from": "check_pcea_session_key_separation",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_key_separation",
      "to": "self::test_labeled_keys_are_distinct_and_encryption_key_affects_ciphertext"
    },
    {
      "from": "check_pcea_session_key_separation",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_key_separation",
      "to": "pcea_session_key_separation"
    },
    {
      "from": "check_pcea_session_public_metadata_minimal",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_public_metadata_minimal",
      "to": "self::test_packet_exports_no_resynchronization_or_ratchet_state"
    },
    {
      "from": "check_pcea_session_public_metadata_minimal",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_public_metadata_minimal",
      "to": "pcea_session_public_metadata_minimal"
    },
    {
      "from": "check_pcea_session_reordering_rejected",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_reordering_rejected",
      "to": "self::test_reordering_is_rejected_without_poisoning_receiver"
    },
    {
      "from": "check_pcea_session_reordering_rejected",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_reordering_rejected",
      "to": "pcea_session_reordering_rejected"
    },
    {
      "from": "check_pcea_session_replay_rejected",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_replay_rejected",
      "to": "self::test_replay_is_rejected"
    },
    {
      "from": "check_pcea_session_replay_rejected",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_replay_rejected",
      "to": "pcea_session_replay_rejected"
    },
    {
      "from": "check_pcea_session_round_trip",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_round_trip",
      "to": "self::test_bidirectional_round_trip_and_independent_sequences"
    },
    {
      "from": "check_pcea_session_round_trip",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_round_trip",
      "to": "pcea_session_round_trip"
    },
    {
      "from": "check_pcea_session_transcript_binding",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_transcript_binding",
      "to": "self::test_associated_data_and_session_id_bind_packet"
    },
    {
      "from": "check_pcea_session_transcript_binding",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_transcript_binding",
      "to": "pcea_session_transcript_binding"
    },
    {
      "from": "check_pcea_session_wrong_secret_rejected",
      "kind": "calls",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_wrong_secret_rejected",
      "to": "self::test_wrong_secret_fails_before_recovery"
    },
    {
      "from": "check_pcea_session_wrong_secret_rejected",
      "kind": "claims_proves",
      "source_block": "CHECKS",
      "source_id": "check_pcea_session_wrong_secret_rejected",
      "to": "pcea_session_wrong_secret_rejected"
    },
    {
      "from": "pcea_cipher",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_cipher",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_cipher",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_cipher",
      "to": "pcea_codec"
    },
    {
      "from": "pcea_cipher",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_cipher",
      "to": "pcea_kdf"
    },
    {
      "from": "pcea_cipher",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_cipher",
      "to": "pcea_primes"
    },
    {
      "from": "pcea_codec",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_codec",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_codec",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_codec",
      "to": "none"
    },
    {
      "from": "pcea_contract",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_contract",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_contract",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_contract",
      "to": "none"
    },
    {
      "from": "pcea_instance",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_instance",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_instance",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_instance",
      "to": "pcea_cipher"
    },
    {
      "from": "pcea_kdf",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_kdf",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_kdf",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_kdf",
      "to": "none"
    },
    {
      "from": "pcea_primes",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_primes",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_primes",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_primes",
      "to": "none"
    },
    {
      "from": "pcea_ratcheted_authenticated_session_prototype",
      "kind": "owns",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_ratcheted_authenticated_session_prototype",
      "to": "Erin Spencer"
    },
    {
      "from": "pcea_ratcheted_authenticated_session_prototype",
      "kind": "requires",
      "source_block": "MODULE_BUILD",
      "source_id": "pcea_ratcheted_authenticated_session_prototype",
      "to": "pcea_cipher"
    }
  ],
  "gaps": [],
  "repo": "pcea"
});
