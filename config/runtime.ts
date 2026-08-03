/**
 * Source: agentic-native-stack.md
 * Context: A.2 Runtime Configuration Example
 * Extraction ID: CODE-067
 * Knowledge Links: KI-068
 * Status: scaffolded
 */

export interface RuntimeConfig {
  server: {
    port: number;
    host: string;
    rustDaemonSocket: string;
  };
  terminal: {
    fontFamily: string;
    fontSize: number;
    scrollback: number;
  };
  agent: {
    provider: string;
    maxTurns: number;
    autoCompact: boolean;
  };
  permissions: {
    defaultPolicy: "allow" | "deny" | "ask";
    rules: PermissionRule[];
  };
}

export interface PermissionRule {
  permission: string;
  decision: "allow" | "deny" | "ask";
  paths?: string[];
  tools?: string[];
  hosts?: string[];
  risk?: Array<"low" | "medium" | "high" | "critical">;
}