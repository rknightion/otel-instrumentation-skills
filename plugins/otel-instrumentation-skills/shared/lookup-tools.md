# Fresh lookup helper

Requires the Python 3.15 standard library and network access. Resolve the installed plugin root from this file, not the project working directory. Run `sh <plugin-root>/scripts/upstream.sh --help`. The launcher uses `python3.15` on PATH, then the Homebrew locations, then a 3.15 that uv resolves from a neutral directory, never the project's own environment. With none of them it exits 1 and names how to install 3.15; report the helper as unavailable, state that as a limitation and use tagged source or official docs, never remembered versions.

Commands (replace uppercase placeholders with inspected identities):

```sh
sh <plugin-root>/scripts/upstream.sh release --repo open-telemetry/semantic-conventions
sh <plugin-root>/scripts/upstream.sh tree --repo open-telemetry/opentelemetry-collector-contrib --ref TAG --match COMPONENT
sh <plugin-root>/scripts/upstream.sh file --repo open-telemetry/opentelemetry-collector-contrib --ref TAG --path VERIFIED_PATH --match TERM
sh <plugin-root>/scripts/upstream.sh semconv --ref RELEASE_TAG --domain http --term route
sh <plugin-root>/scripts/upstream.sh package npm PACKAGE --version VERSION
sh <plugin-root>/scripts/upstream.sh package pypi PACKAGE --version VERSION
sh <plugin-root>/scripts/upstream.sh package go MODULE --version VERSION
```

The helper queries public GitHub/registry endpoints without credentials. Exact-file/tree/semconv queries require an explicit ref and resolve it to a commit. Package queries without a version discover registry latest, not validated compatibility. Repository releases do not enumerate every module line. Use verified module-specific tags/changelogs as necessary.

No cache or hidden mutable state exists. Output identifies live retrieval time, URL, tag/commit and search limits. Semconv is a bounded text lookup, not a YAML resolver: follow references and retrieve the complete relevant group before giving a recommendation. A failed/missing tag is an error, never a fallback to main/latest. Rate limits or unavailable networking require an explicit limitation and a tagged-source/official-doc fallback, not invented facts. For broad investigations use a temporary upstream checkout outside this plugin rather than increasing context indiscriminately.
