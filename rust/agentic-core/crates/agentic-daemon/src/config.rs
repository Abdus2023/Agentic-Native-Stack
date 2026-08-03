//! Source: agentic-native-stack.md
//! Context: 3.14 agentic-daemon
//! Extraction ID: CODE-044
//! Knowledge Links: KI-045
//! Status: scaffolded

#[derive(Debug, Clone, serde::Deserialize)]
pub struct DaemonConfig {
    pub ipc_socket_path: String,
    pub websocket_bind: Option<String>,
    pub ssh_server_bind: Option<String>,
    pub default_shell: Option<String>,
    pub max_sessions: usize,
    pub max_panes_per_session: usize,
    pub snapshot_interval_ms: u64,
    pub permissions: PermissionConfig,
}

#[derive(Debug, Clone, serde::Deserialize)]
pub struct PermissionConfig {
    pub default_policy: String,
    pub auto_allow_read: bool,
    pub auto_allow_write: bool,
    pub auto_allow_network: bool,
    pub require_confirmation_for: Vec<String>,
}