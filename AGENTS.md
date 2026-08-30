# PCEA agent guide

PCEA is a pure-Python, zero-dependency symmetric transform for pre-quantized
neural architecture state.

## Authority

- PCEA decrypts and inverts through synchronized keys, not through UCNS inverse
  operations.
- Runtime state is seed/circle/tensor addressed and depends on protected
  `last_state` synchronization.
- `pcea-ucns/` is an attack and feasibility workspace, not proof of public-key
  security.

## Boundaries

- Load relevant repo-local skills from `.agents/skills/` before changing
  behavior, metadata, tests, cryptographic claims, or UCNS harnesses.
- Do not claim cryptographic security from passing harnesses alone.
- Do not couple runtime correctness to UCNS analytic-frontier assumptions.
- New behavior-bearing modules need skill-lib metadata and tests that exercise
  the declared contract.

## Checks

```bash
python -m pytest -q
python -m pytest -q tests/test_cipher.py tests/test_codec.py tests/test_kdf.py tests/test_instance.py tests/test_contract_spec.py
```

Run attack/regression harnesses when changing `pcea-ucns/`.

## hmmm

- Future PCEA-UCNS key-establishment claims remain gated by measured attacks and
  explicit promotion criteria.
