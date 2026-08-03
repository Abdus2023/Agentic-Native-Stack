//! Source: agentic-native-stack.md
//! Context: 3.9 agentic-session
//! Extraction ID: CODE-024
//! Knowledge Links: KI-025
//! Status: scaffolded

pub struct Session {
    id: SessionId,
    spec: SessionSpec,
    panes: RwLock<Vec<PaneId>>,
}

impl Session {
    pub async fn new(spec: SessionSpec) -> Result<Self, SessionError> {
        Ok(Self {
            id: SessionId::new(),
            spec,
            panes: RwLock::new(Vec::new()),
        })
    }

    pub fn id(&self) -> SessionId {
        self.id
    }

    pub async fn spawn_pane(
        &self,
        _spec: PaneSpec,
    ) -> Result<Pane, SessionError> {
        Ok(Pane {
            id: PaneId::new(),
            session_id: self.id,
        })
    }
}

pub struct Pane {
    id: PaneId,
    session_id: SessionId,
}

impl Pane {
    pub fn id(&self) -> PaneId {
        self.id
    }

    pub fn session_id(&self) -> SessionId {
        self.session_id
    }
}