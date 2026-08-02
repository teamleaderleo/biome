# Biome #11174 mutable member literal widening

Base branch: `ci/biome-focused-base`.

The false positive is produced when `noUnnecessaryConditions` asks the type service for a static or computed member expression and receives a singleton literal type such as `false`, `0`, or `""` for a mutable property.

The test matrix covers:

- mutable object-literal boolean, number, and string properties;
- nested mutable properties;
- generic `useRef(false)` and `useRef(0)`-style inference;
- explicitly widened generic arguments such as `useRef<boolean>(false)`;
- contextual mutable property types;
- computed access through a mutable collection element.

All cases belong in the valid suite. The desired correction is property-literal widening in mutable inference contexts, not a blanket exemption for member expressions in the lint rule. A blanket exemption would lose valid diagnostics for members whose declared type is genuinely a singleton literal or whose object is immutable.

Run the focused suite with:

```console
cargo test -p biome_js_analyze no_unnecessary_conditions -- --nocapture
```

Remaining source work is to identify the common inference path used by object-literal fields and generic call arguments, then add literal-preserving controls for immutable or explicitly singleton-typed members.
