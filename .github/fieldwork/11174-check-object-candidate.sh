#!/usr/bin/env bash
set -euo pipefail

repo_root=$(git rev-parse --show-toplevel)

cd "$repo_root"
git diff --quiet
git diff --cached --quiet

python3 .github/fieldwork/11174-apply-direct-object-candidate.py
trap 'git checkout -- crates/biome_js_type_info/src/local_inference.rs; rm -f crates/biome_js_analyze/tests/specs/suspicious/noUnnecessaryConditions/memberObjectMutationValid.ts crates/biome_js_analyze/tests/specs/suspicious/noUnnecessaryConditions/memberObjectMutationValid.ts.snap' EXIT

python3 - <<'PY'
from pathlib import Path

source = Path("crates/biome_js_type_info/src/local_inference.rs").read_text(encoding="utf-8")
start = source.index("    pub fn from_any_js_object_member(")
end = source.index("\n    pub fn from_any_ts_type_member(", start)
body = source[start:end]

const_check = body.index("is_const_asserted")
widen_check = body.index("TypeData::boolean()")
resolved_fallback = body.index("reference_to_resolved_expression", widen_check)
assert const_check < widen_check < resolved_fallback
assert "if !is_const_asserted" in body
assert "TypeData::number()" in body
assert "TypeData::string()" in body
print("mutable primitive object literals widen; const assertions retain literal inference")
print("generic-returned object properties remain outside this candidate")
PY

rustup component add rustfmt
cargo fmt --all --check
cargo check -p biome_js_type_info
cargo test -p biome_js_analyze no_unnecessary_conditions -- --nocapture

printf '%s\n' 'Biome #11174 direct-object candidate applies and passes focused gates'
