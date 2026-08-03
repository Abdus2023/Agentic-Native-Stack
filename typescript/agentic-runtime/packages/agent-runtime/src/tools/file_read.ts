/**
 * Source: agentic-native-stack.md
 * Context: J.3 TypeScript file_read Tool Example
 * Extraction ID: CODE-084
 * Knowledge Links: KI-085
 * Status: scaffolded
 */

import { readFile } from "node:fs/promises";

export const fileReadTool: ToolDefinition = {
  name: "file_read",
  description: "Read a UTF-8 text file from disk.",
  riskLevel: "low",
  schema: {
    type: "object",
    properties: {
      path: { type: "string" },
      maxBytes: { type: "number" },
    },
    required: ["path"],
  },
  async invoke(args, ctx) {
    const { path, maxBytes = 100_000 } = args as {
      path: string;
      maxBytes?: number;
    };

    const content = await readFile(path, "utf8");

    if (content.length > maxBytes) {
      return {
        truncated: true,
        content: content.slice(0, maxBytes),
      };
    }

    return {
      truncated: false,
      content,
    };
  },
};