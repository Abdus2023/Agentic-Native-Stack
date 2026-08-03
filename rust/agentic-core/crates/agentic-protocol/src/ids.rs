//! Source: agentic-native-stack.md
//! Context: 3.13 agentic-protocol
//! Extraction ID: CODE-042
//! Knowledge Links: KI-043
//! Status: scaffolded

use uuid::Uuid;

macro_rules! id_type {
    ($name:ident, $prefix:expr) => {
        #[derive(Debug, Clone, Copy, PartialEq, Eq, Hash, serde::Serialize)]
        pub struct $name(Uuid);

        impl $name {
            pub fn new() -> Self {
                Self(Uuid::now_v7())
            }

            pub fn to_string_prefixed(&self) -> String {
                format!("{}_{}", $prefix, self.0.as_hyphenated())
            }
        }

        impl Default for $name {
            fn default() -> Self {
                Self::new()
            }
        }
    };
}

pub mod ids {
    use super::*;

    id_type!(SessionId, "sess");
    id_type!(PaneId, "pane");
    id_type!(TabId, "tab");
    id_type!(WindowId, "win");
    id_type!(DomainId, "domain");
    id_type!(AgentId, "agent");
    id_type!(MemoryId, "mem");
    id_type!(EventId, "evt");
}