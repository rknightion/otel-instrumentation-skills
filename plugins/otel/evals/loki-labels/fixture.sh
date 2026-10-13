#!/bin/bash
set -euo pipefail
python3 - <<'OTEL_FIXTURE'
from pathlib import Path
import json
files = json.loads('{"mapping.json": "{\\"structured_log\\": {\\"user_id\\": \\"u-123\\", \\"request_id\\": \\"r-456\\", \\"message\\": \\"checkout completed\\"}, \\"proposed_stream_labels\\": [\\"service\\", \\"user_id\\", \\"request_id\\"], \\"backend\\": \\"Grafana Cloud Loki\\", \\"backend_version\\": \\"unknown\\"}\\n"}')
for name, text in files.items():
    Path(name).write_text(text)
OTEL_FIXTURE
