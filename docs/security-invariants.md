# Security Invariants

The following properties must always hold.

## S1 — No Direct Side Effects From Model Output

LLM or agent output MUST NOT directly execute operating-system operations.

```text
LLM / Agent Output
  ↓
Tool Request
  ↓
Schema Validation
  ↓
Risk Classification
  ↓
Permission Engine
  ↓
Rust Executor
  ↓
Audit Event
```

## S2 — Authoritative Rust Enforcement Boundary

The Rust daemon is the authoritative enforcement boundary. TypeScript clients, plugins, editors, and UIs may propose actions but MUST NOT bypass Rust-side validation and permission checks.

## S3 — Auditability

Every privileged operation MUST generate an audit record containing actor identity, timestamp, session identifier, requested capability, permission decision, and execution result. Audit records MUST be append-only in production configurations.

## S4 — Fail Closed

If the permission engine is unavailable or returns an error, side-effecting operations MUST be denied. Read-only operations MAY continue only if explicitly allowed by policy.

## S5 — Capability Isolation

Plugins receive only declared capabilities. Unknown, undeclared, or excessive capabilities MUST be denied.

## S6 — Secret Non-Recall

Secrets MUST NOT be stored in recallable memory unless explicitly permitted. Secrets MUST be redacted from logs, telemetry, model prompts, memory embeddings, session exports, and audit payloads where possible.

## S7 — Terminal Output Is Low Trust

Terminal output, command output, remote host responses, and file contents are low-trust inputs. They MUST NOT bypass schema validation, permission checks, sandbox policy, or audit logging.

## S8 — Session Isolation

Sessions MUST be isolated by tenant and user where multi-tenancy is enabled.

## S9 — Replay Integrity

Session recordings and snapshots MUST preserve sequence integrity. Replayed sessions MUST NOT inject new privileged actions without audit evidence.

## S10 — Human Override

A human operator MUST be able to interrupt an agent, deny permission, cancel a task, terminate a session, and export audit evidence. Human override takes precedence over agent autonomy.
