//! Source: agentic-native-stack.md
//! Context: 3.6 agentic-ssh
//! Extraction ID: CODE-007
//! Knowledge Links: KI-008
//! Status: scaffolded

use async_trait::async_trait;
use bytes::Bytes;

#[async_trait]
pub trait SshClientHandler: Send + Sync + 'static {
    async fn check_server_key(
        &self,
        server_public_key: &ServerKey,
        address: &str,
    ) -> Result<bool, SshError>;

    async fn channel_open_confirmation(
        &self,
        channel: ChannelId,
    ) -> Result<(), SshError>;

    async fn data(
        &self,
        channel: ChannelId,
        data: Bytes,
    ) -> Result<(), SshError>;

    async fn exit_status(
        &self,
        channel: ChannelId,
        status: u32,
    ) -> Result<(), SshError>;
}

#[async_trait]
pub trait SshServerHandler: Send + Sync + 'static {
    async fn auth_publickey(
        &self,
        user: &str,
        public_key: &PublicKey,
    ) -> Result<AuthDecision, SshError>;

    async fn pty_request(
        &self,
        channel: ChannelId,
        term: &str,
        cols: u32,
        rows: u32,
    ) -> Result<(), SshError>;

    async fn shell_request(
        &self,
        channel: ChannelId,
    ) -> Result<(), SshError>;

    async fn exec_request(
        &self,
        channel: ChannelId,
        command: &str,
    ) -> Result<(), SshError>;
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AuthDecision {
    Accept,
    Reject,
    Partial,
}