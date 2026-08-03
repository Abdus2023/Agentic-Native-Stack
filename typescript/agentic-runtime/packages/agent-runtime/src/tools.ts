/**
 * Source: agentic-native-stack.md
 * Context: 4.8 @agentic/agent-runtime
 * Extraction ID: CODE-059
 * Knowledge Links: KI-060
 * Status: scaffolded
 */

export interface ToolDefinition {
  name: string;
  description: string;
  riskLevel?: "low" | "medium" | "high" | "critical";
  schema: Record<string, unknown>;
  invoke(args: unknown, ctx: ToolContext): Promise<ToolResult>;
}

export interface ToolContext {
  sessionId?: string;
  cwd?: string;
  env?: Record<string, string>;
}

export type ToolResult =
  | string
  | number
  | boolean
  | null
  | Record<string, unknown>
  | ToolResult[];