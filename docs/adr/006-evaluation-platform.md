# ADR-006: Executable Evaluation Platform

**Status:** Accepted
**Date:** 2026-07-28

## Context

Previously, evaluations were document-oriented. The schema validated that case YAML files had
correct fields, but there was no mechanism to actually evaluate agent outputs or detect
regression. The system could answer "does this case file have valid fields?" but not
"does this agent output pass the evaluation?"

We needed a closed loop: Skill → Evaluation → Score → Regression Check → Release Gate.

## Decision

Build an executable evaluation engine with three scoring modes:

### Mode 1: Rule-Based Scoring

The evaluator scans agent output for required keywords from `must_include`. Each keyword match
contributes to a hit rate. The hit rate is converted into dimension scores via weighted average.

**Best for:** Quick CI gates, structured output validation, checklist verification.

### Mode 2: LLM-as-Judge

The evaluator renders a judge prompt template (judge_prompt.md) with case data and agent output,
producing a structured prompt for an external LLM call. The judge LLM scores on four dimensions
and produces a JSON result.

**Best for:** Open-ended tasks (design, code review, architecture). Used when rule-based scoring
is too rigid.

### Mode 3: Human Review

Interactive score entry for human reviewers. The evaluator prompts for each dimension score
and computes the weighted overall.

**Best for:** High-stakes evaluations, security reviews, architecture decisions.

### Regression Detection

The scorecard component (`scorecard.py`) compares scores against thresholds defined in
`registry/skills.yaml`. If any score drops below threshold, `--compare` exits non-zero,
blocking the CI gate.

## Consequences

### Positive
- Evaluations are now executable, not just validatable
- Three modes cover the full spectrum from automated to human review
- Scorecard enables CI gating on regression
- Registry tracks latest_score and last_run for trend analysis

### Negative
- Rule-based scoring is approximate (keyword matching misses semantic understanding)
- LLM-as-Judge requires an external API call for scoring
- Score storage in registry YAML is simple but not a real database

## Related

- [ADR-003: Evaluation Framework](003-evaluation-framework.md)
- [ADR-004: Skill Registry](004-skill-registry.md)
