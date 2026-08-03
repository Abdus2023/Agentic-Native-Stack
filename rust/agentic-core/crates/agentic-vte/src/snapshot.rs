//! Source: agentic-native-stack.md
//! Context: 3.7 agentic-vte
//! Extraction ID: CODE-017
//! Knowledge Links: KI-018
//! Status: scaffolded

#[derive(Debug, Clone, serde::Serialize)]
pub struct TerminalSnapshot {
    pub rows: usize,
    pub cols: usize,
    pub cursor_row: usize,
    pub cursor_col: usize,
    pub alternate_screen: bool,
    pub cells: Vec<Cell>,
}

impl TerminalSnapshot {
    pub fn to_xterm_payload(&self) -> serde_json::Value {
        serde_json::json!({
            "rows": self.rows,
            "cols": self.cols,
            "cursor": {
                "row": self.cursor_row,
                "col": self.cursor_col,
            },
            "alternateScreen": self.alternate_screen,
            "cells": self.cells.iter().map(|cell| {
                serde_json::json!({
                    "char": cell.c.to_string(),
                    "bold": cell.attrs.bold,
                    "italic": cell.attrs.italic,
                    "underline": cell.attrs.underline,
                    "inverse": cell.attrs.inverse,
                })
            }).collect::<Vec<_>>(),
        })
    }
}