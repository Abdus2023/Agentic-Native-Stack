/**
 * Source: agentic-native-stack.md
 * Context: QH.2 Example: Browser Terminal
 * Extraction ID: CODE-097
 * Knowledge Links: KI-163
 * Status: scaffolded
 */

import { test, expect } from "@playwright/test";

test("terminal streams output", async ({ page }) => {
  await page.goto("http://127.0.0.1:8788/test-terminal");
  await page.click("[data-test=create-session]");

  const terminal = page.locator(".xterm");
  await expect(terminal).toBeVisible();

  await page.keyboard.type("echo integration-test");
  await page.keyboard.press("Enter");

  await expect(page.locator(".xterm-rows")).toContainText("integration-test");
});