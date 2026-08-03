//! Source: agentic-native-stack.md
//! Context: 3.7 agentic-vte
//! Extraction ID: CODE-016
//! Knowledge Links: KI-017
//! Status: scaffolded

#[derive(Debug, Clone)]
pub enum VteEvent {
    Print(char),
    LineFeed,
    CarriageReturn,
    Backspace,
    Tab,
    Bell,
    CursorMove {
        row: usize,
        col: usize,
    },
    ClearScreen,
    ClearLine,
    AlternateScreenEnter,
    AlternateScreenLeave,
    Osc {
        params: Vec<String>,
    },
    TitleChanged(String),
    Hyperlink {
        uri: String,
        id: Option<String>,
    },
    PromptMarker,
    CommandStart {
        command: String,
    },
    CommandEnd {
        exit_code: Option<i32>,
    },
}