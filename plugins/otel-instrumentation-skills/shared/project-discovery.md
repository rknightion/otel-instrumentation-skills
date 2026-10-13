# Project discovery
Read repository instructions and inspect the requested scope without exposing secrets. Capture a compact evidence ledger: item, declared constraint, resolved version, runtime/deployed version, source of evidence, unknowns.

- Go: go.mod/go.sum, workspaces, replace directives and resolved module graph. Distinguish core, logs, exporters, contrib, wrappers and build-time instrumentation.
- Python: pyproject.toml, uv.lock/poetry.lock/requirements files, active environment and installed distributions. Distinguish SDK, instrumentation, distro, exporters and runtime compatibility.
- Node: package.json and the actual npm/pnpm/yarn/bun lockfile; resolved packages, Node runtime, engines, ESM/CJS, build output and production startup/preload command. A declared range is not an installed version.
- Deployment: Dockerfiles/image digests, Helm values/chart versions, Kubernetes manifests/Operator CRDs, Terraform, Collector config, OCB manifests, enabled feature gates and environment variable NAMES. Never print secret values. Check binary help/version and deployed image when access is authorized.

Locate existing providers, auto-instrumentation, interceptors/middleware, propagation boundaries, exporters, log bridges and shutdown owners before adding another. Resource identity describes the emitting entity; operation context describes one request. Trace the actual signal path through Collector and backend, including enrichment and promotion into dimensions. Unknown deployment state remains unknown; source configuration alone does not prove what is running.
