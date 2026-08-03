//! Source: agentic-native-stack.md
//! Context: QY.2 Incomplete Sequence Handling
//! Extraction ID: CODE-113
//! Knowledge Links: KI-173
//! Status: scaffolded

pub fn safe_utf8_append(buffer: &mut Vec<u8>, input: &[u8]) -> String {
    buffer.extend_from_slice(input);
    match std::str::from_utf8(buffer) {
        Ok(text) => {
            let out = text.to_string();
            buffer.clear();
            out
        }
        Err(err) => {
            let valid_up_to = err.valid_up_to();
            let valid = String::from_utf8_lossy(&buffer[..valid_up_to]).to_string();
            let incomplete = buffer[valid_up_to..].to_vec();
            *buffer = incomplete;
            valid
        }
    }
}