/**
 * Source: agentic-native-stack.md
 * Context: 4.5 @agentic/protocol
 * Extraction ID: CODE-046
 * Knowledge Links: KI-047
 * Status: scaffolded
 */

import { z } from "zod";

export const SessionIdSchema = z.string().brand<"SessionId">();
export const PaneIdSchema = z.string().brand<"PaneId">();
export const AgentIdSchema = z.string().brand<"AgentId">();

export type SessionId = z.infer<typeof SessionIdSchema>;
export type PaneId = z.infer<typeof PaneIdSchema>;
export type AgentId = z.infer<typeof AgentIdSchema>;