#!/usr/bin/env bash

set -e

if command -v apt-get &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y python3-nautilus python3-pil
elif command -v dnf &> /dev/null; then
    sudo dnf install -y nautilus-python python3-pillow
elif command -v pacman &> /dev/null; then
    sudo pacman -S --noconfirm python-nautilus python-pillow
else
    echo "Unsupported package manager. Please manually install python3-nautilus and python3-pillow."
    exit 1
fi

EXTENSION_DIRECTORY="$HOME/.local/share/nautilus-python/extensions"
mkdir -p "$EXTENSION_DIRECTORY"

cp ./platform/linux/nautilus/extension.py "$EXTENSION_DIRECTORY/"
cp ./image_converter_gui.py "$EXTENSION_DIRECTORY/"
chmod +x "$EXTENSION_DIRECTORY/image_converter_gui.py"

nautilus -q

echo "Installation complete! Right-click any supported image in Nautilus to see the conversion option."