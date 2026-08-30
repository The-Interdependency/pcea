# PCEA Arity Freeze and Test Procedure — v1 Refreeze

**Status:** preregistered, refrozen, pre-execution.

**Baseline:** `main@ecf2ca0dec38bef29382e02121b0edde66763aa9`.

**Authoritative source-identity receipt:** `pcea-ucns/arity/BASELINE_FREEZE_V1.json`.

This protocol asks one bounded question:

> Does PCEA instantiate an irreducible direct-arity relation that contributes measurable cryptanalytic hardness beyond lower-arity decompositions and a matched conventional PRF control?

It is intentionally fail-closed. A structural residual is not a security result. A harder frozen attack is not a security proof. No result automatically promotes runtime PCEA, PCEA-UCNS key establishment, or any cryptographic claim.

## 1. Why this was refrozen

The first arity protocol targeted an older release-readiness branch. Current `main` subsequently changed `pcea/cipher.py` and `pcea/codec.py` and advanced the package to 0.2.0. No actor had begun the arity experiment, so v1 is refrozen against current `main` rather than deliberately testing an obsolete transform.

The current implementation still derives one cell's key stream from exactly three previous-state contributors: the same circle and heptagram neighbors at `-3` and `+3`. Therefore current PCEA enters this experiment as an **A3 state-key baseline**, not as A7 merely because the state has seven circles.

## 2. Authority and boundaries

Repository authority is `AGENTS.md` plus the repo-local skills under `.agents/skills/`. Before implementation, Actor A must read:

```text
AGENTS.md
.agents/skills/README.md
.agents/skills/msdmd/SKILL.md
.agents/skills/meta-module-build/SKILL.md
.agents/skills/test-build/SKILL.md
```

New behavior-bearing research Python modules require module-local `MODULE_BUILD` metadata. Source obligations belong in `CONTRACTS`; executable witnesses belong in test `CHECKS`. Unknowns remain `hmmm`.

The v1 experiment may create or modify only:

```text
pcea-ucns/ARITY_FREEZE_AND_TEST.md
pcea-ucns/arity/**
tests/test_arity_*.py
pcea-ucns/README.md
```

It MUST NOT modify any path listed under `frozen_runtime_paths` in `BASELINE_FREEZE_V1.json`.

The current baseline does not contain the unmerged ratcheted-session prototype. v1 therefore tests current PCEA directly and may use research-only matched-secret adapters where a secret-bearing attack game is needed. Such adapters remain under `pcea-ucns/arity/` and are not runtime APIs.

## 3. Freeze hierarchy

There are two freezes.

### Freeze F0 — source identity

Already fixed by `BASELINE_FREEZE_V1.json`:

```text
repository = The-Interdependency/pcea
baseline = ecf2ca0dec38bef29382e02121b0edde66763aa9
runtime blob SHAs = exact map in BASELINE_FREEZE_V1.json
```

Any runtime mismatch is:

```text
BLOCKED_FREEZE_DRIFT
```

Do not repair the baseline. Restart only through an explicit new refreeze.

### Freeze F1 — candidate/fixture freeze

Actor A builds the research adapters and fixtures but MUST create an F1 candidate-freeze commit **before any actor records experimental conclusions**.

F1 must contain:

```text
pcea-ucns/arity/freeze.json
pcea-ucns/arity/fixtures.json
pcea-ucns/arity/current_dependency_graph.json
pcea-ucns/arity/candidate.py        # or equivalently named research adapter(s)
pcea-ucns/arity/structural.py       # A may implement its own analyzer here
tests/test_arity_freeze.py
tests/test_arity_current_baseline.py
```

`freeze.json` must record F0 identity, F1 commit, Python/platform, fixture-generator version, all parameters, deterministic seeds, metrics, controls, outcome labels, and escalation rules.

The A3 research adapter MUST reproduce frozen current PCEA outputs exactly for matched valid inputs. Failure is `BLOCKED_A3_ADAPTER_MISMATCH`.

Actors B and C branch from F1, not from Actor A's later result commit.

## 4. Definitions

### State-key arity

The number of distinct prior-state circle carriers jointly consumed by the per-cell key-stream relation before the current plaintext value is transformed.

### Direct arity

`A_n` is direct arity `n` only when one per-cell derivation consumes all `n` labeled contributors as one joint relation. A seven-node graph made entirely of overlapping triads is not direct arity seven.

### Lower-arity family

For contributor set `[n]`, every proper subset `S` with `|S| < n` is lower-arity. A higher-arity claim is not earned if the frozen output invariant is exactly reconstructable from the lower-order family under the preregistered test.

### Arity residual

For the exact Boolean structural microscope, an output bit has a direct `n`-way residual when its algebraic normal form has a nonzero degree-`n` coefficient over the `n` binary contributor variables.

Record at minimum:

```text
maximum_algebraic_degree
full_degree_output_bits
output_bits_examined
full_degree_fraction
mismatches_after_deleting_degree_n
mismatch_fraction
```

ANF degree is a structural diagnostic, not a security metric.

## 5. Frozen contributor order

No contributor order may be selected after results.

```text
OFFSETS = [0, -3, +3, -1, +1, -2, +2]

A2 = [0, -3]
A3 = [0, -3, +3]
A5 = [0, -3, +3, -1, +1]
A7 = [0, -3, +3, -1, +1, -2, +2]
```

All indices are modulo seven around the target circle.

A3 is the exact current contributor relation and must be regression-equivalent to baseline PCEA.

## 6. Matched controls

Every `PCEA-A_n` must be compared with `PRF-A_n` using the same:

```text
contributor labels/order/count
public address data
plaintext input
output width
fixture set
master-secret entropy when a secret is in scope
query/transcript budget
```

`PRF-A_n` uses SHA-256/HMAC-SHA256 and omits PCEA's prime selection, base-p representation, Möbius codec, and PCEA state transform.

The control answers the load-bearing question:

> Is any high-order behavior specific to PCEA, or is it ordinary behavior of hashing multiple inputs jointly?

If PCEA and PRF exhibit the same structural behavior and the same attack scaling within the frozen equality rules, PCEA earns no arity-specific cryptographic claim.

## 7. Phase 0 — current dependency audit

Actor A must emit `current_dependency_graph.json` describing, for every encrypted cell:

```text
current plaintext dependency
prior-state contributor dependency
address dependency
prime/base dependency
hash/KDF dependency
```

The expected result to verify is:

```text
state-key direct arity = 3
seven-circle topology = overlapping local triadic relations
```

If source analysis falsifies that description, preserve the exact discovered dependency graph and classify the interpretation `UNRESOLVED_BASELINE_ARITY_DESCRIPTION`; do not redefine arity later to fit results.

## 8. Phase 1 — exact structural microscope

This is the first decisive experiment.

For each `PCEA-A_n` and `PRF-A_n`:

1. isolate one target tensor coordinate and one output cell;
2. hold all non-contributor prior-state cells at a frozen constant;
3. treat each of the `n` contributor values as a binary variable in `{0,1}`;
4. enumerate every `2^n` assignment exactly;
5. evaluate the frozen plaintext set;
6. compute exact Boolean ANF/Möbius coefficients for every output bit;
7. delete full-degree terms and exactly reconstruct the truth table;
8. record all metrics without post-hoc threshold changes.

Frozen v1 values:

```text
PLAINTEXT_VALUES = [0, 1, -1, 2, 127]
WORD_BITS = 8
TARGET_CIRCLE = 0
TARGET_TENSOR = 0
SEED_INDEX = 0
NON_CONTRIBUTOR_VALUE = 0
```

The 8-bit lane is a structural microscope only.

### H-STRUCT

At least one `A_n`, `n > 3`, has at least one output bit with a nonzero degree-`n` term.

```text
no A5/A7 full-degree term -> FALSIFIED_STRUCTURAL_ARITY
A5 or A7 full-degree term -> SURVIVED_STRUCTURAL_ARITY
exact table cannot be established -> BLOCKED
```

### H-PCEA

PCEA's structural result differs reproducibly from matched PRF controls under frozen equality rules.

```text
no material separation -> FALSIFIED_PCEA_SPECIFIC_ARITY
reproducible separation -> SURVIVED_PCEA_SPECIFIC_ARITY
invalid comparison -> UNRESOLVED
```

A full-degree term shared with the PRF control is not a PCEA-specific result.

## 9. Phase 2 — frozen sensitivity grid

Only Actor A's preregistered escalation rules may authorize Phase 2 for its own result lane. Actor B may independently reproduce the same grid if its structural result reaches the same gate.

Vary one frozen dimension at a time:

```text
word_bits = [8, 12, 16]
target_circle = [0, 1, 3, 6]
target_tensor = [0, 1, 3, 6]
plaintext_values = [0, 1, -1, 2, 127]
```

Record:

```text
maximum algebraic degree
full_degree_fraction
single-contributor intervention change fraction
collision count
output-bit balance
```

Do not add values after inspecting results.

## 10. Phase 3 — reduced-entropy attack scaling

Only a frozen gate authorizes expensive scaling. Actor C may always run cheap falsification attacks; reduced-entropy scaling uses a gate token without receiving Actor A/B metrics.

Master-secret search spaces:

```text
B = [8, 12]
TRIALS = 16 per B
```

A `b`-bit integer seed is deterministically expanded to API-compatible secret bytes using SHA-256. Fixture seeds derive from:

```text
SHA256("pcea-arity-v1|secret-fixture|<b>|<trial>")
```

The attacker knows algorithm/source, variant/arity, public parameters, addresses, chosen plaintexts, transcripts/ciphertexts exposed by the game, and fixture-generation rules, but not the master-secret seed.

Run at minimum:

```text
exhaustive secret recovery
lower-arity-partition-assisted recovery
next-output prediction
known-prior-state and hidden-prior-state lanes kept separate
```

Primary work metrics:

```text
candidate secrets evaluated
oracle/transcript queries
surviving candidates after each observation
recovery/prediction success
```

Wall time is environment metadata, not the scientific stopping rule.

### H-HARD

After matching entropy, transcript/query budget, and arity, PCEA requires greater frozen attack work or yields lower recovery/prediction success than its matched PRF control.

```text
no advantage or PCEA weaker -> FALSIFIED_ARITY_HARDNESS_BENEFIT
separation survives frozen harness -> SURVIVED_CURRENT_HARNESS
attack family/resource cannot decide -> UNRESOLVED
```

`SURVIVED_CURRENT_HARNESS` does not mean secure.

Do not extend to `b=16` or larger in v1. A later preregistration is required.

## 11. Multi-actor independence protocol

The actor assignment for this run is:

```text
A — Codex: freeze steward / builder / first execution
B — DeepSeek: independent structural replayer
C — Grok: adversarial attacker
D — Gemini: post-freeze adjudicator
```

### A0/F1 candidate freeze

Codex first produces F1 and commits it before publishing any experimental conclusion. All three active actors then work from the same F1 candidate identity.

### Actor A result isolation

After F1, Codex creates its result branch/commit and runs the preregistered phases. It records its result lock before seeing B/C outputs.

### Actor B independence

DeepSeek receives the protocol, F0/F1 receipts, baseline source, candidate specification, and deterministic fixtures. It MUST independently implement the Phase-1 ANF/Möbius computation and may not import Actor A's structural-analysis implementation. It must not inspect Actor A's result files or interpretation before its own result lock is committed.

### Actor C independence

Grok receives the protocol, F0/F1 receipts, frozen candidate, attack game, and fixtures. It must not inspect Actor A/B result files before its lock. It separates preregistered attacks from exploratory attacks. A successful exploratory attack may falsify immediately; failure of an exploratory attack cannot raise standing.

### Actor D timing

Gemini is not called until A, B, and C have each committed immutable result locks. Gemini receives no intermediate discussion. It adjudicates rather than repairs.

## 12. Actor locks

Each actor emits:

```text
pcea-ucns/arity/locks/ACTOR_<A|B|C>_LOCK.json
```

containing:

```text
actor role/model
F0 baseline commit and receipt hash
F1 candidate commit and freeze hash
actor result commit
every result artifact path + SHA256
outcome labels
known deviations or contamination
hmmm
```

After A/B/C locks exist, create one immutable adjudication packet manifest:

```text
pcea-ucns/arity/ADJUDICATION_PACKET.json
```

It names exact commits/hashes only; it does not reconcile conclusions.

Gemini emits:

```text
pcea-ucns/arity/GEMINI_ADJUDICATION.md
pcea-ucns/arity/locks/ACTOR_D_LOCK.json
```

with one classification per preregistered claim:

```text
FALSIFIED
SURVIVED
UNRESOLVED
BLOCKED
```

No voting. Disagreement is evidence to resolve, not a majority rule.

## 13. Required result artifacts

Actor A:

```text
freeze.json
fixtures.json
current_dependency_graph.json
structural_results_A.json
attack_results_A.json        # only if reached
REPORT_A.md
locks/ACTOR_A_LOCK.json
```

Actor B:

```text
replay_results_B.json
REPORT_B.md
locks/ACTOR_B_LOCK.json
```

Actor C:

```text
attack_results_C.json
REPORT_C.md
locks/ACTOR_C_LOCK.json
```

Adjudication:

```text
ADJUDICATION_PACKET.json
GEMINI_ADJUDICATION.md
locks/ACTOR_D_LOCK.json
```

## 14. Test and resource rules

Every implementation/result branch must run:

```bash
PYTHONPATH=. python -m pytest -q
```

Actor A must add tests that fail if:

```text
F0 runtime blob identity changes
A3 adapter differs from current PCEA
fixture schema changes without version change
artifact points to wrong F0/F1 receipt
outcome label is outside preregistered vocabulary
```

Before each compute phase, preflight whether the environment can reach the natural terminal condition. If materially uncertain, do not start; record `BLOCKED_RESOURCE_PREFLIGHT`. Once a healthy phase starts, let it complete. Do not invent arbitrary wall-clock stopping rules.

## 15. Completion and escalation

The scientific result layer closes when Gemini has adjudicated the locked A/B/C packet, or when a prior hard falsification/block makes later claims impossible.

Interpretation rules:

```text
A5/A7 no exact higher-order residual
  -> structural hypothesis falsified

PCEA residual indistinguishable from matched PRF
  -> no demonstrated PCEA-specific arity property

PCEA-specific structural residual but no attack advantage
  -> interesting structure, no demonstrated cryptographic benefit

PCEA-specific residual + frozen attack advantage
  -> survives current harness; independent professional cryptanalysis next

any practical break
  -> falsified for that claimed security property
```

No merge to runtime and no production-security claim is authorized by this protocol.

## hmmm

- Direct arity may require a richer operationalization than Boolean ANF degree. v1 tests one exact translation and must not silently universalize it.
- PCEA may prove useful as a relational/state transform even if it adds no cryptographic hardness over a standard PRF.
- If v1 survives, the next protocol should test chosen-plaintext/chosen-ciphertext behavior, state compromise, differential structure, session reuse, and conventional AEAD comparisons under independent cryptographic review.
