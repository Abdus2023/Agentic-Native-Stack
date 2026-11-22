---
name: agentic-terminal-runtime-engineering
description: Engineer the Rust-core and TypeScript-runtime terminal execution stack across PTY, VTE, sessions, SSH, events, memory, and orchestration.
---

# Agentic Terminal Runtime Engineering

## Purpose
Translate the Agentic-Native Stack architecture into bounded engineering work while preserving the Rust/TypeScript responsibility split and traceable session execution.

## Activation
Use when designing or modifying the Rust execution core, TypeScript orchestration runtime, PTY/SSH transport, shadow VTE parsing, session multiplexing, structured event flow, memory integration, or terminal-facing tools.

Do not assume that architecture references prove implementation completeness, throughput, safety, or cross-platform behavior.

## Inputs
- Exact repository commit and architecture specification.
- Rust workspace and TypeScript package boundaries.
- Relevant crate/package APIs and tests.
- Session, pane, agent, event and trace identity contracts.
- Platform/OS target, resource budgets and threat model.

## Procedure
1. Pin the architecture specification and distinguish documented design from maintained implementation and unimplemented blueprint.
2. Keep safety-critical process I/O, PTY ownership, SSH transport, signal handling and low-level event handling in the Rust core.
3. Keep agent orchestration, provider integration, plugin APIs and UI-facing services in the TypeScript runtime.
4. Treat terminal output as bytes first; parse into structured VTE/session events only with explicit parser state and provenance.
5. Model sessions and panes independently from UI instances. Define attach/detach, multiplexing, snapshot, replay and rehydration contracts.
6. Preserve stable identities and correlation across agent, session, pane, command, event and trace records.
7. Keep tool schemas, permissions and policy decisions explicit before any OS-facing execution.
8. Ensure event fan-out, PTY drains and scheduler loops are bounded and cooperative; test fairness and cancellation under output pressure.
9. Keep memory retrieval, consolidation and decay behind explicit interfaces with provenance and privacy boundaries.
10. Validate Rust and TypeScript projections against shared protocol fixtures where the same wire contract crosses the language boundary.
11. Use repository tests and CI for execution evidence. A source reference or code file does not prove the behavior described in architecture prose.
12. Do not duplicate canonical Rust/TypeScript modules in skill-local scripts; add a helper only for a distinct deterministic task.

## Outputs
- Component/ownership map.
- Versioned protocol and event contracts.
- Session/PTY/SSH implementation plan.
- Bounded orchestration and memory interfaces.
- Test matrix and revision-bound evidence.

## Failure handling
Stop when Rust and TypeScript both claim authority for the same security-sensitive operation, event identity cannot be correlated, PTY resources are unbounded, a UI lifetime is treated as session authority, or a tool action can bypass the permission boundary.

## Acceptance criteria
- Rust owns safety-critical I/O and process/transport boundaries.
- TypeScript owns higher-level orchestration and provider/plugin ergonomics.
- Sessions survive UI detach/reattach without duplicate process ownership.
- Event provenance and correlation are explicit.
- Resource/fairness/cancellation limits are testable.
- Cross-language contracts have shared fixtures.
- All implementation claims are tied to exact code and test evidence.

## Source references
- `docs/agentic-native-stack.md`
- `rust/agentic-core/crates/agentic-agent-core/`
- `rust/agentic-core/crates/agentic-event/`
- `rust/agentic-core/crates/agentic-session/`
- `rust/agentic-core/crates/agentic-pty/`
- `rust/agentic-core/crates/agentic-ssh/`
- `typescript/agentic-runtime/`

## Validation status
The architecture document is a draft/implementation specification. Claims about complete implementation or platform conformance require separate evidence.
