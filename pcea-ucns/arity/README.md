# PCEA Arity v1 — Refrozen Run Index

Current runtime source freeze:

```text
The-Interdependency/pcea
main@ecf2ca0dec38bef29382e02121b0edde66763aa9
package metadata version: 0.2.0
```

Authoritative files:

```text
../ARITY_FREEZE_AND_TEST.md
BASELINE_FREEZE_V1.json
HANDOFF_A_CODEX.md
HANDOFF_B_DEEPSEEK.md
HANDOFF_C_GROK.md
HANDOFF_D_GEMINI.md
```

## Run order

```text
0. Protocol branch is frozen from current main.
1. Codex (A) builds candidate + fixtures, verifies A3 against baseline, then commits F1 BEFORE results.
2. A, B, C work from the same F1 identity without consulting one another's results.
3. Codex (A) runs the preregistered experiment and locks results.
4. DeepSeek (B) independently reimplements the structural calculation and locks results.
5. Grok (C) attacks the frozen candidate and locks results. It may receive only the outcome-blind Phase-3 gate token from A.
6. Coordinator verifies A/B/C lock hashes and creates ADJUDICATION_PACKET.json without reconciling conclusions.
7. Gemini (D) is called only now. Gemini adjudicates the immutable packet and does not repair/re-run.
```

B and C may run concurrently after F1. Gemini may not.

## Independence rule

The value of multiple actors comes from **separate error surfaces**, not from collaborative authorship.

```text
A owns the candidate freeze and its own measurement.
B independently reconstructs the structural result.
C independently attacks the frozen candidate.
D adjudicates only after A/B/C are immutable.
```

Do not combine A/B/C into a shared discussion before their locks exist.

## Freeze identities

F0 is already fixed by `BASELINE_FREEZE_V1.json`.

F1 does not exist until Actor A builds and commits the candidate/fixture freeze. Once F1 exists, do not give B/C Actor A's later result SHA as their starting point. Give them the exact F1 SHA.

## Coordinator checklist

Before Actor B/C:

```text
[ ] F1 SHA exists
[ ] freeze.json names F0 and F1
[ ] fixtures.json is committed at F1
[ ] A3 baseline regression passes
[ ] frozen runtime files are byte-identical to F0
```

Before Gemini:

```text
[ ] ACTOR_A_LOCK.json committed and hashed
[ ] ACTOR_B_LOCK.json committed and hashed
[ ] ACTOR_C_LOCK.json committed and hashed
[ ] all lock artifact hashes independently verified
[ ] F0 identity same in all locks
[ ] F1 identity same in all locks
[ ] ADJUDICATION_PACKET.json contains identities/hashes only, not reconciliation
[ ] no post-lock artifact has replaced an actor result
```

## Standing

No arity result exists yet. Current standing is:

```text
F0 source identity: FROZEN
F1 candidate identity: NOT YET CREATED
H-STRUCT: UNRESOLVED
H-PCEA: UNRESOLVED
H-HARD: UNRESOLVED
professional cryptographic review: NOT PERFORMED
```

## hmmm

- The Boolean ANF microscope is one exact operationalization of direct arity, not a universal definition of arity.
- A PCEA-specific structural residual would still need a cryptanalytic consequence before it supports a security-relevant claim.
- A valid break by Actor C overrides survival observations for the property it breaks.
