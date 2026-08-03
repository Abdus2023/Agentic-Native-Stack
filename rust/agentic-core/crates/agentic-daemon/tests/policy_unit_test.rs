//! Source: agentic-native-stack.md
//! Context: QF.2 Example: Policy Evaluation
//! Extraction ID: CODE-091
//! Knowledge Links: KI-158
//! Status: scaffolded

#[test]
fn test_deny_overrides_allow() {
    let policy = compile_policy(test_policy()).unwrap();
    let request = PermissionRequest {
        action: "file_write".into(),
        resource: "path:/etc/passwd".into(),
        risk_level: RiskLevel::Critical,
        ..Default::default()
    };
    assert_eq!(policy.evaluate(&request), PolicyEffect::Deny);
}