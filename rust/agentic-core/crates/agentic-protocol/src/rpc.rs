//! v0.2.0 RPC envelopes and method contracts.
use serde::{Deserialize, Serialize};
use crate::{model::SessionId, PROTOCOL_VERSION};

pub mod methods { pub const INITIALIZE: &str = "initialize"; pub const SESSION_CREATE: &str = "session.create"; pub const SESSION_ATTACH: &str = "session.attach"; pub const SESSION_DETACH: &str = "session.detach"; pub const SESSION_LIST: &str = "session.list"; pub const SESSION_CLOSE: &str = "session.close"; pub const TERMINAL_INPUT: &str = "terminal.input"; pub const TERMINAL_RESIZE: &str = "terminal.resize"; }

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ErrorCode { Internal, ProtocolInvalid, VersionUnsupported, SessionNotFound, SessionLimitExceeded, SessionStateInvalid, PtySpawnFailed, PtyIoError, TerminalNotAttached }
impl ErrorCode { pub const fn as_str(&self) -> &'static str { match self { Self::Internal=>"internal.error", Self::ProtocolInvalid=>"protocol.invalid", Self::VersionUnsupported=>"protocol.version_unsupported", Self::SessionNotFound=>"session.not_found", Self::SessionLimitExceeded=>"session.limit_exceeded", Self::SessionStateInvalid=>"session.state_invalid", Self::PtySpawnFailed=>"pty.spawn_failed", Self::PtyIoError=>"pty.io_error", Self::TerminalNotAttached=>"terminal.not_attached" } } }

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RpcRequest { pub v: u32, pub id: String, pub method: String, #[serde(default, skip_serializing_if="Option::is_none")] pub params: Option<serde_json::Value> }
impl RpcRequest { pub fn validate_version(&self) -> Result<(), RpcError> { if self.v == PROTOCOL_VERSION { Ok(()) } else { Err(RpcError::version_unsupported(self.v)) } } }

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RpcResponse { pub v: u32, pub id: String, #[serde(default, skip_serializing_if="Option::is_none")] pub result: Option<serde_json::Value>, #[serde(default, skip_serializing_if="Option::is_none")] pub error: Option<RpcError> }
impl RpcResponse { pub fn success(id: impl Into<String>, result: serde_json::Value) -> Self { Self { v: PROTOCOL_VERSION, id:id.into(), result:Some(result), error:None } } pub fn error(id: impl Into<String>, error: RpcError) -> Self { Self { v:PROTOCOL_VERSION, id:id.into(), result:None, error:Some(error) } } }

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct RpcError { pub code: String, pub message: String, #[serde(default, skip_serializing_if="Option::is_none")] pub retryable: Option<bool>, #[serde(default, skip_serializing_if="Option::is_none")] pub details: Option<serde_json::Value> }
impl RpcError { pub fn new(code: impl Into<String>, message: impl Into<String>) -> Self { Self { code:code.into(), message:message.into(), retryable:None, details:None } } pub fn version_unsupported(v:u32)->Self { Self { code:ErrorCode::VersionUnsupported.as_str().into(), message:format!("unsupported protocol version: {v}"), retryable:Some(false), details:None } } pub fn invalid(m:impl Into<String>)->Self { Self::new(ErrorCode::ProtocolInvalid.as_str(),m) } pub fn session_not_found(id:&SessionId)->Self { Self::new(ErrorCode::SessionNotFound.as_str(),format!("session not found: {id}")) } }

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct EventNotification { pub v:u32, pub method:String, pub params:EventNotificationParams }
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all="camelCase")]
pub struct EventNotificationParams { pub event_type:String, pub payload:serde_json::Value }
impl EventNotification { pub fn new(event_type:impl Into<String>, payload:serde_json::Value)->Self { Self { v:PROTOCOL_VERSION, method:"event".into(), params:EventNotificationParams { event_type:event_type.into(), payload } } } }

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all="camelCase")]
pub struct InitializeParams { pub client_info:ClientInfo, pub protocol_version:u32 }
#[derive(Debug, Clone, Serialize, Deserialize)] pub struct ClientInfo { pub name:String, pub version:String }
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all="camelCase")]
pub struct InitializeResult { pub protocol_version:u32, pub daemon_version:String, pub capabilities:Vec<String> }

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all="snake_case")]
pub enum SessionKind { LocalPty, Mock }
#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(rename_all="camelCase")]
pub struct SessionCreateParams { pub kind:SessionKind, pub shell:Option<String>, #[serde(default="default_rows")] pub rows:u16, #[serde(default="default_cols")] pub cols:u16 }
fn default_rows()->u16 { 24 } fn default_cols()->u16 { 80 }
#[derive(Debug, Clone, Serialize, Deserialize)] #[serde(rename_all="camelCase")] pub struct SessionCreateResult { pub session_id:SessionId }
#[derive(Debug, Clone, Serialize, Deserialize)] #[serde(rename_all="camelCase")] pub struct SessionRefParams { pub session_id:SessionId }
#[derive(Debug, Clone, Serialize, Deserialize)] pub struct SessionAttachResult { pub attached:bool }
#[derive(Debug, Clone, Serialize, Deserialize)] pub struct SessionDetachResult { pub detached:bool }
#[derive(Debug, Clone, Serialize, Deserialize)] pub struct SessionCloseResult { pub closed:bool }
#[derive(Debug, Clone, Serialize, Deserialize)] #[serde(rename_all="camelCase")] pub struct TerminalInputParams { pub session_id:SessionId, pub data:String }
#[derive(Debug, Clone, Serialize, Deserialize)] pub struct TerminalInputResult { pub accepted:bool }
#[derive(Debug, Clone, Serialize, Deserialize)] #[serde(rename_all="camelCase")] pub struct TerminalResizeParams { pub session_id:SessionId, pub rows:u16, pub cols:u16 }
#[derive(Debug, Clone, Serialize, Deserialize)] pub struct TerminalResizeResult { pub resized:bool }
