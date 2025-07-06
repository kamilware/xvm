#!/usr/bin/env bash

set -e

INSTALL_DIR="$HOME/.local/bin"
XVM_PATH="$INSTALL_DIR/xvm"

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

if [[ -f "$XVM_PATH" ]]; then
    echo "Removing $XVM_PATH..."
    rm "$XVM_PATH"
    echo "✅ xvm has been uninstalled from $XVM_PATH"
else
    echo "⚠️  xvm is not installed at $XVM_PATH"
fi

if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
    exit 0
fi

echo ""
echo "⚠️  $INSTALL_DIR might still be in your PATH via shell config."
echo "If you added it manually, consider removing it from your ~/.bashrc or ~/.zshrc:"
echo "    export PATH=\"\$PATH:$INSTALL_DIR\""
