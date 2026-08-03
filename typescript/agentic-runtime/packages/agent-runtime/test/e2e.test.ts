/**
 * Source: agentic-native-stack.md
 * Context: QH.3 Example: Agent Task
 * Extraction ID: CODE-098
 * Knowledge Links: KI-163
 * Status: scaffolded
 */

test("agent runs command and reports result", async ({ request }) => {
  const response = await request.post("/agents/tasks", {
    data: {
      prompt: "Run echo hello and report the output",
    },
  });

  expect(response.ok()).toBeTruthy();
  const { taskId } = await response.json();

  await waitForTaskCompletion(taskId);
  const result = await getTaskResult(taskId);

  expect(result.output).toContain("hello");
});