# Workflow: Bug Fix

**Composed Skills:** [testing](../skills/testing/SKILL.md) → [python-development](../skills/python-development/SKILL.md) → [code-review](../skills/code-review/SKILL.md)

## Entry Criteria

- [ ] Bug confirmed and reproducible
- [ ] Severity classified (P0/P1/P2/P3)
- [ ] Test case written that reproduces the bug

## Flow

```
[1. Bug Confirmation]
         │
         ▼
[2. Testing Skill]  ──── Produces: Reproducing test case, root cause analysis
         │
         ▼
[3. Implementation Skill]  ── Produces: Fix code
         │
         ▼
[4. Code Review Skill]  ──── Produces: Review approval
         │
         ▼
[5. Deploy & Verify]
```

## Quality Gates

### Gate 1: Confirmation → Test
- [ ] Bug reproduced in local/staging environment
- [ ] Test fails before fix (red-green testing)
- [ ] Root cause identified

### Gate 2: Test → Fix
- [ ] Fix is minimal (addresses the root cause, not symptoms)
- [ ] No unrelated changes in the same PR
- [ ] Existing tests still pass

### Gate 3: Fix → Deploy
- [ ] All blocking review findings resolved
- [ ] Regression tests pass
- [ ] Deployment plan documented for production

## Severity Classification

| Severity | Definition | Response Time |
|----------|------------|---------------|
| P0 | System down or data loss | Immediate |
| P1 | Major feature broken, no workaround | 1 hour |
| P2 | Feature broken, workaround exists | 1 day |
| P3 | Minor issue, cosmetic | Next sprint |

## Exit Criteria

- [ ] Fix deployed to production
- [ ] Bug reproducing test now passes
- [ ] Monitoring confirms no regression
- [ ] Postmortem written (P0/P1 only)
