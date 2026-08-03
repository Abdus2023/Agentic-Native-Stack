# Use a server-side shadow terminal parser

## Status

Accepted

## Context

Agents need semantic terminal state, not only rendered pixels.

## Decision

Parse terminal output in Rust using a shadow VTE terminal and emit structured events.

## Consequences

This decision is recorded and will be revisited if implementation constraints change.
