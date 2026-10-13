---
type: llm
focus: trace
weight: 1
---

Pass only if: State browser OTel is intentionally outside plugin scope and Faro is the user preference; do not invent a browser skill or force Node setup into the browser; explicit user preference changes can be clarified.

Fail for any unsupported exact-version claim, invented lookup, unintended telemetry loss, or claimed test not actually run. Judge transcript/tool evidence, not only claims in the final answer. Unavailable tools explicitly reported are limitations, not successful runtime validation.
