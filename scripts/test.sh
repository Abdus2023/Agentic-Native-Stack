#!/usr/bin/env bash
set -euo pipefail
cargo test --workspace --manifest-path rust/agentic-core/Cargo.toml
pnpm -C typescript/agentic-runtime test
