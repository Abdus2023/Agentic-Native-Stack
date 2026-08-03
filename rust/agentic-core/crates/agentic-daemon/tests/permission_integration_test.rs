//! Source: agentic-native-stack.md
//! Context: QG.4 Example: Permission Integration
//! Extraction ID: CODE-096
//! Knowledge Links: KI-162
//! Status: scaffolded

#[tokio::test]
async fn test_high_risk_command_requires_permission() {
    let daemon = TestDaemon::with_policy(deny_all_policy()).await.unwrap();
    let result = daemon
        .run_agent_task("run rm -rf /tmp/test")
        .await;

    assert!(matches!(
        result.unwrap_err(),
        DaemonError::PermissionDenied(_)
    ));
}