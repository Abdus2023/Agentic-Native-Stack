//! Source: agentic-native-stack.md
//! Context: 3.9 agentic-session
//! Extraction ID: CODE-025
//! Knowledge Links: KI-026
//! Status: scaffolded

#[derive(Debug, Clone, serde::Serialize)]
#[serde(tag = "type", rename_all = "snake_case")]
pub enum SessionEvent {
    Created {
        session_id: SessionId,
    },
    PaneAdded {
        session_id: SessionId,
        pane_id: PaneId,
    },
    PaneOutput {
        session_id: SessionId,
        pane_id: PaneId,
        bytes_base64: String,
    },
    PaneResized {
        session_id: SessionId,
        pane_id: PaneId,
        rows: u16,
        cols: u16,
    },
    PaneClosed {
        session_id: SessionId,
        pane_id: PaneId,
    },
    SessionClosed {
        session_id: SessionId,
    },
}