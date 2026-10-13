---
name: otel-sdk-versions
description: "Resolve current OpenTelemetry releases and compatible version lines for Go, Python and Node packages while distinguishing installed, latest and validated versions."
license: Apache-2.0
---

# otel-sdk-versions

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

Inventory the exact package/module identities first using project discovery. Query official registries and release metadata live; do not start by guessing every package in a language has one shared version.

For Go, inspect each module's selected version and its module-specific tags/dependencies. For Python, inspect individual distributions, requires-python and dependency constraints, including intentionally prerelease contrib lines. For Node, inspect each package's dist-tags, versions, engines and peer dependencies. A latest tag or release API is a discovery result, not compatibility proof.

Use the helper package command for an explicitly identified npm/PyPI/Go module and release/file commands for authoritative changelogs and manifests. If a package line intentionally publishes prereleases, preserve that fact rather than silently replacing it with an unrelated stable line. Query wrappers/distributions separately.

Return a compact table: identity, installed/resolved, latest appropriate candidate, constraints, validated compatible (or not tested), lookup timestamp and source. Use otel-upgrade for edits/testing. Never write a version into a manifest that has not been verified to exist.
