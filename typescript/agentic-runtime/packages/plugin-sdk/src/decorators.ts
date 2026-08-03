/**
 * Source: agentic-native-stack.md
 * Context: 4.9 @agentic/plugin-sdk
 * Extraction ID: CODE-065
 * Knowledge Links: KI-066
 * Status: scaffolded
 */

export interface TerminalDecorator {
  name: string;
  decorateLine?(line: string, context: LineContext): LineDecoration | null;
}

export interface LineContext {
  sessionId: string;
  paneId: string;
  lineNumber: number;
}

export interface LineDecoration {
  cssClass?: string;
  gutterIcon?: string;
  tooltip?: string;
}