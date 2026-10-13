---
name: otel-telemetrygen
description: "Generate traces, metrics or logs for Collector/OTTL/pipeline verification or explicitly bounded load tests using the selected telemetrygen binary help."
license: Apache-2.0
---

# otel-telemetrygen

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

Locate the installed binary or selected release artifact and capture its version and top-level help. Inspect signal-specific help before emitting any command. If no binary is available, retrieve tagged official command source and mark the command unexecuted; never invent flags.

Source: https://github.com/open-telemetry/opentelemetry-collector-contrib . Discover the tool path in that tag. Confirm transport, endpoint/TLS, signal, rate/count/duration and attribute controls against that help. Set a finite test budget and local/authorized sink; load testing production needs explicit target authority.

Start the exact Collector under test, send a known input, await export/flush and inspect sink output. Compare counts, transformed fields, resource identity and trace relationships with expectations. Include negative cases when verifying OTTL. If telemetrygen cannot express a required field/shape, use a small synthetic emitter rather than claiming the test covers it.

Record binary identity, help evidence, command with secrets omitted, input budget, sink observations and delivery limitations. A successful sender exit does not establish backend receipt.
