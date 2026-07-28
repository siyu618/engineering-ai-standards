# Workflow: Architecture Review

**Composed Skills:** [design](../skills/design/SKILL.md) → [code-review](../skills/code-review/SKILL.md)

## Entry Criteria

- [ ] Design document submitted
- [ ] At least one alternative considered
- [ ] Failure modes identified

## Flow

```
[1. Design Document Submission]
         │
         ▼
[2. Design Skill Review]  ── Produces: Architecture assessment, trade-off analysis
         │
         ▼
[3. Code Review Skill]  ──── Produces: Design review findings
         │
         ▼
[4. ADR Creation]
         │
         ▼
[5. Decision & Approval]
```

## Quality Gates

### Gate 1: Document → Review
- [ ] Design doc follows the [design doc template](../templates/design-doc.md)
- [ ] All sections completed (not just architecture)
- [ ] Risks and mitigations documented

### Gate 2: Review → ADR
- [ ] All blocking concerns addressed
- [ ] Consensus reached among reviewers
- [ ] ADR follows the [ADR template](../templates/adr.md)

## Review Checklist

- [ ] Requirements are clear and complete
- [ ] Architecture addresses non-functional requirements
- [ ] Data flow is documented for read and write paths
- [ ] Consistency model is appropriate
- [ ] Failure modes are identified and mitigated
- [ ] Security considerations are addressed
- [ ] Scalability ceilings are documented

## Exit Criteria

- [ ] ADR approved and merged
- [ ] Architecture decision communicated to affected teams
- [ ] Implementation tickets created (if applicable)
