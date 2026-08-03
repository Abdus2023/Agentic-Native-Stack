//! Source: agentic-native-stack.md
//! Context: 3.8 agentic-tunnel
//! Extraction ID: CODE-020
//! Knowledge Links: KI-021
//! Status: scaffolded

use bytes::{Buf, BufMut, BytesMut};
use tokio_util::codec::{Decoder, Encoder};

#[derive(Debug, Clone)]
pub struct LengthDelimitedJsonCodec {
    max_len: usize,
}

impl LengthDelimitedJsonCodec {
    pub fn new(max_len: usize) -> Self {
        Self { max_len }
    }
}

impl Decoder for LengthDelimitedJsonCodec {
    type Item = serde_json::Value;
    type Error = std::io::Error;

    fn decode(&mut self, src: &mut BytesMut) -> Result<Option<Self::Item>, Self::Error> {
        if src.len() < 4 {
            return Ok(None);
        }

        let mut len_bytes = [0u8; 4];
        len_bytes.copy_from_slice(&src[..4]);
        let len = u32::from_be_bytes(len_bytes) as usize;

        if len > self.max_len {
            return Err(std::io::Error::new(
                std::io::ErrorKind::InvalidData,
                "frame too large",
            ));
        }

        if src.len() < 4 + len {
            return Ok(None);
        }

        src.advance(4);
        let body = src.split_to(len);

        let value = serde_json::from_slice(&body)
            .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))?;

        Ok(Some(value))
    }
}

impl Encoder<serde_json::Value> for LengthDelimitedJsonCodec {
    type Error = std::io::Error;

    fn encode(
        &mut self,
        item: serde_json::Value,
        dst: &mut BytesMut,
    ) -> Result<(), Self::Error> {
        let body = serde_json::to_vec(&item)
            .map_err(|e| std::io::Error::new(std::io::ErrorKind::InvalidData, e))?;

        if body.len() > self.max_len {
            return Err(std::io::Error::new(
                std::io::ErrorKind::InvalidData,
                "frame too large",
            ));
        }

        dst.put_u32(body.len() as u32);
        dst.put_slice(&body);

        Ok(())
    }
}