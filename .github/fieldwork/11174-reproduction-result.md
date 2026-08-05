# Biome #11174 reproduction result

Focused run `30946698463`, job `92118354511`, reached the diagnostic assertion on the exact losing fixture.

Current source emitted four unexpected diagnostics:

- direct object property initialized with `false`;
- `useRef<boolean>(false)` property;
- `useRef<number>(0)` property;
- direct object property initialized with `true`.

Ten sibling focused specs passed. This is a product reproduction, not a harness failure.

The direct-object candidate is evaluated separately and does not claim the generic `useRef` cases.
