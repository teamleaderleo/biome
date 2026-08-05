# Biome #11174 direct-object candidate scope

The losing fixture reproduces four false positives: direct mutable object properties and generic-returned properties such as `useRef<T>()`.

This candidate intentionally addresses only direct object-literal inference. It widens mutable boolean, number, and string property literals while preserving `as const` literal inference.

A green focused run does not resolve the generic-returned-property cases and is not an issue-complete result.

No canonical-upstream interaction is authorized or performed.
