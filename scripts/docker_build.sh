#!/usr/bin/env bash
# Source: agentic-native-stack.md
# Context: RW.2 Multi-Arch Image
# Extraction ID: CODE-126
# Knowledge Links: KI-185
# Status: scaffolded

  --platform linux/amd64,linux/arm64 \
  --tag ghcr.io/example/agentic-daemon:0.2.0 \
  --push .
