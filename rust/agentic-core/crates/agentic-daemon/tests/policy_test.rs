//! Source: agentic-native-stack.md
//! Context: PN.2 Example Policy Test
//! Extraction ID: CODE-090
//! Knowledge Links: KI-157
//! Status: scaffolded

#[test]
fn test_deny_metadata_endpoint() {
    let policy = compile_policy(test_policy()).unwrap();
    let request = PermissionRequest {
        action: "network_access".into(),
        resource: "host:169.254.169.254".into(),
        risk_level: RiskLevel::High,
        ..Default::default()
    };
    assert_eq!(policy.evaluate(&request), PolicyEffect::Deny);
}

#[test]
fn test_deny_overrides_allow() {
    let policy = compile_policy(policy_with_allow_and_deny()).unwrap();
    let request = PermissionRequest {
        action: "file_write".into(),
        resource: "path:/etc/psswd".into(),
        risk_level: RiskLevel::Critical,
        ..Default::default()
    };
    assert_eq!(policy.evaluate(&request), PolicyEffect::Deny);
}