# Biome #11174: widen mutable object-property literals

Base branch: `ci/biome-focused-base`.

## Source owner

`TypeMember::from_any_js_object_member` currently stores the exact inferred type of a property initializer. For mutable object literals, that preserves singleton types such as `false`, `0`, and `""`. Later, `noUnnecessaryConditions` asks for the member type and receives a value that is incorrectly always falsy.

The same function already distinguishes `as const` members through `TypeMemberKind::with_const_asserted`. The scoped candidate uses that boundary:

- direct boolean, number, and string literal initializers are widened for ordinary mutable object members;
- const-asserted members retain their literal inference;
- non-literal property values continue through existing expression inference;
- nested object properties are handled recursively by the same path.

## Files

- `11174-apply-direct-object-candidate.py`: fail-closed exact-anchor source transformation plus valid fixture and snapshot generation;
- `11174-check-object-candidate.sh`: verifies the const/widening boundary, installs rustfmt, formats, checks the type crate, and runs the focused analyzer suite;
- `11174-candidate-scope.md`: explicit partial-scope boundary;
- `11174-reproduction-result.md`: exact losing-run receipt.

```console
bash .github/fieldwork/11174-check-object-candidate.sh
```

## Executed result

Focused workflow `30974887580`, job `92206760837`, completed successfully at exact carrier head `2121e7c34cb058e23b686df14d5dcf8cd4beba75` before this documentation-only correction. Rust formatting, `biome_js_type_info` compilation, and all 11 focused analyzer specifications passed.

This same-account review is not independent acceptance. A current-main product carrier must retain the exact transformed source/test diff and rerun the relevant gates.

## Deliberate limit

This candidate fixes plain and nested object-literal properties only. Generic call inference such as `useRef(false)` is a separate path: the literal is supplied as a call argument and propagated into a generic type parameter before member lookup. That subproblem remains unresolved and must not be hidden by a blanket lint exemption.

No upstream submission or contact has occurred.
