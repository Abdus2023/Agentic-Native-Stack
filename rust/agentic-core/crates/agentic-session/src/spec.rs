//! Source: agentic-native-stack.md
//! Context: 3.9 agentic-session
//! Extraction ID: CODE-023
//! Knowledge Links: KI-024
//! Status: scaffolded

#[derive(Debug, Clone)]
pub enum SessionSpec {
    LocalPty {
        command: CommandSpec,
        size: Winsize,
    },
    Ssh {
        host: String,
        port: u16,
        user: String,
        command: Option<String>,
        size: Winsize,
    },
    Mock {
        scripted_output: Vec<Vec<u8>>,
    },
}

#[derive(Debug, Clone)]
pub struct PaneSpec {
    pub title: Option<String>,
    pub size: Winsize,
    pub command: Option<CommandSpec>,
}