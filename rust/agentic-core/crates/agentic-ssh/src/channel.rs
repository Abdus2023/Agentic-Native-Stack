//! Source: agentic-native-stack.md
//! Context: 3.6 agentic-ssh
//! Extraction ID: CODE-009
//! Knowledge Links: KI-010
//! Status: scaffolded

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ChannelId(pub u32);

#[derive(Debug, Clone)]
pub enum SshChannelMsg {
    Data(Bytes),
    ExtendedData {
        code: u32,
        data: Bytes,
    },
    Eof,
    ExitStatus(u32),
    ExitSignal {
        signal: String,
        core_dumped: bool,
        error_message: String,
    },
    Close,
}