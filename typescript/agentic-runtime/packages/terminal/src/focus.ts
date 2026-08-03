/**
 * Source: agentic-native-stack.md
 * Context: QS.3 Focus Management
 * Extraction ID: CODE-111
 * Knowledge Links: KI-171
 * Status: scaffolded
 */

export function trapFocus(container: HTMLElement) {
  const focusable = container.querySelectorAll<HTMLElement>(
    'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])',
  );
  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  container.addEventListener("keydown", (event) => {
    if (event.key !== "Tab") return;

    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  });

  first?.focus();
}