# Enforce permissions authoritatively in Rust

## Status

Accepted

## Context

TypeScript plugins and clients are semi-trusted and must not bypass security controls.

## Decision

Make the Rust daemon the authoritative permission enforcement boundary.

## Consequences

This decision is recorded and will be revisited if implementation constraints change.
