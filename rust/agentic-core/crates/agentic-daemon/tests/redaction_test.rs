//! Source: agentic-native-stack.md
//! Context: QF.3 Example: Redaction
//! Extraction ID: CODE-092
//! Knowledge Links: KI-159
//! Status: scaffolded

#[test]
fn test_redact_github_token() {
    let input = "token: ghp_abcdefghijklmnopqrstuvwxyz0123456789";
    let output = redact_secrets(input);
    assert!(!output.contains("ghp_"));
    assert!(output.contains("[REDACTED"));
}