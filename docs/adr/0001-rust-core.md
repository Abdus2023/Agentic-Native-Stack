# Use Rust for safety-critical execution boundaries

## Status

Accepted

## Context

PTY, SSH, terminal parsing, permission enforcement, and audit logging require memory safety, low-level OS access, and predictable performance.

## Decision

Implement the core execution and security boundary in Rust.

## Consequences

This decision is recorded and will be revisited if implementation constraints change.
