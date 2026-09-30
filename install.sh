#!/usr/bin/env bash

set -e

REPOSITORY_URL="https://github.com/your-username/your-repo.git"

# Bootstrap check: If running remotely via curl, clone and re-execute
if [ ! -d "./install" ] || [ ! -f "./image_converter_gui.py" ]; then
    echo "Running in remote bootstrap mode..."
    
    TEMPORARY_DIRECTORY=$(mktemp -d)
    trap 'rm -rf "$TEMPORARY_DIRECTORY"' EXIT

    echo "Cloning repository..."
    git clone --quiet "$REPOSITORY_URL" "$TEMPORARY_DIRECTORY"

    echo "Handing off..."
    cd "$TEMPORARY_DIRECTORY"
    exec bash ./install.sh "$@"
fi

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ACTION="${1:-install}"

# Handle Uninstallation
if [ "$ACTION" = "uninstall" ]; then
    echo "Running uninstallation..."
    UNINSTALL_SCRIPT="$ROOT_DIR/install/nautilus-uninstall.sh"
    
    if [ -f "$UNINSTALL_SCRIPT" ]; then
        bash "$UNINSTALL_SCRIPT"
        exit 0
    else
        echo "Error: Uninstallation script not found at $UNINSTALL_SCRIPT" >&2
        exit 1
    fi
fi

# Handle Installation
echo "Checking system environment and file managers..."

HAS_NAUTILUS=false
if command -v nautilus &> /dev/null; then
    HAS_NAUTILUS=true
elif [ -n "$XDG_CURRENT_DESKTOP" ] && echo "$XDG_CURRENT_DESKTOP" | grep -qi "gnome"; then
    HAS_NAUTILUS=true
fi

if [ "$HAS_NAUTILUS" = true ]; then
    echo "Nautilus file manager environment detected."
    INSTALL_SCRIPT="$ROOT_DIR/install/nautilus.sh"
    
    if [ -f "$INSTALL_SCRIPT" ]; then
        bash "$INSTALL_SCRIPT"
        exit 0
    else
        echo "Error: Missing installation script at: $INSTALL_SCRIPT" >&2
        exit 1
    fi
fi

echo "Error: No supported file manager environment (such as Nautilus) could be detected on this system." >&2
exit 1