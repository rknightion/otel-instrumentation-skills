---
type: llm
focus: trace
weight: 1
---

Pass only if: Inspect version; retrieve function signatures/contexts and component config at tag; preserve originals; guard appropriate types/missing values; provide before/after fixture tests; no guessed function.

Fail for any unsupported exact-version claim, invented lookup, unintended telemetry loss, or claimed test not actually run. Judge transcript/tool evidence, not only claims in the final answer. Unavailable tools explicitly reported are limitations, not successful runtime validation.
