//! Core v0.2.0 domain types.
use serde::{Deserialize, Serialize};

macro_rules! id_type {
    ($name:ident, $prefix:literal) => {
        #[derive(Debug, Clone, PartialEq, Eq, Hash, Serialize, Deserialize)]
        #[serde(transparent)]
        pub struct $name(pub String);
        impl $name { pub fn new() -> Self { Self(format!("{}-{}", $prefix, uuid::Uuid::now_v7())) } }
        impl Default for $name { fn default() -> Self { Self::new() } }
        impl std::fmt::Display for $name { fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result { f.write_str(&self.0) } }
    };
}

id_type!(SessionId, "sess");
id_type!(ClientId, "client");
id_type!(EventId, "evt");

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum SessionState { Created, Running, Attached, Detached, Closing, Closed }

impl SessionState {
    pub fn can_transition_to(self, next: Self) -> bool {
        use SessionState::*;
        matches!((self, next), (Created, Running) | (Running, Attached | Detached | Closing) | (Attached, Detached | Closing) | (Detached, Attached | Closing) | (Closing, Closed))
    }
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct Session { pub id: SessionId, pub state: SessionState, pub shell: String, pub created_at_ms: u64, pub rows: u16, pub cols: u16, pub clients: Vec<ClientId> }

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Client { pub id: ClientId, pub name: String, pub version: String, pub capabilities: Vec<String> }

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct EventEnvelope { pub id: EventId, pub event_type: String, pub timestamp_ms: u64, pub session_id: Option<SessionId>, pub sequence: Option<u64>, pub payload: serde_json::Value }

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all = "camelCase")]
pub struct AuditRecord { pub id: EventId, pub timestamp_ms: u64, pub actor: String, pub action: String, pub session_id: Option<SessionId>, pub decision: String, pub result: String }

#[cfg(test)]
mod tests {
    use super::*;
    #[test] fn transitions() { use SessionState::*; assert!(Created.can_transition_to(Running)); assert!(Running.can_transition_to(Detached)); assert!(Detached.can_transition_to(Closing)); assert!(Closing.can_transition_to(Closed)); assert!(!Closed.can_transition_to(Running)); assert!(!Closing.can_transition_to(Attached)); }
    #[test] fn camel_case_wire_names() { let e = EventEnvelope { id: EventId("evt-1".into()), event_type: "terminal.output".into(), timestamp_ms: 1, session_id: Some(SessionId("sess-1".into())), sequence: Some(42), payload: serde_json::json!({}) }; let v = serde_json::to_value(e).unwrap(); assert!(v.get("eventType").is_some()); assert!(v.get("sessionId").is_some()); }
}
