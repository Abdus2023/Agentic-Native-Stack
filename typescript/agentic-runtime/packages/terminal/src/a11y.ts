/**
 * Source: agentic-native-stack.md
 * Context: QR.4 Announcement Service
 * Extraction ID: CODE-110
 * Knowledge Links: KI-170
 * Status: scaffolded
 */

export class AnnouncementService {
  private politeRegion: HTMLElement;
  private assertiveRegion: HTMLElement;

  constructor() {
    this.politeRegion = document.getElementById("agent-status")!;
    this.assertiveRegion = document.getElementById("permission-alert")!;
  }

  announcePolite(message: string) {
    this.politeRegion.textContent = message;
  }

  announceAssertive(message: string) {
    this.assertiveRegion.textContent = message;
  }
}