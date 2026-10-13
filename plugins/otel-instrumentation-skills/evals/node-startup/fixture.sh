#!/bin/bash
set -euo pipefail
python3 - <<'OTEL_FIXTURE'
from pathlib import Path
import json
files = json.loads('{"package.json": "{\\n  \\"name\\": \\"otel-node-eval\\",\\n  \\"private\\": true,\\n  \\"type\\": \\"module\\",\\n  \\"engines\\": {\\n    \\"node\\": \\">=20\\"\\n  },\\n  \\"scripts\\": {\\n    \\"start\\": \\"node server.js\\"\\n  },\\n  \\"dependencies\\": {\\n    \\"@opentelemetry/api\\": \\"1.9.0\\",\\n    \\"@opentelemetry/sdk-node\\": \\"0.57.2\\"\\n  }\\n}\\n", "server.js": "import http from \'node:http\';\\n// SDK is loaded too late; intentional review fixture.\\nawait import(\'./telemetry.js\');\\nhttp.createServer((req,res) => res.end(\'ok\')).listen(8080);\\n", "telemetry.js": "// Empty intentionally: determine startup and package support before implementing.\\n"}')
for name, text in files.items():
    Path(name).write_text(text)
OTEL_FIXTURE
