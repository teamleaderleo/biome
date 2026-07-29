# Proposed safety fix

## Proven problem

`organizeImports` can reorder two or more `export ... from` declarations. Those declarations cause their target modules to be loaded and evaluated. Reordering them can therefore change observable top-level side effects.

The current rule metadata declares the action as `FixKind::Safe`, so ordinary safe writes may apply the reorder automatically.

## Smallest initial patch

Keep `organizeImports` available, while returning `Applicability::MaybeIncorrect` whenever an `UnsortedChunk` action will reorder at least two re-export declarations.

Specifier sorting, attribute sorting, newline fixes, local export cleanup, and actions without multiple re-exports can remain safe.

Conceptually:

```rust
let applicability = if state.iter().any(|issue| match issue {
    Issue::UnsortedChunk { slot_indexes } => root
        .items()
        .into_iter()
        .skip(slot_indexes.start as usize)
        .take(slot_indexes.len())
        .filter(is_reexport)
        .take(2)
        .count()
        > 1,
    _ => false,
}) {
    Applicability::MaybeIncorrect
} else {
    ctx.metadata().applicability()
};
```

Use that value when constructing `JsRuleAction`.

## Tests

1. Add a focused analyzer fixture with a star re-export followed by a named re-export from different modules.
2. Assert the proposed action is reported as an unsafe fix.
3. Add an integration test showing safe `check --write` leaves the declaration order unchanged.
4. Assert an explicitly requested unsafe/source action can still perform the current organization.

## Stronger alternative

Preserve the relative order of all re-export declarations. This removes the semantic hazard rather than only reclassifying it, but it changes Biome's documented export-sorting behaviour and needs a broader design decision.

## Boundary

This note and reproduction live only in the fork. No upstream issue or pull request has been created.

AI assistance was used to prepare this investigation material and must be disclosed in any future pull request derived from it.
