# Changelog

All notable changes to this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

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
