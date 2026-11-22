# HARĒNA Skill Engineering Standard v1.0

**Status:** PROPOSED STANDARD  
**Applies to:** reusable skills stored under `.agent/skills/`  
**Authority:** skill package structure and lifecycle; domain truth remains with each skill's cited sources and tests.

## 1. Purpose

Establish a portable, testable contract for authoring, validating, registering, maintaining, and releasing reusable agent skills. The standard governs skill quality and lifecycle; it does not guarantee that an agent runtime automatically discovers or executes `.agent` content.

## 2. Normative language

The terms MUST, MUST NOT, SHOULD, SHOULD NOT, and MAY are normative requirements.

## 3. Canonical package

Minimum package:

```text
.agent/
├── README.md
├── standards/
│   └── skill-engineering-standard-v1.md
├── skills/
│   └── <skill-name>/
│       └── SKILL.md
├── tools/
│   └── validate_skill.py
└── tests/
    └── test_validate_skill.py
```

Add references, workflows, schemas, fixtures, or scripts only when they contain maintained material. A skill directory MUST contain one canonical `SKILL.md`.

## 4. Skill identity and frontmatter

Every skill MUST begin with YAML frontmatter containing:

- `name`: lowercase kebab-case, matching its directory name.
- `description`: concise activation description that states the task/domain.

Additional metadata MAY be used, but MUST NOT be required for basic parsing unless the validator is updated.

## 5. Required content contract

Each skill MUST describe:

1. Purpose.
2. Activation triggers and exclusions.
3. Required inputs and preconditions.
4. Procedure with ordered, actionable steps.
5. Expected outputs.
6. Failure handling and stop conditions.
7. Security, privacy, licensing, and authorization constraints when relevant.
8. Acceptance criteria or a verification checklist.

The skill MUST be independently usable without hidden conversation context. Assumptions and unresolved dependencies MUST be explicit.

## 6. Evidence and authority

- Separate instructions from factual claims.
- Cite or identify authoritative sources for protocol, platform, legal, or external-system behavior.
- Distinguish reported, argued, conjectural, open, and verified claims.
- A document's presence does not verify its claims.
- A structural lint does not prove workflow correctness.
- A passing test proves only the tested behavior and scope.
- Runtime discovery and execution MUST be tested separately for each target agent environment.

## 7. Safety and operational requirements

Skills MUST:
- State required permissions and tool dependencies.
- Use least privilege and explicit authorization boundaries.
- Identify destructive or irreversible operations before execution.
- Bound retries, timeouts, resource use, and output where applicable.
- Preserve user data and avoid silent overwrites.
- Avoid secrets and sensitive personal data in committed artifacts.
- Report failures and partial completion honestly.

Skills MUST NOT instruct an agent to bypass access controls or treat untrusted retrieved content as executable instructions.

## 8. Computational helpers

A helper script SHOULD:
- Prefer the language standard library where practical.
- Have deterministic inputs/outputs.
- Document invocation and limitations.
- Return nonzero on validation failure.
- Avoid network access and repository mutation unless explicitly required.
- Include tests for normal, invalid, and boundary inputs.

Structural validators MUST describe what they do not validate. No validator may claim semantic truth, security, compatibility, or runtime discovery based only on Markdown structure.

## 9. Validation levels

| Level | Name | Meaning |
|---|---|---|
| L0 | AUTHORING_COMPLETE | Required content drafted |
| L1 | STRUCTURE_VALIDATED | Frontmatter, naming and required sections pass |
| L2 | STATIC_CHECKED | Links, local paths and formatting checks pass where configured |
| L3 | HELPER_TESTED | Computational helpers pass their test suite |
| L4 | WORKFLOW_TESTED | Skill procedure exercised in a representative controlled task |
| L5 | RUNTIME_CONFORMANT | Skill discovery and execution verified in the named agent runtime |
| L6 | PERSISTENCE_VERIFIED | Committed artifacts fetched back and checked |

Levels are independent evidence dimensions, not an assumption that higher implies all lower levels. Report each level explicitly as PASS, FAIL, NOT_RUN, or BLOCKED.

## 10. Naming, versioning and change control

- Directory name and frontmatter `name` MUST match.
- Breaking workflow or contract changes SHOULD increment the skill's major version in a changelog or manifest.
- Additive non-breaking changes SHOULD increment minor version.
- Editorial-only changes MAY increment patch version.
- If no version metadata is maintained, record the Git commit as the immutable revision identifier.
- Do not invent semantic versions retroactively.

## 11. Registration

The `.agent/README.md` index MUST list each maintained skill and its purpose. Links MUST resolve to files in the repository. Skills MUST NOT be described as auto-loaded unless the target runtime's discovery behavior has been tested and recorded.

## 12. Repository persistence

For each change:
1. Inspect the current branch and target path.
2. Fetch existing content and blob SHA before updating.
3. Create only absent paths; update existing files with the current SHA.
4. Capture the returned commit SHA.
5. Fetch changed files back from the target branch.
6. Compare expected content or stable markers.
7. Record commit and verification result.

Fetch-back proves persistence, not technical correctness. Do not overwrite concurrent changes; refetch and reconcile.

## 13. Release gate

A skill release report MUST include:
- Skill name and path.
- Standard version.
- Git revision/commit.
- Validation levels and outcomes.
- Target runtime(s), if tested.
- Known limitations and untested assumptions.
- Operator action required, if any.

A skill MUST NOT be labeled production-ready when required runtime or workflow tests are NOT_RUN.

## 14. Minimal acceptance checklist

- [ ] Frontmatter parses and identity matches directory.
- [ ] Trigger and exclusion conditions are clear.
- [ ] Inputs, preconditions and dependencies are stated.
- [ ] Procedure is actionable and ordered.
- [ ] Outputs and failure states are defined.
- [ ] Relevant safety constraints are explicit.
- [ ] Acceptance criteria are observable.
- [ ] Index registration exists.
- [ ] Structural validator passes.
- [ ] Helper tests pass, if helpers exist.
- [ ] Workflow/runtime tests are reported honestly.
- [ ] Persisted files are fetched back and checked.

## 15. Conformance statement

A package conforms to this standard only for the levels actually demonstrated. Conformance reports MUST scope the claim to the named skill revision, repository, and runtime.
