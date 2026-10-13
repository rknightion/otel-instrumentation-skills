set shell := ["bash", "-euo", "pipefail", "-c"]

# List supported tasks.
default:
    @just --list

# Verify the dependency-free Python runtime.
setup:
    python3 -c 'import sys; assert sys.version_info >= (3, 11)'

# Format generated metadata.
[group('gen')]
fmt: render

# Check deterministic formatting.
[group('check')]
fmt-check:
    python3 tools/render_manifests.py --check
    python3 tools/render_evals.py --check

# Validate structure, freshness policy and executable helpers.
[group('check')]
lint:
    python3 tools/check.py

# Run deterministic contract tests.
[group('check')]
test:
    python3 -m unittest discover -s tests -v

# Run the complete local gate.
[group('check')]
check:
    python3 tools/check.py

# Generate client manifests from canonical metadata.
[group('gen')]
render:
    python3 tools/render_manifests.py
    python3 tools/render_evals.py

# Run a native live Claude eval with baseline comparison.
[group('check')]
eval case="no-sampling":
    claude plugin eval ./plugins/otel-instrumentation-skills --case '{{ case }}' --runs 1 --judge-model opus --trust-plugin --scaffold --allow-tools WebFetch WebSearch --no-publish --output-dir .local/evals/{{ case }}

