#!/usr/bin/env bash
set -euo pipefail

# Install every Skill folder in skills/ into the Codex personal skills directory.
# Usage: scripts/install.sh [--dest /custom/skills/path]

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
DEST="${CODEX_HOME:-$HOME/.codex}/skills"

if [[ "${1:-}" == "--dest" ]]; then
  DEST="${2:?--dest requires a path}"
fi

mkdir -p "$DEST"
count=0
for skill_dir in "$REPO_ROOT"/skills/*/; do
  name="$(basename "$skill_dir")"
  if [[ ! -d "$skill_dir" ]]; then
    continue
  fi
  rm -rf "$DEST/$name"
  cp -R "$skill_dir" "$DEST/$name"
  echo "installed: $name -> $DEST/$name"
  count=$((count + 1))
done

echo "Installed $count Skills into $DEST"
echo "Refresh or restart Codex for the new Skills to appear in the catalog."
