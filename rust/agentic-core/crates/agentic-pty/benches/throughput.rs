//! Source: agentic-native-stack.md
//! Context: RH.1 Read Throughput Benchmark
//! Extraction ID: CODE-117
//! Knowledge Links: KI-177
//! Status: scaffolded

#[tokio::test]
async fn bench_pty_read_throughput() {
    let pty = UnixPtySystem;
    let pair = pty.openpty(Winsize::default()).unwrap();
    let writer = pair.master.try_clone_writer().unwrap();
    let reader = pair.master.try_clone_reader().unwrap();

    let data = vec![b'x'; 1024 * 1024];

    let start = std::time::Instant::now();

    let write_task = tokio::spawn(async move {
        let mut writer = writer;
        for _ in 0..100 {
            writer.write_all(&data).unwrap();
        }
    });

    let mut total = 0usize;
    let mut buf = vec![0u8; 1024 * 1024];
    let mut reader = reader;

    while total < 100 * 1024 * 1024 {
        let n = reader.read(&mut buf).unwrap();
        total += n;
    }

    write_task.await.unwrap();

    let elapsed = start.elapsed();
    let throughput = total as f64 / elapsed.as_secs_f64() / 1024.0 / 1024.0;

    println!("throughput: {:.2} MB/s", throughput);
    assert!(throughput > 50.0);
}