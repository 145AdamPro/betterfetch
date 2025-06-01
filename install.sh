#!/bin/bash

echo "🚀 Starting BetterFetch Installer"

ASCII_DIR="ascii"
CONFIG_FILE="bfetch_config.txt"

# List available logos
echo "📁 Available ASCII logos:"
ls $ASCII_DIR/*.txt 2>/dev/null | xargs -n1 basename

# Ask for user input
read -p "🎨 Enter the name of the logo file (e.g., macos.txt): " logo

# Check if logo file exists
if [ -f "$ASCII_DIR/$logo" ]; then
    echo "$logo" > "$CONFIG_FILE"
    echo "✅ Logo set to $logo"
else
    echo "⚠️ Logo not found, default will be used."
    echo "$(uname | tr '[:upper:]' '[:lower:]').txt" > "$CONFIG_FILE"
fi

# Install Python dependencies
if command -v pip3 &>/dev/null; then
    pip3 install -r requirements.txt
    echo "✅ Python dependencies installed."
else
    echo "❌ pip3 not found. Please install Python3 and pip."
    exit 1
fi

# Make bfetch.py executable
chmod +x bfetch.py
echo "✅ Setup complete. You can now run it using: ./bfetch.py or python3 bfetch.py"
