#!/usr/bin/env python3
"""Apply the scoped direct-object literal widening candidate."""

from __future__ import annotations

from pathlib import Path


SOURCE = Path("crates/biome_js_type_info/src/local_inference.rs")
FIXTURE = Path(
    "crates/biome_js_analyze/tests/specs/suspicious/noUnnecessaryConditions/"
    "memberObjectMutationValid.ts"
)

OLD = """                    let value = member.value().ok();
                    let kind = if value.as_ref().is_some_and(expression_is_const_assertion) {
                        kind.with_const_asserted()
                    } else {
                        kind
                    };
                    Self {
                        kind,
                        ty: value
                            .map(|value| {
                                resolver.reference_to_resolved_expression(scope_id, &value)
                            })
                            .unwrap_or_default(),
                    }
"""

NEW = """                    let value = member.value().ok();
                    let is_const_asserted =
                        value.as_ref().is_some_and(expression_is_const_assertion);
                    let kind = if is_const_asserted {
                        kind.with_const_asserted()
                    } else {
                        kind
                    };
                    Self {
                        kind,
                        ty: value
                            .map(|value| {
                                if !is_const_asserted {
                                    let widened = match &value {
                                        AnyJsExpression::AnyJsLiteralExpression(
                                            AnyJsLiteralExpression::JsBooleanLiteralExpression(_),
                                        ) => Some(TypeData::boolean()),
                                        AnyJsExpression::AnyJsLiteralExpression(
                                            AnyJsLiteralExpression::JsNumberLiteralExpression(_),
                                        ) => Some(TypeData::number()),
                                        AnyJsExpression::AnyJsLiteralExpression(
                                            AnyJsLiteralExpression::JsStringLiteralExpression(_),
                                        ) => Some(TypeData::string()),
                                        _ => None,
                                    };
                                    if let Some(widened) = widened {
                                        return resolver.reference_to_owned_data(widened);
                                    }
                                }
                                resolver.reference_to_resolved_expression(scope_id, &value)
                            })
                            .unwrap_or_default(),
                    }
"""

FIXTURE_CONTENT = """// should not generate diagnostics

const booleanBox = { current: false };
if (booleanBox.current) {
  console.log("already set");
}
booleanBox.current = true;

const numberBox = { current: 0 };
if (numberBox.current) {
  console.log("already nonzero");
}
numberBox.current = 1;

const stringBox = { current: "" };
if (stringBox.current) {
  console.log("already nonempty");
}
stringBox.current = "ready";

const nested = { state: { ready: false } };
if (nested.state.ready) {
  console.log("already ready");
}
nested.state.ready = true;
"""


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8")
    count = text.count(OLD)
    if count != 1:
        raise SystemExit(f"direct-object candidate anchor count: {count}")
    SOURCE.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
    if FIXTURE.exists():
        raise SystemExit(f"fixture already exists: {FIXTURE}")
    FIXTURE.write_text(FIXTURE_CONTENT, encoding="utf-8")
    print(SOURCE)
    print(FIXTURE)


if __name__ == "__main__":
    main()
