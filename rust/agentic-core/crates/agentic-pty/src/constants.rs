//! Source: agentic-native-stack.md
//! Context: 3.5 agentic-pty
//! Extraction ID: CODE-004
//! Knowledge Links: KI-005
//! Status: scaffolded

pub const READ_BUFFER_SIZE: usize = 1024 * 1024;
pub const MAX_LOCKED_READ: usize = 64 * 1024;
pub const DRAIN_INTERVAL: Duration = Duration::from_millis(5);
pub const FAIRNESS_QUANTUM: Duration = Duration::from_millis(2);