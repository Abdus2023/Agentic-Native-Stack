/**
 * Source: agentic-native-stack.md
 * Context: 4.8 @agentic/agent-runtime
 * Extraction ID: CODE-057
 * Knowledge Links: KI-058
 * Status: scaffolded
 */

export interface AgentRuntimeOptions {
  serverUrl: string;
  provider: Provider;
  permissions: PermissionPrompter;
  plugins?: Plugin[];
  memory?: MemoryClient;
}