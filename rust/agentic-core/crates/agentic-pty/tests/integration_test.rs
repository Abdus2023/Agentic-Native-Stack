//! Source: agentic-native-stack.md
//! Context: QG.2 Example: PTY Integration
//! Extraction ID: CODE-094
//! Knowledge Links: KI-161
//! Status: scaffolded

#[tokio::test]
async fn test_pty_echo() {
    let pty = UnixPtySystem;
    let pair = pty.openpty(Winsize::default()).unwrap();
    let mut writer = pair.master.try_clone_writer().unwrap();
    let mut reader = pair.master.try_clone_reader().unwrap();

    writer.write_all(b"echo hello
").unwrap();
    writer.flush().unwrap();

    let mut buf = vec![0u8; 4096];
    let n = reader.read(&mut buf).unwrap();

    assert!(n > 0);
}