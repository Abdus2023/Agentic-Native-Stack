//! Source: agentic-native-stack.md
//! Context: 3.11 agentic-memory
//! Extraction ID: CODE-036
//! Knowledge Links: KI-037
//! Status: scaffolded

#[derive(Debug, Clone)]
pub struct MemoryEntry {
    pub id: MemoryId,
    pub kind: MemoryKind,
    pub content: String,
    pub embedding: Option<Vec<f32>>,
    pub metadata: Value,
    pub created_at_ms: u64,
    pub last_accessed_ms: u64,
    pub access_count: u64,
    pub salience: f32,
}

#[derive(Debug, Clone, Copy)]
pub enum MemoryKind {
    Episodic,
    Semantic,
    Procedural,
    CommandHistory,
    FileEntity,
    SessionSummary,
    ToolResult,
}