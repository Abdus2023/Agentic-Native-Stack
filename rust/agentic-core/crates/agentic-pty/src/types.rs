//! Source: agentic-native-stack.md
//! Context: 3.5 agentic-pty
//! Extraction ID: CODE-001
//! Knowledge Links: KI-001, KI-002
//! Status: scaffolded

use std::ffi::OsString;
use std::io;
use std::time::Duration;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct Winsize {
    pub rows: u16,
    pub cols: u16,
    pub pixel_width: u16,
    pub pixel_height: u16,
}

impl Default for Winsize {
    fn default() -> Self {
        Self {
            rows: 24,
            cols: 80,
            pixel_width: 0,
            pixel_height: 0,
        }
    }
}

#[derive(Debug, Clone)]
pub struct CommandSpec {
    pub program: OsString,
    pub args: Vec<OsString>,
    pub cwd: Option<OsString>,
    pub env: Vec<(OsString, OsString)>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PtyKind {
    Local,
    SshRemote,
    Container,
    Mock,
}

pub trait PtySystem: Send + Sync {
    fn openpty(&self, size: Winsize) -> io::Result<PtyPair>;
    fn kind(&self) -> PtyKind;
}

pub struct PtyPair {
    pub master: Box<dyn MasterPort>,
    pub slave: Box<dyn SlavePort>,
}

pub trait MasterPort: Send {
    fn resize(&mut self, size: Winsize) -> io::Result<()>;
    fn try_clone_reader(&self) -> io::Result<Box<dyn PtyReader>>;
    fn try_clone_writer(&self) -> io::Result<Box<dyn PtyWriter>>;
    fn raw_fd(&self) -> Option<std::os::fd::RawFd>;
}

pub trait SlavePort: Send {
    fn as_command_stdio(&self) -> io::Result<SlaveStdio>;
    fn raw_fd(&self) -> Option<std::os::fd::RawFd>;
}

pub trait PtyReader: Send {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize>;
}

pub trait PtyWriter: Send {
    fn write_all(&mut self, buf: &[u8]) -> io::Result<()>;
    fn flush(&mut self) -> io::Result<()>;
}

pub struct SlaveStdio {
    pub stdin: std::process::Stdio,
    pub stdout: std::process::Stdio,
    pub stderr: std::process::Stdio,
}