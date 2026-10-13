# Validation and deployment evidence

Verification date: 2026-09-19. This report separates installation, source-based agent behavior, static checks and runtime telemetry. It is not a claim that every generated OTel recommendation is correct or production-validated.

The evidence below was gathered on version `1.0.3`, before publication on GitHub, when the plugin and marketplace were named `otel` and lived at `plugins/otel`. Version 2.0.0 renamed them to `otel-instrumentation-skills`; the skill content is otherwise unchanged.

## Deterministic and native checks

- `just check`: JSON, 15 Agent Skills frontmatters/inventory, generated manifests/evals, version consistency, internal links, freshness lint, Python syntax, helper contract tests and Claude native repository/plugin validation.
- Official Agent Plugins JSON Schema validation passed. All 15 skills passed the Agent Skills creator validator. The older Codex-only creator helper expects a redundant compatibility file, so native portable installation is the integration gate instead.
- Live lookup helper checks retrieved tagged Go source, released semconv snippets and exact npm/PyPI/Go package metadata. No proprietary public-lookup token or persistent lookup cache is required.
- CI runs the same `just check` and explicitly skips native Claude validation where Claude is not installed; its structural/contract checks still run.
- Tests were not added for Markdown/configuration edits; those were structurally validated and exercised through the native clients.

## Native eval history

| Suite | With-plugin passed | Cases | Interpretation |
| --- | ---: | ---: | --- |
| no-sampling-web | 0 | 1 | With/without comparison |
| v1.0.1-all | 2 | 18 | Single-arm smoke |
| browser-judge-check | 1 | 1 | Single-arm smoke |
| v1.0.2-all | 10 | 18 | Single-arm smoke |
| v1.0.2-baseline | 1 | 1 | With/without comparison |
| v1.0.3-all | 7 | 18 | Single-arm smoke |
| v1.0.3-opus | 13 | 18 | Single-arm smoke |

Final-version failed cases: `metric-uid`, `node-startup`, `ottl-current`, `propagation`, `python-fastapi`. These scores are not rewritten based on manual acceptance tests.

The grader now receives `focus: trace`. The client only exposes the first and last 12 messages to that LLM judge, so omitted middle evidence can still affect scores. Earlier suites used the judge alias `sonnet`; the final unchanged-artifact rerun uses `opus`. The CLI has no regrade-only option, so the new run also regenerates agent answers and cannot isolate the judge effect. Recorded agent output uses `claude-opus-5[1m]`, with Haiku used by internal summarizing calls. Each case had one run. These are smoke results, not a statistical reliability estimate. All cases were advisory/read-only with real source lookup; none proves compilation or production delivery.

The v1.0.2 browser-exclusion comparison used identical fixtures: with-plugin 1.0, without-plugin 0.0, delta +1.0. This demonstrates the intended browser/Faro routing preference in that one run only. It does not establish a broad performance improvement. The initial default-judge/no-sampling comparison and its failed attempt to grant shell access are retained locally; neither is represented as a successful runtime test.

Earlier failures included unsupported package/lifecycle details, recommendations with unresolved syntax and cardinality conflation. Version 1.0.3 adds a claim/evidence ledger, prohibits unverified copy-paste recipes, distinguishes metric-series identity from span operation names, and protects existing OTTL destination context. The lookup allowance increased from four to eight targeted sources because upgrades and embedding-component checks can require multiple authoritative files. Pass criteria were not relaxed.

Raw native eval reports and transcripts remain under `.local/` and are deliberately uncommitted. [evaluations.json](evaluations.json) retains sanitized scores, run identity and artifact hashes. Failed cases remain failures; a model's self-reported acceptance is not substituted for the native score.

### Review of the five final Opus failures

These observations come from reviewing the answer evidence, not invented explanations for the judge votes (the native report exposes votes, not a detailed causal justification).

| Case | Remaining answer-quality issue |
| --- | --- |
| `metric-uid` | Recommends a newer HTTP attribute set while its own source analysis says this instrumentation emits the older metric conventions. The useful UID/structured-context distinction is present, but the version-specific recommendation is inconsistent. |
| `node-startup` | Prescribes a loader/startup recipe while declaring built-in module patching unresolved; this exceeds the verified compatibility evidence. |
| `ottl-current` | Adds an optional semantic attribute using a convention version not established for the producer, and leaves route-shape/regex behavior untested. |
| `propagation` | Describes newly created SDK root traces before also establishing that this fixture has no registered provider; the chosen semconv release is explicitly not proven to be the embedded one. |
| `python-fastapi` | Recommends an upgrade and expected exporter pin while compatibility and exporter metadata remain unresolved. |

These failures remain open quality limitations, not installation failures. The plugin's policies explicitly prohibit these forms of unsupported recommendation, but the smoke runs show that instructions alone do not ensure compliance. Do not auto-apply an answer merely because it cites a tagged URL; require the claim/evidence ledger and the validation stages appropriate to the actual change. No claim of a fully green native quality suite or statistically demonstrated general improvement is made.

## Isolated Collector/telemetrygen runtime

An isolated host ran an ephemeral, network-isolated Collector with a local debug sink. Config parser validation succeeded. `telemetrygen traces --help` was captured before constructing the command. Three generated traces with one child each produced six observed spans; all six retained `app.original_name` equal to their original name. No sampling/filtering/backend endpoint was introduced. The disposable container was stopped and removed; no persistent service/config was changed.

Important identity boundary: image `otel/opentelemetry-collector-contrib:0.120.0` at digest `sha256:85ac41c2db88d0df9bd6145e608a3cb023f5d8443868adbfbbf66efb51087917` reports binary **0.120.1**. This is evidence for that observed binary, not an exact-0.120.0 runtime claim. Telemetrygen image tag `v0.120.0`, digest `sha256:a3f9c33736c8150796956ee9dc34039b3ba1a0c6c10c96489c35a1e8836a98a5`.

The initial substring counter counted two startup diagnostics as span occurrences; inspecting per-span output corrected the count to six. Raw output and corrected assertions are retained locally. The test covers successful trace delivery through an additive OTTL transform only: absent/wrong-type cases, metrics/log runtime paths, exporter failures, load behavior and backend receipt were not exercised. The text parser is a test-specific observation, not a stable debug-exporter interface contract.

## Maintenance

Maintenance starts with the complete prompt under [Updating the OTel plugin with a coding agent](../README.md#updating-the-otel-plugin-with-a-coding-agent). Keep red evals visible, review generated claims against their exact sources, and require real before/after telemetry before claiming production correctness.
