//! Source: agentic-native-stack.md
//! Context: QJ.2 Example: Parser Invariant
//! Extraction ID: CODE-101
//! Knowledge Links: KI-165
//! Status: scaffolded

use proptest::prelude::*;

proptest! {
    #[test]
    fn parser_never_panics(input in proptest::collection::vec(any::<u8>(), 0..4096)) {
        let mut terminal = agentic_vte::ShadowTerminal::new(24, 80);
        let _ = terminal.advance(&input);
    }
}