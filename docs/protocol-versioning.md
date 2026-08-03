# Protocol Versioning Policy

The wire protocol and event schemas are versioned independently of crate and package versions.

## Version Format

```text
MAJOR.MINOR.PATCH
```

## MAJOR Changes

A MAJOR version change indicates incompatible wire or schema changes, including removing or renaming fields, changing field semantics, changing message framing, identifier formats, or permission decision semantics. MAJOR changes require an RFC, an ADR, migration documentation, compatibility testing, and release notes.

## MINOR Changes

A MINOR version change indicates backward-compatible additions, including optional fields, event types, RPC methods, tool schemas, and metadata. MINOR changes require schema and protocol documentation updates and compatibility tests.

## PATCH Changes

A PATCH version change indicates documentation or metadata-only changes.

## Compatibility

Event envelopes include `eventVersion`; RPC messages include `v`. Consumers should ignore unknown fields, reject unknown major versions, and support upcasters for older minor versions where required.

Before `1.0`, breaking changes may occur in minor releases. After `1.0`, backward compatibility is required within a major version.
