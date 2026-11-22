# Agentic Terminal Runtime Implementation and Verification

**Status:** operator-run engineering workflow  
**Architecture source:** `docs/agentic-native-stack.md`

## Procedure
1. Pin architecture and source commit.
2. Confirm Rust-core ownership of PTY/process/SSH/VTE/session/event primitives and TypeScript ownership of orchestration, providers, plugins and UI-facing services.
3. Define versioned protocol/event contracts and stable agent/session/pane/trace identities.
4. Implement Rust primitives with explicit resource ownership and cancellation.
5. Implement TypeScript orchestration against the published contract; do not create a competing security authority.
6. Parse terminal streams as data and preserve raw-byte provenance alongside structured events.
7. Apply permission checks before OS-facing actions; model output is a proposal, not authorization.
8. Bound PTY drain, scheduler quantum, concurrency, output, memory and retries.
9. Verify detach/reattach, multiplexing, replay, snapshots, process exit and remote transport behavior.
10. Run Rust and TypeScript tests plus cross-language fixture parity on exact commits.
11. Use CI execution evidence for release claims; local inspection is diagnostic only.
12. Record unsupported platforms, unimplemented architecture claims and unresolved isolation risks.

## Outputs
Protocol contracts, component map, implementation report, test/CI evidence, threat/risk record and release gate.

## Stop conditions
Stop when a tool can bypass permission policy, PTY/session ownership is ambiguous, event identity is lost, untrusted generated code executes without OS-level isolation, or required CI evidence is absent.
