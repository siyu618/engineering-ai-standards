# Engineering AI Standards

A version-controlled engineering knowledge system that combines engineering principles, coding standards, design patterns, AI coding skills, AI tool adapters, evaluation frameworks, and engineering templates.

## Purpose

This repository serves as a shared engineering standard for both human engineers and AI coding agents (Claude Code, Cursor, GitHub Copilot, and future AI agents). It provides a single source of truth for how we build software.

## Architecture

```
Principles
    ↓
Standards
    ↓
Patterns
    ↓
Skills
    ↓
Adapters
```

Each layer builds on the one above it. Principles inform standards, which are implemented through patterns, packaged as skills, and adapted for specific AI tools.

## Repository Structure

| Directory | Purpose | Question Answered |
|-----------|---------|-------------------|
| `principles/` | Engineering philosophy | Why do we build software this way? |
| `standards/` | Mandatory engineering rules | What rules must engineers follow? |
| `patterns/` | Reusable engineering solutions | How do we usually solve this type of problem? |
| `skills/` | AI-consumable structured instruction modules | How should an AI approach this task? |
| `adapters/` | AI tool-specific entry-points | What format does this AI tool require? |
| `evaluations/` | Skill regression prevention | Is the AI still performing correctly? |
| `templates/` | Reusable document templates | What structure should this document follow? |
| `docs/adr/` | Architecture Decision Records | Why was this decision made? |
| `AGENTS.md` | Generic AI agent entry-point | How should agents use this repository? |

## Getting Started

**For human engineers:** Start with `principles/` to understand our engineering philosophy, then review `standards/` for mandatory rules.

**For AI coding agents:** Start with `AGENTS.md` for a high-level overview, then read your tool-specific adapter in `adapters/`. Each adapter references the relevant skills. AI agents should follow the layer hierarchy: principles → standards → patterns → skills.

### AI Agent Entry Points

| Tool | Entry Point |
|------|-------------|
| All agents | [`AGENTS.md`](AGENTS.md) — Generic instructions |
| Claude Code | [`adapters/claude/CLAUDE.md`](adapters/claude/CLAUDE.md) |
| Cursor | [`adapters/cursor/.cursorrules`](adapters/cursor/.cursorrules) |
| GitHub Copilot | [`adapters/github-copilot/copilot-instructions.md`](adapters/github-copilot/copilot-instructions.md) |

## Versioning

This repository follows [Semantic Versioning](https://semver.org/):

- **Major**: Breaking changes to standards or patterns
- **Minor**: New capabilities added
- **Patch**: Fixes, clarifications, wording improvements

## Key Concepts

### Separation of Concerns

Engineering standards, AI skills, and AI tool configurations are kept separate to allow each to evolve independently. Skills reference standards but remain distinct, and adapters reference skills without duplicating them.

### Evaluation Framework

Skills are treated like code. Each skill has corresponding evaluation cases that prevent regression when skills are updated. Before releasing a new version, evaluations must be run to ensure no capabilities are lost. See [`evaluations/README.md`](evaluations/README.md) for the full philosophy and [`evaluations/runner/run.py`](evaluations/runner/run.py) for the validation tool.

### AI-First Design

All content is structured for both human readability and machine parseability. Clear headings, consistent formatting, and explicit references make the repository usable by AI agents without special preprocessing.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
