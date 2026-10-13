---
name: otel-ottl
description: "Write, review or debug version-correct OTTL transformations, normalization, enrichment, routing and conversions; intentional filtering/redaction only when requested."
license: Apache-2.0
---

# otel-ottl

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

Identify exact Collector distribution/version and the component executing OTTL before writing syntax. Use tagged Collector contrib source to retrieve supported contexts, paths, functions, signatures, component configuration and error handling. Locate function registration and tests when docs are ambiguous; a function existing elsewhere does not prove this component exposes it.

Choose transformation/enrichment/routing for non-lossy requirements. Normalize request-specific names/dimensions while preserving useful original identifiers in appropriate structured context. Only introduce filtering/drop behavior for an explicit request; explain what records are lost. Apply redaction when relevant, not as a default telemetry review.

Work at the correct signal/context level. Guard missing fields and wrong types using version-supported syntax. Review effects on shared resource/scope data and aggregation identity. Preserve an existing destination value unless replacement was requested; a type check alone must not authorize overwriting useful context. Verify YAML/string/regex escaping, evaluation order, idempotence and repeated processing. Choose error behavior deliberately from fetched documentation, including how it affects delivery.

Run actual Collector config validation and feed matching, nonmatching, missing, malformed and wrong-type fixtures. Inspect before/after records and counts. Benchmark regex/parse/allocation work when throughput matters. Do not treat plausible-looking expressions as validated.

Source: https://github.com/open-telemetry/opentelemetry-collector-contrib . Use the helper tree/file commands to inspect the selected OTTL package and embedding component; no local function inventory is authoritative.
