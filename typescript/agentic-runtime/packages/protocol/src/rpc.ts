/**
 * Source: agentic-native-stack.md
 * Context: 4.5 @agentic/protocol
 * Extraction ID: CODE-049
 * Knowledge Links: KI-050
 * Status: scaffolded
 */

export interface JsonRpcRequest {
  jsonrpc: "2.0";
  id: string | number;
  method: string;
  params?: unknown;
}

export interface JsonRpcResponse {
  jsonrpc: "2.0";
  id: string | number;
  result?: unknown;
  error?: JsonRpcError;
}

export interface JsonRpcError {
  code: number;
  message: string;
  data?: unknown;
}