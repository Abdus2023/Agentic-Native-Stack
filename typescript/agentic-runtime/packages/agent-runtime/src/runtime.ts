/**
 * Source: agentic-native-stack.md
 * Context: 4.8 @agentic/agent-runtime
 * Extraction ID: CODE-058
 * Knowledge Links: KI-059
 * Status: scaffolded
 */

export class AgentRuntime {
  private tools = new Map<string, ToolDefinition>();

  constructor(private options: AgentRuntimeOptions) {}

  registerTool(tool: ToolDefinition) {
    this.tools.set(tool.name, tool);
  }

  async runTask(input: {
    prompt: string;
    sessionId?: string;
    cwd?: string;
  }): Promise<TaskResult> {
    const events: AgentEvent[] = [];
    await this.emitEvent({ type: "turn_started" });

    const memories = this.options.memory
      ? await this.options.memory.recall(input.prompt, 8)
      : [];

    const modelRequest = await this.prepareRequest(input, memories);
    const response = await this.options.provider.complete(modelRequest);

    if (response.toolCall) {
      const tool = this.tools.get(response.toolCall.name);
      if (!tool) {
        throw new Error(`Unknown tool: ${response.toolCall.name}`);
      }

      const permission = await this.options.permissions({
        permission: `execute_tool:${tool.name}`,
        riskLevel: tool.riskLevel ?? "medium",
        toolName: tool.name,
        sessionId: input.sessionId,
      });

      if (permission.decision === "deny") {
        await this.emitEvent({
          type: "permission_denied",
          permission: `execute_tool:${tool.name}`,
        });
        throw new Error("Permission denied");
      }

      await this.emitEvent({
        type: "permission_granted",
        permission: `execute_tool:${tool.name}`,
      });

      const result = await tool.invoke(response.toolCall.args, {
        sessionId: input.sessionId,
        cwd: input.cwd,
      });

      await this.emitEvent({
        type: "tool_call_completed",
        tool: tool.name,
      });

      await this.emitEvent({ type: "turn_completed" });

      return {
        output: result,
        events,
      };
    }

    await this.emitEvent({ type: "turn_completed" });

    return {
      output: response.content,
      events,
    };
  }

  private async prepareRequest(
    input: { prompt: string; sessionId?: string; cwd?: string },
    memories: unknown[],
  ): Promise<ModelRequest> {
    return {
      model: "default",
      messages: [
        {
          role: "system",
          content:
            "You are an agentic terminal assistant with access to PTY, SSH, and memory tools.",
        },
        {
          role: "user",
          content: input.prompt,
        },
      ],
      tools: [...this.tools.keys()],
      context: {
        memories,
      },
    };
  }

  private async emitEvent(event: AgentEvent) {
    // In production this publishes to the server event stream.
    console.debug("agent event", event);
  }
}