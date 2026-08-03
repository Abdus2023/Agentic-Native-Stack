//! Source: agentic-native-stack.md
//! Context: 3.13 agentic-protocol
//! Extraction ID: CODE-043
//! Knowledge Links: KI-044
//! Status: scaffolded

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum ClientToServer {
    CreateSession {
        spec: Value,
    },
    AttachSession {
        session_id: String,
    },
    DetachSession {
        session_id: String,
    },
    ResizePane {
        pane_id: String,
        rows: u16,
        cols: u16,
    },
    Input {
        pane_id: String,
        bytes_base64: String,
    },
    RunAgentTask {
        prompt: String,
        session_id: Option<String>,
    },
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum ServerToClient {
    SessionCreated {
        session_id: String,
    },
    PaneOutput {
        pane_id: String,
        bytes_base64: String,
    },
    AgentEvent {
        event: Value,
    },
    Snapshot {
        pane_id: String,
        snapshot: Value,
    },
    Error {
        code: String,
        message: String,
    },
}