# Biome #11110 scoped Git-internal watcher candidate

The clean losing run `30973738984` / job `92203345637` established that current `Watcher::watched_paths` retains `.git/index.lock` beside an ordinary project path.

This candidate filters only path components exactly equal to `.git` before project and ignore resolution.

Reversing controls require these paths to remain observable:

- `.github/workflows/ci.yml`;
- `.gitignore`;
- `not.git/file.js`;
- an ordinary project source path.

This addresses only Git-internal event filtering. The symlinked-workspace re-lint behavior from public issue 11110 remains a separate investigation.

No canonical-upstream interaction is authorized or performed.
