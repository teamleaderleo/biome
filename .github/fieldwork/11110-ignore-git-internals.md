# Biome #11110: ignore Git-internal watcher events

Base branch: `ci/biome-focused-base`.

The issue contains two separate behaviors. This candidate addresses only filesystem events under a `.git` path component. Symlinked workspace re-indexing is not included because it has a different path-resolution owner.

Current `Watcher::watched_paths` converts the event path and immediately asks the workspace for project and ignore state. That allows Git-internal events such as `.git/index.lock` to reach indexing or unloading when VCS integration is disabled or project ignore state does not cover Git metadata.

The candidate filters any path containing a `.git` component before project lookup. This is independent of VCS configuration and does not suppress ordinary project files.

Files:

- `11110-ignore-git-internals.patch`: source correction plus focused regression test.
- `11110-check-candidate.sh`: applies the patch to the exact branch, verifies filter placement, formats, and runs the focused test.

```console
bash .github/fieldwork/11110-check-candidate.sh
```

Remaining gates are the broader `biome_service` test set, platform watcher behavior, and an explicit decision on whether nested repositories should be entirely excluded or only their `.git` metadata paths.
