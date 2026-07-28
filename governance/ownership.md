# Skill Ownership

Each skill in this repository has a designated owner responsible for its quality,
accuracy, and evolution.

## Ownership Table

| Skill | Owner | Contact | Status |
|-------|-------|---------|--------|
| design | architecture-team | #architecture-channel | stable |
| python-development | backend-team | #backend-channel | stable |
| testing | qa-team | #qa-channel | stable |
| code-review | architecture-team | #architecture-channel | stable |
| ai-agent-development | ai-platform-team | #ai-platform-channel | stable |

## Owner Responsibilities

- **Review and merge** changes to the skill content
- **Maintain evaluation cases** and keep thresholds current
- **Respond to issues** filed against the skill
- **Coordinate** with dependent skill owners on cross-cutting changes
- **Monitor evaluation scores** and investigate regressions
- **Bump versions** when making changes per semantic versioning

## Escalation

If a skill owner is unresponsive for more than 1 week on a change request or
issue, escalate to the repository maintainers.

## Adding a New Skill

To add a new skill to this repository:

1. Identify the owning team and list them in this file
2. Define the skill's scope and dependencies
3. Create the skill module (SKILL.md, metadata.yaml, CHANGELOG.md, examples/, eval/)
4. Register the skill in `registry/skills.yaml`
5. Follow the [release process](release-process.md) for initial publication
