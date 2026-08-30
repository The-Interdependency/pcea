# Actor D Handoff — Gemini

**Role:** post-freeze adjudicator only.

**Do not start until Actors A, B, and C have each committed immutable lock files and the coordinator has assembled `ADJUDICATION_PACKET.json`.**

You are not a builder, repair agent, tie-breaker by vote, or fourth attack collaborator.

## Required input packet

You should receive only the frozen repository evidence needed to adjudicate:

```text
pcea-ucns/ARITY_FREEZE_AND_TEST.md
pcea-ucns/arity/BASELINE_FREEZE_V1.json
pcea-ucns/arity/freeze.json
pcea-ucns/arity/fixtures.json
pcea-ucns/arity/ADJUDICATION_PACKET.json
pcea-ucns/arity/locks/ACTOR_A_LOCK.json
pcea-ucns/arity/locks/ACTOR_B_LOCK.json
pcea-ucns/arity/locks/ACTOR_C_LOCK.json
all result artifacts named by those locks
F0 baseline source at the exact baseline commit
F1 frozen candidate at the exact candidate commit
```

Do not use intermediate chat, coordination discussion, unpublished drafts, or post-lock explanations to rescue a result.

## First gate — packet integrity

Before interpreting results, verify:

```text
F0 baseline commit matches every lock
BASELINE_FREEZE_V1.json hash matches every lock
F1 candidate commit matches every lock
freeze.json hash matches every lock
fixture identity matches every actor
all result artifact hashes match their lock manifests
actor result commits exist and contain the named artifacts
no actor modified frozen runtime paths
```

If any load-bearing identity cannot be verified, classify the affected claim `BLOCKED` and say exactly what identity is missing or inconsistent.

## Second gate — independence

Check declared independence boundaries:

```text
Actor A locked before consulting B/C
Actor B did not import/copy A's analyzer and did not consult A results
Actor C did not consult A/B results before locking
Actor C separates preregistered and exploratory attacks
Gemini was called only after A/B/C locks
```

If contamination occurred, do not silently discard it. Decide whether it invalidates a claim, narrows independence standing, or leaves a result usable for a more limited conclusion.

## Adjudication questions

Adjudicate each separately.

### Q1 — baseline arity

Does frozen current PCEA actually have direct state-key arity 3 under the preregistered definition?

### Q2 — structural higher arity

Do A5 and/or A7 exhibit an exact full-degree residual under the frozen Boolean ANF/Mobius test?

### Q3 — independent reproduction

Do Actors A and B independently recover the same exact structural result from the same frozen inputs?

Agreement is evidence. Disagreement is `UNRESOLVED` unless one result is demonstrably invalid under the frozen protocol; do not vote.

### Q4 — PCEA-specificity

Does the PCEA result differ from its matched PRF control under the frozen comparison rules?

A high-order effect shared by HMAC/SHA control is not PCEA-specific.

### Q5 — attack benefit

If attack scaling was authorized and run, does PCEA require greater frozen attack work or yield lower recovery/prediction success than the matched PRF after controlling entropy, query/transcript budget, and arity?

### Q6 — breaks

Did Actor C find any preregistered or exploratory attack that falsifies a claimed property? A valid practical break dominates failed attacks and survival observations for that property.

## Allowed classifications

For each claim use exactly one:

```text
FALSIFIED
SURVIVED
UNRESOLVED
BLOCKED
```

`SURVIVED` means only survived the named frozen evidence. It does not mean secure, proven, production-ready, or cryptographically reviewed.

Do not combine classifications into a numerical score unless the protocol explicitly defines one. It does not.

## Decision precedence

Use this precedence:

```text
verified break of claim -> FALSIFIED
load-bearing evidence unavailable/invalid -> BLOCKED
independent valid evidence conflicts -> UNRESOLVED
all preregistered gates for the claim agree without a break -> SURVIVED
```

A majority of actors never overrides a valid counterexample.

## Required output

Write:

```text
pcea-ucns/arity/GEMINI_ADJUDICATION.md
pcea-ucns/arity/locks/ACTOR_D_LOCK.json
```

`GEMINI_ADJUDICATION.md` must contain:

```text
packet integrity verdict
independence verdict
Q1 classification + minimal evidence
Q2 classification + minimal evidence
Q3 classification + minimal evidence
Q4 classification + minimal evidence
Q5 classification + minimal evidence
Q6 classification + minimal evidence
final bounded statement of what PCEA has and has not earned
hmmm
```

`ACTOR_D_LOCK.json` must record:

```text
actor = Gemini
role = D
ADJUDICATION_PACKET SHA256
A/B/C lock hashes
adjudication artifact SHA256
exact classifications
any contamination/identity defects
hmmm
```

## Forbidden actions

Do not:

```text
modify/rewrite A/B/C result artifacts
repair candidate code
rerun experiments and substitute your run for theirs
change metrics, controls, fixtures, or thresholds
average incompatible results
infer security from no observed break
use post-lock explanations to fix missing evidence
```

If you identify a better experiment, put it only under `hmmm / next preregistration`; it does not change v1's adjudication.

## Final sentence constraint

End with one bounded sentence in this form:

```text
Under PCEA arity v1 at F0=<sha> and F1=<sha>, <claim(s)> are <classification(s)>; this does/does not establish a PCEA-specific cryptographic security benefit, and it does not constitute independent professional cryptographic review.
```
