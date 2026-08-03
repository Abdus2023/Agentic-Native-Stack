/**
 * Source: agentic-native-stack.md
 * Context: K.3 Runtime Interpretation
 * Extraction ID: CODE-086
 * Knowledge Links: KI-087
 * Status: scaffolded
 */

export interface Workflow {
  name: string;
  description?: string;
  permissions?: WorkflowPermissions;
  tasks: WorkflowTask[];
}

export interface WorkflowTask {
  id: string;
  agent: string;
  prompt: string;
  needs?: string[];
  tools?: string[];
  isolatedWorktree?: boolean | "inherit";
  capabilityTier?: 0 | 1 | 2 | 3;
}