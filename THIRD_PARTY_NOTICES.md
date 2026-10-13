# Third-party notices

Copyright 2026 Rob Knight. Licensed under Apache-2.0; see LICENSE.

This skill set is independently written. It was designed after inspecting two Apache-2.0 projects at the commits recorded in [sources.lock.json](sources.lock.json):

- OllyGarden, OpenTelemetry Agent Skills, https://github.com/ollygarden/opentelemetry-agent-skills, commit `27c9817904ce1b4db697f443809cf2b2f169b1fe`. Copyright OllyGarden and its contributors.
- Dash0, Agent Skills, https://github.com/dash0hq/agent-skills, commit `b809d934546a57c740b567014f5a0c67b906ebb5`. Copyright Dash0 and its contributors.

## What was taken from each

From OllyGarden: the overall catalogue and decomposition into skills. Fourteen of the fifteen skill names here match skill names in that project (`otel-collector`, `otel-collector-builder`, `otel-declarative-config`, `otel-go`, `otel-js`, `otel-ottl`, `otel-python`, `otel-sdk-versions`, `otel-semantic-conventions`, `otel-span-events-to-logs-migration`, `otel-telemetry-emissions`, `otel-telemetrygen`, `otel-upgrade`, `otel-weaver`), as does the method of resolving the project's exact versions and retrieving tagged upstream source instead of bundling facts.

From Dash0: the `otel-instrumentation` skill name and the instrumentation-quality and pipeline review ideas it applies (cardinality, propagation, duplication, correlation and overhead checks).

## What was not taken

No skill prose, code, eval, fixture or generated inventory from either project is included. This was checked by comparing every file in this repository against both upstream trees at the commits above: no run of more than seven consecutive words in the skills, and none beyond generic Collector configuration and Python boilerplate elsewhere, matches upstream text. Dash0-specific products, endpoints, authentication, operators and derived attributes are deliberately excluded.

Because no upstream material is redistributed, neither project's licence text or notices are required here; they are credited because the design depends on them. Neither repository carried a NOTICE file at the inspected commit. The Apache-2.0 licence text in LICENSE is the standard text, reproduced from the OllyGarden licence file.

If upstream text or code is ever copied in, keep its copyright and licence notice with it, mark the modified files and record exactly what was copied in this file.
