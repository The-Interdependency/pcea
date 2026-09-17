# ratios: loc_comments=30:44 imports_exports=3:1 calls_definitions=12:6
# GPT/Claude generated; context, prompt Erin Spencer
"""
Stateful PCEA instance.

PCEAInstance tracks last_state (a list of seeds) automatically. After each
encrypt or decrypt call, last_state advances to the current plaintext seeds
so that sender and receiver stay synchronized without manual state management.

Each seed is a 7×7 structure: 7 circles × 7 tensors. Each circle is itself
a tensor; each seed is itself a tensor.
"""

# === MODULE_BUILD ===
# id: pcea_instance
#   module_name: instance
#   module_kind: service
#   summary: stateful PCEA session that auto-advances last_state so sender/receiver stay synchronized
#   owner: Erin Spencer
#   public_surface: PCEAInstance
#   internal_surface: _zero_seed
#   auth_boundary: none
#   storage_boundary: none
#   network_boundary: none
#   user_data_boundary: none
#   admin_only: false
#   tests: tests.test_instance
#   rollout: default_enabled
#   rollback: remove module and its references
#   requires: pcea_cipher
#   since: 2026-06-02
#   unresolved: none
# === END MODULE_BUILD ===

# === CONTRACTS ===
# id: instance_initial_state_is_exact_signed_integer_carrier
#   given: PCEAInstance receives an initial state cell
#   then: the cell must be an exact int inside the configured signed word_bits range
#   class: correctness
# === END CONTRACTS ===

from __future__ import annotations

import copy

from .cipher import DEFAULT_WORD_BITS, _validate_seed, decrypt_state, encrypt_state

Seed = list[list[int]]
State = list[Seed]


def _zero_seed() -> Seed:
    return [[0] * 7 for _ in range(7)]


class PCEAInstance:
    """
    Stateful prime-circular encryption session.

    Maintains last_state (list of seeds) internally. After each encrypt call
    last_state advances to the plaintext seeds. The receiver's decrypt call
    mirrors this. Both sides must be initialized with the same seed and
    process states in the same order.

    Args:
        seed:      initial last_state as a non-empty list of 7×7 seeds
                   (list[list[list[int]]]).
        word_bits: Möbius disk size in bits. Must match between sender and
                   receiver. Default 64; set higher for larger value ranges.
    """

    def __init__(self, seed: State, word_bits: int = DEFAULT_WORD_BITS) -> None:
        if not seed:
            raise ValueError("seed must be non-empty")
        for i, s in enumerate(seed):
            _validate_seed(s, f"seed[{i}]", word_bits)
        self._last: State = copy.deepcopy(seed)
        self._word_bits = word_bits

    def encrypt(self, state: State) -> State:
        """Encrypt state and advance internal last_state to state."""
        encrypted = encrypt_state(state, self._last, self._word_bits)
        if state:
            self._last = copy.deepcopy(state)
        return encrypted

    def decrypt(self, encrypted: State) -> State:
        """Decrypt encrypted state and advance internal last_state to recovered state."""
        state = decrypt_state(encrypted, self._last, self._word_bits)
        if state:
            self._last = copy.deepcopy(state)
        return state

    @property
    def last_state(self) -> State:
        """Read-only snapshot of the current last_state."""
        return copy.deepcopy(self._last)
# ratios: loc_comments=30:44 imports_exports=3:1 calls_definitions=12:6
