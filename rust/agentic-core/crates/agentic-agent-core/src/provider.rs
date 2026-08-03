//! Source: agentic-native-stack.md
//! Context: 3.10 agentic-agent-core
//! Extraction ID: CODE-032
//! Knowledge Links: KI-033
//! Status: scaffolded

#[async_trait]
pub trait Provider: Send + Sync {
    async fn complete(
        &self,
        request: ModelRequest,
    ) -> Result<ModelResponse, ProviderError>;

    fn supports_streaming(&self) -> bool {
        false
    }
}

#[derive(Debug, Clone)]
pub struct ModelRequest {
    pub model: String,
    pub messages: Vec<ModelMessage>,
    pub tools: Vec<ModelToolSpec>,
}

#[derive(Debug, Clone)]
pub struct ModelMessage {
    pub role: Role,
    pub content: String,
}

#[derive(Debug, Clone, Copy)]
pub enum Role {
    System,
    User,
    Assistant,
    Tool,
}

#[derive(Debug, Clone)]
pub struct ModelToolSpec {
    pub name: String,
}

#[derive(Debug, Clone)]
pub struct ModelResponse {
    pub messages: Vec<ModelMessage>,
    pub tool_call: Option<ToolCall>,
}

#[derive(Debug, Clone)]
pub struct ToolCall {
    pub name: String,
    pub args: Value,
}