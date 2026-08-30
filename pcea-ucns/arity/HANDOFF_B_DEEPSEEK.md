# Actor B Handoff — DeepSeek

**Role:** independent structural replayer/reimplementation.

**Start only after Actor A publishes the F1 candidate-freeze SHA.**

Do not read Actor A's result commit, `structural_results_A.json`, `REPORT_A.md`, or Actor A's outcome labels before your own lock is committed.

## Start

You will be given `<F1_SHA>`.

```bash
git fetch origin
git switch --detach <F1_SHA>
git switch -c research/arity-v1-actor-b
```

Read:

```text
AGENTS.md
pcea-ucns/ARITY_FREEZE_AND_TEST.md
pcea-ucns/arity/BASELINE_FREEZE_V1.json
pcea-ucns/arity/freeze.json
pcea-ucns/arity/fixtures.json
pcea/cipher.py
pcea/kdf.py
pcea/codec.py
pcea/primes.py
```

For independence, **do not inspect or import Actor A's arity-analysis implementation before locking your result.** Do not open files whose purpose is Actor A's ANF/reconstruction analyzer. Do not import Actor A's candidate adapter for the structural calculation.

Reconstruct the PCEA-A2/A3/A5/A7 relation directly from the written protocol and frozen baseline primitives. In particular, contributor order is fixed:

```text
[0, -3, +3, -1, +1, -2, +2]
```

and each `A_n` uses the corresponding prefix as one joint contributor list to the same hash/KDF relation. Independently reconstruct the matched PRF controls from the protocol.

## Independent calculation

Create your implementation only under a B-specific namespace such as:

```text
pcea-ucns/arity/replay_b/**
tests/test_arity_replay_b.py
```

Do not modify:

```text
pcea/**
pcea-ucns/arity/fixtures.json
pcea-ucns/arity/freeze.json
Actor A implementation files
```

Implement your own exact Boolean truth-table enumeration and ANF/Mobius transform. Do not copy Actor A code.

Verify independently:

```text
A3 reproduces F0 current PCEA
A2/A3/A5/A7 use the frozen contributor order
all 2^n assignments are enumerated exactly
full-degree coefficients are computed exactly
lower-order reconstruction deletes degree-n terms exactly
matched PRF controls use the same declared inputs/budget
```

Run Phase 1. If your own preregistered result reaches Phase 2, run the frozen sensitivity grid. Do not add parameters after seeing results.

## Disagreement rule

You are not trying to agree with Actor A. You should not know Actor A's result.

If your internal calculations disagree with one another, classify `UNRESOLVED_IMPLEMENTATION_DISAGREEMENT` and identify the exact conflicting artifacts.

After your lock is committed, later adjudication may compare A and B. A/B mismatch is not settled by voting.

## Required artifacts

Emit:

```text
pcea-ucns/arity/replay_results_B.json
pcea-ucns/arity/REPORT_B.md
pcea-ucns/arity/locks/ACTOR_B_LOCK.json
```

The lock must record:

```text
actor = DeepSeek
role = B
F0 baseline SHA + receipt SHA256
F1 SHA + freeze.json SHA256
your result commit SHA
artifact path -> SHA256
outcome labels
declaration that Actor A result files were not consulted
any contamination/deviation
hmmm
```

Run the full repository suite before locking:

```bash
PYTHONPATH=. python -m pytest -q
```

Commit and push only your B-specific work.

## Terminal response

Return only:

```text
F1 SHA used
Actor B result SHA
Actor B lock SHA256
Phase reached
Outcome labels
Full-suite result
Any UNRESOLVED/BLOCKED/hmmm
Independence declaration
```

Do not inspect Actor A/C results after finishing unless the coordinator explicitly begins adjudication. Do not merge.
