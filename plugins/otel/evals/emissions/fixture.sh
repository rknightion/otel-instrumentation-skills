#!/bin/bash
set -euo pipefail
python3 - <<'OTEL_FIXTURE'
from pathlib import Path
import json
files = json.loads('{"config.yaml": "receivers:\\n  otlp:\\n    protocols:\\n      http:\\n        endpoint: 127.0.0.1:4318\\nprocessors:\\n  transform:\\n    error_mode: ignore\\n    trace_statements:\\n      - context: span\\n        statements:\\n          - set(attributes[\\"app.original_name\\"], name)\\nexporters:\\n  debug:\\n    verbosity: detailed\\nservice:\\n  pipelines:\\n    traces:\\n      receivers: [otlp]\\n      processors: [transform]\\n      exporters: [debug]\\n", "identity.json": "{\\"distribution\\": \\"otel/opentelemetry-collector-contrib\\", \\"version\\": \\"0.120.0\\", \\"deployed\\": \\"fixture only; not a live deployment\\"}\\n"}')
for name, text in files.items():
    Path(name).write_text(text)
OTEL_FIXTURE
