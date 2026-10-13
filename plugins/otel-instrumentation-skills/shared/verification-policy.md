# Verification policy
Use the smallest authorized reproducible experiment that proves the requested behavior. Separate evidence levels: dependency resolution; compile/unit checks; schema/parser validation; actual binary startup; emitted telemetry; backend receipt/correlation. Never claim a later level because an earlier one passed.

For changed instrumentation, generate successful, failed and concurrent operations across a real boundary where practical. Inspect parent/child trace IDs, propagation, operation names, status/error semantics against the selected convention, units, metric dimension bounds, structured log context and trace/log correlation. Prove that auto and manual instrumentation do not duplicate the same boundary. Exercise shutdown and flush. Record counts before/after transformations to detect unintended loss.

For Collector/OTTL, use the exact distribution and version with synthetic input and an isolated local sink. Test absent fields, wrong types, non-matching records, malformed input and exporter failure when relevant. Validate ordering, retry/backpressure, queue saturation and recovery without treating process liveness as delivery. Use telemetrygen only after checking that binary's help; it may not express every required fixture, so use a small emitter or recorded synthetic OTLP when necessary.

Keep test endpoints local or explicitly authorized. Do not send load to production by default. Bound duration/rate and preserve original config for rollback. Measure application CPU/allocations, export/network, Collector resources and backend/index cardinality separately; do not fix one by blindly deleting telemetry in another.

Report exact artifacts/versions, source links, commands and observed results. Mark unavailable backend access, skipped tests, unsupported signals and unresolved evidence explicitly. A proposed command is not an executed test.
