//! Source: agentic-native-stack.md
//! Context: 3.5 agentic-pty
//! Extraction ID: CODE-002
//! Knowledge Links: KI-003
//! Status: scaffolded

pub trait PtyChild: Send {
    fn pid(&self) -> Option<u32>;
    fn try_wait(&mut self) -> io::Result<Option<ExitStatus>>;
    fn kill(&mut self) -> io::Result<()>;
    fn signal(&mut self, signal: i32) -> io::Result<()>;
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ExitStatus {
    Code(i32),
    Signal(i32),
    Unknown,
}