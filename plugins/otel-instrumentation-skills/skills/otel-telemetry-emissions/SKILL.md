---
name: otel-telemetry-emissions
description: "Determine which traces, metrics, logs and attributes a particular OpenTelemetry instrumentation package or Collector component actually emits at a selected version."
license: Apache-2.0
---

# otel-telemetry-emissions

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

Identify package/component, version, enabled options, target framework and signal. Retrieve exact tagged upstream source first, then official documentation. Inspect metadata definitions, emission call sites, generated code and tests; follow wrappers only far enough to explain the requested signal.

Distinguish specified by upstream, detected by source analysis and observed at runtime. Conditional branches, build tags, feature gates, runtime versions and disabled instruments can make static inventories incomplete. A search finding is not proof of exhaustive emissions, and absence from a scan is not proof of absence.

Return only relevant signal names, units/types/attributes with source context fetched for the version. For a cached/scanned inventory record repository, tag, resolved commit, path, scan date, source files and confidence/limitations. The helper's bounded tree/file search is an acceleration layer, not an emission spec.

When important, exercise the relevant instrumentation with representative successful/error operations and capture output. Compare it with upstream claims; report runtime coverage separately. For upgrades, compare both pinned revisions and actual emitted telemetry.
