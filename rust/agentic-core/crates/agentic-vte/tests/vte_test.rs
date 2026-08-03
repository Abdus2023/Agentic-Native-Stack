//! Source: agentic-native-stack.md
//! Context: C.3 VTE Test Example
//! Extraction ID: CODE-070
//! Knowledge Links: KI-071
//! Status: scaffolded

#[test]
fn test_shadow_terminal_prints_text() {
    let mut term = ShadowTerminal::new(24, 80);
    let events = term.advance(b"hello");

    assert!(events.iter().any(|event| matches!(
        event,
        VteEvent::Print('h')
    )));
}