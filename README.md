# otel

OpenTelemetry skills for Claude Code and Codex. One plugin, one skill tree, two client catalogs.

OpenTelemetry changes faster than a bundled manual. This plugin stores durable workflows, decision criteria and verification procedures; agents retrieve mutable facts from authoritative sources for the exact version in the project. It synthesizes OllyGarden's source-driven workflows with Dash0's useful instrumentation-quality checks. It is neither an upstream fork nor a concatenation of their Markdown.

## Design

Inspect repository/runtime versions before answering. Prefer tagged primary source over model memory, current docs over stale summaries, and observed telemetry over successful process exits. Latest available and validated compatible are different findings. No large configuration tables, package catalogs or semantic-convention inventories are bundled.

Retain telemetry by default. Sampling/filtering is intentional only when requested, never a cost optimisation. Fix pathological metric dimensions, Loki labels and operation names while retaining useful IDs in span/log context. Hashing IDs does not bound cardinality. Do not introduce secret capture; aggressive PII redaction is not the purpose of an instrumentation review.

Grafana Cloud is the usual backend, with current official Grafana lookup when backend behavior matters. The workflows remain vendor-neutral. Browser observability uses Faro outside this plugin; no browser OTel skill is provided. Dedicated language skills cover Go, Python and JavaScript/TypeScript on Node. Java, .NET and Ruby are intentionally excluded.

## Skills

| Skill | Responsibility |
| --- | --- |
| `otel-instrumentation` | Review or improve OpenTelemetry signal quality across traces, metrics and logs: correctness, propagation, correlation, cardinality, duplication and runtime overhead. |
| `otel-go` | Add, review or troubleshoot OpenTelemetry in Go services, including providers, contrib/manual instrumentation, propagation, logging, shutdown and allocation overhead. |
| `otel-python` | Add or debug OpenTelemetry in Python services, including FastAPI-style frameworks, async context, auto/manual instrumentation, structured logs and exporters. |
| `otel-js` | Instrument or troubleshoot JavaScript/TypeScript Node.js services: ESM/CJS startup, early loading, async context, auto/manual duplication, metrics and log correlation. Browser OTel is excluded. |
| `otel-collector` | Configure, review or diagnose OpenTelemetry Collector components and end-to-end pipelines against the exact distribution/version, including topology, reliability and Kubernetes. |
| `otel-collector-builder` | Assess and build custom OpenTelemetry Collector distributions with OCB, aligned component modules, local components and reproducible CI/container builds. |
| `otel-ottl` | Write, review or debug version-correct OTTL transformations, normalization, enrichment, routing and conversions; intentional filtering/redaction only when requested. |
| `otel-semantic-conventions` | Resolve OpenTelemetry attribute placement, span names/kinds/status, metric conventions and compliance using a narrowly queried released semantic-convention registry. |
| `otel-sdk-versions` | Resolve current OpenTelemetry releases and compatible version lines for Go, Python and Node packages while distinguishing installed, latest and validated versions. |
| `otel-upgrade` | Safely upgrade OpenTelemetry dependencies, Collector distributions or instrumentation with release-note analysis, compatibility checks and before/after telemetry evidence. |
| `otel-telemetry-emissions` | Determine which traces, metrics, logs and attributes a particular OpenTelemetry instrumentation package or Collector component actually emits at a selected version. |
| `otel-declarative-config` | Generate or review declarative OpenTelemetry SDK configuration using the schema and implementation support of the exact language/runtime parser. |
| `otel-telemetrygen` | Generate traces, metrics or logs for Collector/OTTL/pipeline verification or explicitly bounded load tests using the selected telemetrygen binary help. |
| `otel-span-events-to-logs-migration` | Assess whether current OpenTelemetry span-event/exception-to-log migration guidance applies to a project and implement a version-supported migration when appropriate. |
| `otel-weaver` | Use OpenTelemetry Weaver for semantic registry authoring, validation, templates/code generation, registry diffing and CI enforcement with current CLI/schema evidence. |

## Architecture

```text
plugin.meta.json                 canonical package metadata
sources.lock.json                synthesis provenance, not runtime knowledge
.claude-plugin/marketplace.json   generated Claude catalog
.agents/plugins/marketplace.json  generated Codex catalog
plugins/otel/
  plugin.json                    generated portable Agent Plugins manifest
  .claude-plugin/plugin.json     generated Claude compatibility manifest
  skills/*/SKILL.md               the only canonical skill implementation
  shared/                        source, preference, discovery and verification policies
  scripts/upstream.py            bounded public-source lookup
  evals/                         18 scenarios, graders and synthetic fixtures
tools/                           renderer and checker
tests/                           deterministic helper contract tests
.github/workflows/ci.yml         GitHub Actions running just check
```

Both catalogs resolve the same `./plugins/otel`. Codex reads the portable manifest directly; Claude reads its generated compatibility manifest. Shared links stay inside the plugin root and survive native caching. Packaging evidence and official references are in [standards.md](docs/standards.md).

## Fresh facts

Every skill begins with project discovery and shared source/observability/verification policies. Agents resolve installed package/component versions, fetch the corresponding official source and report provenance. The Python helper supports exact-ref file/tree lookup, bounded semantic-convention search, release information and individual npm/PyPI/Go package metadata. No proprietary credential is required and no cache is maintained. Output includes retrieval time, URL, requested ref/resolved commit and limitations. A failed tag never falls back silently to latest.

See [lookup-tools.md](plugins/otel/shared/lookup-tools.md). The semconv helper is a text-search aid, not a registry resolver. Follow referenced definitions and read the selected group. Static emission analysis is explicitly distinct from upstream specifications and runtime observations.

## Installation

Prerequisites: a current Claude Code or Codex CLI, Git and Python 3.11+ (the lookup helper and checks are dependency-free).

Claude Code:

```sh
claude plugin marketplace add rknightion/otel-instrumentation-skills
claude plugin install otel@otel --scope user
```

Codex:

```sh
codex plugin marketplace add rknightion/otel-instrumentation-skills
codex plugin add otel@otel
```

The marketplace and plugin are both named `otel`. Restart sessions after installation. Claude invokes `/otel:otel-go`; Codex can discover and invoke `otel-go` from the plugin. Read the loaded skill before using its shared references.

## Updates and versioning

Edit canonical content and plugin.meta.json. PATCH is normal guidance/source-workflow fixes; MINOR adds skills/capabilities or substantial compatible workflows; MAJOR breaks structure, invocation or behavior. Run `just render`; `just check` rejects stale manifests or mismatched versions. Bump the version whenever installed content changes because client caches use it.

```sh
claude plugin marketplace update otel
claude plugin update otel@otel --scope user
codex plugin marketplace upgrade otel
codex plugin add otel@otel
```

Explicit updates and fresh sessions are the verified path; a running session does not prove new content loaded.

## Tests and evals

`just check` runs JSON/frontmatter/inventory checks, deterministic manifest comparison, portable field/version checks, internal links, stale-knowledge lint, Python syntax/contract tests and eval fixture checks. It also invokes Claude native validation when available, explicitly reporting a skip otherwise. GitHub Actions runs `just check` on every push and pull request; it does not perform authenticated live model evals.

For a full official portable-schema check, fetch the schema URL in plugin.json and validate with a JSON Schema implementation. Installed Codex 0.155.1 has no separate plugin validator: native marketplace/add/list plus fresh-session loading is its integration gate. The bundled legacy plugin-creator validator requires a compatibility file and is not the validator for this portable-only Codex package.

The 18 cases in [corpus.json](plugins/otel/evals/corpus.json) have explicit pass/fail criteria. They cover Go review/upgrade, Python/Node setup, semconv, propagation, duplicate instrumentation, dimension/label hygiene, Collector/OTTL, emissions, telemetrygen, default retention, explicit sampling and browser exclusion. Fixtures intentionally contain defects; their versions are test inputs, never recommendations.

```sh
just eval no-sampling
claude plugin eval ./plugins/otel --runs 1 --judge-model opus --trust-plugin --scaffold --allow-tools WebFetch WebSearch --no-publish --output-dir .local/evals/all
```

The LLM grader uses `focus: trace` (the native judge sees the first and last 12 messages, not every middle message); use full local transcripts when auditing omitted evidence. The documented recipe uses Opus for the nuanced rubric. The native runner seeds identical fixtures in both arms, starts fresh sessions and grades tool/output evidence. Default ablation compares with/without the plugin. One run is smoke evidence, not statistical proof of improvement; use at least three runs for a meaningful comparison. Models/providers, case IDs, artifact revision and both-arm results must be recorded. Keep raw transcripts local and publish sanitized summaries only. Web-only evals intentionally cannot establish compile/runtime delivery. Separate installed-profile sessions prove native discovery and shared-file access. For implementation evals, use authorized disposable workspaces with Bash permissions and real telemetry sinks; do not label advisory evals as live telemetry proof.

Native eval scores and their limitations are recorded in [validation.md](docs/validation.md) and [evaluations.json](docs/evaluations.json).

## Provenance and acknowledgements

This skill set is independently written, but it owes a clear debt to two Apache-2.0 projects:

- [OllyGarden's OpenTelemetry Agent Skills](https://github.com/ollygarden/opentelemetry-agent-skills): the shape of the skill set and fourteen of the fifteen skill names follow its catalogue, as does the source-driven method of resolving versions and retrieving tagged upstream source rather than bundling facts.
- [Dash0's Agent Skills](https://github.com/dash0hq/agent-skills): the `otel-instrumentation` skill and the signal-quality review ideas (cardinality, propagation, duplication, correlation) build on its instrumentation and pipeline review checks.

No skill prose, code or generated inventory was copied from either project. [sources.lock.json](sources.lock.json) records the exact upstream commits that were inspected, and [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) states the relationship in full. Upstream changes are reviewed for durable improvements, not imported. Apache-2.0 is the project licence.

## Troubleshooting

- New skill missing: verify catalog registration, enabled plugin, cache version and a fresh session. Relative paths start at the loaded skill file, not project cwd.
- Lookup fails/rate limits: use exact tagged official source or report the missing evidence. No invented defaults or automatic latest fallback.
- Eval sandbox cannot exclude existing credential paths: use read/WebFetch/WebSearch-only evals as supplied, or repair the independently owned local configuration. Do not weaken sandbox protections or claim runtime validation.
- Older OTel skill conflict: install and functionally verify otel first, then disable only the conflicting OTel plugin or skill. Preserve unrelated tools.

## Updating the OTel plugin with a coding agent

Copy this complete prompt into a capable coding agent:

```text
Update this otel plugin end-to-end. Read AGENTS.md, README.md, docs/standards.md, the architecture, shared policies, renderer and evals before changing anything. Read sources.lock.json and record its before commits.

Fetch the latest default branches of https://github.com/ollygarden/opentelemetry-agent-skills and https://github.com/dash0hq/agent-skills into temporary checkouts outside the repository. Compare each against the exact recorded commit; inspect meaningful changed areas rather than copying their trees. Verify their licences/notices and research current authoritative OpenTelemetry sources for changed technical guidance.

Preserve the architecture: one canonical skill tree; durable workflows, preferences and verification procedures locally; mutable facts retrieved at invocation for the project's actual versions. Preserve telemetry by default, with no cost-driven sampling/filtering. Keep cardinality hygiene: no UIDs/request IDs in metric dimensions or Loki stream labels, stable operation names, useful identifiers retained as structured span/log context. PII redaction is not the primary goal, and secrets must never be captured. Grafana Cloud is the usual backend but behavior must be researched; Faro owns browser observability. Dedicated languages remain Go, Python and JS/TS Node only. Preserve exclusions of Java/.NET/Ruby/browser OTel and all Dash0-specific products, endpoints, auth, operators and derived attributes.

Integrate new upstream capabilities only if they improve this plugin. Remove obsolete guidance, keep shared policies and the skill tree DRY, and keep large mutable tables out. Update sources.lock.json with before/after provenance and accurate inspection dates. If any upstream text or code is copied, keep its licence and copyright notice, mark the changed files and update THIRD_PARTY_NOTICES.md and the README acknowledgements to say exactly what was copied.

Run deterministic tests, static validation, freshness lint, internal links and eval fixture checks. Run representative live evals with the same fixtures and model/provider in with/without arms; record failures, unrun cases and runtime limits honestly. Render/check packaging manifests from plugin.meta.json, validate native Claude and portable/Codex behavior, and bump PATCH/MINOR/MAJOR appropriately. Document meaningful changes and test evidence. Do not change unrelated infrastructure or config.

Finish with upstream commits before/after, meaningful guidance changes, changed files, static/native/live tests and eval results, remaining genuine blockers and the final commit/version. Do not stop at a plan or claim completion with unexplained unverified checks.
```
