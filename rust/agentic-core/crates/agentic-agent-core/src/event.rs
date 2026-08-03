//! Source: agentic-native-stack.md
//! Context: 3.10 agentic-agent-core
//! Extraction ID: CODE-026
//! Knowledge Links: KI-027
//! Status: scaffolded

use serde_json::Value;

#[derive(Debug, Clone, serde::Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum AgentEvent {
    TurnStarted,
    TurnCompleted,
    PromptQueued,
    PromptDispatched,
    ModelRequestPrepared,
    ModelRequestSent,
    ModelChunkReceived,
    ModelResponseCompleted,
    ModelError,
    ToolCallRequested,
    ToolCallApproved,
    ToolCallDenied,
    ToolCallStarted,
    ToolCallCompleted,
    ToolCallFailed,
    PermissionRequested,
    PermissionGranted,
    PermissionDenied,
    MemoryRecallStarted,
    MemoryRecallCompleted,
    MemoryStored,
    SubAgentSpawned,
    SubAgentCompleted,
    ContextCompacted,
    SessionAttached,
    SessionDetached,
}