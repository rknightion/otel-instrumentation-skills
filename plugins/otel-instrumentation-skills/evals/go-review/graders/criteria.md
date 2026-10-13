---
type: llm
focus: trace
weight: 1
---

Pass only if: Inspect go.mod and source; identify discarded incoming context, redundant server span, missing provider/flush, UID dimensions; fetch exact-version source; avoid sampling.

Fail for any unsupported exact-version claim, invented lookup, unintended telemetry loss, or claimed test not actually run. Judge transcript/tool evidence, not only claims in the final answer. Unavailable tools explicitly reported are limitations, not successful runtime validation.
