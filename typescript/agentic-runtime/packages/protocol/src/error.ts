/**
 * Source: agentic-native-stack.md
 * Context: F.4 TypeScript Error Mapping
 * Extraction ID: CODE-079
 * Knowledge Links: KI-080
 * Status: scaffolded
 */

export class AgenticError extends Error {
  constructor(
    public code: string,
    message: string,
    public retryable: boolean,
    public details?: unknown,
  ) {
    super(message);
    this.name = "AgenticError";
  }
}

export function mapRustError(error: unknown): AgenticError {
  const value = error as {
    code?: string;
    message?: string;
    retryable?: boolean;
    details?: unknown;
  };

  return new AgenticError(
    value.code ?? "internal",
    value.message ?? "Unknown error",
    value.retryable ?? false,
    value.details,
  );
}