# Packaging research, 2026-09-19

Inspected with Claude Code 2.1.278, Codex CLI 0.155.1. CLI help is the authority for command spelling on these installations: Codex uses `plugin add`, not `plugin install`. Claude has `plugin validate`, `plugin details` and `plugin eval`; Codex has no standalone plugin validation command in this release. Native add/list plus fresh-session discovery provide its integration check.

Authoritative sources read before packaging:

- [Claude plugins](https://code.claude.com/docs/en/plugins-reference): `.claude-plugin/plugin.json`, plugin-root containment, shared resources and native validation.
- [Claude marketplaces](https://code.claude.com/docs/en/plugin-marketplaces): Git/SSH private sources, relative plugin sources, authentication and update behavior.
- [Claude plugin evals](https://code.claude.com/docs/en/plugin-evals): isolated fresh sessions, scaffold fixtures, graders and with/without-plugin arms.
- [OpenAI packaging](https://developers.openai.com/plugins/build/plugins): portable root `plugin.json`, compatibility fallback, Git-backed marketplaces and CLI add/upgrade.
- [Codex skills](https://developers.openai.com/codex/skills): skill discovery and progressive disclosure.
- [Agent Plugins 1.0](https://agent-plugins.org/specification): fixed `skills/` discovery, portable schema, containment and extension namespaces.
- [Agent Skills specification](https://agentskills.io/specification): frontmatter, name/description constraints and supporting resources.

Decision: root portable manifest plus Claude compatibility manifest. No Codex compatibility copy is needed on the tested version. Both catalogs resolve `./plugins/otel-instrumentation-skills`; the complete plugin is cached, including shared/ and scripts/. Shared references climb from a skill folder to this plugin root only. Native sessions must demonstrate actual reads before deployment acceptance.

Versioned metadata lives only in plugin.meta.json. tools/render_manifests.py renders the portable/Claude manifests and both catalogs. Codex catalog has no duplicated plugin version: it reads the manifest. All fields that carry a version must match exactly.

The repository is a public GitHub marketplace, so installation needs no authentication. Explicit refresh commands are the reliable maintenance path. Codex marketplace upgrade refreshes its Git snapshot; plugin add refreshes/enables the chosen plugin. Existing sessions need restarting to load updated skills.

The bundled plugin-creator validator currently assumes a `.codex-plugin/plugin.json` compatibility file. For this intentionally simplified portable package, validate the official root schema and native Codex installation instead; do not add an unused manifest merely to satisfy that older helper.
