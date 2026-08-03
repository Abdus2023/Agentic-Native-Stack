//! Authoritative v0.2.0 wire and domain contract.
//!
//! This crate owns serialization and validation types only. It does not own
//! transport, authorization, execution, session authority, or persistence.

pub mod model;
pub mod rpc;

// Legacy modules remain exported while dependent scaffold crates migrate to the
// v0.2.0 model. They are compatibility-only and are not the wire contract.
#[doc(hidden)]
pub mod error;
#[doc(hidden)]
pub mod ids;
#[doc(hidden)]
pub mod messages;

pub use model::*;
pub use rpc::*;

pub const PROTOCOL_VERSION: u32 = 1;
pub const MAX_FRAME_SIZE: usize = 16 * 1024 * 1024;
