# Contributing

Contributions are welcome. Open an issue or RFC before large changes.

## Development Checks

```bash
cargo fmt --all --check --manifest-path rust/agentic-core/Cargo.toml
cargo clippy --workspace --manifest-path rust/agentic-core/Cargo.toml -- -D warnings
cargo test --workspace --manifest-path rust/agentic-core/Cargo.toml
pnpm -C typescript/agentic-runtime lint
pnpm -C typescript/agentic-runtime typecheck
pnpm -C typescript/agentic-runtime test
```

## Commit Convention

```text
feat(scope): summary
fix(scope): summary
docs(scope): summary
build(scope): summary
ci(scope): summary
test(scope): summary
```

## Pull Request Workflow

1. Open an issue or RFC for large changes.
2. Add tests and documentation.
3. Run all checks.
4. Submit a pull request.
