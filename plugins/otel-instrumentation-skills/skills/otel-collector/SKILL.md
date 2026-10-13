---
name: otel-collector
description: "Configure, review or diagnose OpenTelemetry Collector components and end-to-end pipelines against the exact distribution/version, including topology, reliability and Kubernetes."
license: Apache-2.0
---

# otel-collector

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

1. Establish binary/distribution, image digest/version, build component inventory, rendered configuration and feature gates. A contrib directory is not proof a component is bundled. Resolve renamed aliases against this release.
2. For every relevant component fetch tagged README, configuration structs/validation, metadata and tests. Check each key, default, signal support and stability; inherited exporter/helper options require their matching source too. Use the helper tree search to locate paths rather than deriving directory names from config IDs.
3. Trace receiver-to-processor-to-exporter paths and connectors/extensions. Verify signal wiring, enrichment consistency and processor ordering based on data dependencies and release behavior; do not prescribe a universal order from memory.
4. Reason about agent/gateway/sidecar topology, Kubernetes identity/RBAC, duplicate scraping and deployment ownership. Examine stateful grouping, partition affinity and scaling/restart effects.
5. Review buffering, memory bounds, retry, persistent queues and backpressure as a reliability system. Explain overflow or refusal behavior and quantify the workload assumptions. Do not introduce loss or sampling as generic optimisation.
6. Check the installed binary's help, then run its supported configuration validation. Exercise the pipeline with known generated telemetry and a local sink, including failure/recovery where relevant. Report schema, runtime and delivery evidence separately.

Sources: https://github.com/open-telemetry/opentelemetry-collector , https://github.com/open-telemetry/opentelemetry-collector-contrib and https://github.com/open-telemetry/opentelemetry-collector-releases . Use otel-ottl for expressions and otel-telemetrygen for test traffic.
