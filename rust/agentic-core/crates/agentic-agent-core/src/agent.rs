//! Source: agentic-native-stack.md
//! Context: 3.10 agentic-agent-core
//! Extraction ID: CODE-031
//! Knowledge Links: KI-032
//! Status: scaffolded

pub struct Agent {
    id: AgentId,
    name: String,
    provider: Arc<dyn Provider>,
    memory: Option<Arc<dyn Memory>>,
    permissions: Arc<dyn PermissionGate>,
    tools: ToolRegistry,
    hooks: Vec<Arc<dyn Hook>>,
    max_turns: usize,
    auto_compact: bool,
}

impl Agent {
    pub async fn run_turn(
        &self,
        input: AgentInput,
        event_sink: Arc<dyn EventSink>,
    ) -> Result<AgentTurnOutput, AgentError> {
        event_sink.emit(AgentEvent::TurnStarted).await;

        let permission_context = PermissionContext {
            agent_id: self.id,
            session_id: input.session_id,
            tool_name: None,
            risk_level: RiskLevel::Medium,
        };

        if let Some(memory) = &self.memory {
            event_sink.emit(AgentEvent::MemoryRecallStarted).await;
            let memories = memory
                .recall(&input.prompt, 8)
                .await
                .unwrap_or_default();
            event_sink.emit(AgentEvent::MemoryRecallCompleted).await;
            // Memories would be injected into the model context here.
            let _ = memories;
        }

        let model_request = self.prepare_model_request(&input).await?;
        event_sink.emit(AgentEvent::ModelRequestPrepared).await;

        let response = self.provider.complete(model_request).await?;
        event_sink.emit(AgentEvent::ModelResponseCompleted).await;

        if let Some(tool_call) = response.tool_call {
            let tool = self
                .tools
                .get(&tool_call.name)
                .ok_or_else(|| AgentError::UnknownTool(tool_call.name.clone()))?;

            let permission = tool.required_permission();
            event_sink.emit(AgentEvent::PermissionRequested).await;

            let decision = self
                .permissions
                .decide(&permission, &permission_context)
                .await;

            match decision {
                PermissionDecision::Allow
                | PermissionDecision::AllowOnce
                | PermissionDecision::AllowForSession
                | PermissionDecision::Sandbox { .. } => {
                    event_sink.emit(AgentEvent::PermissionGranted).await;
                    event_sink.emit(AgentEvent::ToolCallStarted).await;

                    let ctx = ToolContext {
                        session_id: input.session_id,
                        agent_id: self.id,
                        cwd: input.cwd.clone(),
                        env: input.env.clone(),
                        permission_token: None,
                    };

                    let output = tool.invoke(tool_call.args, ctx).await?;
                    event_sink.emit(AgentEvent::ToolCallCompleted).await;
                    event_sink.emit(AgentEvent::TurnCompleted).await;

                    return Ok(AgentTurnOutput {
                        messages: vec![],
                        tool_output: Some(output),
                    });
                }
                _ => {
                    event_sink.emit(AgentEvent::PermissionDenied).await;
                    event_sink.emit(AgentEvent::ToolCallDenied).await;
                    event_sink.emit(AgentEvent::TurnCompleted).await;
                    return Err(AgentError::PermissionDenied(permission));
                }
            }
        }

        event_sink.emit(AgentEvent::TurnCompleted).await;
        Ok(AgentTurnOutput {
            messages: response.messages,
            tool_output: None,
        })
    }

    async fn prepare_model_request(
        &self,
        input: &AgentInput,
    ) -> Result<ModelRequest, AgentError> {
        Ok(ModelRequest {
            model: "default".into(),
            messages: vec![ModelMessage {
                role: Role::User,
                content: input.prompt.clone(),
            }],
            tools: self
                .tools
                .names()
                .into_iter()
                .map(|name| ModelToolSpec { name })
                .collect(),
        })
    }
}