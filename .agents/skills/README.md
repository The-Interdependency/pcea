# Repo-local agent skills

This repo consumes The Interdependency organization skill library.

Canonical source:
- Preferred: `The-Interdependency/skill-lib`
- Temporary source: `The-Interdependency/a0/skill-lib`

Source commit: `The-Interdependency/skill-lib` @ `5c46d0534fa0726a9078f0a242c66a217fbaa501` (verbatim sync).

Installed skills:
- `msdmd/` — Module Self-Declared Metadata Markdown
- `test-build/` — test contract metadata blocks
- `meta-module-build/` — metadata-first module scaffolding
- `manifest/` — living-spec generator for `CLAUDE.md`; CI runs `generate.py --check`. Refresh with `python .agents/skills/manifest/generate.py --write`.

Agents working in this repo should read `meta-module-build/SKILL.md` before
creating new modules, routes, services, schemas, adapters, workers, engines,
UI panels, migrations, or experiments.

Usage guidance:
- Treat the source commit above as the exact canonical snapshot for vendored skill files.
- Run the repository's manifest/skill drift workflow after changing `.agents/skills/`.
- Update vendored canonical files only by propagation from `The-Interdependency/skill-lib`; keep repo-local additions explicitly local.
