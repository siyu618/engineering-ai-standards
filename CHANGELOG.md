# Changelog

All notable changes to this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.4.0] - 2026-07-28

### Added

- `evaluations/runner/evaluator.py` — Executable evaluation engine with 3 modes: rule-based keyword scoring, LLM-as-Judge prompt generation, human review
- `evaluations/runner/scorecard.py` — Score tracking and regression detection with CI gating
- `runtime/` — Agent runtime concepts (context-management, memory-policy, tool-policy, verification-loop)
- 12 new architecture-level skills (system-design, distributed-system, database-design, api-design, security-review, production-readiness, incident-response, ai-agent-design, rag-design, mcp-development, llm-evaluation, agent-memory)
- `docs/adr/006-evaluation-platform.md` — ADR for executable evaluation engine
- `docs/adr/007-agent-runtime-model.md` — ADR for agent runtime model
- Registry now tracks per-skill compatibility (claude/cursor/copilot), latest_score, and last_run

### Changed

- `registry/skills.yaml` — Expanded from 5 to 17 skills with compatibility, latest_score, last_run fields
- `README.md` — Added runtime/, updated skill count to 17, added evaluator tool references
- `AGENTS.md` — Added runtime reference and evaluator usage instructions

## [1.3.0] - 2026-07-28

### Added

- `registry/skills.yaml` — Central machine-readable skill registry with versions, owners, dependencies, and evaluation thresholds
- `skills/*/metadata.yaml` — Per-skill metadata extracted from SKILL.md frontmatter
- `skills/*/examples/` — Usage examples for each skill (payment system design, refactoring, test strategy, review output, support agent)
- `skills/*/eval/` — Restructured evaluation directory with separate files per case and per-skill README
- `workflows/` — Workflow orchestration layer composing multiple skills:
  - `feature-development.md` — Feature development lifecycle
  - `bug-fix.md` — Bug fix process
  - `architecture-review.md` — Architecture review workflow
  - `production-incident.md` — Incident response workflow
- `governance/` — Governance layer:
  - `ownership.md` — Skill ownership table and responsibilities
  - `review-policy.md` — Change classification (patch/minor/major/breaking) with review requirements
  - `release-process.md` — Semantic versioning and release checklist
- `docs/adr/004-skill-registry.md` — ADR for centralized registry
- `docs/adr/005-governance-model.md` — ADR for governance model
- `.github/workflows/markdown-validation.yml` — Renamed from validate.yml, updated for new directories
- `.github/workflows/skill-evaluation.yml` — Renamed from evaluate.yml, enhanced with changed-skill detection, registry validation, and metadata checks

### Changed

- `evaluations/runner/run.py` — Added `--registry` flag for registry consistency validation
- `evaluations/schema.yaml` — Added `threshold` field support
- `README.md` — Updated architecture diagram and repository structure for v1.3 layers
- `AGENTS.md` — Updated architecture line to include Workflows and Governance
- `CONTRIBUTING.md` — Added workflow and governance sections
- Skills enriched: each module now has metadata.yaml, examples/, and eval/ subdirectory
- CI workflows renamed for clarity (validate.yml → markdown-validation.yml, evaluate.yml → skill-evaluation.yml)

## [1.2.0] - 2026-07-28

## [1.2.0] - 2026-07-28

### Added

- `skills/design/` — Module with SKILL.md (YAML frontmatter), CHANGELOG.md, eval.yaml
- `skills/python-development/` — Module with SKILL.md (YAML frontmatter), CHANGELOG.md, eval.yaml
- `skills/testing/` — Module with SKILL.md (YAML frontmatter), CHANGELOG.md, eval.yaml
- `skills/code-review/` — Module with SKILL.md (YAML frontmatter), CHANGELOG.md, eval.yaml
- `skills/ai-agent-development/` — Module with SKILL.md (YAML frontmatter), CHANGELOG.md, eval.yaml
- `AGENTS.md` — Generic AI agent entry-point at repository root
- `evaluations/README.md` — Evaluation philosophy documentation (Skill=Code model)
- `evaluations/schema.yaml` — Evaluation case schema definition
- `evaluations/runner/run.py` — Python validation runner for evaluation cases
- `evaluations/runner/judge_prompt.md` — LLM-judge evaluation prompt template
- `evaluations/cases/system-design/` — Standardized evaluation cases (cache, wallet, agent, testing)
- `evaluations/cases/coding/` — Standardized evaluation cases (python-refactor, code-review, ai-agent-eval)
- `docs/adr/001-three-layer-architecture.md` — Architecture decision record
- `docs/adr/002-skill-versioning.md` — Skill versioning ADR
- `docs/adr/003-evaluation-framework.md` — Evaluation framework ADR

### Changed

- Restructured 5 flat skill files into independent modules with YAML frontmatter metadata
- Evaluation YAMLs standardized to `expected.must_include` + `expected.forbidden` + 4-dimension scoring
- `adapters/claude/CLAUDE.md` streamlined to identity + workflow + references (entry-point only)
- `.github/workflows/evaluate.yml` updated to use `evaluations/runner/run.py`
- `.github/workflows/validate.yml` updated to check new directories and doc paths

### Removed

- `skills/design.md`, `skills/python-development.md`, `skills/testing.md`, `skills/code-review.md`, `skills/ai-agent-development.md` (replaced by modules)
- Old evaluation YAMLs under `evaluations/system-design/` and `evaluations/coding/` (moved to `evaluations/cases/`)

## [1.1.0] - 2026-07-28

## [1.0.0] - 2026-07-28

### Added

- Initial release of Engineering AI Standards
- `principles/engineering-principles.md` — Core engineering philosophy
- `standards/coding/general.md` — General coding standards
- `standards/coding/python.md` — Python-specific coding standards
- `standards/testing/testing.md` — Testing standards
- `standards/architecture/system-design.md` — System design and architecture standards
- `patterns/distributed-system/idempotency.md` — Idempotency pattern
- `patterns/distributed-system/retry.md` — Retry pattern
- `patterns/distributed-system/consistency.md` — Consistency model patterns
- `patterns/cache/cache-aside.md` — Cache-Aside pattern
- `patterns/ai-agent/architecture.md` — AI agent architecture patterns
- `patterns/ai-agent/memory.md` — AI agent memory patterns
- `patterns/ai-agent/tool-use.md` — AI agent tool-use patterns
- `patterns/ai-agent/evaluation.md` — AI agent evaluation patterns
- `skills/design.md` — System design skill for AI agents
- `skills/python-development.md` — Python development skill for AI agents
- `skills/testing.md` — Testing strategy skill for AI agents
- `skills/code-review.md` — Code review skill for AI agents
- `skills/ai-agent-development.md` — AI agent development skill
- `adapters/claude/CLAUDE.md` — Claude Code adapter
- `adapters/cursor/.cursorrules` — Cursor adapter
- `adapters/github-copilot/copilot-instructions.md` — GitHub Copilot adapter
- `evaluations/system-design/cache-design.yaml` — Cache design evaluation case
- `evaluations/system-design/wallet-system.yaml` — Wallet system evaluation case
- `evaluations/system-design/agent-design.yaml` — AI agent design evaluation case
- `evaluations/coding/python-refactor.yaml` — Python refactoring evaluation case
- `templates/design-doc.md` — Design document template
- `templates/adr.md` — Architecture Decision Record template
- `templates/rfc.md` — Request for Comments template
- `templates/architecture-review.md` — Architecture review template
