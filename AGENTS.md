# otel-instrumentation-skills
One canonical plugin lives in plugins/otel-instrumentation-skills. Read README.md and sources.lock.json first.
Encode durable decisions; fetch mutable OTel facts at invocation. Preserve telemetry by default.
Do not copy upstream skill trees. If upstream text or code is ever copied, update THIRD_PARTY_NOTICES.md and the README acknowledgements in the same change.
Change plugin.meta.json and run just render for metadata.
Public GitHub repository rknightion/otel-instrumentation-skills: main is the delivery branch. Keep credentials, machine-local state, host names and home paths out; installation and deployment for any particular machine belong outside this repository.
## Task interface
Run just check before committing. Run live evals for meaningful workflow changes and report untested boundaries.

## Cursor Cloud specific instructions

The base image supplies `just`. The floor is Python 3.15, pinned in `.python-version`.
`just setup` checks that `python3` is 3.15 or newer and installs no dependencies;
where the image's `python3` is older, run recipes as
`PYTHON="uv run --no-project python" just <recipe>`.

- Fast check: `just fmt-check`
- Full repository gate: `just check`

The structural checks run offline. The gate reports a skip for native plugin
validation when the Claude CLI is unavailable. Use an environment with network
access for live source lookups and with an authenticated Claude CLI for live evals.
