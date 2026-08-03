//! Source: agentic-native-stack.md
//! Context: QO.2 Agent Test Harness
//! Extraction ID: CODE-109
//! Knowledge Links: KI-169
//! Status: scaffolded

pub struct AgentTestHarness {
    agent: Arc<Agent>,
    events: Arc<TestEventSink>,
}

impl AgentTestHarness {
    pub fn new(agent: Agent) -> Self {
        Self {
            agent: Arc::new(agent),
            events: Arc::new(TestEventSink::new()),
        }
    }

    pub async fn run_prompt(&self, prompt: &str) -> AgentResult {
        let task = AgentTask {
            prompt: prompt.to_string(),
            session_id: SessionId::new(),
            cwd: Some("/tmp".to_string()),
            env: vec![],
        };

        run_agent_loop(self.agent.clone(), task, self.events.clone()).await
    }
}