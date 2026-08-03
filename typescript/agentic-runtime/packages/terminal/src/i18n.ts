/**
 * Source: agentic-native-stack.md
 * Context: RB.3 Message Resolver
 * Extraction ID: CODE-114
 * Knowledge Links: KI-174
 * Status: scaffolded
 */

export class MessageResolver {
  constructor(private messages: Record<string, string>) {}

  t(key: string, vars?: Record<string, string>): string {
    let message = this.messages[key] ?? key;
    if (vars) {
      for (const [name, value] of Object.entries(vars)) {
        message = message.replaceAll(`{${name}}`, value);
      }
    }
    return message;
  }
}