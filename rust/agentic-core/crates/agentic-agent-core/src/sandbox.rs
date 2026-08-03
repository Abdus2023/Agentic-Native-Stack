//! Source: agentic-native-stack.md
//! Context: D.5 Sandbox Model
//! Extraction ID: CODE-072
//! Knowledge Links: KI-073
//! Status: scaffolded

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct SandboxPolicy {
    pub filesystem: FilesystemSandbox,
    pub network: NetworkSandbox,
    pub process: ProcessSandbox,
    pub max_runtime_ms: Option<u64>,
    pub max_output_bytes: Option<u64>,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct FilesystemSandbox {
    pub readable: Vec<String>,
    pub writable: Vec<String>,
    pub denied: Vec<String>,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct NetworkSandbox {
    pub allowed_hosts: Vec<String>,
    pub denied_hosts: Vec<String>,
    pub allow_localhost: bool,
}

#[derive(Debug, Clone, serde::Serialize, serde::Deserialize)]
pub struct ProcessSandbox {
    pub allow_spawn: bool,
    pub allowed_programs: Vec<String>,
    pub max_children: usize,
}