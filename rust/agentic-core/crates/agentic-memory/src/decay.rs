//! Source: agentic-native-stack.md
//! Context: 3.11 agentic-memory
//! Extraction ID: CODE-038
//! Knowledge Links: KI-039
//! Status: scaffolded

#[derive(Debug, Clone)]
pub struct DecayPolicy {
    pub half_life_ms: u64,
    pub min_salience: f32,
    pub access_boost: f32,
    pub relation_boost: f32,
}

impl DecayPolicy {
    pub fn default_agent_policy() -> Self {
        Self {
            half_life_ms: 1000 * 60 * 60 * 24 * 14,
            min_salience: 0.05,
            access_boost: 0.03,
            relation_boost: 0.01,
        }
    }
}