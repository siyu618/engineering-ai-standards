You are evaluating an AI agent's response for a `{{skill}}` task.

## Task

{{task}}

## Context

{{context}}

## Requirements

The agent's response **must include**:
{% for item in must_include %}
- {{ item }}
{% endfor %}

The agent's response **must NOT include**:
{% for item in forbidden %}
- {{ item }}
{% endfor %}

## Agent Output

```
{{output}}
```

## Scoring Instructions

Score the agent's output on four dimensions, each from 0 to 100.

### 1. Correctness (Weight: {{correctness_weight}}%)
Consider: Is the output technically accurate? Are the claims correct? Are there errors or
misunderstandings?

Score: /100

Rationale:

### 2. Completeness (Weight: {{completeness_weight}}%)
Consider: Does the output cover all required aspects? Are there any gaps?

Score: /100

Rationale:

### 3. Architecture (Weight: {{architecture_weight}}%)
Consider: Is the structure clean and appropriate? Are the components well-organized?
Are interfaces well-defined?

Score: /100

Rationale:

### 4. Maintainability (Weight: {{maintainability_weight}}%)
Consider: Can the output be operated, understood, and evolved over time?
Is it practical and well-documented?

Score: /100

Rationale:

## Final Score

Correctness: /100 (weight {{correctness_weight}}%)
Completeness: /100 (weight {{completeness_weight}}%)
Architecture: /100 (weight {{architecture_weight}}%)
Maintainability: /100 (weight {{maintainability_weight}}%)

**Overall Score:** (weighted sum) /100
