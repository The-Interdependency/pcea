# Actor A Handoff — Codex

**Role:** freeze steward, candidate/harness builder, first preregistered execution.

**Do not merge. Do not modify runtime PCEA. Do not claim security.**

## Start

Work in `The-Interdependency/pcea`.

```bash
git fetch origin
git switch research/arity-v1-refreeze
git pull --ff-only origin research/arity-v1-refreeze
git switch -c research/arity-v1-actor-a
```

Before changing anything, read completely:

```text
AGENTS.md
.agents/skills/README.md
.agents/skills/msdmd/SKILL.md
.agents/skills/meta-module-build/SKILL.md
.agents/skills/test-build/SKILL.md
pcea-ucns/ARITY_FREEZE_AND_TEST.md
pcea-ucns/arity/BASELINE_FREEZE_V1.json
```

The frozen runtime baseline is:

```text
ecf2ca0dec38bef29382e02121b0edde66763aa9
```

Verify every runtime blob in `BASELINE_FREEZE_V1.json` against that commit before implementation. Any mismatch is `BLOCKED_FREEZE_DRIFT`; do not repair or reinterpret the baseline.

## Stage A0 — build the candidate, then freeze it

Implement only under:

```text
pcea-ucns/arity/**
tests/test_arity_*.py
```

Do not edit `pcea/**`.

Create the smallest complete research implementation needed by the protocol:

```text
candidate adapters for PCEA-A2/A3/A5/A7
matched PRF-A2/A3/A5/A7 controls
deterministic fixture generator
exact Boolean ANF/Mobius analyzer
dependency-graph emitter
freeze verifier
contract/check tests
```

All behavior-bearing Python modules must carry repo-compliant `MODULE_BUILD` and source `CONTRACTS`; test witnesses carry `CHECKS`. Preserve ratios/provenance conventions used by this repo.

The A3 adapter must reproduce current frozen PCEA exactly for matched valid inputs. If it does not, stop `BLOCKED_A3_ADAPTER_MISMATCH` and repair only the research adapter.

Before computing or recording any scientific result, create:

```text
pcea-ucns/arity/freeze.json
pcea-ucns/arity/fixtures.json
pcea-ucns/arity/current_dependency_graph.json
```

Run the full suite and commit the candidate/fixture freeze as a dedicated commit:

```bash
PYTHONPATH=. python -m pytest -q
git add pcea-ucns/arity tests/test_arity_*.py
git commit -m 'research(arity): freeze v1 candidate and fixtures'
git push -u origin research/arity-v1-actor-a
```

Call this exact commit **F1**. Add its SHA to `freeze.json` if necessary in one immediate metadata-only correction commit, then freeze the resulting receipt hash. Do not alter candidate behavior after F1. If behavior must change, invalidate F1 and create an explicit new freeze version rather than silently continuing.

F1 must be usable by Actors B and C without requiring your later result commit.

## Stage A1 — execute without consulting B/C

After F1, run Phase 0 and Phase 1 exactly as preregistered.

Do not:

```text
change contributor order
add fixtures or plaintexts
tune controls
change metrics/tolerances
inspect Actor B/C output
```

Follow the frozen escalation rule for Phase 2/3. Preflight compute before a phase; once a healthy phase starts, let it complete naturally.

After the preregistered structural/PCEA-specific gate is decided, emit an **outcome-blind gate token** for Actor C:

```text
pcea-ucns/arity/PHASE3_GATE.json
```

It contains only:

```text
schema = pcea-arity-phase3-gate-v1
F0 baseline SHA
F1 candidate SHA
freeze.json SHA256
authorized = true | false
criterion = frozen Phase-3 escalation rule
issuer = Actor A / Codex
```

Do not put structural metrics, effect sizes, outcome labels, interpretation, or report excerpts in this token. Actor C may learn only whether the preregistered reduced-entropy scaling gate opened.

Emit only reached artifacts:

```text
structural_results_A.json
attack_results_A.json        # only if authorized/reached
PHASE3_GATE.json
REPORT_A.md
locks/ACTOR_A_LOCK.json
```

Your actor lock must include:

```text
actor = Codex
role = A
F0 baseline SHA + BASELINE_FREEZE_V1.json SHA256
F1 SHA + freeze.json SHA256
PHASE3_GATE.json SHA256
result commit SHA
artifact path -> SHA256
preregistered outcome labels
any deviation/contamination
hmmm
```

Run the full suite again, commit results separately from F1, and push.

## Output discipline

Use only the protocol's standings. A passing harness does not mean secure. In particular:

```text
SURVIVED_STRUCTURAL_ARITY != PCEA-specific
SURVIVED_PCEA_SPECIFIC_ARITY != cryptographic hardness
SURVIVED_CURRENT_HARNESS != secure
```

If PCEA and PRF controls behave the same, say so plainly.

## Terminal response

Return only:

```text
F1 candidate-freeze SHA
F1 freeze.json SHA256
Actor A result SHA
Actor A lock SHA256
PHASE3_GATE authorized status + SHA256
Phase reached
Outcome labels
Full-suite result
Any BLOCKED/UNRESOLVED/hmmm
```

Do not merge or begin reconciliation with the other actors.
