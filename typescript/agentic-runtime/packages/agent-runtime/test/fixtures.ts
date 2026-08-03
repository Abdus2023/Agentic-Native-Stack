/**
 * Source: agentic-native-stack.md
 * Context: QN.2 Mock Provider Fixture
 * Extraction ID: CODE-106
 * Knowledge Links: KI-168
 * Status: scaffolded
 */

export class MockProvider implements Provider {
  private index = 0;

  constructor(private responses: ModelResponse[]) {}

  async complete(_request: ModelRequest): Promise<ModelResponse> {
    const response = this.responses[this.index % this.responses.length];
    this.index += 1;
    return response;
  }
}