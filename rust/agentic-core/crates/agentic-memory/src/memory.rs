//! Source: agentic-native-stack.md
//! Context: 3.11 agentic-memory
//! Extraction ID: CODE-035
//! Knowledge Links: KI-036
//! Status: scaffolded

#[async_trait]
pub trait Memory: Send + Sync {
    async fn remember(
        &self,
        entry: MemoryEntry,
    ) -> Result<MemoryId, MemoryError>;

    async fn recall(
        &self,
        query: &str,
        limit: usize,
    ) -> Result<Vec<MemoryEntry>, MemoryError>;

    async fn relate(
        &self,
        from: MemoryId,
        to: MemoryId,
        relation: Relation,
    ) -> Result<(), MemoryError>;

    async fn decay(
        &self,
        policy: DecayPolicy,
    ) -> Result<usize, MemoryError>;
}