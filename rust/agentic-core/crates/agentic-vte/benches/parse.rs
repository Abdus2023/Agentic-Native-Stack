//! Source: agentic-native-stack.md
//! Context: RH.2 Parse Throughput Benchmark
//! Extraction ID: CODE-118
//! Knowledge Links: KI-178
//! Status: scaffolded

#[bench]
fn bench_vte_parse_1mb(b: &mut Bencher) {
    let input = include_bytes!("../bench/data/ansi-1mb.bin");
    let mut terminal = ShadowTerminal::new(32, 120);

    b.iter(|| {
        terminal.advance(input);
    });
}