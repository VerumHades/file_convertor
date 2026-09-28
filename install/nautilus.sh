#!/usr/bin/env bash

set -e

if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y python3-nautilus python3-pil python3-tk
elif command -v dnf &> /dev/null; then
    sudo dnf install -y nautilus-python python3-pillow python3-tk
elif command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm python-nautilus python-pillow python3-tk
else
    echo "Unsupported package manager. Please manually install python3-nautilus and python3-pillow."
    exit 1
fi

# Define directories
APPLICATION_DIRECTORY="$HOME/.local/share/file-convertor"
EXTENSION_DIRECTORY="$HOME/.local/share/nautilus-python/extensions"

# Create directories
mkdir -p "$APPLICATION_DIRECTORY"
mkdir -p "$EXTENSION_DIRECTORY"

# Copy the GUI application script to the shared application directory
cp ./image_converter_gui.py "$APPLICATION_DIRECTORY/"
chmod +x "$APPLICATION_DIRECTORY/image_converter_gui.py"

# Copy ONLY the Nautilus extension wrapper to the extensions directory
cp ./platform/linux/nautilus/extension.py "$EXTENSION_DIRECTORY/"

# Restart Nautilus to load the extension
nautilus -q

echo "Installation complete! Right-click any supported image in Nautilus to see the conversion option."