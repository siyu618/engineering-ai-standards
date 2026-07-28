# Workflow: Feature Development

**Composed Skills:** [design](../skills/design/SKILL.md) → [python-development](../skills/python-development/SKILL.md) → [testing](../skills/testing/SKILL.md) → [code-review](../skills/code-review/SKILL.md)

## Entry Criteria

- [ ] Requirements documented and approved
- [ ] Acceptance criteria defined
- [ ] Feature flag created (if applicable)

## Flow

```
[1. Requirement Analysis]
         │
         ▼
[2. Design Skill]  ──── Produces: Architecture design document
         │
         ▼
[3. Implementation Skill]  ── Produces: Production code
         │
         ▼
[4. Testing Skill]  ─────── Produces: Test suite, coverage report
         │
         ▼
[5. Code Review Skill]  ─── Produces: Review findings, approval
         │
         ▼
[6. Release Checklist]
```

## Quality Gates

### Gate 1: Design → Implementation
- [ ] Design reviewed by at least one peer
- [ ] Failure modes documented
- [ ] API contracts defined before implementation

### Gate 2: Implementation → Testing
- [ ] All type checks pass
- [ ] Linter clean (no warnings above configured threshold)
- [ ] No dead code, commented code, or TODOs without tickets

### Gate 3: Testing → Code Review
- [ ] Unit test coverage >= 80%
- [ ] Integration tests pass for all critical paths
- [ ] No flaky tests in test suite

### Gate 4: Code Review → Release
- [ ] All blocking findings resolved
- [ ] No unresolved security concerns
- [ ] CHANGELOG updated

## Exit Criteria

- [ ] PR merged to main
- [ ] All CI checks pass
- [ ] Feature flag enabled (if applicable)
- [ ] Monitoring dashboards updated
- [ ] Runbook updated (if needed)
