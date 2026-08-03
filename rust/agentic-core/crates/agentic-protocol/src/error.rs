//! Source: agentic-native-stack.md
//! Context: F.2 Rust Error Enum
//! Extraction ID: CODE-078
//! Knowledge Links: KI-079
//! Status: scaffolded

#[derive(Debug, thiserror::Error)]
pub enum AgenticError {
    #[error("configuration error: {0}")]
    Config(String),
    #[error("transport error: {0}")]
    Transport(String),
    #[error("authentication error: {0}")]
    Auth(String),
    #[error("permission denied: {0}")]
    Permission(String),
    #[error("pty error: {0}")]
    Pty(#[from] std::io::Error),
    #[error("ssh error: {0}")]
    Ssh(String),
    #[error("vte error: {0}")]
    Vte(String),
    #[error("session error: {0}")]
    Session(String),
    #[error("tool error: {0}")]
    Tool(String),
    #[error("provider error: {0}")]
    Provider(String),
    #[error("memory error: {0}")]
    Memory(String),
    #[error("protocol error: {0}")]
    Protocol(String),
    #[error("resource exhausted: {0}")]
    ResourceExhausted(String),
    #[error("timeout: {0}")]
    Timeout(String),
    #[error("internal error: {0}")]
    Internal(String),
}