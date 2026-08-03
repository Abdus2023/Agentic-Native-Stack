//! Source: agentic-native-stack.md
//! Context: 3.12 agentic-event
//! Extraction ID: CODE-040
//! Knowledge Links: KI-041
//! Status: scaffolded

use tokio::sync::broadcast;

pub struct EventBus {
    tx: broadcast::Sender<EventEnvelope>,
}

impl EventBus {
    pub fn new(capacity: usize) -> Self {
        let (tx, _) = broadcast::channel(capacity);
        Self { tx }
    }

    pub fn publish(&self, event: EventEnvelope) {
        let _ = self.tx.send(event);
    }

    pub fn subscribe(&self) -> broadcast::Receiver<EventEnvelope> {
        self.tx.subscribe()
    }
}