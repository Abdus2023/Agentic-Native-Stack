/**
 * Source: agentic-native-stack.md
 * Context: 4.6 @agentic/server
 * Extraction ID: CODE-051
 * Knowledge Links: KI-052
 * Status: scaffolded
 */

import Fastify from "fastify";
import websocket from "@fastify/websocket";
import {
  CreateSessionSchema,
  PaneOutputSchema,
  type AgentEvent,
} from "@agentic/protocol";

export interface ServerOptions {
  rustDaemonSocket: string;
  port: number;
  host: string;
}

export async function createAgenticServer(options: ServerOptions) {
  const app = Fastify({
    logger: true,
  });

  await app.register(websocket);

  const sessions = new Map<string, SessionBridge>();

  app.post("/sessions", async (request, reply) => {
    const parsed = CreateSessionSchema.safeParse(request.body);

    if (!parsed.success) {
      return reply.code(400).send({
        error: "invalid_request",
        details: parsed.error.flatten(),
      });
    }

    const bridge = await connectToRustDaemon(options.rustDaemonSocket);
    const sessionId = await bridge.createSession(parsed.data.spec);
    
    sessions.set(sessionId, bridge);

    return {
      sessionId,
    };
  });

  app.get("/sessions/:sessionId/terminal", { websocket: true }, (socket, request) => {
    const sessionId = (request.params as any).sessionId as string;
    const bridge = sessions.get(sessionId);

    if (!bridge) {
      socket.close(4404, "session_not_found");
      return;
    }

    bridge.onOutput((output) => {
      socket.send(JSON.stringify(output));
    });

    socket.on("message", (raw) => {
      const message = JSON.parse(raw.toString());
      
      if (message.type === "input") {
        bridge.sendInput(message.bytesBase64);
      }
      if (message.type === "resize") {
        bridge.resize(message.rows, message.cols);
      }
    });

    socket.on("close", () => {
      bridge.detach();
    });
  });

  app.post("/agents/tasks", async (request, reply) => {
    const body = request.body as {
      prompt: string;
      sessionId?: string;
    };

    const bridge = body.sessionId
      ? sessions.get(body.sessionId)
      : await connectToRustDaemon(options.rustDaemonSocket);

    if (!bridge) {
      return reply.code(400).send({
        error: "no_session",
      });
    }

    const taskId = await bridge.runAgentTask(body.prompt);

    return {
      taskId,
    };
  });

  await app.listen({
    port: options.port,
    host: options.host,
  });

  return app;
}