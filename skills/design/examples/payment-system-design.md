# Example: Payment System Design

This example walks through using the [Design Skill](../SKILL.md) to design a payment processing system.

## Step 1: Understand Requirements

**Functional:**
- Process credit card payments
- Handle refunds
- Provide transaction history
- Support multiple currencies

**Non-functional:**
- 99.99% availability
- p99 latency under 200ms
- PCI-DSS compliance
- 10,000 TPS peak

## Step 2: Design Architecture

```
[Client] → [API Gateway] → [Payment Service] → [Processor Adapter] → [External Gateway]
                                │                       │
                          [Transaction DB]        [Fraud Detection]
```

## Step 3: Trade-offs

| Decision | Alternative | Chosen | Rationale |
|----------|-------------|--------|-----------|
| Synchronous vs async processing | Async | Sync for payments | Users need immediate confirmation |
| Idempotency key storage | Redis vs PostgreSQL | PostgreSQL | Strong consistency required for payments |

## Step 4: Failure Analysis

- **Payment service down**: Queue requests, return 503, retry with backoff
- **External gateway timeout**: Retry with idempotency key, circuit breaker after 3 failures
- **Database partition**: Read replica promotion, eventual consistency acceptable for history queries

## Step 5: Implementation Plan

1. Core API and idempotency layer
2. Processor adapter interface (Stripe, Adyen)
3. Fraud detection integration
4. Reconciliation and audit pipeline
