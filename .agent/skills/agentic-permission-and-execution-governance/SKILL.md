---
name: agentic-permission-and-execution-governance
description: Design and audit permission-gated agent tool execution, sandbox boundaries, approvals, and execution provenance.
---

# Agentic Permission and Execution Governance

## Purpose
Ensure agent-proposed actions cross a fail-closed permission boundary before reaching process, filesystem, network or remote-session effects.

## Activation
Use when designing or reviewing tool registration, permission gates, capability tiers, sandboxing, shell execution, approvals, audit records or multi-agent task orchestration.

Do not treat a model-generated tool call, schema-valid payload, or plugin declaration as authorization.

## Inputs
- Exact source revision and tool contract.
- Principal/agent identity and capability tier.
- Action schema, target resource, arguments and risk classification.
- Approval policy and human decision record.
- Sandbox, filesystem, network and process boundary.
- Execution journal and observation contract.

## Procedure
1. Identify the authoritative permission decision point before OS-facing execution.
2. Treat model output, provider response, terminal content and plugin input as untrusted proposals/data.
3. Require each tool to declare a stable identity, version, input schema, required capabilities and risk level.
4. Evaluate allow/deny/ask-user/sandbox policy before dispatch. Fail closed for unknown or malformed actions.
5. Bind approval to exact action identity, arguments, target scope and relevant expiry/revision.
6. Enforce sandbox boundaries at the operating-system execution layer; an in-process policy check is not a substitute for isolation.
7. Keep agent/session identity and trace IDs attached across tool request, authorization, execution and observed result.
8. Record both permission decision and actual execution observation. Do not infer execution from authorization or authorization from a command proposal.
9. Bound process lifetime, output volume, concurrency, retry, cancellation and resource use.
10. Test denied, malformed, stale, replayed, over-scoped and concurrent requests, including direct attempts to bypass the public tool dispatcher.
11. Preserve human approval and policy overrides as attributable records.
12. Report residual risk when secure isolation or resource enforcement is only a hook or design intention.

## Outputs
- Tool/capability manifest.
- Permission policy and approval binding.
- Sandbox and execution-boundary design.
- Audit/trace schema.
- Threat cases and verification evidence.

## Failure handling
Reject unknown tools, undeclared capabilities, stale approvals, scope mismatch, invalid schemas and policy-evaluation errors. Stop when an action can reach the OS without a recorded authorization decision or when the sandbox is only assumed.

## Acceptance criteria
- Tool proposals are not authorization.
- Permission evaluation is fail-closed and occurs before OS effects.
- Approval binds to exact action and scope.
- Sandboxing is enforced outside the untrusted in-process component.
- Execution and observation are separately recorded.
- Trace provenance is end-to-end.
- Resource bounds and denial paths are tested.

## Source references
- `docs/agentic-native-stack.md`, Agent Runtime Model and Policy Runtime.
- `rust/agentic-core/crates/agentic-agent-core/src/permission.rs`
- `rust/agentic-core/crates/agentic-agent-core/src/policy_matcher.rs`
- `rust/agentic-core/crates/agentic-agent-core/src/sandbox.rs`
- `rust/agentic-core/crates/agentic-agent-core/src/tool.rs`
- `rust/agentic-core/crates/agentic-agent-core/src/tools/shell_exec.rs`

## Validation status
The presence of permission/sandbox modules does not prove secure isolation or complete enforcement; use revision-bound tests and security review.
