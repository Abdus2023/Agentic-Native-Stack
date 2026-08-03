#!/usr/bin/env bash
# Source: agentic-native-stack.md
# Context: QK.2 Example: Daemon Crash
# Extraction ID: CODE-103
# Knowledge Links: KI-166
# Status: scaffolded


agentic session new --shell /bin/bash &
SESSION_PID=$!
sleep 1

kill -9 "$(pgrep agentic-daemon)"
sleep 2

agentic health || echo "daemon not healthy"
agentic session list || echo "session list failed"
