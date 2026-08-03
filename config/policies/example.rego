# Source: agentic-native-stack.md
# Context: IX.1 Rego Example
# Extraction ID: CODE-088
# Knowledge Links: KI-154
# Status: scaffolded

package agentic.permissions

default decision = "ask"

decision = "deny" {
  input.action == "network_access"
  input.resource == "host:169.254.169.254"
}

decision = "allow" {
  input.action == "file_read"
  startswith(input.resource, "path:/repo/")
}

decision = "ask" {
  input.action == "execute_tool:shell_exec"
  input.risk_level == "high"
}