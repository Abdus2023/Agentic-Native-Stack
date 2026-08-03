#!/usr/bin/env bash
set -euo pipefail
cargo build --workspace --manifest-path rust/agentic-core/Cargo.toml
pnpm -C typescript/agentic-runtime install
pnpm -C typescript/agentic-runtime build
