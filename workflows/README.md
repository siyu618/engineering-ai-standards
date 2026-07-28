# Workflows

Workflows compose multiple skills into end-to-end engineering processes. Each workflow
defines a DAG of steps, where each step references a skill from `skills/` and produces
an output artifact.

## Architecture

```
Skills (building blocks) → Workflows (orchestrated processes)
```

## Available Workflows

| Workflow | Skills | Entry Criteria | Exit Criteria |
|----------|--------|----------------|---------------|
| [Feature Development](feature-development.md) | design → python-development → testing → code-review | Approved requirements | Merged PR with passing CI |
| [Bug Fix](bug-fix.md) | testing → python-development → code-review | Confirmed bug report | Fix deployed and verified |
| [Architecture Review](architecture-review.md) | design → code-review | Design document submitted | Approved ADR |
| [Production Incident](production-incident.md) | ai-agent-development → code-review | P0/P1 incident declared | Postmortem completed |

## Workflow Structure

Each workflow document specifies:

- **Entry criteria**: conditions that must be true before starting
- **Step-by-step flow**: ordered steps with skill references
- **Quality gates**: checks that must pass between steps
- **Artifacts**: outputs produced at each step
- **Exit criteria**: conditions that define completion
