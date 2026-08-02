#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)
patch_file="$repo_root/.github/fieldwork/11110-ignore-git-internals.patch"

cd "$repo_root"
git diff --quiet
git diff --cached --quiet

git apply --check "$patch_file"
git apply "$patch_file"
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
print(".git component filtering precedes project and ignore resolution")
PY

cargo fmt --check -- crates/biome_service/src/scanner/watcher.rs crates/biome_service/src/scanner/watcher.tests.rs
cargo test -p biome_service should_ignore_git_internal_events -- --nocapture

printf '%s\n' 'Biome #11110 git-internal watcher candidate applies and passes focused test'
