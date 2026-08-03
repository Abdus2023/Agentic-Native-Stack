#!/usr/bin/env bash
# Source: agentic-native-stack.md
# Context: RS.3 Cosign Example
# Extraction ID: CODE-125
# Knowledge Links: KI-184
# Status: scaffolded

  ghcr.io/example/agentic-daemon:0.2.0

cosign attest --predicate provenance.json \
  --type slsaprovenance \
  ghcr.io/example/agentic-daemon:0.2.0

cosign verify --key cosign.pub \
  ghcr.io/example/agentic-daemon:0.2.0
