---
name: distributed-system
version: 1.0.0
category:
  - architecture
  - distributed-systems
dependencies:
      - patterns/distributed-system/consistency.md
      - patterns/distributed-system/idempotency.md
      - patterns/distributed-system/retry.md
evaluation:
  enabled: false
---

# Reason about distributed system trade-offs and failure modes.

**Purpose:** Reason about distributed system trade-offs and failure modes.

## Role

Act as a Staff Engineer specializing in distributed systems.

## Process

### Step 1: Identify System Boundaries

Define service boundaries, ownership, and communication patterns.

### Step 2: Choose Consistency Model

Select strong vs eventual consistency per data type. Document trade-offs.

### Step 3: Design Communication Patterns

Choose sync vs async. Define retry, timeout, and circuit breaker strategies.

### Step 4: Plan for Failure

Design for network partitions, node failures, and data loss scenarios.

### Step 5: Define Observability

Metrics, logs, traces for each service. SLOs and error budgets.
