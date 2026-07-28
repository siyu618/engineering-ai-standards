# Evaluation Framework

## Philosophy

We treat engineering skills like code. Each skill has corresponding evaluation cases that
prevent regression when skills are updated.

| Concept | Software Analogy | In This Repository |
|---------|-----------------|-------------------|
| **Skill** | Code | A skill module in `skills/` |
| **Evaluation Case** | Test | A YAML case in `evaluations/cases/` |
| **Score** | Test Result | A numerical score across 4 dimensions |
| **Release** | Version | A tagged version of the skill module |

## Evaluation Methods

### 1. Rule-Based Evaluation

Automated checks against structured outputs.

**Best for:** Validating YAML structure, required fields, scoring weights.
**Implementation:** `evaluations/runner/run.py` validates all case definitions.

### 2. LLM-as-Judge

A separate LLM evaluates the agent's output against the case criteria.

**Best for:** Open-ended tasks (design, code review, strategy). Use
`evaluations/runner/judge_prompt.md` as the judge prompt template.

**Process:**
1. Agent produces output for a given evaluation case.
2. Judge LLM receives: task, context, expected capabilities, forbidden behaviors, agent output.
3. Judge scores each dimension (1-5) and provides rationale.
4. Scores are aggregated into an overall score.

### 3. Human Review

A human expert evaluates the output against the scoring criteria.

**Best for:** Complex system designs, architectural decisions, security-sensitive tasks.

## Evaluation Process

```
1. Update Skill (e.g., change a skill's SKILL.md)
       │
       ▼
2. Run Evaluation Suite → python evaluations/runner/run.py
       │
       ▼
3. Compare Scores vs. Baseline
       │
       ├── Improved or equal → Release (bump version)
       │
       └── Regressed → Investigate and fix
              │
              ▼
           (back to step 1)
```

## Scoring Rubric

Each evaluation case scores 4 dimensions, each weighted to sum to 100:

| Dimension | Typical Weight | What It Measures |
|-----------|---------------|------------------|
| Correctness | 30-35% | Is the output technically accurate? |
| Completeness | 20-25% | Are all required aspects covered? |
| Architecture | 20-25% | Is the structure clean and appropriate? |
| Maintainability | 15-20% | Can it be operated and evolved? |

Each dimension is scored 0-100. The overall score is the weighted sum.

## Case Structure

Every evaluation case in `evaluations/cases/` follows this structure:

```yaml
---
id: unique-case-id
skill: skill-module-name
category: system-design|coding|testing
version: "1.0.0"
task: >
  The prompt given to the agent under evaluation.
context:
  - Background information the agent needs
expected:
  must_include:
    - Required capabilities the agent must demonstrate
  forbidden:
    - Behaviors the agent must avoid
scoring:
  correctness: { weight: 30, description: "...", criteria: [...] }
  completeness: { weight: 25, description: "...", criteria: [...] }
  architecture: { weight: 25, description: "...", criteria: [...] }
  maintainability: { weight: 20, description: "...", criteria: [...] }
---
```

## Getting Started

1. Run `python evaluations/runner/run.py` to validate all evaluation cases.
2. To evaluate a skill, run the agent with the case's `task` as input.
3. Score the output using the case's `scoring` criteria (LLM-judge or human).
4. Track scores and compare against previous baselines.
