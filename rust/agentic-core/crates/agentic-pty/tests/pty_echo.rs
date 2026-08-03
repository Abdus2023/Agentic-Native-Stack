//! Source: agentic-native-stack.md
//! Context: C.2 PTY Test Example
//! Extraction ID: CODE-069
//! Knowledge Links: KI-070
//! Status: scaffolded

#[tokio::test]
async fn test_local_pty_echo() {
    let pty_system = UnixPtySystem;
    let pair = pty_system.openpty(Winsize::default()).unwrap();
    let mut writer = pair.master.try_clone_writer().unwrap();
    let mut reader = pair.master.try_clone_reader().unwrap();

    writer.write_all(b"echo hello
").unwrap();
    writer.flush().unwrap();

    let mut buf = vec![0u8; 4096];
    let n = reader.read(&mut buf).unwrap();

    assert!(n > 0);
}