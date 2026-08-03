#!/usr/bin/env bash
# Source: agentic-native-stack.md
# Context: QK.3 Example: Network Partition
# Extraction ID: CODE-104
# Knowledge Links: KI-166
# Status: scaffolded


# Simulate network partition by dropping SSH port.
sudo iptables -A OUTPUT -p tcp --dport 22 -j DROP
sleep 30
sudo iptables -D OUTPUT -p tcp --dport 22 -j DROP

# Verify reconnection behavior.
agentic session list
