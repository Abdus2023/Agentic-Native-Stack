//! Source: agentic-native-stack.md
//! Context: 3.11 agentic-memory
//! Extraction ID: CODE-037
//! Knowledge Links: KI-038
//! Status: scaffolded

use std::collections::HashMap;

pub struct GraphMemory {
    nodes: HashMap<MemoryId, MemoryEntry>,
    edges: Vec<MemoryEdge>,
}

impl GraphMemory {
    pub fn new() -> Self {
        Self {
            nodes: HashMap::new(),
            edges: Vec::new(),
        }
    }

    pub fn insert(&mut self, entry: MemoryEntry) {
        self.nodes.insert(entry.id, entry);
    }

    pub fn add_edge(&mut self, edge: MemoryEdge) {
        self.edges.push(edge);
    }

    pub fn neighbors(&self, id: MemoryId) -> Vec<MemoryId> {
        self.edges
            .iter()
            .filter_map(|edge| {
                if edge.from == id {
                    Some(edge.to)
                } else if edge.to == id {
                    Some(edge.from)
                } else {
                    None
                }
            })
            .collect()
    }
}

#[derive(Debug, Clone)]
pub struct MemoryEdge {
    pub from: MemoryId,
    pub to: MemoryId,
    pub relation: Relation,
    pub weight: f32,
}

#[derive(Debug, Clone)]
pub enum Relation {
    CausedBy,
    RelatedTo,
    Mentions,
    ModifiedFile,
    RanCommand,
    ProducedOutput,
    ChildTaskOf,
    Summarizes,
}