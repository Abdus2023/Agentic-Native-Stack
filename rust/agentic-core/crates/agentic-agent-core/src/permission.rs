//! Source: agentic-native-stack.md
//! Context: 3.10 agentic-agent-core
//! Extraction ID: CODE-029
//! Knowledge Links: KI-030
//! Status: scaffolded

#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum Permission {
    ExecuteTool(String),
    ReadFile(String),
    WriteFile(String),
    NetworkAccess(String),
    SpawnProcess(String),
    SshConnect(String),
    MemoryWrite,
    SubAgentSpawn,
}

#[derive(Debug, Clone)]
pub enum PermissionDecision {
    Allow,
    Deny,
    AskUser,
    AllowOnce,
    AllowForSession,
    Sandbox {
        restrictions: Vec<String>,
    },
}

#[async_trait]
pub trait PermissionGate: Send + Sync {
    async fn decide(
        &self,
        permission: &Permission,
        context: &PermissionContext,
    ) -> PermissionDecision;
}

#[derive(Debug, Clone)]
pub struct PermissionContext {
    pub agent_id: AgentId,
    pub session_id: SessionId,
    pub tool_name: Option<String>,
    pub risk_level: RiskLevel,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RiskLevel {
    Low,
    Medium,
    High,
    Critical,
}

#[derive(Debug, Clone)]
pub struct PermissionToken {
    pub permission: Permission,
    pub expires_at_ms: Option<u64>,
    pub scope: PermissionScope,
}

#[derive(Debug, Clone)]
pub enum PermissionScope {
    Once,
    Session,
    Persistent,
}