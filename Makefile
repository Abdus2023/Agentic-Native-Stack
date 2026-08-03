.PHONY: help build test lint fmt fmt-check

help:
	@echo "Targets: build, test, lint, fmt, fmt-check"

build:
	./scripts/build.sh

test:
	./scripts/test.sh

lint:
	cd rust/agentic-core && cargo clippy --workspace -- -D warnings
	pnpm -C typescript/agentic-runtime lint

fmt:
	cd rust/agentic-core && cargo fmt --all

fmt-check:
	cd rust/agentic-core && cargo fmt --all --check
