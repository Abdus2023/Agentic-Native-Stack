//! Source: agentic-native-stack.md
//! Context: QI.2 VTE Fuzz Target
//! Extraction ID: CODE-099
//! Knowledge Links: KI-164
//! Status: scaffolded

#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    let mut terminal = agentic_vte::ShadowTerminal::new(32, 120);
    let _ = terminal.advance(data);
});