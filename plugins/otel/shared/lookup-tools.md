# Fresh lookup helper

Requires Python 3.11+ standard library and network access. Resolve the installed plugin root from this file, not the project working directory. Run `python3 <plugin-root>/scripts/upstream.py --help`.

Commands (replace uppercase placeholders with inspected identities):

```sh
python3 <plugin-root>/scripts/upstream.py release --repo open-telemetry/semantic-conventions
python3 <plugin-root>/scripts/upstream.py tree --repo open-telemetry/opentelemetry-collector-contrib --ref TAG --match COMPONENT
python3 <plugin-root>/scripts/upstream.py file --repo open-telemetry/opentelemetry-collector-contrib --ref TAG --path VERIFIED_PATH --match TERM
python3 <plugin-root>/scripts/upstream.py semconv --ref RELEASE_TAG --domain http --term route
python3 <plugin-root>/scripts/upstream.py package npm PACKAGE --version VERSION
python3 <plugin-root>/scripts/upstream.py package pypi PACKAGE --version VERSION
python3 <plugin-root>/scripts/upstream.py package go MODULE --version VERSION
```

The helper queries public GitHub/registry endpoints without credentials. Exact-file/tree/semconv queries require an explicit ref and resolve it to a commit. Package queries without a version discover registry latest, not validated compatibility. Repository releases do not enumerate every module line. Use verified module-specific tags/changelogs as necessary.

No cache or hidden mutable state exists. Output identifies live retrieval time, URL, tag/commit and search limits. Semconv is a bounded text lookup, not a YAML resolver: follow references and retrieve the complete relevant group before giving a recommendation. A failed/missing tag is an error, never a fallback to main/latest. Rate limits or unavailable networking require an explicit limitation and a tagged-source/official-doc fallback, not invented facts. For broad investigations use a temporary upstream checkout outside this plugin rather than increasing context indiscriminately.
