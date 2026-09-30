#!/usr/bin/env bash

set -e

# Define directories used during installation
APPLICATION_DIRECTORY="$HOME/.local/share/file-convertor"
EXTENSION_DIRECTORY="$HOME/.local/share/nautilus-python/extensions"

echo "Removing application files..."
if [ -d "$APPLICATION_DIRECTORY" ]; then
    rm -rf "$APPLICATION_DIRECTORY"
    echo "Removed $APPLICATION_DIRECTORY"
else
    echo "Application directory not found, skipping."
fi

echo "Removing Nautilus extension wrapper..."
if [ -f "$EXTENSION_DIRECTORY/extension.py" ]; then
    rm -f "$EXTENSION_DIRECTORY/extension.py"
    echo "Removed $EXTENSION_DIRECTORY/extension.py"
else
    echo "Nautilus extension file not found, skipping."
fi

# Restart Nautilus to unload the extension
if command -v nautilus &> /dev/null; then
    echo "Restarting Nautilus..."
    nautilus -q
fi

echo "Uninstallation complete!"