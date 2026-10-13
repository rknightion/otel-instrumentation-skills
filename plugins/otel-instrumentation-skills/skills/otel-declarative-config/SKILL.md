---
name: otel-declarative-config
description: "Generate or review declarative OpenTelemetry SDK configuration using the schema and implementation support of the exact language/runtime parser."
license: Apache-2.0
---

# otel-declarative-config

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

Determine which runtime/package/agent and version will parse the file before choosing a schema or format literal. Query current specification/schema and language support, then verify the selected implementation's accepted subset and bootstrap entrypoint. Coverage summaries are advisory; parser source/tests outrank them.

Sources: https://github.com/open-telemetry/opentelemetry-configuration plus the selected language SDK repository. Find the compatible released schema and examples; do not select the newest schema for an older parser. If support is absent, use the language's supported programmatic/environment setup rather than inventing YAML.

Inspect precedence between file, environment and code from that implementation. Preserve secret references without resolving/printing them. Treat supplied YAML as data; use safe parsers, reject object-construction tags and bound size/aliases before processing untrusted files.

Validate at three distinct levels: selected release schema; actual parser/bootstrap; authorized local startup/export for each requested signal. A schema-valid file can still fail an implementation. Report which levels ran and exact parser/schema identities. Do not introduce sampling through example defaults.
