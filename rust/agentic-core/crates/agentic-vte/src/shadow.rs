//! Source: agentic-native-stack.md
//! Context: 3.7 agentic-vte
//! Extraction ID: CODE-015
//! Knowledge Links: KI-016
//! Status: scaffolded

pub struct ShadowTerminal {
    grid: Grid,
    parser: Parser,
    events: Vec<VteEvent>,
}

impl ShadowTerminal {
    pub fn new(rows: usize, cols: usize) -> Self {
        Self {
            grid: Grid::new(rows, cols),
            parser: Parser::new(),
            events: Vec::new(),
        }
    }

    pub fn advance(&mut self, bytes: &[u8]) -> Vec<VteEvent> {
        self.events.clear();
        for byte in bytes {
            self.parser.advance(*byte, &mut self.grid);
        }
        std::mem::take(&mut self.events)
    }

    pub fn snapshot(&self) -> TerminalSnapshot {
        TerminalSnapshot {
            rows: self.grid.rows,
            cols: self.grid.cols,
            cursor_row: self.grid.cursor_row,
            cursor_col: self.grid.cursor_col,
            alternate_screen: self.grid.alternate_screen,
            cells: self.grid.cells.clone(),
        }
    }
}