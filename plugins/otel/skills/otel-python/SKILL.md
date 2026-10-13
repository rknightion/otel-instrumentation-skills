---
name: otel-python
description: "Add or debug OpenTelemetry in Python services, including FastAPI-style frameworks, async context, auto/manual instrumentation, structured logs and exporters."
license: Apache-2.0
---

# otel-python

Read [source policy](../../shared/source-policy.md), [observability policy](../../shared/observability-policy.md), [project discovery](../../shared/project-discovery.md) and [verification policy](../../shared/verification-policy.md) before acting. These paths resolve from this SKILL.md inside the installed plugin; do not resolve them from the user's working directory. Read them once per task and reuse them across specialist skills.

Inspect lockfiles, installed environment, interpreter, framework startup and worker model. Retrieve matching SDK/contrib source and package metadata; the distro, instrumentation and SDK need not share a version. Look up current zero-code tooling, logging integration, exporters and declarative support rather than assuming entrypoints.

1. Locate automatic instrumentation and provider ownership. Choose framework integration versus manual boundaries from current support, not a frozen package list.
2. Verify initialization timing in the actual worker/process lifecycle. Avoid double patching a framework or installing duplicate logging handlers. Check reload and multi-worker behavior.
3. Trace context through async tasks, thread pools and messaging. Test overlapping requests so context leaks cannot hide behind a single happy path.
4. Retrieve exact APIs for metrics, readers/processors and log correlation. Keep metric attributes bounded; preserve useful request/user context in structured fields.
5. Inspect blocking export work, batching and exporter retry behavior from selected source. Measure overhead under representative concurrency; verify shutdown/flush at the application lifecycle boundary.
6. Validate imports/dependency compatibility, framework startup and emitted traces, metrics and correlated logs using an isolated sink.

Sources: https://github.com/open-telemetry/opentelemetry-python , https://github.com/open-telemetry/opentelemetry-python-contrib and https://pypi.org .
