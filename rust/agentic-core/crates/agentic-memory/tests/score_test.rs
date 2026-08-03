//! Source: agentic-native-stack.md
//! Context: QF.4 Example: Score Calculation
//! Extraction ID: CODE-093
//! Knowledge Links: KI-160
//! Status: scaffolded

#[test]
fn test_memory_score_decay() {
    let memory = StoredMemory {
        salience: 0.8,
        last_accessed_ms: 1000,
        ..Default::default()
    };
    let policy = DecayPolicy {
        half_life_ms: 1000,
        ..Default::default()
    };
    let score_at_1000 = score_memory(&memory, 0.5, 0.0, 1000, &policy);
    let score_at_2000 = score_memory(&memory, 0.5, 0.0, 2000, &policy);
    assert!(score_at_2000 < score_at_1000);
}