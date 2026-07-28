# Testing Standards

## Testing Pyramid

Follow the standard testing pyramid:

1. **Unit tests** (70% of effort) — Fast, isolated, testing individual functions and classes.
2. **Integration tests** (20% of effort) — Testing interactions between components, databases, and external services.
3. **End-to-end tests** (10% of effort) — Testing complete user workflows through the system.

## Unit Testing

- Every public function must have unit tests covering:
  - Happy path
  - Edge cases (empty input, boundary values, type mismatches)
  - Error conditions and exception paths
- Tests must be independent. No test should depend on another test's execution or state.
- Use test doubles (mocks, stubs, fakes) for external dependencies, but prefer fakes over mocks when the fake is simpler than the mock setup.
- Avoid mocking what you don't own — write integration tests for third-party library interactions instead.

## Integration Testing

- Integration tests should cover the critical paths through databases, message queues, caches, and external APIs.
- Use testcontainers or similar for managing ephemeral infrastructure.
- Clean test data between runs. Prefer transaction rollback or truncation over teardown logic.
- Integration tests should be runnable locally with minimal setup.

## Test Quality

- Tests must be deterministic: same code, same test, same result, every time.
- Avoid test logic (no `if` statements, loops, or complex expressions in tests).
- One assertion concept per test. Multiple assertions are acceptable if they test the same behavior from different angles.
- Tests should read as specifications: the test name should describe the expected behavior in plain language.

```python
# Good
def test_withdraw_reduces_balance_when_sufficient_funds():
    ...

# Avoid
def test_withdraw():
    ...
```

## Test Naming Convention

```
test_<unit>_<expected_behavior>_<condition>()
```

Examples:
- `test_transfer_succeeds_when_balance_sufficient()`
- `test_transfer_fails_when_balance_insufficient()`
- `test_transfer_raises_error_when_amount_negative()`

## Coverage Requirements

- Line coverage: minimum 80%, target 90%
- Branch coverage: minimum 70%, target 85%
- Critical paths (payment, auth, data integrity): minimum 95% branch coverage
- Coverage of error handlers: 100%

## Performance Testing

- All critical paths must have performance benchmarks.
- Performance tests must be repeatable and run in a controlled environment.
- Define performance budgets per endpoint/function and alert when they are exceeded.
- Load tests must simulate realistic traffic patterns, not just straight-line throughput.

## Security Testing

- All input validation logic must be tested for injection attacks, boundary violations, and encoding issues.
- Authentication and authorization logic must have dedicated test suites.
- Dependency vulnerability scanning must be part of the CI pipeline.
- Secrets and credentials must never appear in test output or logs.
