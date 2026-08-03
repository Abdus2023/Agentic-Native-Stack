//! Source: agentic-native-stack.md
//! Context: QO.1 Daemon Test Harness
//! Extraction ID: CODE-108
//! Knowledge Links: KI-169
//! Status: scaffolded

pub struct TestDaemon {
    handle: DaemonHandle,
    client: IpcClient,
}

impl TestDaemon {
    pub async fn start() -> Result<Self, TestError> {
        let config = test_config();
        let handle = start_daemon(config).await?;
        let client = IpcClient::connect(&handle.ipc_path).await?;
        Ok(Self { handle, client })
    }

    pub async fn rpc(&self, request: JsonRpcRequest) -> JsonRpcResponse {
        self.client.request(request).await.unwrap()
    }

    pub async fn shutdown(self) {
        self.handle.shutdown().await;
    }
}