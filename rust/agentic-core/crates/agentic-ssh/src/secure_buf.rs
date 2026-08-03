//! Source: agentic-native-stack.md
//! Context: 3.6 agentic-ssh
//! Extraction ID: CODE-008
//! Knowledge Links: KI-009
//! Status: scaffolded

use zeroize::{Zeroize, ZeroizeOnDrop};

#[derive(Zeroize, ZeroizeOnDrop)]
pub struct SecretBuf {
    inner: Vec<u8>,
}

impl SecretBuf {
    pub fn new() -> Self {
        Self { inner: Vec::new() }
    }

    pub fn from_slice(data: &[u8]) -> Self {
        Self {
            inner: data.to_vec(),
        }
    }

    pub fn as_slice(&self) -> &[u8] {
        &self.inner
    }

    pub fn extend_from_slice(&mut self, data: &[u8]) {
        self.inner.extend_from_slice(data);
    }
}