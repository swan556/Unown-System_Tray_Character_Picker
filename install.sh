#!/usr/bin/env bash

set -euo pipefail

APP_NAME="unown"

INSTALL_DIR="$HOME/.local/share/$APP_NAME"
BIN_DIR="$HOME/.local/bin"
DESKTOP_DIR="$HOME/.local/share/applications"
ICON_DIR="$HOME/.local/share/icons/hicolor/256x256/apps"

echo "Installing $APP_NAME..."

# Ensure we're in the repository root
cd "$(dirname "$0")"

# Check required commands
for cmd in python rsync; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        echo "Error: '$cmd' is not installed."
        exit 1
    fi
done

if [ ! -f requirements.txt ]; then
    echo "Error: requirements.txt not found."
    exit 1
fi

# Create directories
mkdir -p "$INSTALL_DIR"
mkdir -p "$BIN_DIR"
mkdir -p "$DESKTOP_DIR"
mkdir -p "$ICON_DIR"

echo "Copying project..."

rsync -a --delete \
    --exclude=".git" \
    --exclude=".github" \
    --exclude=".venv" \
    --exclude="__pycache__" \
    --exclude="*.pyc" \
    --exclude=".pytest_cache" \
    --exclude=".mypy_cache" \
    --exclude=".idea" \
    --exclude=".vscode" \
    --exclude="install.sh" \
    --exclude=".DS_Store" \
    ./ "$INSTALL_DIR/"

cd "$INSTALL_DIR"

# Create venv only once
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python -m venv .venv
fi

source .venv/bin/activate

python -m pip install --upgrade pip

# Install dependencies only if requirements changed
REQ_HASH_FILE=".requirements.sha256"
NEW_HASH=$(sha256sum requirements.txt | cut -d' ' -f1)

if [ ! -f "$REQ_HASH_FILE" ] || [ "$NEW_HASH" != "$(cat "$REQ_HASH_FILE")" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt
    echo "$NEW_HASH" > "$REQ_HASH_FILE"
else
    echo "Python dependencies already up to date."
fi

echo "Creating launcher..."

cat > "$BIN_DIR/unown" <<EOF
#!/usr/bin/env bash
source "$INSTALL_DIR/.venv/bin/activate"
exec python "$INSTALL_DIR/main.py" "\$@"
EOF

chmod +x "$BIN_DIR/unown"

echo "Installing desktop entry..."

cat > "$DESKTOP_DIR/unown.desktop" <<EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=Unown
Comment=Emoji and Kaomoji Picker
Exec=unown
Icon=unown
Terminal=false
Categories=Utility;
StartupNotify=true
EOF

if [ -f assets/icon.png ]; then
    echo "Installing icon..."
    cp assets/icon.png "$ICON_DIR/unown.png"
fi

# Optional Hyprland integration
HYPR_CONF="$HOME/.config/hypr/configs/Keybinds.conf"

if [ -f "$HYPR_CONF" ]; then
    echo
    read -rp "Add Super+Alt+E Hyprland keybind? [y/N] " ans

    if [[ "$ans" =~ ^[Yy]$ ]]; then
        if ! grep -q "exec, unown" "$HYPR_CONF"; then
            cat >> "$HYPR_CONF" <<EOF

# Unown
bind = SUPER ALT, E, exec, unown
EOF

            if command -v hyprctl >/dev/null 2>&1; then
                hyprctl reload >/dev/null
            fi

            echo "Hyprland keybind added."
        else
            echo "Hyprland keybind already exists."
        fi
    fi
fi

# PATH check
case ":$PATH:" in
    *":$HOME/.local/bin:"*) ;;
    *)
        echo
        echo "WARNING:"
        echo "~/.local/bin is not in your PATH."
        echo
        echo 'Add this line to ~/.bashrc or ~/.zshrc:'
        echo
        echo 'export PATH="$HOME/.local/bin:$PATH"'
        ;;
esac

echo
echo "======================================="
echo " Unown installed successfully!"
echo "======================================="
echo
echo "Launch it with:"
echo
echo "    unown"
echo
echo "You may now delete the cloned repository if you wish."