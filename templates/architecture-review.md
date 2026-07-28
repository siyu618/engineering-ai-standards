# Architecture Review: [System Name]

**Review Date:** [YYYY-MM-DD]
**Reviewers:** [Names]
**System Version:** [Version]

## Review Scope

[What is being reviewed? Which components, services, or design documents are in scope?]

## Summary

[One-paragraph summary of the review outcome — key findings, overall assessment, go/no-go decision.]

## Checklist

### Requirements

- [ ] Functional requirements are clearly defined and complete
- [ ] Non-functional requirements (latency, throughput, availability) are quantified
- [ ] Constraints are identified and documented
- [ ] Success criteria are measurable

### Architecture

- [ ] System context and boundaries are defined
- [ ] Components have clear, single responsibilities
- [ ] Data flow is documented for read and write paths
- [ ] Technology choices are justified with trade-off analysis
- [ ] APIs are well-defined and versioned

### Reliability

- [ ] Failure modes are identified for each component
- [ ] Degradation paths are documented
- [ ] Retry, timeout, and circuit breaker strategies are defined
- [ ] Data durability and backup strategy are documented
- [ ] Disaster recovery plan exists and is tested

### Security

- [ ] Authentication and authorization are designed in
- [ ] Data is encrypted at rest and in transit
- [ ] Input validation is at all system boundaries
- [ ] Secrets management is defined
- [ ] Security review has been completed

### Scalability

- [ ] Scalability ceilings are identified
- [ ] Horizontal scaling strategy is defined
- [ ] Database scaling (sharding, replication) is addressed
- [ ] Caching strategy is defined
- [ ] Load testing plan exists

### Observability

- [ ] Metrics (RED/USE) are defined for all components
- [ ] Structured logging with correlation IDs is implemented
- [ ] Distributed tracing is configured
- [ ] Alerting rules are defined with runbooks
- [ ] Dashboards exist for key metrics

### Operations

- [ ] Deployment strategy (rolling, blue/green) is defined
- [ ] Rollback procedure is documented
- [ ] Configuration management is externalized
- [ ] Capacity planning is addressed

## Findings

### [Severity]: [Finding Title]

**Area:** [Architecture | Reliability | Security | Scalability | Observability | Operations]
**Component:** [Affected component]

**Observation:**
[Detailed description of the finding]

**Impact:**
[What is the potential impact if not addressed?]

**Recommendation:**
[Specific, actionable suggestion for addressing the finding]

---

### [Severity]: [Finding Title]

**Area:** [Architecture | Reliability | Security | Scalability | Observability | Operations]
**Component:** [Affected component]

**Observation:**
[Detailed description of the finding]

**Impact:**
[What is the potential impact if not addressed?]

**Recommendation:**
[Specific, actionable suggestion for addressing the finding]

## Action Items

| # | Action Item | Owner | Due Date | Status |
|---|-------------|-------|----------|--------|
| 1 | [Action] | [Name] | [Date] | [Open/In Progress/Closed] |
| 2 | [Action] | [Name] | [Date] | [Open/In Progress/Closed] |

## Decision

**Approved:** [Yes/No/With Conditions]

**Conditions:** [If approved with conditions, list them here.]

## Appendix

- [Link to design document]
- [Link to related ADRs]
- [Link to risk assessment]
