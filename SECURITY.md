# Security Policy

## Reporting a Vulnerability

Please do not open public GitHub issues for security vulnerabilities.

Use the repository's private security disclosure channel. We aim to acknowledge reports within 72 hours.

## Supported Versions

| Version | Supported |
|---|---|
| 0.1.x | pre-release |

## Security Boundaries

The Rust daemon is the authoritative enforcement boundary for PTY execution, SSH execution, permission checks, audit logging, and memory persistence. See [docs/security-invariants.md](docs/security-invariants.md) and [docs/threat-model.md](docs/threat-model.md).
