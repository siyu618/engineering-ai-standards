# Changelog

All notable changes to this repository are documented here.

The format is based on [Keep a Changelog](https://keepachangelog.com/),
and this project adheres to [Semantic Versioning](https://semver.org/).

## [1.1.0] - 2026-07-28

### Added

- Root-level symlinks: `CLAUDE.md` → `adapters/claude/CLAUDE.md`, `.cursorrules` → `adapters/cursor/.cursorrules`
- `standards/coding/typescript.md` — TypeScript coding standards
- `standards/coding/go.md` — Go coding standards
- `standards/coding/rust.md` — Rust coding standards
- `patterns/cache/read-through.md` — Read-Through cache pattern
- `patterns/cache/write-through.md` — Write-Through cache pattern
- `patterns/cache/write-behind.md` — Write-Behind cache pattern
- `evaluations/system-design/testing-strategy.yaml` — Testing strategy evaluation case
- `evaluations/coding/code-review-detect.yaml` — Code review bug detection evaluation case
- `evaluations/coding/ai-agent-eval-design.yaml` — AI agent evaluation framework design case
- `.github/workflows/validate.yml` — CI validation workflow (structure, markdown, YAML, symlinks, references)
- `.github/workflows/evaluate.yml` — Scheduled evaluation workflow
- `CLAUDE.md` (symlink at repo root) — Auto-detected by Claude Code
- `.cursorrules` (symlink at repo root) — Auto-detected by Cursor

### Changed

- Updated CHANGELOG for v1.1.0

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
