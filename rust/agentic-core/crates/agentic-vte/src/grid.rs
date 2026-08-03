//! Source: agentic-native-stack.md
//! Context: 3.7 agentic-vte
//! Extraction ID: CODE-014
//! Knowledge Links: KI-015
//! Status: scaffolded

#[derive(Debug, Clone)]
pub struct Cell {
    pub c: char,
    pub attrs: CellAttrs,
}

#[derive(Debug, Clone, Copy, Default)]
pub struct CellAttrs {
    pub bold: bool,
    pub italic: bool,
    pub underline: bool,
    pub inverse: bool,
    pub faint: bool,
    pub fg: Color,
    pub bg: Color,
}

#[derive(Debug, Clone, Copy, Default)]
pub enum Color {
    #[default]
    Default,
    Index(u8),
    Rgb(u8, u8, u8),
}

#[derive(Debug, Clone)]
pub struct Grid {
    pub rows: usize,
    pub cols: usize,
    pub cells: Vec<Cell>,
    pub cursor_row: usize,
    pub cursor_col: usize,
    pub alternate_screen: bool,
}

impl Grid {
    pub fn new(rows: usize, cols: usize) -> Self {
        Self {
            rows,
            cols,
            cells: vec![
                Cell {
                    c: ' ',
                    attrs: CellAttrs::default()
                };
                rows * cols
            ],
            cursor_row: 0,
            cursor_col: 0,
            alternate_screen: false,
        }
    }

    pub fn put_char(&mut self, c: char) {
        if self.cursor_col >= self.cols {
            self.cursor_col = 0;
            self.cursor_row += 1;
        }

        if self.cursor_row >= self.rows {
            self.scroll_up(1);
            self.cursor_row = self.rows - 1;
        }

        let idx = self.cursor_row * self.cols + self.cursor_col;
        self.cells[idx].c = c;
        self.cursor_col += 1;
    }

    pub fn scroll_up(&mut self, n: usize) {
        let shift = n * self.cols;
        if shift >= self.cells.len() {
            self.cells.clear();
            self.cells.resize(
                self.rows * self.cols,
                Cell {
                    c: ' ',
                    attrs: CellAttrs::default(),
                },
            );
            return;
        }

        self.cells.rotate_left(shift);
        for cell in &mut self.cells[self.cells.len() - shift..] {
            *cell = Cell {
                c: ' ',
                attrs: CellAttrs::default(),
            };
        }
    }
}