# AI Agent Evaluation

## Context

AI agent behavior is non-deterministic — the same input can produce different outputs across runs, model versions, or prompt changes. Without systematic evaluation, regressions go unnoticed and improvements cannot be measured.

## Problem

How to systematically evaluate an AI agent's performance, detect regressions, and measure improvements?

## Solution

### Evaluation Framework

```
Evaluation Case → Agent Execution → Scoring → Report
```

An **evaluation case** defines a specific task with expected capabilities and scoring criteria. The agent executes the task, and the result is scored against the criteria.

### Evaluation Case Structure

Every evaluation case contains:

| Field | Description | Required |
|-------|-------------|----------|
| `name` | Unique identifier | Yes |
| `category` | Domain (coding, design, testing, etc.) | Yes |
| `task` | The prompt or instruction given to the agent | Yes |
| `context` | Background information the agent needs | No |
| `expected_capabilities` | What the agent should demonstrate | Yes |
| `forbidden_behaviors` | What the agent must NOT do | No |
| `scoring_criteria` | How to score the agent's output | Yes |

### Scoring Dimensions

| Dimension | Description | Typical Weight |
|-----------|-------------|----------------|
| **Correctness** | Does the output solve the problem accurately? | 30% |
| **Completeness** | Are all required aspects addressed? | 25% |
| **Quality** | Is the output well-structured and maintainable? | 20% |
| **Safety** | Does it avoid harmful or risky patterns? | 15% |
| **Efficiency** | Is the solution performant and resource-conscious? | 10% |

### Evaluation Types

#### 1. Rule-Based Evaluation

Automated checks against the agent's output using static analysis.

**Examples:**
- Does the code pass linting?
- Are there any type errors?
- Are all required sections present in the output?
- Is the output within the specified token limit?

#### 2. LLM-Judge Evaluation

A second LLM evaluates the agent's output against scoring criteria.

**Prompt structure:**
```
You are evaluating an AI agent's output for a [TASK_TYPE] task.

Task: [task description]
Expected: [expected capabilities]
Forbidden: [forbidden behaviors]

Agent Output:
[agent output]

Score each dimension from 1-5:
- Correctness: ...
- Completeness: ...
...
```

#### 3. Execution-Based Evaluation

Run the agent's output (code, configuration, commands) and observe the result.

**Examples:**
- Run tests against generated code.
- Deploy the configuration to a sandbox and validate behavior.
- Execute the agent's instructions and verify the outcome.

#### 4. Human Review

A human expert evaluates the output against the criteria.

**Best for:** Complex system designs, architectural decisions, security-sensitive outputs.

### Evaluation Pipeline

```
┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐
│  Case    │──>│  Agent   │──>│ Scoring  │──>│  Report  │
│  Loader  │   │ Executor │   │ Engine   │   │ Generator│
└──────────┘   └──────────┘   └──────────┘   └──────────┘
```

### Regression Prevention

When updating skills or prompts, follow this process:

```
1. Update Skill
       │
       ▼
2. Run Full Evaluation Suite
       │
       ▼
3. Compare Scores vs. Baseline
       │
       ├── Scores Improved → Release
       │
       ├── Scores Same → Release
       │
       └── Scores Regressed → Investigate & Fix
              │
              ▼
           (back to step 1)
```

### Baseline Tracking

Maintain a baseline score for each evaluation case:

```yaml
# evaluation-baseline.yaml
version: "1.0.0"
timestamp: 2026-07-28
baselines:
  cache-design:
    overall: 88
    per_dimension:
      correctness: 90
      completeness: 85
      architecture_quality: 88
      maintainability: 89
  python-refactor:
    overall: 92
    per_dimension:
      correctness: 95
      completeness: 90
      code_quality: 90
      testing: 88
```

### Reporting

Each evaluation run should produce:

1. **Overall score** across all cases.
2. **Per-case scores** with dimension breakdowns.
3. **Regression list** (cases that scored lower than baseline).
4. **Improvement list** (cases that scored higher than baseline).
5. **Trend** over the last N runs.

## Consequences

### Benefits
- Measurable quality: agent performance is quantified, not guessed.
- Regression detection: prompt changes that break behavior are caught before release.
- Continuous improvement: changes can be validated against objective criteria.

### Trade-offs
- Evaluation latency: full evaluation suites take time and tokens.
- Judge bias: LLM judges have their own biases that must be calibrated.
- Coverage gaps: no evaluation suite is exhaustive — edge cases will be missed.

## Related Patterns

- [Architecture](architecture.md): The agent architecture being evaluated.
- [Memory](memory.md): Evaluation results stored in agent memory.
- [Tool Use](tool-use.md): Evaluating tool selection and execution.
