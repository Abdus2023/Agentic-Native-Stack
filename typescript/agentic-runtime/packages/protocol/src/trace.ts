/**
 * Source: agentic-native-stack.md
 * Context: E.6 Agent Observability Events
 * Extraction ID: CODE-077
 * Knowledge Links: KI-078
 * Status: scaffolded
 */

export interface AgentTraceView {
  agentId: string;
  turns: AgentTurnView[];
  toolCalls: ToolCallView[];
  permissions: PermissionEventView[];
  memories: MemoryEventView[];
}

export interface AgentTurnView {
  turnId: string;
  startedAtMs: number;
  completedAtMs?: number;
  model?: string;
  promptSummary: string;
  responseSummary?: string;
}

export interface ToolCallView {
  tool: string;
  args: unknown;
  status: "pending" | "success" | "error" | "denied";
  startedAtMs: number;
  completedAtMs?: number;
  outputSummary?: string;
}