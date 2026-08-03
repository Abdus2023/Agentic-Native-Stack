//! Source: agentic-native-stack.md
//! Context: 3.6 agentic-ssh
//! Extraction ID: CODE-012
//! Knowledge Links: KI-013
//! Status: scaffolded

#[derive(Debug, Clone, serde::Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum AgentSshServerEvent {
    SessionOpened {
        session_id: String,
        user: String,
    },
    ChannelOpened {
        session_id: String,
        channel: u32,
    },
    PtyAlloc {
        session_id: String,
        channel: u32,
        term: String,
        rows: u32,
        cols: u32,
    },
    Exec {
        session_id: String,
        channel: u32,
        command: String,
    },
    Exit {
        session_id: String,
        channel: u32,
        code: u32,
    },
    Closed {
        session_id: String,
    },
}