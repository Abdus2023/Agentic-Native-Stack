//! Source: agentic-native-stack.md
//! Context: 3.5 agentic-pty
//! Extraction ID: CODE-003
//! Knowledge Links: KI-004
//! Status: scaffolded

use nix::fcntl::{open, OFlag};
use nix::pty::{openpty, Winsize as NixWinsize};
use nix::sys::stat::Mode;
use nix::unistd::{fork, ForkResult};
use std::os::fd::{AsRawFd, FromRawFd, OwnedFd};

pub struct UnixPtySystem;

impl PtySystem for UnixPtySystem {
    fn openpty(&self, size: Winsize) -> io::Result<PtyPair> {
        let ws = NixWinsize {
            ws_row: size.rows,
            ws_col: size.cols,
            ws_xpixel: size.pixel_width,
            ws_ypixel: size.pixel_height,
        };

        let pty = openpty(Some(&ws), None)
            .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;

        let master = UnixMasterPort {
            fd: pty.master,
        };

        let slave = UnixSlavePort {
            fd: pty.slave,
        };

        Ok(PtyPair {
            master: Box::new(master),
            slave: Box::new(slave),
        })
    }

    fn kind(&self) -> PtyKind {
        PtyKind::Local
    }
}

struct UnixMasterPort {
    fd: OwnedFd,
}

impl MasterPort for UnixMasterPort {
    fn resize(&mut self, size: Winsize) -> io::Result<()> {
        let ws = libc::winsize {
            ws_row: size.rows,
            ws_col: size.cols,
            ws_xpixel: size.pixel_width,
            ws_ypixel: size.pixel_height,
        };

        let ret = unsafe {
            libc::ioctl(self.fd.as_raw_fd(), libc::TIOCSWINSZ, &ws)
        };

        if ret == -1 {
            Err(io::Error::last_os_error())
        } else {
            Ok(())
        }
    }

    fn try_clone_reader(&self) -> io::Result<Box<dyn PtyReader>> {
        let fd = nix::unistd::dup(self.fd.as_raw_fd())
            .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;

        Ok(Box::new(UnixPtyReader {
            fd: unsafe { OwnedFd::from_raw_fd(fd) },
        }))
    }

    fn try_clone_writer(&self) -> io::Result<Box<dyn PtyWriter>> {
        let fd = nix::unistd::dup(self.fd.as_raw_fd())
            .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;

        Ok(Box::new(UnixPtyWriter {
            fd: unsafe { OwnedFd::from_raw_fd(fd) },
        }))
    }

    fn raw_fd(&self) -> Option<std::os::fd::RawFd> {
        Some(self.fd.as_raw_fd())
    }
}

struct UnixSlavePort {
    fd: OwnedFd,
}

impl SlavePort for UnixSlavePort {
    fn as_command_stdio(&self) -> io::Result<SlaveStdio> {
        let stdin = std::process::Stdio::from(unsafe {
            std::fs::File::from_raw_fd(nix::unistd::dup(self.fd.as_raw_fd())
                .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?)
        });
        let stdout = std::process::Stdio::from(unsafe {
            std::fs::File::from_raw_fd(nix::unistd::dup(self.fd.as_raw_fd())
                .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?)
        });
        let stderr = std::process::Stdio::from(unsafe {
            std::fs::File::from_raw_fd(nix::unistd::dup(self.fd.as_raw_fd())
                .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?)
        });

        Ok(SlaveStdio {
            stdin,
            stdout,
            stderr,
        })
    }

    fn raw_fd(&self) -> Option<std::os::fd::RawFd> {
        Some(self.fd.as_raw_fd())
    }
}

struct UnixPtyReader {
    fd: OwnedFd,
}

impl PtyReader for UnixPtyReader {
    fn read(&mut self, buf: &mut [u8]) -> io::Result<usize> {
        let n = nix::unistd::read(self.fd.as_raw_fd(), buf)
            .map_err(|e| io::Error::new(io::ErrorKind::Other, e))?;
        Ok(n)
    }
}

struct UnixPtyWriter {
    fd: OwnedFd,
}

impl PtyWriter for UnixPtyWriter {
    fn write_all(&mut self, mut buf: &[u8]) -> io::Result<()> {
        while !buf.is_empty() {
            match nix::unistd::write(self.fd.as_raw_fd(), buf) {
                Ok(0) => {
                    return Err(io::Error::new(
                        io::ErrorKind::WriteZero,
                        "zero-length write",
                    ))
                }
                Ok(n) => buf = &buf[n..],
                Err(nix::errno::Errno::EINTR) => continue,
                Err(e) => return Err(io::Error::new(io::ErrorKind::Other, e)),
            }
        }
        Ok(())
    }

    fn flush(&mut self) -> io::Result<()> {
        Ok(())
    }
}