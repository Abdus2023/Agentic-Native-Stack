//! Source: agentic-native-stack.md
//! Context: 3.8 agentic-tunnel
//! Extraction ID: CODE-019
//! Knowledge Links: KI-020
//! Status: scaffolded

#[derive(Debug, Clone)]
pub enum TransportSpec {
    Tcp {
        host: String,
        port: u16,
    },
    Unix {
        path: String,
    },
    WebSocket {
        url: String,
    },
    Quic {
        host: String,
        port: u16,
    },
    InProcess {
        name: String,
    },
    SshForwarded {
        connection_id: String,
        remote_host: String,
        remote_port: u16,
    },
}