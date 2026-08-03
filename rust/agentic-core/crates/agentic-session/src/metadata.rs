//! Source: agentic-native-stack.md
//! Context: 3.9 agentic-session
//! Extraction ID: CODE-021
//! Knowledge Links: KI-022
//! Status: scaffolded

use agentic_protocol::ids::{DomainId, PaneId, SessionId, TabId, WindowId};

#[derive(Debug, Clone)]
pub struct SessionMetadata {
    pub session_id: SessionId,
    pub title: String,
    pub cwd: Option<String>,
    pub transport: String,
    pub created_at_ms: u64,
}