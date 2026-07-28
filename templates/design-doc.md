# Design Document: [Title]

**Status:** [Draft | In Review | Approved | Superseded]
**Author(s):** [Name]
**Date:** [YYYY-MM-DD]
**PR/FD:** [Link to design review PR or document]

## 1. Background

[Explain the context and motivation for this design. What problem are we solving? What triggered this work? Include relevant history and previous attempts if applicable.]

## 2. Goals

- [Goal 1: Measurable outcome]
- [Goal 2: Measurable outcome]
- [Goal 3: Measurable outcome]

## 3. Non-Goals

- [Explicitly out of scope 1]
- [Explicitly out of scope 2]

## 4. Requirements

### Functional Requirements

- [FR1]: [Description]
- [FR2]: [Description]

### Non-Functional Requirements

- **Scalability**: [Target throughput, latency, data volume]
- **Availability**: [Target uptime, RTO, RPO]
- **Security**: [Authentication, authorization, data protection]
- **Compliance**: [Regulatory requirements]
- **Operability**: [Monitoring, deployment, rollback]

## 5. Architecture

### System Context

[Describe the system and its external dependencies. Include a context diagram or description.]

### Components

| Component | Responsibility | Technology | Rationale |
|-----------|---------------|------------|-----------|
| [Name] | [What it does] | [Tech stack] | [Why this choice] |
| [Name] | [What it does] | [Tech stack] | [Why this choice] |

### Data Flow

**Write path:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Read path:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

### Data Model

[Describe key data entities, their relationships, and storage strategy. Include schema if relevant.]

## 6. Alternatives Considered

| Alternative | Pros | Cons | Verdict |
|-------------|------|------|---------|
| [Option A] | [Pros] | [Cons] | [Why rejected] |
| [Option B] | [Pros] | [Cons] | [Why chosen] |

## 7. Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| [Risk description] | [High/Med/Low] | [High/Med/Low] | [Mitigation strategy] |
| [Risk description] | [High/Med/Low] | [High/Med/Low] | [Mitigation strategy] |

## 8. Testing Plan

- **Unit tests**: [What will be unit tested]
- **Integration tests**: [What integration tests are needed]
- **End-to-end tests**: [E2E test scenarios]
- **Performance tests**: [Load/stress test targets]
- **Chaos tests**: [Failure injection scenarios]

## 9. Implementation Plan

### Phase 1: [Name]
- **Duration**: [Estimate]
- **Deliverables**: [What ships]
- **Dependencies**: [What must exist first]

### Phase 2: [Name]
- **Duration**: [Estimate]
- **Deliverables**: [What ships]
- **Dependencies**: [What must exist first]

## 10. Appendix

- [Link to related documents, RFCs, benchmarks]
- [Glossary of terms]
