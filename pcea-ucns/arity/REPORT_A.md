# Actor A Report - PCEA Arity v1

Role: Actor A / Codex.

Boundary: this report records the preregistered structural microscope only. It is not a cryptographic security claim.

## Phase Reached

PHASE1_EXACT_STRUCTURAL_MICROSCOPE

## Outcome Labels

- H_STRUCT: SURVIVED_STRUCTURAL_ARITY
- H_PCEA: FALSIFIED_PCEA_SPECIFIC_ARITY
- H_HARD: UNRESOLVED

## Phase 3 Gate

- authorized: false
- criterion: authorized only when H_STRUCT == SURVIVED_STRUCTURAL_ARITY and H_PCEA == SURVIVED_PCEA_SPECIFIC_ARITY

## Structural Metrics

| variant | arity | max degree | full-degree bits | examined bits | mismatch fraction |
|---|---:|---:|---:|---:|---:|
| pcea | 2 | 2 | 20 | 40 | 0.125000 |
| pcea | 3 | 3 | 15 | 40 | 0.046875 |
| pcea | 5 | 5 | 15 | 40 | 0.011719 |
| pcea | 7 | 7 | 15 | 40 | 0.002930 |
| prf | 2 | 2 | 30 | 40 | 0.187500 |
| prf | 3 | 3 | 10 | 40 | 0.031250 |
| prf | 5 | 5 | 20 | 40 | 0.015625 |
| prf | 7 | 7 | 10 | 40 | 0.001953 |

## hmmm

- Direct arity may need richer operationalizations beyond this Boolean ANF microscope.
- Shared behavior with the matched PRF control is not PCEA-specific evidence.
