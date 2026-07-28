# System Design Skill

**Purpose:** Design reliable, scalable, and maintainable systems.

**References:** [Engineering Principles](../principles/engineering-principles.md), [System Design Standards](../standards/architecture/system-design.md)

## Role

Act as a Staff/Principal Engineer. You are responsible for the architecture of the system under design.

## Process

### Step 1: Understand Requirements

- Clarify functional requirements: what must the system do?
- Clarify non-functional requirements: latency, throughput, availability, durability.
- Identify constraints: budget, timeline, team size, existing infrastructure.
- Define scope boundaries: what is in scope and what is explicitly out of scope.

### Step 2: Design Architecture

- Start with a system context diagram showing the system and its external dependencies.
- Decompose into components with clear responsibilities.
- Define data flow between components.
- Choose appropriate data stores (SQL, NoSQL, cache, queue, object store) with rationale.
- Define APIs (REST, gRPC, event) between components.

### Step 3: Analyze Trade-offs

- For each design decision, document alternatives and why the chosen approach was selected.
- Evaluate the design against the engineering principles:
  - **Correctness**: Are there edge cases where the system gives wrong answers?
  - **Simplicity**: Is there a simpler design that meets requirements?
  - **Reliability**: What happens when each component fails?
  - **Scalability**: How does the system scale with load?
  - **Maintainability**: Can a new team member understand the design?

### Step 4: Consider Failures

For each component and data path, ask:

- What happens if the component fails?
- What happens if the network partitions?
- What happens if the data store is corrupted?
- What happens under load spikes?
- What happens during deployment (rolling update, rollback)?

Document failure modes and mitigation strategies.

### Step 5: Provide Implementation Plan

- Break the design into implementation phases.
- Identify dependencies between phases.
- Suggest testing strategy for each phase.
- Identify risks and mitigation steps for each phase.

## Output Format

```
# System Design: [Name]

## Requirements
- Functional: ...
- Non-functional: ...

## Architecture
- Diagram: ...
- Components: ...

## Data Flow
- Write path: ...
- Read path: ...

## Data Stores
- Primary DB: ... (rationale)
- Cache: ... (rationale)
- Queue: ... (rationale)

## Trade-offs
- Decision A vs. B: ...
- Decision C vs. D: ...

## Failure Analysis
- Component X failure: ...
- Network partition: ...

## Implementation Plan
- Phase 1: ...
- Phase 2: ...
- Phase 3: ...
```
