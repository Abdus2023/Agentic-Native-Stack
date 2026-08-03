/**
 * Source: agentic-native-stack.md
 * Context: C.4 Permission Test Example
 * Extraction ID: CODE-071
 * Knowledge Links: KI-072
 * Status: scaffolded
 */

import { describe, expect, it } from "vitest";

describe("permission policy", () => {
  it("denies high-risk shell execution by default", async () => {
    const policy = createDefaultPolicy();
    const decision = await policy.decide({
      permission: "execute_tool:shell_exec",
      riskLevel: "high",
      toolName: "shell_exec",
    });

    expect(decision.decision).not.toBe("allow");
  });
});