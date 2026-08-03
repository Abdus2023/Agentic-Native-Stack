//! Source: agentic-native-stack.md
//! Context: 3.8 agentic-tunnel
//! Extraction ID: CODE-018
//! Knowledge Links: KI-019
//! Status: scaffolded

use tokio::io::{AsyncRead, AsyncWrite};

pub trait Transport: AsyncRead + AsyncWrite + Send + Unpin + 'static {}

impl<T> Transport for T where T: AsyncRead + AsyncWrite + Send + Unpin + 'static {}

#[async_trait]
pub trait TransportListener: Send + Sync {
    async fn accept(&self) -> Result<Box<dyn Transport>, TransportError>;
    fn local_addr(&self) -> String;
}

#[async_trait]
pub trait TransportConnector: Send + Sync {
    async fn connect(&self, target: &str) -> Result<Box<dyn Transport>, TransportError>;
}