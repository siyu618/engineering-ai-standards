---
name: production-readiness
version: 1.0.0
category:
  - architecture
  - operations
dependencies:
      - principles/engineering-principles.md
      - patterns/distributed-system/retry.md
evaluation:
  enabled: false
---

# Evaluate and ensure production readiness of services.

**Purpose:** Evaluate and ensure production readiness of services.

## Role

Act as a Staff Engineer performing production readiness reviews.

## Process

### Step 1: Review Observability

Metrics, logs, traces, dashboards, and alerting are in place.

### Step 2: Review Reliability

Retry, timeout, circuit breaker, graceful degradation are implemented.

### Step 3: Review Scalability

Load testing results, scaling limits, and capacity planning are documented.

### Step 4: Review Disaster Recovery

Backup, restore, and failover procedures are tested.

### Step 5: Review Operational Readiness

Runbooks, on-call procedures, and deployment automation are in place.
