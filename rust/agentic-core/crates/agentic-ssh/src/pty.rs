//! Source: agentic-native-stack.md
//! Context: 3.6 agentic-ssh
//! Extraction ID: CODE-011
//! Knowledge Links: KI-012
//! Status: scaffolded

#[derive(Debug, Clone)]
pub struct RemotePtyRequest {
    pub term: String,
    pub cols: u32,
    pub rows: u32,
    pub width_px: u32,
    pub height_px: u32,
    pub modes: Vec<(PtyMode, u32)>,
}

#[derive(Debug, Clone, Copy)]
pub enum PtyMode {
    Echo,
    ICANON,
    IUTF8,
    ONLCR,
    VINTR,
    VQUIT,
    VERASE,
    VKILL,
}