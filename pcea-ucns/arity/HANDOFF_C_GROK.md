# Actor C Handoff — Grok

**Role:** independent adversarial attacker.

**Start only after Actor A publishes the F1 candidate-freeze SHA.**

You may inspect the frozen candidate implementation because you are attacking the actual candidate. You may **not** inspect Actor A/B result files, reports, outcome labels, or discussion before your own lock is committed.

## Start

You will be given `<F1_SHA>`.

```bash
git fetch origin
git switch --detach <F1_SHA>
git switch -c research/arity-v1-actor-c
```

Read:

```text
AGENTS.md
pcea-ucns/ARITY_FREEZE_AND_TEST.md
pcea-ucns/arity/BASELINE_FREEZE_V1.json
pcea-ucns/arity/freeze.json
pcea-ucns/arity/fixtures.json
pcea-ucns/arity/current_dependency_graph.json
all frozen candidate/adapter code present at F1
pcea/cipher.py
pcea/kdf.py
pcea/codec.py
pcea/primes.py
```

Do not read later Actor A/B commits.

## Attack objective

Try to falsify, not confirm, these claims:

```text
higher direct arity cannot be reduced to lower-arity information
any PCEA-specific residual exists beyond the matched PRF
any such residual increases cryptanalytic work
```

A clean break is a successful result.

## Two attack lanes

Keep these strictly separate in artifacts.

### C1 — preregistered v1 attacks

Implement/run the exact attack games declared in `ARITY_FREEZE_AND_TEST.md`:

```text
lower-arity-partition-assisted recovery
next-output prediction
known-prior-state lane
hidden-prior-state lane
matched PRF controls
```

Always perform low-cost static and exact attacks that can terminate a claim without expensive scaling.

Reduced-entropy exhaustive scaling (`B=[8,12]`, 16 trials each) is run only if the coordinator gives you a frozen `PHASE3_GATE.json` whose `authorized` field is true. You may inspect that gate token only; do not inspect the metrics or report that caused it.

If the gate is false, record `PHASE3_NOT_AUTHORIZED` and finish C1 without inventing a substitute workload.

### C2 — exploratory attacks

You are encouraged to design attacks not anticipated by v1, including where applicable:

```text
chosen-plaintext structure
single-contributor and multi-contributor differentials
state-reuse/equal-state probes
cross-circle correlation
prime/base representation leakage
address permutation or symmetry attacks
collision/aliasing behavior
candidate-state reconstruction from exposed outputs
shortcut attacks that bypass the intended lower-arity game
```

These are **exploratory**. Keep each attack's assumptions, attacker knowledge, fixtures, and cost explicit.

A successful exploratory attack may falsify a security-relevant candidate immediately. A failed exploratory attack cannot upgrade standing because it was not part of the frozen acceptance criteria.

## Mutation boundary

Write only C-specific attack code/results, for example:

```text
pcea-ucns/arity/attacks_c/**
tests/test_arity_attacks_c.py
pcea-ucns/arity/attack_results_C.json
pcea-ucns/arity/REPORT_C.md
pcea-ucns/arity/locks/ACTOR_C_LOCK.json
```

Do not modify:

```text
pcea/**
frozen candidate code
fixtures.json
freeze.json
Actor A/B files
```

Behavior-bearing Python modules must follow repo-local MODULE_BUILD/CONTRACTS conventions; tests own CHECKS.

## Measurement discipline

Primary attack work metrics are:

```text
candidate secrets evaluated
oracle/transcript queries
surviving candidates after each observation
recovery success
prediction success
```

Wall time is metadata only. Preflight finite workloads before starting; once healthy computation begins, let it reach its natural terminal condition.

Do not infer security from failure to break.

## Required artifacts

Emit:

```text
pcea-ucns/arity/attack_results_C.json
pcea-ucns/arity/REPORT_C.md
pcea-ucns/arity/locks/ACTOR_C_LOCK.json
```

`attack_results_C.json` must contain separate top-level sections for:

```text
preregistered_v1
exploratory
```

The lock must record:

```text
actor = Grok
role = C
F0 baseline SHA + receipt SHA256
F1 SHA + freeze.json SHA256
PHASE3_GATE hash/status if supplied
result commit SHA
artifact path -> SHA256
successful breaks
preregistered outcome labels where applicable
declaration that Actor A/B result files were not consulted
contamination/deviations
hmmm
```

Run the full suite:

```bash
PYTHONPATH=. python -m pytest -q
```

Commit and push only your C-specific work.

## Terminal response

Return only:

```text
F1 SHA used
Phase3 gate status/hash
Actor C result SHA
Actor C lock SHA256
Preregistered attack outcomes
Exploratory breaks, if any
Full-suite result
Any UNRESOLVED/BLOCKED/hmmm
Independence declaration
```

Do not merge and do not reconcile with A/B.
