//! Source: agentic-native-stack.md
//! Context: 3.10 agentic-agent-core
//! Extraction ID: CODE-034
//! Knowledge Links: KI-035
//! Status: scaffolded

#[derive(Debug, Clone)]
pub enum OrchestrationMode {
    Sequential,
    Parallel,
    ForkJoin,
    WorktreeIsolated,
}

pub struct SubAgentPlan {
    pub parent_agent_id: AgentId,
    pub mode: OrchestrationMode,
    pub tasks: Vec<SubAgentTask>,
}

pub struct SubAgentTask {
    pub task_id: String,
    pub prompt: String,
    pub cwd: Option<String>,
    pub isolated_worktree: bool,
}