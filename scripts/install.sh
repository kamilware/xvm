#!/usr/bin/env bash

set -e

REPO="kamilware/xvm"
INSTALL_DIR="$HOME/.local/bin"

echo "🧹 Running uninstall script..."
curl -fsSL https://raw.githubusercontent.com/kamilware/xvm/master/scripts/uninstall.sh | bash

echo "🗑 Removing autoupdate jobs..."

OS=$(uname -s | tr '[:upper:]' '[:lower:]')
ARCH=$(uname -m)

case "$ARCH" in
    x86_64|amd64) ARCH="x64" ;;
    arm64|aarch64) ARCH="arm64" ;;
    *) echo "Unsupported architecture: $ARCH"; exit 1 ;;
esac

if [[ "$OS" == "linux" ]]; then
    systemctl --user disable --now xvm-go-autoupdate.service || true
    systemctl --user disable --now xvm-node-autoupdate.service || true
elif [[ "$OS" == "darwin" ]]; then
    launchctl unload ~/Library/LaunchAgents/xvm.go.autoupdate.plist 2>/dev/null || true
    launchctl unload ~/Library/LaunchAgents/xvm.node.autoupdate.plist 2>/dev/null || true
    rm -f ~/Library/LaunchAgents/xvm.{go,node}.autoupdate.plist
fi

VERSION=$(curl -s https://api.github.com/repos/$REPO/releases/latest | grep -Po '"tag_name": "\K.*?(?=")')
if [[ -z "$VERSION" ]]; then
    echo "❌ Failed to resolve latest release from GitHub"
    exit 1
fi

FILENAME="xvm-${OS}-${ARCH}"
URL="https://github.com/${REPO}/releases/download/${VERSION}/${FILENAME}"

echo "⬇️  Downloading $FILENAME from $VERSION..."
curl -L "$URL" -o "$FILENAME"
chmod +x "$FILENAME"

echo "📦 Installing to $INSTALL_DIR..."
mkdir -p "$INSTALL_DIR"
mv "$FILENAME" "$INSTALL_DIR/xvm"

echo "✅ xvm installed to $INSTALL_DIR/xvm"

if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    echo "⚠️  $INSTALL_DIR is not in your PATH"
    echo "👉 Add this to your shell config (e.g., ~/.bashrc or ~/.zshrc):"
    echo "export PATH=\"\$PATH:$INSTALL_DIR\""
fi

echo "🚀 Run 'xvm --help' to get started."
