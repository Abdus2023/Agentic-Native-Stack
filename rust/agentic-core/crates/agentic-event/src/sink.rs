//! Source: agentic-native-stack.md
//! Context: 3.12 agentic-event
//! Extraction ID: CODE-041
//! Knowledge Links: KI-042
//! Status: scaffolded

#[async_trait]
pub trait EventSink: Send + Sync {
    async fn emit(&self, event: AgentEvent);
}

pub struct BroadcastEventSink {
    bus: Arc<EventBus>,
    source: EventSource,
}

#[async_trait]
impl EventSink for BroadcastEventSink {
    async fn emit(&self, event: AgentEvent) {
        self.bus.publish(EventEnvelope {
            id: EventId::new(),
            timestamp: SystemTime::now(),
            source: self.source.clone(),
            payload: EventPayload::Agent(event),
        });
    }
}