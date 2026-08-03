//! Source: agentic-native-stack.md
//! Context: D.6 Secret Handling
//! Extraction ID: CODE-073
//! Knowledge Links: KI-074
//! Status: scaffolded

use zeroize::{Zeroize, ZeroizeOnDrop};

#[derive(Zeroize, ZeroizeOnDrop)]
pub struct SshPassword {
    secret: Vec<u8>,
}

impl SshPassword {
    pub fn new(secret: impl Into<Vec<u8>>) -> Self {
        Self {
            secret: secret.into(),
        }
    }

    pub fn expose(&self) -> &[u8] {
        &self.secret
    }
}