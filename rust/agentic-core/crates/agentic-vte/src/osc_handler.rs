//! Source: agentic-native-stack.md
//! Context: G.6 Parser Interpretation
//! Extraction ID: CODE-081
//! Knowledge Links: KI-082
//! Status: scaffolded

impl ShadowTerminal {
    pub fn handle_osc(&mut self, params: &[&[u8]]) {
        let joined = params
            .iter()
            .map(|p| String::from_utf8_lossy(p).to_string())
            .collect::<Vec<_>>()
            .join(";");

        if let Some(command) = joined.strip_prefix("1337;AgenticCommandStart=") {
            self.events.push(VteEvent::CommandStart {
                command: command.to_string(),
            });
        }

        if let Some(code) = joined.strip_prefix("1337;AgenticCommandEnd=") {
            self.events.push(VteEvent::CommandEnd {
                exit_code: code.parse().ok(),
            });
        }
    }
}