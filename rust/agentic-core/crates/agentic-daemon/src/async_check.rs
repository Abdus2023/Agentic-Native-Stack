//! Source: agentic-native-stack.md
//! Context: RF.4 Blocking Call Detection
//! Extraction ID: CODE-115
//! Knowledge Links: KI-175
//! Status: scaffolded

// Bad: blocking read inside async context.
// let content = std::fs::read_to_string(path)?;

// Good: spawn blocking for file I/O.
// let content = tokio::task::spawn_blocking(move || {
//     std::fs::read_to_string(path)
// })
// .await??;