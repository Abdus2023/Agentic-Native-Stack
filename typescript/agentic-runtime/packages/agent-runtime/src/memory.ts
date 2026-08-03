/**
 * Source: agentic-native-stack.md
 * Context: 4.8 @agentic/agent-runtime
 * Extraction ID: CODE-061
 * Knowledge Links: KI-062
 * Status: scaffolded
 */

export interface MemoryClient {
  remember(entry: unknown): Promise<string>;
  recall(query: string, limit: number): Promise<unknown[]>;
}