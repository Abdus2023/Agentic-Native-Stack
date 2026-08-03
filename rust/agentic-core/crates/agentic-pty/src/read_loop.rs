//! Source: agentic-native-stack.md
//! Context: RL.2 Example: Buffer Reuse
//! Extraction ID: CODE-120
//! Knowledge Links: KI-180
//! Status: scaffolded

pub struct ReadLoop {
    buf: Vec<u8>,
}

impl ReadLoop {
    pub fn new() -> Self {
        Self {
            buf: vec![0u8; 1024 * 1024],
        }
    }

    pub fn read_into(&mut self, fd: RawFd) -> io::Result<&[u8]> {
        let n = unsafe {
            libc::read(fd, self.buf.as_mut_ptr() as *mut _, self.buf.len())
        };

        if n < 0 {
            return Err(io::Error::last_os_error());
        }

        Ok(&self.buf[..n as usize])
    }
}