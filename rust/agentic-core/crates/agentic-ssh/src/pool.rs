//! Source: agentic-native-stack.md
//! Context: 3.6 agentic-ssh
//! Extraction ID: CODE-010
//! Knowledge Links: KI-011
//! Status: scaffolded

use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::Mutex;

#[derive(Debug, Clone, Hash, PartialEq, Eq)]
pub struct ConnectionKey {
    pub host: String,
    pub port: u16,
    pub user: String,
}

pub struct SshConnectionPool {
    connections: Mutex<HashMap<ConnectionKey, Arc<SshConnection>>>,
}

impl SshConnectionPool {
    pub fn new() -> Self {
        Self {
            connections: Mutex::new(HashMap::new()),
        }
    }

    pub async fn get_or_connect(
        &self,
        key: ConnectionKey,
        connector: impl AsyncSshConnector,
    ) -> Result<Arc<SshConnection>, SshError> {
        let mut conns = self.connections.lock().await;

        if let Some(conn) = conns.get(&key) {
            if conn.is_alive().await {
                return Ok(conn.clone());
            } else {
                conns.remove(&key);
            }
        }

        let conn = Arc::new(connector.connect(&key).await?);
        conns.insert(key, conn.clone());
        Ok(conn)
    }
}

#[async_trait]
pub trait AsyncSshConnector: Send + Sync {
    async fn connect(
        &self,
        key: &ConnectionKey,
    ) -> Result<SshConnection, SshError>;
}

pub struct SshConnection {
    pub key: ConnectionKey,
    // Internal russh handle would live here.
}

impl SshConnection {
    pub async fn is_alive(&self) -> bool {
        true
    }
}