# Evaluation Guide

## Overview

Evaluations are automated tests for skills. They prevent regression when skills are updated.
The evaluation framework supports three methods:

| Method | Use Case | Automation |
|--------|----------|------------|
| Rule-based | Quick CI gates, checklist verification | Fully automated |
| LLM-as-Judge | Open-ended tasks (design, code review) | Semi-automated (needs LLM API) |
| Human review | High-stakes evaluations | Manual score entry |

## How to Write an Evaluation Case

### 1. Create the case file

Create a YAML file under `evaluations/cases/<category>/<case-name>.yaml`:

```yaml
id: my-case-001
skill: my-skill
category: architecture
difficulty: senior
task: "Design a system for..."
context:
  - "high traffic service"
  - "Redis as cache"
must_include:
  - "consistency discussion"
  - "failure handling"
forbidden:
  - "using cache as source of truth"
scoring:
  correctness: 30
  architecture: 30
  tradeoff: 20
  clarity: 20
```

### 2. Register in the skill's evaluation config

In `registry/skills.yaml`, add the case ID to the skill's `evaluation.cases` list.

### 3. Validate the case

```bash
python evaluations/runner/run.py --verbose
```

## How to Run Evaluations

### Rule-based scoring

```bash
python evaluations/runner/evaluator.py --case my-case --method rule --output agent_output.md
```

### LLM-as-Judge

```bash
python evaluations/runner/evaluator.py --case my-case --method llm-judge --output agent_output.md
```
This renders a judge prompt. Pipe the output to an LLM for actual scoring.

### CLI tool

```bash
python tools/ai-standard/cli.py eval <skill-name>
```

## How to Check for Regression

```bash
python evaluations/runner/scorecard.py --compare
```

Or via the CLI:

```bash
python tools/ai-standard/cli.py report
```

## How to Interpret Results

| Score | Meaning |
|-------|---------|
| 90-100 | Excellent — meets all criteria |
| 75-89 | Good — minor improvements possible |
| 60-74 | Fair — significant gaps |
| Below 60 | Poor — major issues |

A score below the skill's `threshold` in `registry/skills.yaml` is flagged as regression.
