#!/usr/bin/env python3
"""Apply the scoped `.git` watcher-event filter and reversing controls."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path("crates/biome_service/src/scanner/watcher.rs")
TESTS = Path("crates/biome_service/src/scanner/watcher.tests.rs")

OLD = """            .filter_map(|path| {
                let path = Utf8PathBuf::from_path_buf(path).ok()?;
                workspace
"""

NEW = """            .filter_map(|path| {
                let path = Utf8PathBuf::from_path_buf(path).ok()?;
                if path
                    .components()
                    .any(|component| component.as_str() == ".git")
                {
                    return None;
                }
                workspace
"""

TEST = """

#[test]
fn should_ignore_git_internal_events() {
    let fs = TemporaryFs::new("should_ignore_git_internal_events");
    let os_fs = fs.create_os();
    let project_path = Utf8Path::new(fs.cli_path());

    let (mock_bridge, _bridge_rx) = MockWorkspaceWatcherBridge::new(
        &os_fs,
        ProjectKey::new(),
        ScanKind::Project,
    );

    let source_path = project_path.join("ui/something.js");
    let github_path = project_path.join(".github/workflows/ci.yml");
    let gitignore_path = project_path.join(".gitignore");
    let suffix_path = project_path.join("not.git/file.js");
    let watched = Watcher::watched_paths(
        &mock_bridge,
        vec![
            project_path.join(".git/index.lock").into_std_path_buf(),
            project_path
                .join("nested/.git/objects/pack.lock")
                .into_std_path_buf(),
            source_path.clone().into_std_path_buf(),
            github_path.clone().into_std_path_buf(),
            gitignore_path.clone().into_std_path_buf(),
            suffix_path.clone().into_std_path_buf(),
        ],
    );

    assert_eq!(
        watched,
        vec![source_path, github_path, gitignore_path, suffix_path]
    );
}
"""


def main() -> None:
    source = SOURCE.read_text(encoding="utf-8")
    count = source.count(OLD)
    if count != 1:
        raise SystemExit(f"watcher candidate anchor count: {count}")
    SOURCE.write_text(source.replace(OLD, NEW, 1), encoding="utf-8")

    tests = TESTS.read_text(encoding="utf-8")
    if "fn should_ignore_git_internal_events()" in tests:
        raise SystemExit("watcher discriminator already exists")
    TESTS.write_text(tests.rstrip() + TEST + "\n", encoding="utf-8")

    print(SOURCE)
    print(TESTS)


if __name__ == "__main__":
    main()
