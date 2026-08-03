//! Source: agentic-native-stack.md
//! Context: 3.5 agentic-pty
//! Extraction ID: CODE-005
//! Knowledge Links: KI-006
//! Status: scaffolded

use tokio::io::unix::AsyncFd;
use tokio::io::Interest;

pub async fn drain_master(
    master_fd: std::os::fd::RawFd,
    mut emit: impl FnMut(&[u8]),
) -> io::Result<()> {
    let async_fd = AsyncFd::with_interest(master_fd, Interest::READABLE)?;
    let mut buf = vec![0u8; READ_BUFFER_SIZE];

    loop {
        let mut guard = async_fd.readable().await?;

        match guard.try_io(|inner| {
            let fd = inner.get_ref();
            unsafe {
                libc::read(
                    *fd,
                    buf.as_mut_ptr() as *mut libc::c_void,
                    buf.len(),
                )
            }
        }) {
            Ok(result) => {
                let n = result?;
                if n == 0 {
                    return Ok(());
                }
                emit(&buf[..n as usize]);
            }
            Err(_would_block) => continue,
        }
    }
}