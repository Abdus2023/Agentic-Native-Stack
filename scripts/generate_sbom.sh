#!/usr/bin/env bash
# Source: agentic-native-stack.md
# Context: RX.2 SBOM Generation Example
# Extraction ID: CODE-127
# Knowledge Links: KI-186
# Status: scaffolded

syft packages dir:. -o cyclonedx-json > sbom-full.cdx.json
