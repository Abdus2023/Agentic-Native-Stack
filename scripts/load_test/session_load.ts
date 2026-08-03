/**
 * Source: agentic-native-stack.md
 * Context: QL.2 Example: Session Load
 * Extraction ID: CODE-105
 * Knowledge Links: KI-167
 * Status: scaffolded
 */

import { WebSocket } from "ws";

const SESSION_COUNT = 50;

async function main() {
  for (let i = 0; i < SESSION_COUNT; i++) {
    const response = await fetch("http://127.0.0.1:8787/sessions", {
      method: "POST",
      headers: { "content-type": "application/json" },
      body: JSON.stringify({
        type: "create_session",
        spec: { kind: "mock", rows: 24, cols: 80 },
      }),
    });

    const { sessionId } = await response.json();

    const ws = new WebSocket(
      `ws://127.0.0.1:8787/sessions/${sessionId}/terminal`,
    );

    await new Promise((resolve) => ws.once("open", resolve));

    for (let j = 0; j < 100; j++) {
      ws.send(
        JSON.stringify({
          type: "input",
          bytesBase64: Buffer.from(`echo load-${i}-${j}\n`).toString("base64"),
        }),
      );
    }
  }
}

main().catch(console.error);