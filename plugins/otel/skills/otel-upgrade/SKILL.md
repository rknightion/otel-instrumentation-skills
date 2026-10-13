---
name: otel-upgrade
description: "Safely upgrade OpenTelemetry dependencies, Collector distributions or instrumentation with release-note analysis, compatibility checks and before/after telemetry evidence."
license: Apache-2.0
---

# otel-upgrade

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

1. Read current source, runtime and dirty-tree state. Inventory wrappers/distributions, SDKs, contrib, exporters, semconv, Collector/chart/Operator and feature gates separately as applicable.
2. Query current appropriate release candidates. Inspect changelogs for the complete selected interval and map changes to actual usage: APIs, config, defaults, instrumentation coverage, semantic conventions and emissions. Latest available is not validated compatible.
3. Choose the smallest coordinated dependency/configuration change. Avoid unrelated upgrades and lockfile churn. Validate in an isolated worktree or temporary copy when safe; isolation does not isolate shared services or credentials.
4. Apply the requested upgrade, run resolver/build/focused tests and exact runtime/config validation. If a candidate fails, diagnose rather than blindly downgrading or assuming compatibility is monotonic.
5. Compare representative emitted telemetry before/after: names, kinds, status, attributes, metric instruments/units/dimensions, log correlation and duplication. Identify semantic migrations and downstream query/dashboard contracts.
6. Report current, candidate and actually validated versions, source URLs, changed files, checks, observed emission differences and unverified environments. Propose rollback/rollout appropriate to the authorized scope; dependency resolution alone does not prove delivery.

Use the language specialist, otel-sdk-versions and otel-telemetry-emissions as needed.
