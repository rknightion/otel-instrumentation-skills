---
type: llm
focus: trace
weight: 1
---

Pass only if: Identify unbounded dimension; bound/remove it from metric grouping while retaining useful span/log context; hashing is not a cardinality fix.

Fail for any unsupported exact-version claim, invented lookup, unintended telemetry loss, or claimed test not actually run. Judge transcript/tool evidence, not only claims in the final answer. Unavailable tools explicitly reported are limitations, not successful runtime validation.
