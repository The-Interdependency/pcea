# PCEA Arity Freeze and Test Procedure

**Status:** preregistered research procedure; no arity result is claimed by this document.

**Purpose:** determine whether PCEA's relational structure contains a measurable direct-arity effect, whether that effect survives lower-arity partitioning, whether it is attributable to PCEA rather than the underlying hash/PRF, and only then whether it changes cryptanalytic attack cost.

This procedure is intentionally fail-closed. A positive structural result is not a security result. A positive attack-cost result is not a security proof. No runtime promotion follows automatically from any result.

## 1. Decision boundary

The decision this run must inform is:

> Does PCEA instantiate irreducible relational arity that contributes measurable cryptographic hardness beyond lower-arity decompositions and a matched conventional PRF control?

The earliest load-bearing unknown is structural:

> Is the current seven-circle construction actually heptadic, or is it a seven-member topology assembled from lower-arity local relations?

The current frozen implementation derives one cell's PCEA key stream from exactly three previous-state contributors: the same circle plus the two heptagram neighbors at `-3` and `+3`. Therefore the current implementation must enter this experiment as the **A3 baseline**, not be called A7 merely because the state has seven circles.

## 2. Authority and non-transfer

This is a PCEA proving-ground experiment. It may test arity-shaped relations but may not promote an arity result into UCNS, METAPAT, or cryptographic canon.

METAPAT supplies a useful question-form: tensor is simultaneous arrangement; relation is readable configuration within tensor. It does not make cryptographic arity a root axiom. Arity in this procedure is an application/research variable that must earn standing through intervention and partition tests.

The prior arity research supplies the falsification form: a claimed `n`-ary relation is not earned if lower-arity partitions reproduce every relevant invariant. That form transfers. Consciousness, scale, Möbius ontology, or other domain claims do not transfer into this cryptographic test.

## 3. Frozen baseline

The implementation baseline is the PCEA release-readiness candidate:

```text
repository: The-Interdependency/pcea
baseline_commit: f69ca59a278f81c9b2df80d7cb8053ca1cb8c5f5
```

The following baseline source objects are frozen for this experiment and MUST NOT be edited by the implementing actor:

```text
pcea/cipher.py
pcea/codec.py
pcea/kdf.py
pcea/primes.py
pcea/instance.py
pcea/contract.py
pcea/__init__.py
pcea-ucns/ratcheted_session.py
```

The experiment branch may contain this procedure and new research-only files after the baseline commit. Before running any experiment, the implementing actor MUST verify that every frozen path is byte-identical to `baseline_commit`.

A required freeze receipt is:

```text
pcea-ucns/arity/freeze.json
```

It MUST record:

```text
repository
baseline_commit
experiment_commit
frozen_path -> git blob SHA
python version
platform
experiment schema version
fixture generator version
all parameter sets
all deterministic fixture seeds
all metrics
all controls
all outcome labels
all escalation rules
```

If any frozen path differs from the baseline, classify the run `BLOCKED` and do not execute the experiment.

## 4. Mutation boundary

For v1, Codex may create or modify only:

```text
pcea-ucns/arity/**
tests/test_arity_*.py
pcea-ucns/ARITY_FREEZE_AND_TEST.md
pcea-ucns/README.md
```

Do not modify `pcea/` or `pcea-ucns/ratcheted_session.py`.

All new executable Python files must follow the repository's ratios/provenance conventions and remain stdlib-only except for pytest as an existing dev dependency.

The arity implementation is a proving-ground harness, not a new public API.

## 5. Definitions

### 5.1 State-key arity

For this experiment, **state-key arity** is the number of distinct prior-state circle carriers jointly supplied to the per-cell key-stream relation before the current plaintext value is transformed.

This deliberately does not count the current plaintext cell itself. If a later experiment wants total transform arity, that must be named separately.

### 5.2 Direct arity

A variant `A_n` has declared direct state-key arity `n` only when one per-cell key derivation consumes all `n` labeled contributors as one joint input relation.

A graph containing `n` objects connected only by dyads or triads is not automatically `n`-ary.

### 5.3 Lower-arity partition

For direct arity `n`, a lower-arity partition uses only proper subsets of the contributor set:

```text
S subset [n], with |S| < n
```

A claimed `n`-ary residual survives structurally only if at least one frozen output invariant cannot be reconstructed from the complete family of lower-order components under the exact v1 reconstruction test.

### 5.4 Arity residual

`arity_residual` is a research diagnostic, not a security metric.

For the exact Boolean toy-domain test, it is present for an output bit when that bit's algebraic normal form contains a nonzero degree-`n` coefficient over the `n` binary contributor variables.

Equivalently, the exact Möbius/Boolean transform of the truth table has a nonzero coefficient on the full contributor set.

Record:

```text
full_degree_output_bits
output_bits_examined
full_degree_fraction
maximum_algebraic_degree
```

Do not replace this exact test with an ML predictor or a correlation proxy.

## 6. Frozen contributor order and variants

Use one seven-carrier rotational order so arity changes are not chosen after results:

```text
OFFSETS = [0, -3, +3, -1, +1, -2, +2]
```

For the target circle `c`, indices are modulo 7.

The v1 variants are prefixes of that order:

```text
A2 = [0, -3]
A3 = [0, -3, +3]              # exact current PCEA contributor relation
A5 = [0, -3, +3, -1, +1]
A7 = [0, -3, +3, -1, +1, -2, +2]
```

The A3 research adapter MUST reproduce frozen current PCEA output exactly for matched inputs. If it does not, the experiment is `BLOCKED`; repair the adapter, not the baseline.

## 7. Matched controls

Every `A_n` PCEA variant MUST have a matched `PRF-A_n` control.

The control must:

- use the same contributor order and count;
- use the same public address information;
- use the same provisioned/master secret entropy when a secret is in scope;
- use SHA-256/HMAC-SHA256, matching the experiment lane's primitive;
- produce the same output bit width;
- transform the same current plaintext cell/state;
- omit PCEA prime selection, base-`p` representation, Möbius codec, and PCEA state transform.

The purpose is to answer:

> Is the measured arity effect a PCEA contribution, or merely the ordinary high-order behavior of a cryptographic hash/PRF over multiple inputs?

Also retain:

```text
PCEA-A3-current
```

as the exact frozen-current baseline.

## 8. Hypotheses and outcome labels

Freeze these before execution.

### H-STRUCT: structural direct-arity residual

For at least one `A_n`, `n > 3`, at least one output bit has an exact degree-`n` component under the Boolean toy-domain test.

- no full-degree component -> `FALSIFIED_STRUCTURAL_ARITY`
- full-degree component -> `SURVIVED_STRUCTURAL_ARITY`
- harness cannot establish exact truth table -> `BLOCKED`

### H-PCEA: PCEA-specific arity contribution

PCEA's structural arity diagnostics differ reproducibly from its matched `PRF-A_n` control under the frozen fixtures.

- no material difference beyond the frozen equality/tolerance rules -> `FALSIFIED_PCEA_SPECIFIC_ARITY`
- reproducible difference -> `SURVIVED_PCEA_SPECIFIC_ARITY`
- comparison invalid or underpowered -> `UNRESOLVED`

### H-HARD: cryptanalytic benefit

After controlling master-secret entropy, transcript exposure, query budget, and arity, an arity-preserving PCEA variant requires greater frozen attack work or yields lower recovery/prediction success than its matched PRF control.

- no advantage or PCEA is weaker -> `FALSIFIED_ARITY_HARDNESS_BENEFIT`
- advantage survives all frozen controls -> `SURVIVED_CURRENT_HARNESS`
- resource/attack family cannot decide -> `UNRESOLVED`

`SURVIVED_CURRENT_HARNESS` is never rewritten as `secure`, `hard`, `production-ready`, or `reviewed`.

## 9. Phase 0 — structural dependency audit

Before implementing A2/A5/A7, generate a machine-readable dependency description of frozen current PCEA.

For every encrypted cell identify:

```text
current plaintext cell dependencies
prior-state cell dependencies
address dependencies
prime/base dependency
hash/KDF dependency
session-secret-derived dependency when the ratcheted wrapper is used
```

Emit:

```text
pcea-ucns/arity/current_dependency_graph.json
```

Required v1 finding to verify, not assume:

```text
current PCEA state-key direct arity = 3
seven-circle topology = overlapping local relations
```

If inspection shows that statement is incomplete or wrong, record the exact dependency relation and revise only the interpretation section of the eventual report. Do not silently redefine arity after seeing later results.

## 10. Phase 1 — exact structural arity test

This is the minimal decisive experiment and MUST run before cryptanalytic scaling.

### 10.1 Exact toy domain

Isolate one target tensor coordinate and one target output cell.

For each `A_n` and `PRF-A_n`:

1. Hold all non-contributor prior-state cells at a frozen constant.
2. Treat each of the `n` contributor values as one binary variable in `{0,1}`.
3. Enumerate all `2^n` contributor assignments exactly.
4. Use frozen current plaintext values:

```text
PLAINTEXT_VALUES = [0, 1, -1, 2, 127]
```

5. Use:

```text
WORD_BITS = 8
TARGET_CIRCLE = 0
TARGET_TENSOR = 0
SEED_INDEX = 0
```

6. For every output bit, compute the exact Boolean algebraic normal form / Möbius transform over the contributor variables.
7. Record the highest degree and whether the degree-`n` coefficient is nonzero.

The small `word_bits` value is an exact structural microscope only. It makes no 8-bit security claim.

### 10.2 Exact lower-order reconstruction

For each output bit, reconstruct the function after deleting all degree-`n` terms.

Record:

```text
truth_table_rows
exact_matches_without_degree_n
mismatches_without_degree_n
mismatch_fraction
```

If deleting the full-degree component changes no output for every fixture, the declared `n`-way component is absent under this representation.

### 10.3 Phase-1 stop/escalation rule

- If A5 and A7 both lack full-degree components: stop. H-STRUCT is falsified; do not run the maximal cryptanalytic program.
- If A5 or A7 has a full-degree component but the matched PRF control shows the same result: continue only through the PCEA-specific comparison; do not infer a PCEA security benefit.
- If PCEA shows a reproducible residual not present in the matched PRF control: enter Phase 2.
- Any adapter mismatch with A3 current output: `BLOCKED` until prerequisite repair.

## 11. Phase 2 — sensitivity and PCEA-specific controls

Phase 2 asks whether the structural result is robust and PCEA-specific.

Use the same exact enumeration while varying only one frozen dimension at a time:

```text
word_bits: [8, 12, 16]
target_tensor: [0, 1, 3, 6]
target_circle: [0, 1, 3, 6]
plaintext_values: frozen list above
```

Do not add parameter values after seeing results.

For every PCEA variant and matched PRF variant record:

```text
maximum algebraic degree
full_degree_fraction
changed-output fraction per single contributor intervention
collision count
output-bit balance
```

Balance, collision rate, and avalanche/sensitivity are diagnostics only; none is a security proof.

H-PCEA survives only if the predeclared comparison shows a reproducible PCEA/control difference across the frozen parameter grid rather than one cherry-picked coordinate.

## 12. Phase 3 — reduced-entropy cryptanalytic scaling

Run only if the frozen escalation rule reaches this phase.

The purpose is to measure attack scaling exactly at toy/reduced entropy before spending effort on realistic key sizes.

### 12.1 Master-secret fixtures

Use master-secret seeds with entropy:

```text
B = [8, 12]
```

A `b`-bit seed is deterministically expanded with SHA-256 into the API-compatible secret bytes so all constructions use the same actual secret length while the exhaustive search space remains exactly `2^b`.

Fixture secrets MUST be generated before attack execution from:

```text
SHA256("pcea-arity-v1|secret-fixture|<b>|<trial>")
```

Freeze the first 16 trials for each `b`.

### 12.2 Attacker knowledge

The v1 attacker knows:

```text
algorithm and source
variant and arity
all public parameters
session id
direction
sequence numbers
AAD
ciphertexts
chosen plaintexts supplied by the attack harness
all non-secret fixture-generation rules
```

The attacker does not receive the master-secret seed.

State which prior plaintext/state values are attacker-known in each attack. Do not mix known-state and hidden-state attacks in one metric.

### 12.3 Frozen attacks

Run at minimum:

1. **Exhaustive secret recovery** — enumerate candidate master-secret seeds until the transcript uniquely matches.
2. **Lower-arity partition-assisted recovery** — give the attacker the complete frozen family of lower-arity subset observations allowed by the game and measure whether candidate pruning beats ordinary exhaustive recovery.
3. **Next-output prediction** — after the frozen chosen-plaintext transcript, predict the next target output without the secret; record exact success rate over trials.
4. **Known-state versus hidden-state split** — run the same game once with previous plaintext state known and once with it withheld, keeping those results separate.

Measure work primarily as:

```text
candidate secrets evaluated
oracle/transcript queries
exact surviving candidates after each observation
```

Record wall time only as environment metadata. Do not use wall time as the scientific stopping rule.

### 12.4 Phase-3 escalation

If neither `b=8` nor `b=12` shows a PCEA/control separation in attack work, stop and classify H-HARD according to the frozen rules.

Only if a separation survives may a later preregistration authorize `b=16` or larger. Do not extend key sizes merely because the run is already open.

## 13. Conventional control interpretation

The PRF control is load-bearing.

Possible outcomes:

```text
PCEA and PRF both show n-way structural terms
    -> arity may be ordinary joint-hash behavior; no PCEA-specific claim

PCEA shows less structural interaction than PRF
    -> PCEA structure is not adding the hypothesized effect

PCEA shows a reproducible structural residual absent from PRF
    -> interesting PCEA-specific structure; proceed to attacks

PCEA attack cost <= matched PRF attack cost
    -> no demonstrated security benefit from PCEA arity

PCEA attack cost > matched PRF under all frozen controls
    -> survives current harness only; escalate to independent cryptanalysis
```

## 14. Required artifacts

Codex must emit:

```text
pcea-ucns/arity/freeze.json
pcea-ucns/arity/current_dependency_graph.json
pcea-ucns/arity/fixtures.json
pcea-ucns/arity/structural_results.json
pcea-ucns/arity/attack_results.json        # only if Phase 3 is reached
pcea-ucns/arity/REPORT.md
```

Implementation files should remain under:

```text
pcea-ucns/arity/
```

Tests should be named:

```text
tests/test_arity_freeze.py
tests/test_arity_current_baseline.py
tests/test_arity_structural.py
tests/test_arity_controls.py
tests/test_arity_attack_scaling.py         # only if Phase 3 is reached
```

Every result artifact must state the exact experiment commit and freeze receipt hash.

## 15. Full-suite requirement

After every implementation commit:

```bash
PYTHONPATH=. python -m pytest -q
```

The pre-existing PCEA suite must remain green.

The arity tests must fail loudly if:

- a frozen source object changes;
- the A3 adapter stops matching current PCEA;
- fixture generation changes without schema version change;
- an expected result artifact is missing;
- a result was produced from a different freeze receipt;
- an outcome label is outside the preregistered vocabulary.

Do not convert optional UCNS skips into arity successes.

## 16. Resource preflight

Before each compute phase Codex must estimate whether the environment can reach the phase's natural terminal condition using the exact enumerations and trial counts above.

- Phase 0: source analysis only; expected feasible.
- Phase 1: at most `2^7` contributor states per frozen plaintext/variant; expected feasible.
- Phase 2: bounded exact grid above; preflight before starting.
- Phase 3: exhaustive `2^8` and `2^12` candidate-secret spaces over frozen trials; preflight before starting.

If completion feasibility is materially uncertain, do not start the phase. Record `BLOCKED_RESOURCE_PREFLIGHT` and the decisive resource uncertainty.

Once a healthy phase begins, let it finish to its natural terminal condition. Do not add an arbitrary wall-clock timeout.

## 17. Multi-actor protocol

This research benefits from multiple actors, but only when their independence is preserved.

### Actor A — freeze steward / harness builder

Recommended: **Codex**.

Actor A may:

- implement this procedure exactly;
- create fixtures and research adapters;
- run the frozen tests;
- report results using only preregistered labels.

Actor A may not:

- modify frozen baseline files;
- alter parameters after seeing results;
- invent a new attack and silently fold it into v1;
- promote a survival result into a security claim.

Actor A publishes its experiment commit and result hashes before seeing independent actor results.

### Actor B — independent recovery/reimplementation

Actor B receives:

```text
this procedure
freeze.json
baseline source identity
fixture-generation specification
```

Actor B SHOULD reimplement the Phase-1 exact structural calculation independently rather than importing Actor A's arity-analysis functions.

Actor B should not receive Actor A's interpretation of the result until its own result commit/hash is frozen.

The strongest first independence check is:

```text
same frozen truth tables / fixtures
independent implementation
same exact ANF/Möbius coefficients and outcome label
```

A mismatch is `UNRESOLVED_IMPLEMENTATION_DISAGREEMENT`, not a vote.

### Actor C — adversarial attacker

Actor C receives the frozen candidate and attack game but is allowed to design additional attacks **outside v1 scoring**.

Actor C must separate:

```text
preregistered v1 attacks
new exploratory attacks
```

A successful new attack can falsify a candidate immediately. A failed exploratory attack cannot upgrade standing because it was not part of the frozen acceptance criteria.

### Actor D — adjudicator

Actor D compares Actor A/B/C only after their commit/result hashes are frozen.

The adjudicator checks:

```text
freeze identity
fixture identity
implementation independence
metric identity
result agreement/disagreement
whether any exploratory attack falsified the candidate
```

The adjudicator does not average incompatible results.

### Minimum useful actor count

```text
2 actors: builder + independent replayer/attacker
3 actors: builder + independent replayer + independent attacker   <- preferred
4 actors: add a separate adjudicator                              <- strongest
```

Parallel co-authoring of one harness is not a substitute for independent replay.

## 18. Codex run instruction

Codex should treat the following as its execution handoff:

```text
Read repository CLAUDE.md and current vendored skills first.
Read pcea-ucns/ARITY_FREEZE_AND_TEST.md completely.

Implement the preregistered PCEA arity experiment without changing any frozen
baseline source path. Begin with Phase 0 and Phase 1 only. Produce freeze.json,
the current dependency graph, deterministic fixtures, exact structural results,
and REPORT.md. Run the full repository test suite after the implementation.

Obey the frozen escalation rule. Do not start Phase 2 or Phase 3 unless the
preceding phase's preregistered outcome authorizes it. Do not add parameter
values, attacks, or interpretations after seeing results. If a prerequisite
fails, classify it BLOCKED and repair only the owning experimental layer.

If Phase 3 is reached, preflight the exact exhaustive workload before launch;
once healthy execution begins, let it finish.

Commit each completed phase separately. The final report must state exact
commit SHAs, freeze receipt hash, all outcome labels, controls, and hmmm.

Do not merge. Do not modify runtime PCEA. Do not claim security.
```

## 19. Completion condition

The v1 run is complete when one of these occurs:

```text
H-STRUCT falsified -> stop
H-PCEA falsified -> stop or redirect to non-PCEA arity research
H-HARD falsified -> stop; no demonstrated arity security benefit
SURVIVED_CURRENT_HARNESS -> stop and hand frozen artifacts to independent actors
BLOCKED / UNRESOLVED -> stop and name the prerequisite needed to decide
```

There is no momentum-based continuation.

## hmmm

- Algebraic degree on the Boolean toy domain is an exact structural diagnostic, but whether it is the best cryptographic translation of the broader arity concept remains open; that is why the matched PRF control and attack phases are mandatory.
- A high-order term can be created by SHA/HMAC itself. PCEA earns no arity-specific standing unless the matched controls separate it.
- If a future result suggests a security benefit, the next step is independent cryptanalysis of a separately preregistered candidate, not runtime promotion.
- Higher-dimensional `z,x` / `z,y` / `z,x,y` relation semantics are not silently imported into this v1 test. They require their own precise operational definition before becoming a PCEA variable.
