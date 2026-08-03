/**
 * Source: agentic-native-stack.md
 * Context: 4.6 @agentic/server
 * Extraction ID: CODE-052
 * Knowledge Links: KI-053
 * Status: scaffolded
 */

export interface SessionBridge {
  createSession(spec: unknown): Promise<string>;
  sendInput(bytesBase64: string): void;
  resize(rows: number, cols: number): void;
  onOutput(listener: (output: unknown) => void): void;
  onAgentEvent(listener: (event: AgentEvent) => void): void;
  runAgentTask(prompt: string): Promise<string>;
  detach(): void;
}

export async function connectToRustDaemon(
  socketPath: string,
): Promise<SessionBridge> {
  // In production this connects to the Rust daemon over Unix socket
  // or spawns the daemon as a sidecar and communicates over stdio.
  throw new Error("not implemented");
}