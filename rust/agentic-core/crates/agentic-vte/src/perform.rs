//! Source: agentic-native-stack.md
//! Context: 3.7 agentic-vte
//! Extraction ID: CODE-013
//! Knowledge Links: KI-014
//! Status: scaffolded

pub trait Perform {
    fn print(&mut self, c: char);
    fn execute(&mut self, byte: u8);
    fn hook(&mut self, params: &[i64], intermediates: &[u8], ignore: bool, action: char);
    fn put(&mut self, byte: u8);
    fn unhook(&mut self);
    fn osc_dispatch(&mut self, params: &[&[u8]], bell_terminated: bool);
    fn csi_dispatch(&mut self, params: &[i64], intermediates: &[u8], ignore: bool, action: char);
    fn esc_dispatch(&mut self, intermediates: &[u8], ignore: bool, byte: u8);
}