# Engineering AI Standards

A version-controlled engineering platform that combines engineering principles, coding standards,
design patterns, AI skills, workflow orchestration, evaluations, and governance.

## Purpose

This repository serves as a shared engineering standard for both human engineers and AI coding
agents (Claude Code, Cursor, GitHub Copilot, and future AI agents). It is not a prompt collection.
It is an **Engineering AI Platform**.

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
Workflows
    ↓
Evaluations
    ↓
Adapters
    ↓
AI Coding Agents
```

Each layer builds on the one above it. Principles inform standards, which are implemented through
patterns, packaged as skills, composed into workflows, validated by evaluations, and adapted for
specific AI tools — all governed by ownership and review policies.

## Repository Structure

| Directory | Purpose | Question Answered |
|-----------|---------|-------------------|
| `principles/` | Engineering philosophy | Why do we build software this way? |
| `standards/` | Mandatory engineering rules | What rules must engineers follow? |
| `patterns/` | Reusable engineering solutions | How do we usually solve this type of problem? |
| `skills/` | AI-consumable skill packages (17 skills) | How should an AI approach this task? |
| `workflows/` | Composed skill orchestrations | In what order should skills be applied? |
| `evaluations/` | Skill regression prevention + execution engine | Is the AI still performing correctly? |
| `adapters/` | AI tool-specific entry-points | What format does this AI tool require? |
| `runtime/` | Agent operating model (context, memory, tools, verification) | How should agents operate? |
| `templates/` | Reusable document templates | What structure should this document follow? |
| `tools/` | CLI tool (`ai-standard`) for managing the platform | How to manage skills and evaluations? |
| `reports/` | Generated evaluation reports (JSON + Markdown) | What are the latest evaluation scores? |
| `registry/` | Central skill metadata index (17 skills) | What skills are available? |
| `governance/` | Ownership, review, release policies | Who decides? How do we release? |
| `docs/` | User guides (evaluation, skill development, CLI) | How do I use this platform? |
| `docs/adr/` | Architecture Decision Records (7 records) | Why was this decision made? |
| `AGENTS.md` | Generic AI agent entry-point | How should agents use this repository? |

## Getting Started

**For human engineers:** Start with `principles/` to understand our engineering philosophy,
then review `standards/` for mandatory rules.

**For AI coding agents:** Start with `AGENTS.md` for a high-level overview, then read your
tool-specific adapter in `adapters/`. AI agents should follow the layer hierarchy.

### AI Agent Entry Points

| Tool | Entry Point |
|------|-------------|
| All agents | [`AGENTS.md`](AGENTS.md) — Generic instructions |
| All agents (runtime) | [`runtime/README.md`](runtime/README.md) — Operating model |
| Claude Code | [`adapters/claude/CLAUDE.md`](adapters/claude/CLAUDE.md) |
| Cursor | [`adapters/cursor/.cursorrules`](adapters/cursor/.cursorrules) |
| GitHub Copilot | [`adapters/github-copilot/copilot-instructions.md`](adapters/github-copilot/copilot-instructions.md) |

## Key Concepts

### Separation of Concerns

Engineering standards, AI skills, AI tool configurations, workflows, and governance are kept
separate to allow each to evolve independently. Skills reference standards but remain distinct,
workflows compose skills without duplicating them, and adapters reference skills without
embedding them.

### Skill Registry

The `registry/skills.yaml` file is the central machine-readable index of all skills. It tracks
versions, owners, dependencies, and evaluation thresholds. Automation and CI use this file as
the source of truth for skill metadata.

### Workflow Orchestration

Workflows in `workflows/` compose multiple skills into end-to-end engineering processes.
A feature development workflow sequences design → implementation → testing → code review,
with quality gates between each step.

### Evaluation Framework

Skills are treated like code. Each skill has corresponding evaluation cases that prevent
regression when skills are updated. The framework supports three modes:

- **Rule-based scoring** via [`evaluations/runner/evaluator.py`](evaluations/runner/evaluator.py)
- **LLM-as-Judge** via the [`judge_prompt.md`](evaluations/runner/judge_prompt.md) template
- **Human review** for high-stakes evaluations

Score regression is detected via [`evaluations/runner/scorecard.py`](evaluations/runner/scorecard.py)
and gated in CI. See [`evaluations/README.md`](evaluations/README.md) for the full philosophy.

### Governance

The `governance/` directory defines ownership, review policies, and release processes.
Each skill has a designated owner, changes are classified by severity (patch/minor/major/breaking),
and releases follow semantic versioning with evaluation gates.

### Agent Runtime

The [`runtime/`](runtime/) directory defines how AI agents should operate — context management,
memory policy, tool usage guidelines, and a self-verification loop. These are agent-agnostic
concepts that apply regardless of which AI tool is used.

### AI-First Design

All content is structured for both human readability and machine parseability. Clear headings,
consistent formatting, YAML frontmatter, and explicit references make the repository usable by
AI agents without special preprocessing.

## Versioning

This repository follows [Semantic Versioning](https://semver.org/):

- **Major**: Breaking changes to structure, standards, or skill contracts
- **Minor**: New capabilities (registry, workflows, governance, skill additions)
- **Patch**: Fixes, clarifications, wording improvements

Skills within the repository follow independent semantic versioning tracked in `registry/skills.yaml`.

## License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
