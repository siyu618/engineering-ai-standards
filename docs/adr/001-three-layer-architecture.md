# ADR-001: Three-Layer Architecture of Engineering Standards

**Status:** Accepted
**Date:** 2026-07-28

## Context

The repository needs to serve both human engineers and AI coding agents. Early designs mixed
principles, mandatory rules, reusable solutions, and AI instructions into single documents,
making them hard to maintain, version, and reference.

We identified four distinct content types that should not coexist:

- **Engineering philosophy** (principles) — changes rarely, aspirational
- **Mandatory rules** (standards) — changes with tech stack, must be explicit
- **Reusable solutions** (patterns) — changes as we learn better approaches
- **AI instructions** (skills) — changes with AI capabilities and prompt engineering

## Decision

Separate repository content into four distinct layers, plus two supporting layers:

```
Principles → Standards → Patterns → Skills → Adapters
                                            ↓
                                       Evaluations
```

### Layer Definitions

1. **Principles** — `principles/` — Why we build software this way. Correctness, simplicity,
   reliability, scalability, maintainability. Changes rarely. Read by all humans and agents.
2. **Standards** — `standards/` — Mandatory engineering rules. Python style, testing requirements,
   API design conventions. Changes when tools or conventions evolve. Enforced in CI.
3. **Patterns** — `patterns/` — Reusable solutions. Idempotency, retry, cache-aside, agent
   architecture. Changes when we learn better approaches. Referenced, not enforced.
4. **Skills** — `skills/` — AI-consumable instructions for recurring tasks. Design, Python
   development, testing, code review. Changes with AI capabilities. Versioned independently.
5. **Adapters** — `adapters/` — AI tool-specific entry points (CLAUDE.md, .cursorrules). Must
   NOT contain rules or instructions — only references to the layers above.
6. **Evaluations** — `evaluations/` — Regression detection for skills. Each skill has evaluation
   cases that define expected capabilities and scoring criteria.

### Boundary Rules

A file in one layer must NOT:
- Duplicate content from another layer (e.g., no rules in adapters)
- Mix concerns (e.g., no AI instructions in standards)
- Bypass the layer hierarchy (e.g., an adapter should reference a skill, not embed it)

## Consequences

### Positive

- Each layer can be versioned, reviewed, and updated independently.
- AI agents can navigate the hierarchy predictably: identity → principles → standards → patterns.
- Adapters are thin entry points, making them trivial to maintain across tool updates.

### Negative

- Some content may require cross-referencing across layers (e.g., a skill references a standard).
- Layer boundaries require enforcement; new contributors may need guidance.
- Slight indirection when reading: following a skill means visiting multiple files.

## Related

- [ADR-002: Skill Versioning](002-skill-versioning.md)
- [ADR-003: Evaluation Framework](003-evaluation-framework.md)
