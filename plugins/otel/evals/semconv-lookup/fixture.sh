#!/bin/bash
set -euo pipefail
python3 - <<'OTEL_FIXTURE'
from pathlib import Path
import json
files = json.loads('{"go.mod": "module example.com/otel-eval\\n\\ngo 1.23\\n\\nrequire (\\n go.opentelemetry.io/otel v1.32.0\\n go.opentelemetry.io/otel/sdk v1.32.0\\n go.opentelemetry.io/otel/metric v1.32.0\\n go.opentelemetry.io/otel/trace v1.32.0\\n go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp v0.57.0\\n)\\n", "main.go": "package main\\nimport (\\n \\"context\\"\\n \\"net/http\\"\\n \\"go.opentelemetry.io/otel\\"\\n \\"go.opentelemetry.io/otel/attribute\\"\\n \\"go.opentelemetry.io/contrib/instrumentation/net/http/otelhttp\\"\\n)\\n// Deliberately flawed review fixture; initialization and flushing are missing.\\nfunc handler(w http.ResponseWriter, r *http.Request) {\\n ctx, span := otel.Tracer(\\"checkout\\").Start(context.Background(), \\"GET \\" + r.URL.Path)\\n defer span.End()\\n uid := r.Header.Get(\\"X-User-ID\\")\\n span.SetAttributes(attribute.String(\\"app.user_id\\", uid))\\n counter, _ := otel.Meter(\\"checkout\\").Int64Counter(\\"requests\\")\\n _ = counter\\n _ = ctx // async/outbound calls below would lose this context\\n w.WriteHeader(200)\\n}\\nfunc main() { http.ListenAndServe(\\":8080\\", otelhttp.NewHandler(http.HandlerFunc(handler), \\"checkout\\")) }\\n", "review-notes.md": "Assume the real workload also records app.user_id on every metric measurement and starts a second manual HTTP server span inside the already instrumented middleware. Review; do not run this incomplete fixture as a production service.\\n"}')
for name, text in files.items():
    Path(name).write_text(text)
OTEL_FIXTURE
