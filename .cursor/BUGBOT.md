# OpenTelemetry skills review

This repository publishes one Markdown skill tree through Claude and Codex
catalogs. The Python lookup helper resolves current upstream facts. Keep
recommendations tied to the exact SDK or Collector version and evidence from
authoritative sources. Distinguish what code can emit from what a runtime
check observed.

Review the shared policies and skill instructions for changes that discard
telemetry, introduce unbounded dimensions or capture secrets. Keep helper
output explicit about provenance and lookups that fail. Eval prompts,
grading inputs, and synthetic fixtures should test the same behavior across
clients. Keep generated manifests and eval scaffolds derived from their
canonical inputs.

`just check` verifies generated files, skill frontmatter and links, version
and freshness rules, Python syntax, and helper tests. Focus feedback on
incorrect guidance or missing evidence beyond what those checks enforce.
