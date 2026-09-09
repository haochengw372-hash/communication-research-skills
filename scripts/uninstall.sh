#!/usr/bin/env bash
set -euo pipefail

# Remove only the eighteen folders installed by install.sh.
# Usage: scripts/uninstall.sh [--dest /custom/skills/path]

DEST="${CODEX_HOME:-$HOME/.codex}/skills"

if [[ "${1:-}" == "--dest" ]]; then
  DEST="${2:?--dest requires a path}"
fi

names=(
  "communication-research-workflow"
  "communication-literature"
  "communication-theory"
  "communication-construct"
  "communication-scale"
  "communication-method-router"
  "communication-experiment"
  "communication-content-analysis"
  "communication-network-analysis"
  "communication-causal-inference"
  "communication-temporal-analysis"
  "communication-multimodal-analysis"
  "communication-spatial-analysis"
  "communication-simulation"
  "communication-writing"
  "communication-prose-revision"
  "communication-reviewer"
  "scholarly-access"
)

removed=0
for name in "${names[@]}"; do
  if [[ -d "$DEST/$name" ]]; then
    rm -rf "$DEST/$name"
    echo "removed: $name"
    removed=$((removed + 1))
  fi
done

echo "Removed $removed Skills from $DEST"
