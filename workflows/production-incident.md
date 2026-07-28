# Workflow: Production Incident

**Composed Skills:** [ai-agent-development](../skills/ai-agent-development/SKILL.md) → [code-review](../skills/code-review/SKILL.md)

## Entry Criteria

- [ ] P0 or P1 incident declared
- [ ] Incident response team activated
- [ ] Communication channel established

## Flow

```
[1. Incident Detection]
         │
         ▼
[2. Triage & Mitigation]  ── Produces: Mitigation applied, service restored
         │
         ▼
[3. Root Cause Analysis]  ─ Produces: RCA document
         │
         ▼
[4. Fix Implementation]  ── Produces: Fix code (via bug-fix workflow)
         │
         ▼
[5. Code Review Skill]  ─── Produces: Review approval for fix
         │
         ▼
[6. Postmortem]
```

## Quality Gates

### Gate 1: Triage → RCA
- [ ] Service is restored or mitigated
- [ ] Timeline of events documented
- [ ] All relevant logs, metrics, and traces collected

### Gate 2: RCA → Fix
- [ ] Root cause identified and agreed upon
- [ ] Fix addresses root cause (not just symptoms)
- [ ] Test reproducing the incident scenario written

### Gate 3: Fix → Postmortem
- [ ] Fix deployed and verified
- [ ] Monitoring confirms incident resolved
- [ ] Blameless postmortem drafted

## Postmortem Requirements

- [ ] Incident summary (1-2 paragraphs)
- [ ] Timeline with all key events (detection, triage, mitigation, fix)
- [ ] Root cause analysis
- [ ] Contributing factors
- [ ] Action items with owners and due dates
- [ ] Monitoring and alerting improvements
- [ ] How to prevent recurrence

## Exit Criteria

- [ ] Service is healthy (all SLOs met)
- [ ] Postmortem completed and shared
- [ ] Action items created and tracked
- [ ] Playbook updated with lessons learned
