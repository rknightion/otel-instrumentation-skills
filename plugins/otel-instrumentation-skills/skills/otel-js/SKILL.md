---
name: otel-js
description: "Instrument or troubleshoot JavaScript/TypeScript Node.js services: ESM/CJS startup, early loading, async context, auto/manual duplication, metrics and log correlation. Browser OTel is excluded."
license: Apache-2.0
---

# otel-js

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

Read package.json, the resolved lockfile, runtime version, transpilation/bundler output and production launch command. Determine ESM/CJS from the actual executed code, not merely the source extension. Query current SDK/API/contrib package metadata, supported framework versions, loaders/preload mechanics, exporters and defaults at the selected versions.

1. Identify existing startup instrumentation. Arrange SDK/instrumentation initialization before affected modules load, using the mechanism documented for that Node/module-system/package combination. Verify it with the real startup command; do not guess preload flags.
2. Check API singleton/provider compatibility, package peer dependencies and auto-instrumentation coverage. Avoid duplicate framework/request spans. Enrich the active span where appropriate.
3. Test async context across promises, callbacks, queues and concurrent requests. Verify incoming extraction and outgoing injection.
4. Retrieve current metric and structured logging APIs, including bridge behavior. Bound dimensions and verify correlation rather than only formatting trace IDs into strings.
5. Check shutdown promises, buffered export and signal-handler ordering; avoid exiting before flush completes. Measure event-loop/CPU/allocation overhead separately from export traffic.
6. Validate type/build checks, production startup and actual emitted telemetry. State experimental/stable status only from fetched matching sources.

Sources: https://github.com/open-telemetry/opentelemetry-js , https://github.com/open-telemetry/opentelemetry-js-contrib and https://registry.npmjs.org .
