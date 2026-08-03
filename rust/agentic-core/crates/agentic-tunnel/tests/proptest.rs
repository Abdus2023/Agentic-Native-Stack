//! Source: agentic-native-stack.md
//! Context: QJ.3 Example: Protocol Round-Trip
//! Extraction ID: CODE-102
//! Knowledge Links: KI-165
//! Status: scaffolded

proptest! {
    #[test]
    fn frame_round_trip(value in any_json_value()) {
        let mut codec = JsonFrameCodec::new(1024 * 1024);
        let mut buffer = BytesMut::new();

        codec.encode(value.clone(), &mut buffer).unwrap();
        let decoded = codec.decode(&mut buffer).unwrap().unwrap();

        prop_assert_eq!(value, decoded);
    }
}