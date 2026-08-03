//! Source: agentic-native-stack.md
//! Context: 3.12 agentic-event
//! Extraction ID: CODE-039
//! Knowledge Links: KI-040
//! Status: scaffolded

use std::time::SystemTime;

#[derive(Debug, Clone)]
pub struct EventEnvelope {
    pub id: EventId,
    pub timestamp: SystemTime,
    pub source: EventSource,
    pub payload: EventPayload,
}

#[derive(Debug, Clone)]
pub enum EventSource {
    Pty,
    Ssh,
    Vte,
    Session,
    Agent,
    Memory,
    Tunnel,
    Daemon,
}

#[derive(Debug, Clone)]
pub enum EventPayload {
    Pty(PtyEvent),
    Session(SessionEvent),
    Agent(AgentEvent),
    Vte(VteEvent),
    Custom(Value),
}