/**
 * Source: agentic-native-stack.md
 * Context: 4.7 @agentic/terminal
 * Extraction ID: CODE-056
 * Knowledge Links: KI-057
 * Status: scaffolded
 */

import { useEffect, useRef } from "react";
import { AgenticTerminal } from "@agentic/terminal";

export function TerminalPanel({
  sessionId,
  websocketUrl,
}: {
  sessionId: string;
  websocketUrl: string;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!ref.current) return;

    const terminal = new AgenticTerminal({
      sessionId,
      websocketUrl,
    });

    terminal.open(ref.current);
    terminal.connect();

    return () => {
      terminal.dispose();
    };
  }, [sessionId, websocketUrl]);

  return <div ref={ref} style={{ height: "100%", width: "100%" }} />;
}