# Actor B Report — PCEA Arity v1 (independent structural replay)

Role: Actor B / DeepSeek.

Boundary: this report records Actor B's own Phase-1 exact structural
microscope replay. It is not a cryptographic security claim.

## F1 identity used

```text
F1 candidate-freeze commit: e5fb94defae29a4c1b6d3e796763d575b34e4c08
F0 baseline commit:        ecf2ca0dec38bef29382e02121b0edde66763aa9
```

The on-disk `freeze.json` at the F1 commit itself still carries
`candidate_commit: PENDING_F1_SHA_UNTIL_CANDIDATE_COMMIT` by design; the
metadata-only correction commit records the F1 SHA. Both receipts are recorded
in the lock.

## Independence declaration

**FALSE.** Actor A's `REPORT_A.md` outcome labels and metrics table, and
`ACTOR_A_LOCK.json` preregistered labels, were seen by this agent before its
own lock was committed (during run discovery, before taking the Actor B role).
Actor A's implementation files (`candidate.py`, `structural.py`) and
`structural_results_A.json` were **not** opened. The lock records this
contamination explicitly. The coordinator must weigh it in adjudication.

## What was reconstructed independently

- B-specific namespace: `pcea-ucns/arity/replay_b/**`
- Own GF(2) Mobius/ANF transform, degree extraction, and full-degree deletion
  (`replay_b/anf.py`)
- Own PCEA-A_n cell adapter built directly from the frozen baseline primitives
  (`pcea.codec`, `pcea.kdf`, `pcea.primes`) and the frozen contributor order
  `[0, -3, +3, -1, +1, -2, +2]` (`replay_b/adapters.py`)
- A3 adapter verified against runtime `pcea.cipher.encrypt_seed` on the four
  frozen `a3_regression_cases` fixtures: exact match on every cell.
- Frozen runtime blob receipts verified against `BASELINE_FREEZE_V1.json`.

## PRF control reconstruction (B interpretation)

The PRF-A_n control keeps the same contributor labels/order/count, the same
public address serialization, the same plaintext input, the same output width,
and the same base-p digit shift surface as the PCEA adapter, but:

```text
key digits = HMAC-SHA256(key=b"pcea-arity-v1|prf-control", msg=<same payload>)
p = 2 fixed for the 8-bit structural lane (omits PCEA prime selection)
plaintext word position = value & 0xFF (omits Mobius codec)
```

At the target cell `(circle 0, tensor 0)` PCEA's selected prime is
`prime_at(0) = 2`, so the fixed `p = 2` coincides with PCEA there. For the
frozen 8-bit lane, the Mobius codec and the plain word mask coincide. The only
material difference at the target cell is therefore the hash construction:
PCEA's SHA-256 key stream versus HMAC-SHA256.

## Phase reached

```text
PHASE1_EXACT_STRUCTURAL_MICROSCOPE
```

Phase 2 was not authorized: H_PCEA did not reach
`SURVIVED_PCEA_SPECIFIC_ARITY`, so the frozen escalation gate stays closed.

## Phase-1 structural metrics (frozen parameters)

word_bits=8, target circle 0, target tensor 0, seed_index 0,
plaintext_values [0, 1, -1, 2, 127], non_contributor_value 0.
Examined bits = 8 output bits × 5 plaintext values = 40 per row.

| variant | arity | max degree | full-degree bits | examined bits | full-degree fraction | mismatch fraction |
|---|---:|---:|---:|---:|---:|---:|
| pcea | 2 | 2 | 20 | 40 | 0.500000 | 0.125000 |
| pcea | 3 | 3 | 15 | 40 | 0.375000 | 0.046875 |
| pcea | 5 | 5 | 15 | 40 | 0.375000 | 0.011719 |
| pcea | 7 | 7 | 15 | 40 | 0.375000 | 0.002930 |
| prf  | 2 | 2 | 25 | 40 | 0.625000 | 0.156250 |
| prf  | 3 | 3 | 15 | 40 | 0.375000 | 0.046875 |
| prf  | 5 | 5 | 15 | 40 | 0.375000 | 0.011719 |
| prf  | 7 | 7 | 25 | 40 | 0.625000 | 0.004883 |

## Outcome labels

```text
H_STRUCT: SURVIVED_STRUCTURAL_ARITY
H_PCEA:   FALSIFIED_PCEA_SPECIFIC_ARITY
H_HARD:   UNRESOLVED
```

Reasoning (mechanical, from frozen rules):

- PCEA-A5 and PCEA-A7 each have nonzero degree-5 and degree-7 output-bit
  coefficients, so H-STRUCT survives under the frozen definition.
- The matched PRF-A5 and PRF-A7 controls also show full-degree presence and
  the same maximum degrees. Under the frozen equality rules, full-degree
  presence shared with the matched PRF is not PCEA-specific, so H-PCEA is
  falsified.

## Full-suite result

```text
PYTHONPATH=. python -m pytest -q
136 passed, 2 skipped in 75.15s
```

## Observations and deviations

- `ratios_check.py --root . --strict` on the F1 tree reports pre-existing
  drift in Actor A's files `pcea-ucns/arity/candidate.py` and
  `pcea-ucns/arity/structural.py` (recorded vs computed ratio values differ).
  Actor B did not modify them. B's own files are covered with zero drift.
- Actor B used the existing pcea venv Python 3.12.3
  (`/home/wayseer_interdependentway_org/.venvs/pcea/bin/python`), matching the
  freeze environment.

## hmmm

- Boolean ANF full-degree residual is one exact operationalization of direct
  arity, not a universal definition.
- A PCEA-specific structural residual would still need a cryptanalytic
  consequence before any hardness claim.
- The PRF reconstruction is Actor B's documented interpretation of the frozen
  protocol text; a different but equally frozen-compatible PRF reading could
  shift the exact full-degree bit counts (the qualitative H-PCEA outcome is
  robust to this because both PCEA and the PRF show high-arity full-degree
  presence under every reading attempted).
- Actor B's independence is contaminated (see declaration above); the
  coordinator must decide how much separate-error-surface value this replay
  retains.
