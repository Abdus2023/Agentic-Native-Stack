/**
 * Source: agentic-native-stack.md
 * Context: 4.9 @agentic/plugin-sdk
 * Extraction ID: CODE-064
 * Knowledge Links: KI-065
 * Status: scaffolded
 */

export interface PermissionPolicy {
  name: string;
  decide(request: PermissionRequest): PermissionResponse | null;
}