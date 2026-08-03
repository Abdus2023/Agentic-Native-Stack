# Source Traceability: Implementation-Controlled Mode and v0.2.0 Contract Corpus

## Source

- Origin: conversation message supplied after the README validation exchange.
- Source type: architecture decisions, implementation charter, protocol specification, code artifacts, review findings, and milestone definition.
- Version status: this message contains an evolving sequence of proposals. The latest stated status is implementation-controlled mode with the v0.2.0 execution-kernel contract frozen.

## Supersession and Relationships

1. Repository foundation and v0.1.0 bootstrap material is superseded by the v0.2.0 execution-kernel implementation charter for the immediate implementation scope.
2. Earlier IPC descriptions are refined by ADR-0007 and `docs/ipc-transport.md`.
3. Earlier concurrency descriptions are refined by ADR-0008 and the Tokio task-per-responsibility model.
4. The initial Commit 1 protocol file set is followed by review findings that update:
   - fixture path handling;
   - explicit camelCase serialization tests;
   - protocol method constants;
   - an internal error-code enum while retaining string wire compatibility;
   - a protocol crate README.
5. The final v0.2.0 contract adds `Closing` to the session state machine, per-session event sequence numbers, restart-safe socket handling, minimal audit records, compatibility fixtures, IPC security tests, and a canonical end-to-end local-terminal test.

## Explicit Artifacts Identified

### Documentation and governance

- `docs/adr/0007-ipc-transport.md`
- `docs/ipc-transport.md`
- `docs/adr/0008-async-runtime-model.md`
- `docs/protocol-versioning.md`
- `docs/security-invariants.md`
- RFC process under `rfcs/`
- v0.2.0 implementation charter and definition of done

### Protocol schemas and fixtures

- `schemas/protocol/rpc.json`
- `schemas/protocol/session.json`
- `schemas/protocol/permission.json`
- `schemas/fixtures/initialize-request.json`
- `schemas/fixtures/initialize-response.json`
- `schemas/fixtures/session-create-request.json`
- `schemas/fixtures/session-create-response.json`
- `schemas/fixtures/terminal-input-request.json`
- `schemas/fixtures/terminal-output-event.json`
- `schemas/fixtures/error-response.json`

### Rust implementation artifacts

- `rust/agentic-core/crates/agentic-protocol/Cargo.toml`
- `rust/agentic-core/crates/agentic-protocol/src/lib.rs`
- `rust/agentic-core/crates/agentic-protocol/src/model.rs`
- `rust/agentic-core/crates/agentic-protocol/src/rpc.rs`
- `rust/agentic-core/crates/agentic-protocol/tests/fixtures.rs`
- `rust/agentic-core/crates/agentic-protocol/README.md`
- `rust/agentic-core/tests/ipc_security.rs`
- `rust/agentic-core/tests/e2e_local_terminal.rs`

### Runtime and milestone artifacts

- Unix domain socket IPC with length-prefixed JSON frames
- protocol version negotiation
- request/response IDs
- server event notifications
- session lifecycle methods and events
- Tokio async runtime and bounded channels
- v0.2.0 commit sequence and acceptance criteria

## Existing Repository Comparison

The repository already contains an older/scaffolded `agentic-protocol` implementation under `rust/agentic-core/crates/agentic-protocol/src/` using `ids.rs`, `messages.rs`, and `error.rs`. The supplied v0.2.0 protocol model uses a different module/file surface (`model.rs`, `rpc.rs`, and a new `lib.rs`) and different identifiers and wire envelopes.

Status: **migration applied**. The v0.2.0 protocol surface is now authoritative through `src/lib.rs`, `src/model.rs`, and `src/rpc.rs`; the prior `ids.rs`, `messages.rs`, and `error.rs` modules remain hidden compatibility exports because existing scaffold crates still reference them. They are not the v0.2.0 wire contract and must be migrated before removal.

The workspace already exposes the UUID `v7` and `serde` features required by the supplied `Uuid::now_v7()` examples. The protocol crate manifest, protocol README, v0.2.0 schemas, and compatibility fixtures were added. The full daemon IPC, security-test, and end-to-end implementations remain unresolved because the source supplied specifications/stubs rather than complete implementation bodies.

## Extraction and Verification Status

- Documentation/artifact categories identified: complete for the supplied message.
- Exact source code copied into repository: none from this message; no source file was overwritten.
- Repository scaffolding assigned: explicit paths recorded above.
- Unresolved locations: all listed implementation artifacts remain unresolved until the protocol revision is explicitly selected and complete corrected file contents are supplied.
- Duplicate content: extensive; later v0.2.0 charter material supersedes earlier foundation-only descriptions.
- Conflicts: existing scaffolded protocol module surface conflicts with the proposed Commit 1 module surface.
- Missing items: complete corrected versions of the files affected by the review findings were not supplied in one authoritative code block.
- Ambiguous items: whether to replace the existing protocol scaffold or preserve it alongside the v0.2.0 contract.

## Subsequent v0.2.0 Evolution

The same conversation message continues through accepted/corrected Commit 2 through Commit 7 material:

- Commit 2: `agentic-event` with `EventSource`, `EventFilter`, `SessionSequenceTracker`, bounded `EventBus`, deferred component filtering, and lag recovery.
- Commit 3: `agentic-pty` with Unix PTY allocation, synchronous I/O primitives, fork-safety constraints, checked child setup calls, exclusive wait ownership, NUL validation before fork, and Unix-only tests.
- Commit 4: `agentic-session` with `Created → Running → Attached/Detached → Closing → Closed`, blocking PTY read task, periodic child polling, EventBus sequencing, manager-owned state, and task lifecycle tracking.
- Commit 5: `agentic-daemon` with Unix-socket framed JSON IPC, protocol dispatch, permissions, audit logging, client filtering/cleanup, lock-file ownership, and graceful shutdown.
- Commit 6: `agentic-cli` with split reader/writer architecture, request correlation, event broadcast, raw-mode RAII cleanup, daemon discovery, and protocol-only client coupling.
- Commit 7: Unix-only end-to-end tests for daemon readiness, protocol handshake, session lifecycle, resize, detach/reattach, error handling, and multiple sessions.

The latest stated status is that Commit 1 through Commit 7 are approved/merged in the supplied project narrative, with the v0.2.0 release gate requiring formatting, clippy, workspace tests, and workspace build. This status is documentation provenance only; the local repository has not been verified to contain or pass all of those commits.

## Implementation Conflicts and Verification Limits

The supplied code blocks contain Markdown rendering artifacts in Rust identifiers, operators, HTML entities, and URLs. They require source-level normalization before compilation; no such normalization is recorded as an exact source extraction.

The local repository contains pre-existing scaffold implementations for PTY, event, session, daemon, and protocol modules that do not match the complete v0.2.0 file layout described in the message. No blind overwrite was performed.

The local environment has no `cargo` executable, so the stated release gate could not be executed. The v0.2.0 milestone is therefore **not locally verified**.

## v0.3.0 Terminal Intelligence Scope

The supplied follow-up establishes v0.2.0 as approved in the conversation narrative and defines v0.3.0 as a consumer layer over raw `terminal.output` bytes.

### `agentic-vte` responsibilities

- VTE escape-sequence parsing
- terminal grid state
- OSC 133 command-boundary detection
- prompt detection
- exit-code extraction
- semantic event emission
- alternate-screen tracking
- scrollback

### `agentic-vte` non-responsibilities

- PTY allocation or I/O
- session authority
- permissions
- transport or IPC
- agent reasoning
- memory persistence

### Semantic event registry

The event contract is to remain in `agentic-protocol`, including typed session identity access, semantic event names, wire representations, validation, and compatibility. The proposed semantic events are `command.started`, `command.completed`, `prompt.detected`, `output.line`, `grid.updated`, `alternate_screen.entered`, and `alternate_screen.exited`.

### v0.3.0 implementation phases

1. VTE parser
2. Grid state
3. Command detection
4. Semantic event emission
5. Integration

### Pre-implementation artifacts

- typed session identity accessor or typed event envelope;
- protocol-owned semantic event registry;
- versioned semantic event schemas under `schemas/events/`;
- semantic-event compatibility fixtures;
- deterministic replay and golden terminal fixtures as follow-up items.

### Traceability status

This is architectural scope and review guidance. No `agentic-vte` implementation files were added from this message. The local repository still has not been verified against the v0.2.0 narrative release gate.
