//! Source: agentic-native-stack.md
//! Context: 3.10 agentic-agent-core
//! Extraction ID: CODE-033
//! Knowledge Links: KI-034
//! Status: scaffolded

#[async_trait]
pub trait Hook: Send + Sync {
    async fn before_tool_call(
        &self,
        tool_name: &str,
        args: &Value,
    ) -> Result<(), HookError> {
        let _ = (tool_name, args);
        Ok(())
    }

    async fn after_tool_call(
        &self,
        tool_name: &str,
        output: &ToolOutput,
    ) -> Result<(), HookError> {
        let _ = (tool_name, output);
        Ok(())
    }

    async fn before_model_request(
        &self,
        request: &mut ModelRequest,
    ) -> Result<(), HookError> {
        let _ = request;
        Ok(())
    }

    async fn after_model_response(
        &self,
        response: &ModelResponse,
    ) -> Result<(), HookError> {
        let _ = response;
        Ok(())
    }
}