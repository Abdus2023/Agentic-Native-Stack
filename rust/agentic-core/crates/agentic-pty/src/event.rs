//! Source: agentic-native-stack.md
//! Context: 3.5 agentic-pty
//! Extraction ID: CODE-006
//! Knowledge Links: KI-007
//! Status: scaffolded

use agentic_protocol::ids::{PaneId, SessionId};

#[derive(Debug, Clone)]
pub enum PtyEvent {
    Created {
        session_id: SessionId,
        pane_id: PaneId,
        kind: PtyKind,
    },
    Resized {
        pane_id: PaneId,
        size: Winsize,
    },
    Output {
        pane_id: PaneId,
        bytes: Vec<u8>,
    },
    ChildExited {
        pane_id: PaneId,
        status: ExitStatus,
    },
    IoError {
        pane_id: PaneId,
        message: String,
    },
    Closed {
        pane_id: PaneId,
    },
}