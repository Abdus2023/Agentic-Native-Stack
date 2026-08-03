# Threat Model and Trust Boundaries

## Trust Zones

```text
UNTRUSTED
  ↓
Agent / LLM Output
  ↓
TypeScript Runtime: plugins / integrations
  ↓
Rust Security Boundary: permissions / execution
  ↓
Operating System
```

Agent output, plugin code, terminal output, and remote hosts are semi-trusted or untrusted. All side-effecting operations pass through schema validation, risk classification, permission evaluation, audit logging, and controlled execution.
