#!/usr/bin/env bash
set -euo pipefail

# This script splits the current monorepo into 4 independent branches using git subtree
# and optionally pushes them to new remotes. Fill in the REMOTE_* variables below.

# ========== Configuration ==========
# Replace the following with your actual remote repository URLs.
REMOTE_FRANKLIN="https://github.com/your-org/Franklin.git"
REMOTE_ARXIV="https://github.com/your-org/arxiv_llm_digest.git"
REMOTE_IDCONVERT="https://github.com/your-org/IDconvert.git"
REMOTE_DNATRANSLATE="https://github.com/your-org/DNAtranslate.git"

# Target branch name on each split repo
TARGET_BRANCH="main"

# ========== Safety checks ==========
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "[ERROR] Not inside a git repository."
  exit 1
fi

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "[ERROR] Working tree has uncommitted changes. Please commit or stash them first."
  exit 1
fi

# ========== Split helper ==========
split_and_push() {
  local prefix="$1"        # e.g., Franklin
  local branch="$2"        # e.g., split/Franklin
  local remote_name="$3"   # e.g., franklin-origin
  local remote_url="$4"    # e.g., https://github.com/your-org/Franklin.git

  echo "\n=== Splitting $prefix into branch $branch ==="
  # Create or update split branch
  if git show-ref --verify --quiet "refs/heads/$branch"; then
    echo "[INFO] Branch $branch exists, deleting and recreating..."
    git branch -D "$branch"
  fi
  git subtree split --prefix="$prefix" -b "$branch"

  if [[ -n "$remote_url" && "$remote_url" != "https://github.com/your-org/${prefix}.git" ]]; then
    echo "[INFO] Adding remote $remote_name -> $remote_url (if not exists)"
    if git remote get-url "$remote_name" >/dev/null 2>&1; then
      git remote set-url "$remote_name" "$remote_url"
    else
      git remote add "$remote_name" "$remote_url"
    fi

    echo "[INFO] Pushing $branch to $remote_name:$TARGET_BRANCH"
    git push -f "$remote_name" "$branch:$TARGET_BRANCH"
  else
    echo "[WARN] Remote URL for $prefix not configured. Skipping push."
  fi
}

# ========== Execute splits ==========
split_and_push "Franklin" "split/Franklin" "franklin-origin" "$REMOTE_FRANKLIN"
split_and_push "arxiv_llm_digest" "split/arxiv_llm_digest" "arxiv-origin" "$REMOTE_ARXIV"
split_and_push "IDconvert" "split/IDconvert" "idconvert-origin" "$REMOTE_IDCONVERT"
split_and_push "DNAtranslate" "split/DNAtranslate" "dnatranslate-origin" "$REMOTE_DNATRANSLATE"

echo "\nAll done. You can now clone the target repositories and verify the results."
