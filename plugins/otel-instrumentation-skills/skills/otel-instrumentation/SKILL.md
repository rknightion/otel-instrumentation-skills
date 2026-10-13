---
name: otel-instrumentation
description: "Review or improve OpenTelemetry signal quality across traces, metrics and logs: correctness, propagation, correlation, cardinality, duplication and runtime overhead."
license: Apache-2.0
---

# otel-instrumentation

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

1. Build the version and signal-path ledger before recommending changes. Identify existing automatic boundaries and provider ownership; use the matching Go, Python or Node specialist for implementation.
2. Review resource/service identity across signals. Distinguish persistent entity identity from per-operation context; check enrichment consistency and downstream dimension promotion.
3. Follow a representative request through inbound, outbound, database and messaging boundaries. Check extracted/injected context, parent-child relationships, async handoffs and active context. Use the released semantic convention for name, kind, status and error handling.
4. Compare automatic spans/metrics with manual instrumentation. Add missing business boundaries or enrich active spans when useful; do not wrap an already instrumented operation a second time.
5. Review metric instruments, units, temporality and aggregation against the actual SDK and convention. Establish a finite dimension budget from domain values; retain debugging IDs on spans/logs rather than series.
6. Review structured logs, severity and trace/log correlation. Check logging bridges, duplicate handlers and secret capture without turning the review into indiscriminate PII removal.
7. Inspect batching, exporting, graceful flush/shutdown and runtime overhead. Benchmark hot-path allocations/CPU if performance matters. Make the smallest useful change and verify emitted telemetry.

Return findings with location, observed consequence, proposed change, version-correct evidence and validation. Prioritize correctness and useful signal, never backend cost.
