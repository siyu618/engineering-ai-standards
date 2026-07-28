# ADR-004: Centralized Skill Registry

**Status:** Accepted
**Date:** 2026-07-28

## Context

As the number of skills grows, we need a machine-readable index of all available skills
for automation, CI, and discoverability. Previously, skill metadata was embedded in the
YAML frontmatter of each SKILL.md, making it difficult for tools to query across skills.

We considered two approaches:

1. **SKILL.md frontmatter only** — Keep metadata in each SKILL.md. Simple but requires
   parsing every file to get an overview.
2. **Central registry + per-skill metadata** — A single `registry/skills.yaml` as the
   source of truth, plus `metadata.yaml` in each skill module for local reference.

## Decision

Create a centralized skill registry at `registry/skills.yaml` as the source of truth
for skill metadata, while retaining `metadata.yaml` in each skill module for human
readability and local context.

### Why Centralized

- **Single discovery point**: Tools and CI can read one file to list all skills
- **Cross-skill queries**: Find skills by owner, category, status, or evaluation threshold
- **Registry versioning**: The registry has its own version for tracking schema changes
- **Evaluation gating**: Thresholds in the registry enable CI gating without parsing eval files

### Why Keep Per-Skill metadata.yaml

- **Local context**: Developers working on a single skill don't need to navigate to the root
- **Self-containment**: Each skill module remains independently navigable
- **Backup reference**: If the registry is accidentally corrupted, per-skill files can rebuild it

### Data Ownership

| Field | Registry | metadata.yaml | SKILL.md Frontmatter |
|-------|----------|---------------|---------------------|
| Name / Version | Primary | Copy | Copy |
| Owner | Primary | — | — |
| Status | Primary | — | — |
| Dependencies | Primary | Copy | Copy |
| Evaluation config | Primary | Copy | Copy |
| Skill instructions | — | — | Primary |

## Consequences

### Positive

- CI can validate registry consistency against skill modules
- Automation can discover skills by owner, category, or status
- Future tooling (skill dashboards, dependency graphs) has a single data source

### Negative

- Three locations to update on version changes (registry, metadata.yaml, SKILL.md frontmatter)
- Registry must be kept in sync with skill modules — enforced by CI
- Additional file to maintain as skills evolve

## Related

- [ADR-002: Skill Versioning](002-skill-versioning.md)
- [ADR-005: Governance Model](005-governance-model.md)
