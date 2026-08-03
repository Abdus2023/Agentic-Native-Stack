//! Source: agentic-native-stack.md
//! Context: 3.9 agentic-session
//! Extraction ID: CODE-022
//! Knowledge Links: KI-023
//! Status: scaffolded

use std::collections::HashMap;
use std::sync::Arc;
use tokio::sync::RwLock;

pub struct Mux {
    sessions: RwLock<HashMap<SessionId, Arc<Session>>>,
    panes: RwLock<HashMap<PaneId, Arc<Pane>>>,
}

impl Mux {
    pub fn new() -> Self {
        Self {
            sessions: RwLock::new(HashMap::new()),
            panes: RwLock::new(HashMap::new()),
        }
    }

    pub async fn create_session(
        &self,
        spec: SessionSpec,
    ) -> Result<Arc<Session>, SessionError> {
        let session = Session::new(spec).await?;
        let session = Arc::new(session);

        self.sessions
            .write()
            .await
            .insert(session.id(), session.clone());

        Ok(session)
    }

    pub async fn get_session(
        &self,
        session_id: SessionId,
    ) -> Option<Arc<Session>> {
        self.sessions.read().await.get(&session_id).cloned()
    }

    pub async fn attach_pane(
        &self,
        session_id: SessionId,
        pane_spec: PaneSpec,
    ) -> Result<Arc<Pane>, SessionError> {
        let session = self
            .get_session(session_id)
            .await
            .ok_or(SessionError::NotFound(session_id))?;

        let pane = session.spawn_pane(pane_spec).await?;
        let pane = Arc::new(pane);

        self.panes.write().await.insert(pane.id(), pane.clone());

        Ok(pane)
    }
}