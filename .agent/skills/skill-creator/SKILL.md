---
name: skill-creator
description: Design, create, validate, revise, register, and release reusable agent skills under the HARĒNA Skill Engineering Standard.
---

# Skill Creator

## Purpose
Create maintainable, portable, testable skills from repeatable workflows, technical domains, or verified bodies of knowledge. This meta-skill governs authoring quality; it does not establish the truth of domain claims.

## Activation
Use when creating a skill, extracting a process from a conversation/project, revising a skill, adding helpers, registering skills, or preparing a release. Do not substitute it for domain, security, legal, or runtime integration review.

## Inputs
Identify task/domain, intended agents, triggers/exclusions, target repository/runtime, tools/permissions, outputs, acceptance criteria, safety constraints, evidence sources, and unknowns. Ask one focused question only if an essential decision cannot safely be assumed; otherwise state assumptions.

## Procedure
1. Reconstruct the source process from available conversation, files, commands, tool results, and operator decisions. Separate performed actions from proposals and inferred improvements.
2. Extract triggers, inputs, preconditions, steps, branches, failure paths, state transitions, outputs, and handoffs.
3. Define the skill contract: purpose, activation, exclusions, dependencies, outputs, safety boundaries, and acceptance tests.
4. Draft independently usable instructions; do not depend on hidden chat context.
5. Keep SKILL.md focused; add references/workflows/schemas only when maintained value exists.
6. Add helpers selectively; require deterministic behavior, documentation, bounded execution, safe defaults, and tests.
7. Validate frontmatter, kebab-case name, directory/name match, required content sections, links, and local references. The structural validator accepts documented heading aliases (for example Trigger for Activation and Stop conditions for Failure handling); it checks section presence, not section quality or full YAML validity.
8. Test helpers with normal, malformed, and boundary inputs; record exact commands and results.
9. Exercise a representative controlled workflow where possible.
10. Test discovery and invocation separately in each target runtime. Never assume .agent auto-load behavior.
11. Register the skill in .agent/README.md with a working relative link.
12. Inspect existing paths; create absent files and update existing files using their current blob SHA.
13. Fetch every changed file back and compare content or stable markers.
14. Report revision, files, validation levels, runtime scope, gaps, and operator actions.
15. Maintain tests, index, references, and standard when contracts change; document breaking changes.

## Outputs
A skill package, index registration, validation evidence, repository revision, and release report.

## Failure handling
Stop if repository identity/write permission is ambiguous, an overwrite cannot be reconciled, essential evidence is unavailable, or legal/security constraints block intended use. Report partial completion and the exact blocked gate.

## Acceptance criteria
- Frontmatter contains name and description.
- Skill name matches directory.
- Purpose, activation, inputs, procedure, outputs, failure handling, and acceptance criteria exist.
- Claims and evidence statuses are distinguished.
- Dependencies and safety constraints are explicit.
- Structural/helper tests are accurately reported.
- Runtime discovery is tested or marked NOT_RUN.
- Skill is registered and changed files are fetched back.

## Validation status
Report AUTHORING_COMPLETE, STRUCTURE_VALIDATED, STATIC_CHECKED, HELPER_TESTED, WORKFLOW_TESTED, RUNTIME_CONFORMANT, and PERSISTENCE_VERIFIED independently. Each is PASS, FAIL, NOT_RUN, or BLOCKED.

## Governing standard
Follow .agent/standards/skill-engineering-standard-v1.md. If unavailable in another repository, apply these requirements and report that the standard document was unavailable.
