//! Source: agentic-native-stack.md
//! Context: J.2 Rust shell_exec Tool Example
//! Extraction ID: CODE-083
//! Knowledge Links: KI-084
//! Status: scaffolded

pub struct ShellExecTool {
    pty: Arc<dyn PtySystem>,
}

#[async_trait]
impl Tool for ShellExecTool {
    fn name(&self) -> &'static str {
        "shell_exec"
    }

    fn description(&self) -> &'static str {
        "Execute a shell command in a PTY and capture structured output."
    }

    fn schema(&self) -> Value {
        serde_json::json!({
            "type": "object",
            "properties": {
                "command": { "type": "string" },
                "cwd": { "type": "string" },
                "timeout_ms": { "type": "integer" }
            },
            "required": ["command"]
        })
    }

    fn required_permission(&self) -> Permission {
        Permission::ExecuteTool("shell_exec".to_string())
    }

    async fn invoke(
        &self,
        args: Value,
        ctx: ToolContext,
    ) -> Result<ToolOutput, ToolError> {
        let command = args["command"]
            .as_str()
            .ok_or_else(|| ToolError::InvalidArgs("command must be string".into()))?;

        let cwd = args["cwd"]
            .as_str()
            .map(|s| s.to_string())
            .or(ctx.cwd.clone());

        let output = run_pty_command(self.pty.clone(), command, cwd).await?;

        Ok(ToolOutput {
            content: vec![ToolContent::Text(output.text)],
            structured: Some(serde_json::json!({
                "exitCode": output.exit_code,
                "durationMs": output.duration_ms,
            })),
            is_error: output.exit_code != Some(0),
        })
    }
}