/**
 * Source: agentic-native-stack.md
 * Context: 4.9 @agentic/plugin-sdk
 * Extraction ID: CODE-063
 * Knowledge Links: KI-064
 * Status: scaffolded
 */

import type { Plugin } from "@agentic/plugin-sdk";

export const gitWorktreePlugin: Plugin = {
  name: "git-worktree",
  version: "0.1.0",
  register(api) {
    api.registerTool({
      name: "git_worktree_create",
      description: "Create an isolated git worktree for parallel agent work.",
      riskLevel: "medium",
      schema: {
        type: "object",
        properties: {
          branch: { type: "string" },
          path: { type: "string" },
        },
        required: ["branch", "path"],
      },
      async invoke(args) {
        const { branch, path } = args as {
          branch: string;
          path: string;
        };
        return {
          status: "created",
          branch,
          path,
        };
      },
    });
  },
};