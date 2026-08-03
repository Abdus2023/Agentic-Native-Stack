//! Source: agentic-native-stack.md
//! Context: 3.10 agentic-agent-core
//! Extraction ID: CODE-027
//! Knowledge Links: KI-028
//! Status: scaffolded

use async_trait::async_trait;

#[async_trait]
pub trait Tool: Send + Sync {
    fn name(&self) -> &'static str;
    fn description(&self) -> &'static str;
    fn schema(&self) -> Value;
    fn required_permission(&self) -> Permission {
        Permission::ExecuteTool(self.name().to_string())
    }

    async fn invoke(
        &self,
        args: Value,
        ctx: ToolContext,
    ) -> Result<ToolOutput, ToolError>;
}

#[derive(Debug, Clone)]
pub struct ToolContext {
    pub session_id: SessionId,
    pub agent_id: AgentId,
    pub cwd: Option<String>,
    pub env: Vec<(String, String)>,
    pub permission_token: Option<PermissionToken>,
}

#[derive(Debug, Clone)]
pub struct ToolOutput {
    pub content: Vec<ToolContent>,
    pub structured: Option<Value>,
    pub is_error: bool,
}

#[derive(Debug, Clone)]
pub enum ToolContent {
    Text(String),
    Json(Value),
    TerminalSnapshot(Value),
    FileDiff(String),
    Image { mime: String, bytes_base64: String },
}