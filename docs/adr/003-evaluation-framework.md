# ADR-003: Evaluation Framework for Skill Regression Prevention

**Status:** Accepted
**Date:** 2026-07-28

## Context

Skills are AI-consumable instructions that directly affect the behavior of AI coding agents.
A small change to a skill can silently degrade agent output quality — producing less complete
designs, missing error cases, or generating lower-quality code.

Without systematic evaluation, we cannot:

- Detect when a skill change introduces regressions
- Measure whether a skill change is an improvement
- Compare agent performance across model versions
- Establish a baseline for "acceptable" agent behavior

## Decision

Introduce a first-class evaluation framework modeled on software testing.

### Mental Model

| Software Engineering | This Repository |
|---------------------|-----------------|
| Code | Skill (`SKILL.md`) |
| Test | Evaluation case (`eval.yaml`) |
| Test result | Score (0-100 per dimension) |
| Version | Skill version |

### Evaluation Methods

Three methods are supported, in order of increasing reliability:

1. **Rule-based validation** — automated checks via `evaluations/runner/run.py`. Validates
   evaluation case structure (required fields, scoring weights). Fast, deterministic.
2. **LLM-as-Judge** — a separate LLM evaluates the agent's output against the case criteria.
   Uses `evaluations/runner/judge_prompt.md` as the prompt template. Suitable for open-ended
   tasks like design and code review.
3. **Human review** — a human expert evaluates the output using the case scoring criteria.
   Used for complex system designs, architectural decisions, and security-sensitive tasks.

### Scoring Rubric

Every evaluation case defines four scoring dimensions:

| Dimension | Weight | What It Measures |
|-----------|--------|------------------|
| Correctness | 30-35% | Technical accuracy |
| Completeness | 20-25% | Coverage of all required aspects |
| Architecture | 20-25% | Structure and design quality |
| Maintainability | 15-20% | Operability and evolvability |

Each dimension is scored 0-100. The overall score is the weighted sum. Weights must sum to 100.

### Regression Detection Process

```
1. Update skill SKILL.md  ──→  2. Run evaluation suite
                                      │
                            ┌─────────┴──────────┐
                            ▼                    ▼
                     Scores improved        Scores regressed
                            │                    │
                            ▼                    ▼
                     Bump version          Investigate and fix
                     Release                      │
                                                  ▼
                                             (back to step 1)
```

### Baseline Tracking

Each evaluation run should compare scores against a stored baseline. Baselines are versioned.
A regression is defined as any dimension scoring more than 10 points below the baseline.

## Evaluation Case Format

Every evaluation case in `evaluations/cases/` contains:

```yaml
---
id: unique-id
skill: skill-name
category: system-design|coding|testing
version: "1.0.0"
task: "Agent prompt under evaluation"
context:
  - "Background information"
expected:
  must_include:
    - "Required capabilities"
  forbidden:
    - "Behaviors to avoid"
scoring:
  correctness:  { weight: 30, description: "...", criteria: [...] }
  completeness: { weight: 25, description: "...", criteria: [...] }
  architecture: { weight: 25, description: "...", criteria: [...] }
  maintainability: { weight: 20, description: "...", criteria: [...] }
---
```

## Consequences

### Positive

- Regressions are detected before skills are released.
- Skill quality is quantified, not guessed.
- Evaluation infrastructure is lightweight (YAML + Python + LLM-judge).
- Consistent scoring across all skills enables comparison.

### Negative

- Evaluation coverage requires ongoing maintenance.
- LLM-judge scoring introduces variability — scores are not perfectly deterministic.
- Not all agent behaviors can be captured in evaluation cases (nuance, context awareness).

## Related

- [ADR-001: Three-Layer Architecture](001-three-layer-architecture.md)
- [ADR-002: Skill Versioning](002-skill-versioning.md)
