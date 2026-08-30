# PCEA Arity — Gemini Fourth-Actor Adjudication

**Status:** normative addendum to `ARITY_FREEZE_AND_TEST.md` section 17 for the v1 arity experiment.

**Purpose:** preserve the epistemic value of a fourth actor by assigning Gemini only the post-freeze adjudication role. This addendum does not change the frozen hypotheses, fixtures, metrics, controls, attack games, escalation rules, or outcome vocabulary in `ARITY_FREEZE_AND_TEST.md`.

## 1. Actor identity

For v1:

```text
Actor A: Codex — freeze steward / harness builder
Actor B: independent replayer — independent Phase-1 derivation/reimplementation
Actor C: independent attacker — adversarial analysis of the frozen candidate
Actor D: Gemini — adjudicator only
```

The fourth actor is valuable because it is not another collaborator. Gemini must remain outside construction, replay, attack design, repair, and reconciliation until A/B/C are complete.

## 2. Hard timing rule

**Do not call Gemini before Actors A, B, and C have each finished and frozen their outputs.**

The sequence is:

```text
A finishes -> freeze A
B finishes independently -> freeze B
C finishes independently -> freeze C
A+B+C locks verified -> assemble adjudication packet
only then -> call Gemini
```

If Gemini sees intermediate discussion, partial results, proposed repairs, or another actor's interpretation before all three locks exist, the fourth-actor independence claim is contaminated. Record that run as `UNRESOLVED_ADJUDICATOR_CONTAMINATION` and do not represent it as the v1 independent adjudication.

## 3. Required A/B/C lock records

Before Gemini is called, preserve one immutable lock record per actor:

```text
pcea-ucns/arity/actors/A_LOCK.json
pcea-ucns/arity/actors/B_LOCK.json
pcea-ucns/arity/actors/C_LOCK.json
```

Each lock must record at minimum:

```text
actor_label
actor_role
model/tool identity if known
baseline_commit
experiment/provenance commit SHA
freeze receipt hash
result artifact paths
SHA-256 of every result artifact
stated outcome label(s)
hmmm / unresolved boundaries
completed_at
```

The lock is a receipt, not a summary. It must point to the exact frozen artifacts Gemini will receive.

If any actor needs to repair its own work after locking, the repaired result is a **new** result set with a new lock. Preserve the earlier lock; do not overwrite history.

## 4. Independence rules before locking

### Actor A — Codex

May see only the preregistration, repository authority, frozen baseline, and its own execution outputs while building/running v1.

A must freeze its result before receiving B or C conclusions.

### Actor B — independent replayer

Receives the preregistration, baseline identity, freeze receipt, and fixture-generation specification needed for independent recovery.

B should independently implement the exact structural derivation. B must not import A's arity-analysis implementation and should not see A's interpretation before B freezes.

### Actor C — independent attacker

Receives the frozen candidate and the declared attack game. C may invent exploratory attacks, but must separate them from preregistered v1 scoring exactly as required by `ARITY_FREEZE_AND_TEST.md`.

C should not receive A or B conclusions before C freezes.

## 5. Adjudication packet

After A/B/C are locked, assemble a read-only packet containing exactly:

```text
1. pcea-ucns/ARITY_FREEZE_AND_TEST.md
2. this addendum
3. frozen baseline commit identity
4. freeze.json and its SHA-256
5. A_LOCK.json + A frozen artifacts
6. B_LOCK.json + B frozen artifacts
7. C_LOCK.json + C frozen artifacts
8. exact hashes for every supplied file
9. repository authority files needed only to interpret standing/labels
```

Do **not** include:

```text
chat transcripts about hoped-for outcomes
post-result reconciliation between A/B/C
suggested fixes
new acceptance criteria
arguments for why PCEA "should" work
security marketing language
```

The adjudicator should evaluate evidence, not inherit a consensus narrative.

## 6. Gemini authority boundary

Gemini may:

- verify that all supplied artifacts correspond to the declared freeze;
- compare A/B/C results against the preregistered criteria;
- identify implementation or interpretation disagreements;
- determine whether exploratory attacks falsify a candidate;
- determine whether each claimed standing is supported by the frozen evidence;
- assign only the already-authorized outcome/standing vocabulary, plus the disagreement/contamination states defined by the protocol;
- state what remains `hmmm`.

Gemini may not:

- repair code;
- rerun the experiment as part of adjudication;
- tune parameters;
- add samples after seeing results;
- redefine arity;
- replace the matched PRF control;
- discard an inconvenient actor result;
- average incompatible results;
- invent a stronger acceptance criterion and retroactively apply it;
- weaken a criterion because the result is promising;
- promote `SURVIVED_CURRENT_HARNESS` to `secure`, `hard`, `production-ready`, or `reviewed`.

If Gemini determines a rerun or repair is necessary, the adjudication result is `BLOCKED` or `UNRESOLVED` with the exact prerequisite. Repair happens in a later run under a new freeze; Gemini does not perform it inside v1 adjudication.

## 7. Disagreement handling

Actor disagreement is evidence, not a vote.

Use these rules:

```text
A == B == C and freeze valid
    -> adjudicate against preregistered criteria

A/B structural mismatch
    -> UNRESOLVED_IMPLEMENTATION_DISAGREEMENT

C produces a valid break
    -> candidate is falsified for the attacked claim even if A/B agree

C finds no break
    -> no standing upgrade by itself

artifact/hash/freeze mismatch
    -> BLOCKED

Gemini cannot determine whether criteria were met from supplied evidence
    -> UNRESOLVED
```

A majority of models does not override an exact counterexample or a broken freeze.

## 8. Required Gemini output

Gemini must produce one adjudication record with this structure:

```text
baseline_commit:
freeze_receipt_hash:
A_lock_hash:
B_lock_hash:
C_lock_hash:

freeze_valid: yes | no | unresolved
independence_valid: yes | no | unresolved
A_B_reproduction_agreement: yes | no | unresolved
C_falsifying_attack_present: yes | no | unresolved

H_STRUCT: <authorized label>
H_PCEA: <authorized label>
H_HARD: <authorized label or NOT_REACHED>

overall_standing: FALSIFIED | SURVIVED_CURRENT_HARNESS | UNRESOLVED | BLOCKED

criterion_trace:
  - <criterion -> exact evidence artifact/hash -> decision>

disagreements:
  - <actor disagreement, if any>

exploratory_attacks:
  - <separately identified exploratory result>

forbidden_inferences_checked:
  secure: not_claimed
  production_ready: not_claimed
  independent_crypto_review: not_claimed

hmmm:
  - <remaining unresolved boundary>
```

The adjudication itself must be frozen after completion with its own artifact hash.

Recommended path:

```text
pcea-ucns/arity/actors/D_GEMINI_ADJUDICATION.md
pcea-ucns/arity/actors/D_LOCK.json
```

## 9. Gemini handoff prompt

Use this after A/B/C are locked:

```text
You are Actor D, the independent adjudicator for the frozen PCEA arity v1 experiment.

Adjudicate only. Do not repair code, rerun experiments, tune parameters, add tests,
or redesign the protocol.

Read ARITY_FREEZE_AND_TEST.md and ARITY_GEMINI_ADJUDICATION.md first. Verify the
baseline commit, freeze receipt, A/B/C lock records, and artifact hashes. Then compare
the three frozen result sets strictly against the preregistered criteria.

Do not treat agreement by majority as proof. A valid falsifying attack overrides
positive agreement. An A/B reproduction mismatch is unresolved rather than something
to average away. A broken freeze is BLOCKED.

Return the required Gemini adjudication record. Use only the authorized standing
vocabulary. In particular, SURVIVED_CURRENT_HARNESS does not mean secure, hard,
production-ready, or independently cryptographically reviewed.

Identify every criterion using the exact artifact/hash that supports your decision.
Preserve all unresolved boundaries under hmmm.
```

## 10. Why the fourth actor is delayed

The fourth actor does not primarily add another search for bugs. Its strongest contribution is **independent judgment of whether the frozen evidence actually satisfies the frozen claim**.

Calling Gemini early changes its role from adjudicator to collaborator and allows shared interpretation to propagate into A/B/C. Calling Gemini after A/B/C are immutable lets it detect:

- post-hoc criterion drift;
- selective reconciliation;
- unsupported promotion of a structural result into a security result;
- ignored counterexamples;
- actor disagreement hidden by summary prose;
- freeze/provenance mismatch.

Therefore the v1 sequence is load-bearing:

```text
three independent producers first -> immutable evidence -> Gemini fourth
```

## hmmm

- Model-family independence is not statistical independence; shared training priors may remain correlated even with strict information separation.
- If Gemini finds an adjudication prerequisite that was absent from the original protocol, that finding can motivate v2, but it cannot be retrofitted into v1 scoring.
- A later human cryptographer remains categorically different from fourth-model adjudication and would be required before any production cryptographic security claim.
