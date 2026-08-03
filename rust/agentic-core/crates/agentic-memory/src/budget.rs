//! Source: agentic-native-stack.md
//! Context: RG.3 Memory Budget Example
//! Extraction ID: CODE-116
//! Knowledge Links: KI-176
//! Status: scaffolded

pub struct MemoryBudget {
    pub max_scrollback_lines: usize,
    pub max_replay_events: usize,
    pub max_snapshot_count: usize,
    pub max_recording_buffer_bytes: usize,
}

impl Default for MemoryBudget {
    fn default() -> Self {
        Self {
            max_scrollback_lines: 100_000,
            max_replay_events: 10_000,
            max_snapshot_count: 100,
            max_recording_buffer_bytes: 64 * 1024 * 1024,
        }
    }
}