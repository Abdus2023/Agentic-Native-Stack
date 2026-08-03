//! Source: agentic-native-stack.md
//! Context: RK.2 Bytes-Based Pipeline
//! Extraction ID: CODE-119
//! Knowledge Links: KI-179
//! Status: scaffolded

use bytes::Bytes;

pub struct OutputPipeline {
    buffer: Bytes,
}

impl OutputPipeline {
    pub fn share(&self) -> Bytes {
        self.buffer.clone()
    }
}