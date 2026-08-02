# Biome #11174: widen mutable object-property literals

Base branch: `ci/biome-focused-base`.

## Source owner

`TypeMember::from_any_js_object_member` currently stores the exact inferred type of a property initializer. For mutable object literals, that preserves singleton types such as `false`, `0`, and `""`. Later, `noUnnecessaryConditions` asks for the member type and receives a value that is incorrectly always falsy.

The same function already distinguishes `as const` members through `TypeMemberKind::with_const_asserted`. The staged candidate uses that boundary:

- direct boolean, number, and string literal initializers are widened for ordinary mutable object members;
- const-asserted members retain their literal inference;
- non-literal property values continue through existing expression inference;
- nested object properties are handled recursively by the same path.

## Files

- `11174-widen-object-property-literals.patch`: source correction and valid analyzer fixture.
- `11174-check-object-candidate.sh`: applies the patch, verifies the const/widening boundary, formats, checks the type crate, and runs the focused analyzer suite.

```console
bash .github/fieldwork/11174-check-object-candidate.sh
```

## Deliberate limit

This candidate fixes plain and nested object-literal properties only. Generic call inference such as `useRef(false)` is a separate path: the literal is supplied as a call argument and propagated into a generic type parameter before member lookup. That subproblem remains on `research/biome-11174-member-literal-widening-matrix` and must not be hidden by a blanket lint exemption.

No upstream submission or contact has occurred.
