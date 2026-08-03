# Source: agentic-native-stack.md
# Context: RR.3 RPM Spec Snippet
# Extraction ID: CODE-123
# Knowledge Links: KI-183
# Status: scaffolded

Name:           agentic-native
Version:        0.2.0
Release:        1%{?dist}
Summary:        Agentic-native terminal stack
License:        MIT OR Apache-2.0
URL:            https://example.com/agentic-native

%description
Rust core and TypeScript runtime for agent-aware terminal sessions.

%install
install -D -m 0755 agentic %{buildroot}/usr/local/bin/agentic
install -D -m 0755 agentic-daemon %{buildroot}/usr/local/bin/agentic-daemon