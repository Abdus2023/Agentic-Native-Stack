//! Source: agentic-native-stack.md
//! Context: QI.3 Protocol Fuzz Target
//! Extraction ID: CODE-100
//! Knowledge Links: KI-164
//! Status: scaffolded

#![no_main]
use libfuzzer_sys::fuzz_target;

fuzz_target!(|data: &[u8]| {
    let mut codec = agentic_tunnel::JsonFrameCodec::new(1024 * 1024);
    let mut buffer = bytes::BytesMut::from(data);

    loop {
        match tokio_util::codec::Decoder::decode(&mut codec, &mut buffer) {
            Ok(Some(_)) => continue,
            Ok(None) => break,
            Err(_) => break,
        }
    }
});