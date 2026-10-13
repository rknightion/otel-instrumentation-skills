---
name: otel-semantic-conventions
description: "Resolve OpenTelemetry attribute placement, span names/kinds/status, metric conventions and compliance using a narrowly queried released semantic-convention registry."
license: Apache-2.0
---

# otel-semantic-conventions

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

1. Identify the boundary/domain, then inspect the instrumentation's schema/version evidence. SDK version alone does not prove a semconv release; inspect imports, schema URLs, instrumentation source and opt-in migration settings. If unresolved, state the uncertainty rather than selecting latest silently.
2. Resolve the applicable released registry/tag. Start at https://github.com/open-telemetry/semantic-conventions and follow official repository moves when the domain has moved; verify the new source and release separately.
3. Query only the needed group/attribute and its referenced definition. Use the semconv helper for bounded source snippets, then fetch the full selected group if context is incomplete. Search results are discovery, not a resolved registry.
4. Prefer existing standard concepts. Retrieve requirement level, stability, applicability and allowed values from that release. Check placement on resource, span, event/log or metric datapoint and assess cardinality in the actual backend mapping.
5. Apply that convention's name/kind/status rules exactly; do not add arbitrary labels to standard operation names. Use its permitted low-cardinality fallback when a route is unavailable.
6. Introduce a custom namespace only after a targeted registry search fails to cover the concept. Explain why, placement and dimension bounds.

Return domain/group, exact version/commit, source path/URL and compatibility limits with each recommendation. No bundled attribute table is the source of truth.
