# Agentic-Native Stack — Reusable Agent Workspace

This `.agent/` workspace turns the Rust-core / TypeScript-runtime architecture and OUROBOROS M0 execution contracts into composable skills. Canonical implementations remain in `rust/`, `typescript/` and `ouroboros/M0/ourob/`; skills do not duplicate source modules.

## Skills
- [skill-creator](skills/skill-creator/SKILL.md)
- [agentic-terminal-runtime-engineering](skills/agentic-terminal-runtime-engineering/SKILL.md)
- [agentic-permission-and-execution-governance](skills/agentic-permission-and-execution-governance/SKILL.md)
- [ouroboros-evidence-boundary-engineering](skills/ouroboros-evidence-boundary-engineering/SKILL.md)

## Workflows
- [Agentic terminal runtime implementation and verification](workflows/agentic-terminal-runtime-implementation.md)
- [OUROBOROS M0 evidence lifecycle](workflows/ouroboros-m0-evidence-lifecycle.md)

## Computational tools
- [validate_skill.py](tools/validate_skill.py) — structural skill lint only.
- [test_validate_skill.py](tests/test_validate_skill.py) — validator regression tests.
- Canonical implementation modules remain in Rust, TypeScript and `ouroboros/M0/ourob/`.

## Evidence boundary
The architecture specification is Draft / Implementation Specification. OUROBOROS M0 defines a repository-native implementation contract, but a documented invariant is not a passing implementation test. Use exact-revision CI evidence and distinguish implementation, execution, verification and promotion.
