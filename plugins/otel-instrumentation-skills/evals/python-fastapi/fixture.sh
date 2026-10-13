#!/bin/bash
set -euo pipefail
python3 - <<'OTEL_FIXTURE'
from pathlib import Path
import json
files = json.loads('{"app.py": "from fastapi import FastAPI\\napp = FastAPI()\\n@app.get(\\"/orders/{order_id}\\")\\nasync def order(order_id: str):\\n    return {\\"id\\": order_id}\\n", "pyproject.toml": "[project]\\nname = \\"otel-python-eval\\"\\nversion = \\"0.1.0\\"\\nrequires-python = \\">=3.11\\"\\ndependencies = [\\"fastapi==0.115.6\\", \\"opentelemetry-api==1.29.0\\", \\"opentelemetry-sdk==1.29.0\\"]\\n"}')
for name, text in files.items():
    Path(name).write_text(text)
OTEL_FIXTURE
