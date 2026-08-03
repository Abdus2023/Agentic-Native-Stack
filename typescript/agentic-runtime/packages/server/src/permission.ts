/**
 * Source: agentic-native-stack.md
 * Context: 4.6 @agentic/server
 * Extraction ID: CODE-053
 * Knowledge Links: KI-054
 * Status: scaffolded
 */

export interface PermissionRequest {
  permission: string;
  riskLevel: "low" | "medium" | "high" | "critical";
  toolName?: string;
  sessionId?: string;
}

export interface PermissionResponse {
  decision:
    | "allow"
    | "deny"
    | "allow_once"
    | "allow_for_session"
    | "sandbox";
  restrictions?: string[];
}

export type PermissionPrompter = (
  request: PermissionRequest,
) => Promise<PermissionResponse>;