/**
 * Source: agentic-native-stack.md
 * Context: 4.5 @agentic/protocol
 * Extraction ID: CODE-048
 * Knowledge Links: KI-049
 * Status: scaffolded
 */

export const AgentEventSchema = z.discriminatedUnion("type", [
  z.object({ type: z.literal("turn_started") }),
  z.object({ type: z.literal("turn_completed") }),
  z.object({ type: z.literal("tool_call_requested"), tool: z.string() }),
  z.object({ type: z.literal("tool_call_completed"), tool: z.string() }),
  z.object({ type: z.literal("tool_call_failed"), tool: z.string() }),
  z.object({ type: z.literal("permission_requested"), permission: z.string() }),
  z.object({ type: z.literal("permission_granted"), permission: z.string() }),
  z.object({ type: z.literal("permission_denied"), permission: z.string() }),
  z.object({ type: z.literal("memory_stored"), memoryId: z.string() }),
  z.object({ type: z.literal("sub_agent_spawned"), agentId: AgentIdSchema }),
  z.object({ type: z.literal("context_compacted") }),
]);

export type AgentEvent = z.infer<typeof AgentEventSchema>;