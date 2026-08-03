/**
 * Source: agentic-native-stack.md
 * Context: 4.5 @agentic/protocol
 * Extraction ID: CODE-047
 * Knowledge Links: KI-048
 * Status: scaffolded
 */

export const CreateSessionSchema = z.object({
  type: z.literal("create_session"),
  spec: z.object({
    kind: z.enum(["local_pty", "ssh", "mock"]),
    command: z.string().optional(),
    args: z.array(z.string()).optional(),
    cwd: z.string().optional(),
    rows: z.number().int().positive().default(24),
    cols: z.number().int().positive().default(80),
    ssh: z
      .object({
        host: z.string(),
        port: z.number().int().positive().default(22),
        user: z.string(),
      })
      .optional(),
  }),
});

export type CreateSession = z.infer<typeof CreateSessionSchema>;

export const PaneOutputSchema = z.object({
  type: z.literal("pane_output"),
  paneId: PaneIdSchema,
  bytesBase64: z.string(),
  kind: z.enum(["stdout", "stderr", "pty"]).default("pty"),
  monotonicNs: z.string().optional(),
});

export type PaneOutput = z.infer<typeof PaneOutputSchema>;