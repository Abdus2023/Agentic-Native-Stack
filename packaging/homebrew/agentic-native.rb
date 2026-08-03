# Source: agentic-native-stack.md
# Context: RR.4 Homebrew Formula
# Extraction ID: CODE-124
# Knowledge Links: KI-183
# Status: scaffolded

class AgenticNative < Formula
  desc "Agentic-native terminal stack"
  homepage "https://example.com/agentic-native"
  version "0.2.0"

  on_macos do
    if Hardware::CPU.arm?
      url "https://example.com/releases/agentic-0.2.0-aarch64-apple-darwin.tar.gz"
      sha256 "abcdef..."
    else
      url "https://example.com/releases/agentic-0.2.0-x86_64-apple-darwin.tar.gz"
      sha256 "abcdef..."
    end
  end

  def install
    bin.install "agentic"
    bin.install "agentic-daemon"
  end
end