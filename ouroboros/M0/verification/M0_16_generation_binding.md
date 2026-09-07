# M0.16 — Generation Binding

## Contract

A cold bootstrap establishes a repository-generation snapshot before executing any repository-declared capability code.

Bootstrap MUST reject trust if the repository generation differs after capability reconstruction.

Formally:

```text
G0 = generation(repository)
        |
        v
  reconstruct runtime
        |
        v
G1 = generation(repository)

trusted := G0 == G1
```

This closes the bootstrap time-of-check/time-of-use window at the repository-generation boundary.

## Security meaning

The generation is a content identity, not an authorization token. Promotion remains authoritative only when verification evidence is bound to the same generation. A future signed/external promotion attestation may provide an immutable authorization anchor; M0.16 does not pretend that a self-stored generation value can provide that property.

## Invariant

**M0-INV-14** — Cold bootstrap MUST NOT report a trusted runtime when repository content changes during reconstruction.
