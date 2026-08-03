# ADR-0006: Threat Model and Trust Boundaries

## Status

Accepted

## Context

The stack spans multiple trust zones: agent/LLM output, the TypeScript runtime and its plugins, the Rust security boundary, and the operating system. Agent output, plugin code, terminal output, and remote hosts are semi-trusted or untrusted.

## Decision

Adopt an explicit threat model with the Rust daemon as the authoritative security boundary. All side-effecting operations must pass through schema validation, risk classification, permission evaluation, audit logging, and controlled execution.

## Consequences

- TypeScript cannot bypass permission enforcement.
- Plugins must declare capabilities.
- Terminal output is low-trust input.
- Audit evidence is required for high-risk actions.
- Security reviews are required for trust-boundary changes.
