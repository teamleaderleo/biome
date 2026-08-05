#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
cd "$repo_root"

git diff --quiet
git diff --cached --quiet

python3 .github/fieldwork/11110-apply-git-internal-candidate.py
trap 'git checkout -- crates/biome_service/src/scanner/watcher.rs crates/biome_service/src/scanner/watcher.tests.rs' EXIT

python3 - <<'PY'
from pathlib import Path

source = Path("crates/biome_service/src/scanner/watcher.rs").read_text(encoding="utf-8")
start = source.index("    fn watched_paths(")
end = source.index("\n    fn index_folders(", start)
body = source[start:end]

filter_pos = body.index('component.as_str() == ".git"')
project_lookup_pos = body.index("find_project_with_scan_kind_for_path")
assert filter_pos < project_lookup_pos
assert 'contains(".git")' not in body
print("exact .git component filtering precedes project and ignore resolution")
print("substring-like paths remain covered by reversing controls")
PY

cargo fmt --all --check
cargo test -p biome_service --features stable should_ignore_git_internal_events -- --nocapture

printf '%s\n' 'Biome #11110 scoped Git-internal watcher candidate passes focused gates'
