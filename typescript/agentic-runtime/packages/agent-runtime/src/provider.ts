/**
 * Source: agentic-native-stack.md
 * Context: 4.8 @agentic/agent-runtime
 * Extraction ID: CODE-060
 * Knowledge Links: KI-061
 * Status: scaffolded
 */

export interface Provider {
  complete(request: ModelRequest): Promise<ModelResponse>;
}

export interface ModelRequest {
  model: string;
  messages: ModelMessage[];
  tools: string[];
  context?: Record<string, unknown>;
}

export interface ModelMessage {
  role: "system" | "user" | "assistant" | "tool";
  content: string;
}

export interface ModelResponse {
  content?: string;
  toolCall?: {
    name: string;
    args: unknown;
  };
}