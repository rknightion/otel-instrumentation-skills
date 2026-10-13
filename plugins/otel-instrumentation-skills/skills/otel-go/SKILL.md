---
name: otel-go
description: "Add, review or troubleshoot OpenTelemetry in Go services, including providers, contrib/manual instrumentation, propagation, logging, shutdown and allocation overhead."
license: Apache-2.0
---

# otel-go

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

Inspect modules, replacements, provider setup and runtime first. Retrieve APIs and compatibility from the selected tags of the Go SDK and Go contrib repositories; resolve logging/exporter/contrib modules independently. Query current compile-time/zero-code support and declarative support only when relevant.

1. Reuse existing providers and resource identity. Determine who initializes and shuts down each signal; do not add a second global SDK inside a library.
2. Compare current automatic/contrib coverage with required HTTP, gRPC, database and messaging boundaries. Trace context through request contexts, goroutines and message envelopes; verify extraction/injection using the installed propagator APIs.
3. Retrieve exact trace, metric and log APIs before coding. Check instruments/units and semantic placement. Enrich active spans or add meaningful business spans without duplicates.
4. Inspect batch/export behavior, failure handling and shutdown ordering from current selected source. Exercise termination with buffered telemetry and a reachable local sink.
5. For hot paths, benchmark with representative concurrent work. Inspect attribute construction, formatting, allocation and lock contention. Guard expensive enrichment on non-recording telemetry only where the selected API permits and preserve required metric/log work. Do not conflate application allocation savings with backend volume reduction.
6. Run focused Go tests and benchmarks, then inspect actual emitted signals and parent-child linkage.

Use otel-sdk-versions for release discovery, otel-semantic-conventions for boundary rules and otel-upgrade for version changes. Sources: https://github.com/open-telemetry/opentelemetry-go and https://github.com/open-telemetry/opentelemetry-go-contrib .
