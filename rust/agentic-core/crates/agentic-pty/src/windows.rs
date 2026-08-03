//! Source: agentic-native-stack.md
//! Context: H.3 Windows ConPTY Notes
//! Extraction ID: CODE-082
//! Knowledge Links: KI-083
//! Status: scaffolded

pub struct WindowsConPtySystem;

impl PtySystem for WindowsConPtySystem {
    fn openpty(&self, size: Winsize) -> io::Result<PtyPair> {
        // Create ConPTY and pipe handles.
        unimplemented!()
    }

    fn kind(&self) -> PtyKind {
        PtyKind::Local
    }
}