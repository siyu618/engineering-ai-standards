# Example: Payment System Testing Strategy

This example walks through using the [Testing Skill](../SKILL.md) to design a test strategy.

## Step 1: Analyze the Code

- **Type**: Distributed microservices with async message flows
- **Dependencies**: Payment gateway (external), Kafka, PostgreSQL, Redis
- **Critical paths**: Payment authorization, refund processing, reconciliation

## Step 2: Design Test Strategy

| Level | Coverage | Focus |
|-------|----------|-------|
| Unit | 80% | Business logic, validation, idempotency key generation |
| Integration | 15% | Database queries, Kafka producers/consumers, gateway adapter |
| E2E | 5% | Complete payment flow (authorize → capture → settle) |

## Step 3: Key Test Cases

### Unit: Idempotency Key Validation

```python
def test_idempotency_key_rejects_duplicate():
    key = IdempotencyKey("550e8400-e29b-41d4-a716-446655440000")
    assert key.is_valid()
    result = payment_service.process(key=key, amount=100)
    assert result.status == "completed"
    duplicate = payment_service.process(key=key, amount=100)
    assert duplicate.status == "duplicated"
    assert duplicate.original_id == result.id
```

### Integration: Kafka Message Delivery

```python
def test_payment_confirmed_message_published():
    payment = create_payment(amount=100)
    messages = kafka_consumer.poll(timeout=5)
    assert any(
        m.topic == "payment.confirmed" and m.value["payment_id"] == payment.id
        for m in messages
    )
```

## Step 4: Verify Test Quality

- All tests pass 10/10 runs (determinism check)
- Mutation testing: >90% of mutants killed
- No flaky tests in past 2 weeks of CI runs
