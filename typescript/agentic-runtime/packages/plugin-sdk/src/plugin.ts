/**
 * Source: agentic-native-stack.md
 * Context: 4.9 @agentic/plugin-sdk
 * Extraction ID: CODE-062
 * Knowledge Links: KI-063
 * Status: scaffolded
 */

export interface Plugin {
  name: string;
  version: string;
  register(api: PluginAPI): void | Promise<void>;
}

export interface PluginAPI {
  registerTool(tool: ToolDefinition): void;
  registerPermissionPolicy(policy: PermissionPolicy): void;
  registerEventHandler(handler: EventHandler): void;
  registerTerminalDecorator(decorator: TerminalDecorator): void;
  registerMemorySource(source: MemorySource): void;
}