# Source: agentic-native-stack.md
# Context: G.3 Bash Integration
# Extraction ID: CODE-080
# Knowledge Links: KI-081
# Status: scaffolded

__agentic_precmd() {
  local exit_code=$?
  printf '\033]1337;AgenticPromptStart\007'
  printf '\033]1337;AgenticCwd=%s\007' "$PWD"
  printf '\033]1337;AgenticCommandEnd=%s\007' "$exit_code"
}

__agentic_preexec() {
  printf '\033]1337;AgenticPromptEnd\007'
  printf '\033]1337;AgenticCommandStart=%s\007' "$1"
}

trap '__agentic_preexec "$BASH_COMMAND"' DEBUG
PROMPT_COMMAND="__agentic_precmd;${PROMPT_COMMAND}"
