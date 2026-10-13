---
name: otel-collector-builder
description: "Assess and build custom OpenTelemetry Collector distributions with OCB, aligned component modules, local components and reproducible CI/container builds."
license: Apache-2.0
---

# otel-collector-builder

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

First show why an existing distribution cannot meet the required component, patch or footprint constraints. Do not create a custom distribution merely because one is possible.

Discover the selected OCB release and exact builder help, manifest schema/examples and supported Go toolchain from Collector core. Resolve each module version independently, including replacements and local custom components. Check compatibility against the generated module graph rather than aligning unrelated version numbers by appearance.

Build in an isolated directory with pinned inputs. Record builder version, manifest, module sums, toolchain and resulting component inventory. For local components, validate factories, supported signals and integration with the distribution. Avoid unexplained replace directives.

Run unit/build checks, inspect CLI help, validate a minimal config and exercise required signals. Container and multi-architecture builds must name target OS/architecture, base-image identity and architecture-specific validation; a cross-compile is not a runtime test. Wire the same reproducible build and validation into the project's existing CI/task surface.

Retrieve OCB documentation under https://github.com/open-telemetry/opentelemetry-collector and distribution manifests under https://github.com/open-telemetry/opentelemetry-collector-releases .
