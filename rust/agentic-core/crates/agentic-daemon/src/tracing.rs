//! Source: agentic-native-stack.md
//! Context: E.3 Rust Tracing Example
//! Extraction ID: CODE-075
//! Knowledge Links: KI-076
//! Status: scaffolded

use tracing::{info_span, instrument, Instrument};

#[instrument(skip_all, fields(session_id = %session_id))]
pub async fn run_command(session_id: &str, command: &str) -> Result<(), AgentError> {
    let span = info_span!("command", command = %command);

    async {
        // Command execution would occur here.
        Ok(())
    }
    .instrument(span)
    .await
}