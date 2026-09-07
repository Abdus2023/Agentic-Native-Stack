# M0.17 — Immutable Promotion Evidence

## Purpose

M0.16 binds cold bootstrap trust to a stable repository generation during reconstruction. It does not, by itself, establish an immutable authorization anchor for a promoted generation.

M0.17 defines the boundary between **self-reported state** and **promotion authority**.

## Contract

A promotion decision MUST be based on verification evidence bound to one repository generation and one verification epoch.

The runtime MUST NOT treat a repository-maintained mutable value as an independent proof that the same value was previously authorized.

Formally:

```text
verification
    |
    +-- generation = G
    +-- epoch      = E
    +-- all gates  = PASS
    |
    v
promotion decision
    |
    v
external / immutable anchor (future capability)
```

Until an immutable or externally anchored promotion mechanism exists, M0 promotion is a **runtime authorization decision**, not a cryptographic attestation.

## Required properties

1. Promotion MUST reject stale repository generations.
2. Promotion MUST reject verification results from another epoch.
3. Promotion MUST reject any non-PASS result.
4. Promotion MUST NOT infer authority from a mutable `promoted` marker stored by the runtime.
5. Bootstrap MUST NOT elevate such a marker into trust.
6. Any future persistent promotion record MUST contain at least the generation, verification epoch, gate evidence identifiers, and promotion identity.
7. An immutable/external anchor, when introduced, MUST be checked independently of the runtime's mutable repository state.

## Threat model

A self-written file such as:

```text
.promotion/current = <generation>
```

is useful as a journal/index, but is not an authorization root. The same runtime that writes repository state could rewrite that file. Therefore:

```text
self-written claim != independent authority
```

## Invariant

**M0-INV-15** — Promotion MUST never derive independent authority from a mutable repository claim that the runtime itself can rewrite.

## Consequence

M0 deliberately stops short of pretending that local promotion is equivalent to signed release provenance. The architecture remains honest: repository generation supplies identity; verification supplies evidence; promotion supplies a runtime decision; an external or immutable trust anchor is a separate future layer.
