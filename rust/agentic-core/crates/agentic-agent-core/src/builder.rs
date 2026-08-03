//! Source: agentic-native-stack.md
//! Context: 3.10 agentic-agent-core
//! Extraction ID: CODE-030
//! Knowledge Links: KI-031
//! Status: scaffolded

pub struct AgentBuilder {
    name: Option<String>,
    provider: Option<Arc<dyn Provider>>,
    memory: Option<Arc<dyn Memory>>,
    permissions: Option<Arc<dyn PermissionGate>>,
    tools: ToolRegistry,
    hooks: Vec<Arc<dyn Hook>>,
    max_turns: usize,
    auto_compact: bool,
}

impl AgentBuilder {
    pub fn new() -> Self {
        Self {
            name: None,
            provider: None,
            memory: None,
            permissions: None,
            tools: ToolRegistry::new(),
            hooks: Vec::new(),
            max_turns: 32,
            auto_compact: true,
        }
    }

    pub fn name(mut self, name: impl Into<String>) -> Self {
        self.name = Some(name.into());
        self
    }

    pub fn provider(mut self, provider: Arc<dyn Provider>) -> Self {
        self.provider = Some(provider);
        self
    }

    pub fn memory(mut self, memory: Arc<dyn Memory>) -> Self {
        self.memory = Some(memory);
        self
    }

    pub fn permissions(mut self, gate: Arc<dyn PermissionGate>) -> Self {
        self.permissions = Some(gate);
        self
    }

    pub fn tool(mut self, tool: Arc<dyn Tool>) -> Self {
        self.tools.register(tool);
        self
    }

    pub fn hook(mut self, hook: Arc<dyn Hook>) -> Self {
        self.hooks.push(hook);
        self
    }

    pub fn max_turns(mut self, max_turns: usize) -> Self {
        self.max_turns = max_turns;
        self
    }

    pub fn auto_compact(mut self, enabled: bool) -> Self {
        self.auto_compact = enabled;
        self
    }

    pub fn build(self) -> Result<Agent, AgentError> {
        Ok(Agent {
            id: AgentId::new(),
            name: self.name.unwrap_or_else(|| "agent".into()),
            provider: self.provider.ok_or(AgentError::MissingProvider)?,
            memory: self.memory,
            permissions: self
                .permissions
                .ok_or(AgentError::MissingPermissionGate)?,
            tools: self.tools,
            hooks: self.hooks,
            max_turns: self.max_turns,
            auto_compact: self.auto_compact,
        })
    }
}