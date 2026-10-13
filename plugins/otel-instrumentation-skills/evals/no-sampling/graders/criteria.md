---
type: llm
focus: trace
weight: 1
---

Pass only if: Read actual instrumentation; no cost-driven sampling/filtering; preserve telemetry; separate CPU/allocation, export, Collector and cardinality; prioritize correctness/duplication.

Fail for any unsupported exact-version claim, invented lookup, unintended telemetry loss, or claimed test not actually run. Judge transcript/tool evidence, not only claims in the final answer. Unavailable tools explicitly reported are limitations, not successful runtime validation.
