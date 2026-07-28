# ADR-005: Governance Model for Skills

**Status:** Accepted
**Date:** 2026-07-28

## Context

As the repository grows beyond a single contributor, we need formal governance to manage
ownership, review processes, and releases. Without governance, changes can conflict,
ownership is unclear, and there is no quality gating before releases.

We identified three governance dimensions that need formalization:

1. **Ownership** — Who is responsible for each skill?
2. **Review policy** — What level of review is required for each type of change?
3. **Release process** — How are versions bumped, and what gates must pass?

## Decision

Create a `governance/` directory with three documents, each addressing one dimension.

### Ownership Model

Each skill has a single owning team. The owner is responsible for the skill's quality,
accuracy, and evolution. Ownership is documented in `governance/ownership.md` and
mirrored in `registry/skills.yaml`.

### Review Classification

Changes are classified into four types: Patch, Minor, Major, Breaking. Each type
has different review requirements and evaluation gates.

| Type | Review | Evaluation | Example |
|------|--------|------------|---------|
| Patch | 1 reviewer | Optional | Typo fix |
| Minor | 1 reviewer + eval pass | Required | New section |
| Major | Architecture review | Required + threshold | Process change |
| Breaking | Architecture review + plan | Required + approval | Contract change |

### Release Process

Skills follow semantic versioning independently of the repository. The release checklist
requires: CHANGELOG update, version bump in metadata.yaml and registry, evaluation pass,
and review approval.

### Why Not Monolithic Governance

We rejected a single governance document because each dimension is maintained by
different roles and changes at different frequencies:

- Ownership changes when teams reorganize (rare)
- Review policy changes when process evolves (occasional)
- Release process is procedural and changes rarely

## Consequences

### Positive

- Clear ownership reduces confusion about who to contact for changes
- Review classification provides predictable process for contributors
- Release checklist ensures quality gates are not skipped
- Governance documents are independently maintainable

### Negative

- Overhead: contributors must read governance documents before making changes
- Classification disputes: what counts as a minor vs major change may require judgment
- Threshold gating requires evaluation infrastructure to be functional

## Related

- [ADR-002: Skill Versioning](002-skill-versioning.md)
- [ADR-004: Skill Registry](004-skill-registry.md)
