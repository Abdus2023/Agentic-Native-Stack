//! Source: agentic-native-stack.md
//! Context: QG.3 Example: RPC Integration
//! Extraction ID: CODE-095
//! Knowledge Links: KI-162
//! Status: scaffolded

#[tokio::test]
async fn test_rpc_session_create() {
    let daemon = TestDaemon::start().await.unwrap();
    let response = daemon
        .rpc(JsonRpcRequest {
            id: 1.into(),
            method: "session.create".into(),
            params: Some(serde_json::json!({
                "kind": "mock"
            })),
        })
        .await;

    assert!(response.result.is_some());
    assert!(response.error.is_none());
}