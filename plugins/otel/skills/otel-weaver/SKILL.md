---
name: otel-weaver
description: "Use OpenTelemetry Weaver for semantic registry authoring, validation, templates/code generation, registry diffing and CI enforcement with current CLI/schema evidence."
license: Apache-2.0
---

# otel-weaver

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

Identify installed Weaver, registry format and upstream semconv dependency versions separately. Retrieve current tagged docs/schema and inspect CLI help for the selected binary. Source: https://github.com/open-telemetry/weaver . Do not assume a package-manager name resolves to this project.

Author only concepts missing from standard conventions; reference upstream definitions rather than duplicating boundary attributes. Verify required fields, extension rules and stability annotations against the selected schema. Use an organization namespace for genuinely custom concepts.

Before templating, inspect resolved schema output and the selected template engine/filter behavior. Generate into an isolated directory, format with the language formatter and compare against committed output. Check schema validity, registry diff compatibility and reproducibility as separate results.

Wire version-pinned validation, generation freshness and intentional baseline diff checks into the existing task/CI surface. Retrieve current commands rather than embedding flag lists. For optional live validation capabilities, first confirm release support and test scope. Record tool/schema/registry identities and any untested consumers.
