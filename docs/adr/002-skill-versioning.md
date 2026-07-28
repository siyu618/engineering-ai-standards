# ADR-002: Skill Versioning with Independent Modules

**Status:** Accepted
**Date:** 2026-07-28

## Context

Skills in this repository are AI-consumable instructions that evolve over time as AI models
improve, prompting patterns change, and requirements shift. Early skills were flat Markdown
files with no metadata, making it impossible to:

- Track which version of a skill an agent was using
- Detect regressions when updating skill instructions
- Run evaluations against specific skill versions
- Automate skill release workflows

We considered two approaches:

1. **Monolithic versioning** — one version for the entire repository. Simple but imprecise;
   a change to one skill would bump the version for all skills.
2. **Independent skill modules** — each skill has its own version, changelog, and evaluation
   cases. More overhead but precise tracking and independent release cycles.

## Decision

Treat each skill as an independent module with its own version, changelog, and evaluation cases.

### Module Structure

Every skill under `skills/` follows this structure:

```
skills/<skill-name>/
├── SKILL.md          # Skill instructions with YAML frontmatter metadata
├── CHANGELOG.md      # Version history for this skill
└── eval.yaml         # Evaluation cases for regression detection
```

### SKILL.md Frontmatter

```yaml
---
name: skill-name
version: "1.0.0"
category:
  - domain1
  - domain2
dependencies:
  - standards/path.md
  - patterns/path.md
evaluation:
  enabled: true
  cases:
    - case-id
---
```

### Versioning Rules

- **Major**: Breaking changes to skill behavior or output format.
- **Minor**: New capabilities or expanded instructions, backwards compatible.
- **Patch**: Fixes, clarifications, wording improvements with no behavior change.

### Skill Dependencies

Skills declare dependencies on standards and patterns via the `dependencies` field.
These are informational: they tell the agent what to read before using the skill.
They are not automatically enforced.

### Evaluation Cases

Each skill lists evaluation cases in its `evaluation.cases` field. These reference cases
in `evaluations/cases/`. Before releasing a new skill version, all listed cases must pass.

## Consequences

### Positive

- Each skill can be versioned and released independently.
- Evaluation results can be attributed to specific skill versions.
- Machine-readable metadata enables automated tooling (CI validation, skill registries).
- Changes are traceable via per-skill CHANGELOGs.

### Negative

- More files to maintain (3 files per skill instead of 1).
- Cross-skill coordination requires checking multiple CHANGELOGs.
- Skills that depend on each other require careful coordination of version bumps.

## Related

- [ADR-001: Three-Layer Architecture](001-three-layer-architecture.md)
- [ADR-003: Evaluation Framework](003-evaluation-framework.md)
