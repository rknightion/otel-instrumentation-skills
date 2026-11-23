set shell := ["bash", "-euo", "pipefail", "-c"]

# Python 3.15 is the floor, pinned in .python-version. python3 on PATH must be 3.15
# or newer. Elsewhere: PYTHON="uv run --no-project python" just check
py := env("PYTHON", "python3")

# List supported tasks.
default:
    @just --list

# Verify the dependency-free Python 3.15 runtime.
setup:
    {{ py }} -c 'import sys; assert sys.version_info >= (3, 15)' || { echo "Python 3.15 or newer is required: install it with 'brew install python@3.15' or 'uv python install 3.15', then run PYTHON=\"uv run --no-project python\" just <recipe>" >&2; exit 1; }

# Format generated metadata.
[group('gen')]
fmt: render

# Check deterministic formatting.
[group('check')]
fmt-check: setup
    {{ py }} tools/render_manifests.py --check
    {{ py }} tools/render_evals.py --check

# Validate structure, freshness policy and executable helpers.
[group('check')]
lint: setup
    {{ py }} tools/check.py

# Run deterministic contract tests.
[group('check')]
test: setup
    {{ py }} -m unittest discover -s tests -v

# Run the complete local gate.
[group('check')]
check: setup
    {{ py }} tools/check.py

# Generate client manifests from canonical metadata.
[group('gen')]
render: setup
    {{ py }} tools/render_manifests.py
    {{ py }} tools/render_evals.py

# Run a native live Claude eval with baseline comparison.
[group('check')]
eval case="no-sampling":
    claude plugin eval ./plugins/otel-instrumentation-skills --case '{{ case }}' --runs 1 --judge-model opus --trust-plugin --scaffold --allow-tools WebFetch WebSearch --no-publish --output-dir .local/evals/{{ case }}

