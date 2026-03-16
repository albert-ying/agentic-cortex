#!/usr/bin/env bash
set -euo pipefail

# ─── Cross-platform sed -i ────────────────────────────────────────────────────
# macOS sed requires -i '', GNU sed requires -i without arg.
# We detect once and define a helper used throughout.
if sed --version 2>/dev/null | grep -q 'GNU'; then
    sedi() { sed -i "$@"; }
else
    sedi() { sed -i '' "$@"; }
fi

# ─── Dependency checks ────────────────────────────────────────────────────────
check_dep() {
    if ! command -v "$1" &>/dev/null; then
        echo "Error: '$1' is required but not installed."
        exit 1
    fi
}
check_dep git
check_dep python3

# ─── Banner ───────────────────────────────────────────────────────────────────
echo ""
echo "╔══════════════════════════════════════════╗"
echo "║   Agentic Cortex — Personal AI OS Setup  ║"
echo "╚══════════════════════════════════════════╝"
echo ""

# ─── Locate the repo ─────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Verify seed-vault exists (sanity check that we're in the right repo)
if [[ ! -d "$SCRIPT_DIR/seed-vault" ]]; then
    echo "Error: seed-vault/ not found in $SCRIPT_DIR"
    echo "Make sure you're running setup.sh from the agentic-cortex repo root."
    exit 1
fi

# ─── Gather user input ───────────────────────────────────────────────────────
read -rp "Vault location [~/agentic-cortex-vault]: " VAULT_PATH
VAULT_PATH="${VAULT_PATH:-$HOME/agentic-cortex-vault}"
VAULT_PATH="${VAULT_PATH/#\~/$HOME}"
# Resolve to absolute path
VAULT_PATH="$(cd "$(dirname "$VAULT_PATH")" 2>/dev/null && pwd)/$(basename "$VAULT_PATH")" || VAULT_PATH="$VAULT_PATH"

read -rp "Your name: " USER_NAME
read -rp "Your email: " USER_EMAIL

if [[ -z "$USER_NAME" || -z "$USER_EMAIL" ]]; then
    echo "Error: Name and email are required."
    exit 1
fi

# Escape special characters for sed replacement
escape_sed() { printf '%s\n' "$1" | sed 's/[&/\]/\\&/g'; }
USER_NAME_ESC="$(escape_sed "$USER_NAME")"
USER_EMAIL_ESC="$(escape_sed "$USER_EMAIL")"

# ─── Handle existing vault ───────────────────────────────────────────────────
if [[ -d "$VAULT_PATH" ]] && [[ "$(ls -A "$VAULT_PATH" 2>/dev/null)" ]]; then
    echo ""
    echo "Warning: $VAULT_PATH already exists and is not empty."
    read -rp "Overwrite contents? Existing .git history will be preserved. [y/N]: " OVERWRITE
    if [[ ! "$OVERWRITE" =~ ^[Yy] ]]; then
        echo "Aborted. Choose a different vault location or empty the directory."
        exit 0
    fi
fi

# ─── Create vault and copy seed data ─────────────────────────────────────────
echo ""
echo "Creating vault at $VAULT_PATH ..."
mkdir -p "$VAULT_PATH"

# Copy seed vault contents (preserve directory structure)
cp -r "$SCRIPT_DIR/seed-vault/"* "$VAULT_PATH/"
# Copy hidden files/dirs (.cache, etc.) — ignore errors for absent dotfiles
cp -r "$SCRIPT_DIR/seed-vault/".* "$VAULT_PATH/" 2>/dev/null || true

# ─── Initialize git ──────────────────────────────────────────────────────────
cd "$VAULT_PATH"
if [[ ! -d .git ]]; then
    git init --quiet
    git branch -m main
    echo "Initialized git repository."
else
    echo "Git repository already exists — preserving history."
fi

# ─── Write .gitignore ────────────────────────────────────────────────────────
cat > "$VAULT_PATH/.gitignore" << 'GITIGNORE'
# OS
.DS_Store
Thumbs.db

# Screenpipe & sync caches
.cache/cc-screenpipe-*.json
.cache/cc-briefing-*.json
.cache/sync-state/*.json
.cache/sync-state/.updater-lock
.cache/*.log

# Large media (track PNGs, skip video)
assets/*.mp4

# Python
__pycache__/
*.pyc
*.db
GITIGNORE

# ─── Replace placeholders in vault files ──────────────────────────────────────
echo "Personalizing vault files ..."
while IFS= read -r -d '' f; do
    sedi "s/{{USER_NAME}}/$USER_NAME_ESC/g" "$f"
    sedi "s/{{USER_EMAIL}}/$USER_EMAIL_ESC/g" "$f"
done < <(find "$VAULT_PATH" -name "*.md" -print0)

# ─── Copy vault-level CLAUDE.md ──────────────────────────────────────────────
cp "$SCRIPT_DIR/config/CLAUDE.md" "$VAULT_PATH/CLAUDE.md"
sedi "s/{{USER_NAME}}/$USER_NAME_ESC/g" "$VAULT_PATH/CLAUDE.md"
sedi "s/{{USER_EMAIL}}/$USER_EMAIL_ESC/g" "$VAULT_PATH/CLAUDE.md"

# ─── Set up auto-memory directory ─────────────────────────────────────────────
# Claude Code stores per-project memory at ~/.claude/projects/-<escaped-path>/memory/
ESCAPED_PATH=$(echo "$VAULT_PATH" | sed 's|^/||' | sed 's|/|-|g')
MEMORY_DIR="$HOME/.claude/projects/-${ESCAPED_PATH}/memory"
mkdir -p "$MEMORY_DIR"
cp "$SCRIPT_DIR/config/memory/MEMORY.md" "$MEMORY_DIR/"
cp "$SCRIPT_DIR/config/memory/command-center.md" "$MEMORY_DIR/"
sedi "s|\[will be set by setup.sh\]|$VAULT_PATH|g" "$MEMORY_DIR/MEMORY.md"
echo "Auto-memory initialized at $MEMORY_DIR"

# ─── Install skills (project-scoped) ─────────────────────────────────────────
mkdir -p "$VAULT_PATH/.claude"
if [[ -d "$VAULT_PATH/.claude/skills" ]]; then
    rm -rf "$VAULT_PATH/.claude/skills"
fi
cp -r "$SCRIPT_DIR/skills" "$VAULT_PATH/.claude/skills"
echo "Installed skills to .claude/skills/"

# ─── Copy helper scripts ─────────────────────────────────────────────────────
mkdir -p "$VAULT_PATH/.scripts"
if ls "$SCRIPT_DIR/scripts/"* &>/dev/null; then
    cp "$SCRIPT_DIR/scripts/"* "$VAULT_PATH/.scripts/"
    chmod +x "$VAULT_PATH/.scripts/"*.py 2>/dev/null || true
    echo "Copied helper scripts to .scripts/"
fi

# ─── Global CLAUDE.md ─────────────────────────────────────────────────────────
GLOBAL_CLAUDE="$HOME/.claude/CLAUDE.md"
if [[ -f "$GLOBAL_CLAUDE" ]]; then
    echo ""
    echo "Global ~/.claude/CLAUDE.md already exists."
    read -rp "Append agentic-cortex preferences? [y/N]: " APPEND
    if [[ "$APPEND" =~ ^[Yy] ]]; then
        echo "" >> "$GLOBAL_CLAUDE"
        echo "# --- Added by agentic-cortex setup ---" >> "$GLOBAL_CLAUDE"
        cat "$SCRIPT_DIR/config/global-preferences.md" >> "$GLOBAL_CLAUDE"
        sedi "s/{{USER_NAME}}/$USER_NAME_ESC/g" "$GLOBAL_CLAUDE"
        sedi "s/{{USER_EMAIL}}/$USER_EMAIL_ESC/g" "$GLOBAL_CLAUDE"
        echo "Appended to $GLOBAL_CLAUDE"
    else
        echo "Skipped — global preferences unchanged."
    fi
else
    mkdir -p "$HOME/.claude"
    cp "$SCRIPT_DIR/config/global-preferences.md" "$GLOBAL_CLAUDE"
    sedi "s/{{USER_NAME}}/$USER_NAME_ESC/g" "$GLOBAL_CLAUDE"
    sedi "s/{{USER_EMAIL}}/$USER_EMAIL_ESC/g" "$GLOBAL_CLAUDE"
    echo "Created $GLOBAL_CLAUDE"
fi

# ─── Initial commit ──────────────────────────────────────────────────────────
cd "$VAULT_PATH"
git add -A
if git diff --cached --quiet; then
    echo "No changes to commit (vault already up to date)."
else
    git commit --quiet -m "Initial vault setup via agentic-cortex"
    echo "Created initial commit."
fi

# ─── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo "════════════════════════════════════════════"
echo "  Setup complete!"
echo "════════════════════════════════════════════"
echo ""
echo "  Vault:    $VAULT_PATH"
echo "  Skills:   $VAULT_PATH/.claude/skills/"
echo "  Memory:   $MEMORY_DIR"
echo ""
echo "  Next steps:"
echo "  1. cd $VAULT_PATH"
echo "  2. Start a Claude Code session:  claude"
echo "  3. Follow Chapter 1 in the README"
echo ""
echo "  The AI should greet you by name and"
echo "  know it's managing your vault. Try:"
echo "    \"What do you know about me?\""
echo ""
