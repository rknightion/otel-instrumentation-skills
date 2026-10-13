---
name: otel-span-events-to-logs-migration
description: "Assess whether current OpenTelemetry span-event/exception-to-log migration guidance applies to a project and implement a version-supported migration when appropriate."
license: Apache-2.0
---

# otel-span-events-to-logs-migration

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

Treat migration status as mutable. On every relevant invocation retrieve the current specification/OTEP or accepted proposal state, then the selected language SDK and instrumentation support. Start at https://github.com/open-telemetry/opentelemetry-specification and follow its official proposal references; a historical plan is not a universal deprecation.

Inventory actual event/exception APIs, consumers and signal export. Establish whether the project's installed versions support the intended logs/events behavior and correlation. Separate accepted guidance, released SDK support and the project's adopted behavior.

If migration applies, preserve event meaning, severity/error status, timestamp and trace/span correlation using APIs verified for the selected versions. Avoid dual emission unless a deliberate transition requires it; define its end. Check downstream queries/alerts and verify error paths and buffered shutdown.

If it does not apply, explain why and leave working instrumentation intact. Report spec/proposal state, SDK versions, sources, changed call sites and observed telemetry. Do not migrate simply because an old skill called span events deprecated.
