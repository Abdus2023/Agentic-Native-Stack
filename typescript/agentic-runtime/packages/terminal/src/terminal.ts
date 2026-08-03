/**
 * Source: agentic-native-stack.md
 * Context: 4.7 @agentic/terminal
 * Extraction ID: CODE-055
 * Knowledge Links: KI-056
 * Status: scaffolded
 */

import { Terminal } from "@xterm/xterm";
import { FitAddon } from "@xterm/addon-fit";

export interface AgenticTerminalOptions {
  sessionId: string;
  websocketUrl: string;
  rows?: number;
  cols?: number;
}

export class AgenticTerminal {
  private term: Terminal;
  private fitAddon: FitAddon;
  private ws?: WebSocket;

  constructor(private options: AgenticTerminalOptions) {
    this.term = new Terminal({
      cursorBlink: true,
      fontFamily: "JetBrains Mono, Menlo, monospace",
      fontSize: 13,
      rows: options.rows ?? 24,
      cols: options.cols ?? 80,
    });

    this.fitAddon = new FitAddon();
    this.term.loadAddon(this.fitAddon);
  }

  open(element: HTMLElement) {
    this.term.open(element);
    this.fitAddon.fit();
  }

  connect() {
    const ws = new WebSocket(this.options.websocketUrl);
    this.ws = ws;

    ws.addEventListener("open", () => {
      this.sendResize();
    });

    ws.addEventListener("message", (event) => {
      const message = JSON.parse(event.data);
      if (message.type === "pane_output") {
        const bytes = base64ToBytes(message.bytesBase64);
        this.term.write(bytes);
      }
      if (message.type === "snapshot") {
        this.rehydrate(message.snapshot);
      }
    });

    this.term.onData((data) => {
      ws.send(
        JSON.stringify({
          type: "input",
          bytesBase64: bytesToBase64(new TextEncoder().encode(data)),
        }),
      );
    });

    this.term.onResize(() => {
      this.sendResize();
    });
  }

  private sendResize() {
    if (!this.ws) return;
    this.ws.send(
      JSON.stringify({
        type: "resize",
        rows: this.term.rows,
        cols: this.term.cols,
      }),
    );
  }

  private rehydrate(snapshot: unknown) {
    // Snapshot rehydration can either replay serialized cells
    // or write a VT-compatible reconstruction into xterm.js.
    const payload = snapshot as { text?: string };
    if (payload.text) {
      this.term.reset();
      this.term.write(payload.text);
    }
  }

  dispose() {
    this.ws?.close();
    this.term.dispose();
  }
}

function base64ToBytes(input: string): Uint8Array {
  const binary = atob(input);
  const bytes = new Uint8Array(binary.length);
  for (let i = 0; i < binary.length; i++) {
    bytes[i] = binary.charCodeAt(i);
  }
  return bytes;
}

function bytesToBase64(bytes: Uint8Array): string {
  let binary = "";
  for (const byte of bytes) {
    binary += String.fromCharCode(byte);
  }
  return btoa(binary);
}