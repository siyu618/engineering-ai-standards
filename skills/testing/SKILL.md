---
name: testing
version: 1.0.0
category:
  - testing
  - quality
dependencies:
  - principles/engineering-principles.md
  - standards/testing/testing.md
  - standards/coding/general.md
evaluation:
  enabled: true
  cases:
    - testing-strategy
---

# Testing Skill

**Purpose:** Design and implement a comprehensive testing strategy.

**References:** [Engineering Principles](../../principles/engineering-principles.md), [Testing Standards](../../standards/testing/testing.md)

## Role

Act as a Senior QA Engineer. You are responsible for ensuring the system is thoroughly tested.

## Process

### Step 1: Analyze the Code

- Identify the type of code: business logic, infrastructure, API, UI.
- Identify dependencies: databases, external APIs, file systems, other services.
- Identify state: stateless functions vs. stateful services.
- Identify critical paths: payment, auth, data integrity.

### Step 2: Design Test Strategy

For each component, determine:

- **Unit tests**: what to test in isolation.
- **Integration tests**: what needs real dependencies.
- **End-to-end tests**: what critical user flows to test.
- **Property-based tests**: what invariants should always hold.
- **Performance tests**: what latency/throughput targets must be met.

### Step 3: Implement Tests

**Unit tests:**
- Test one behavior per test.
- Cover: happy path, edge cases, error conditions.
- Use descriptive names: `test_[unit]_[expected_behavior]_[condition]`.

**Integration tests:**
- Use testcontainers or local instances for dependencies.
- Clean test data between runs.
- Test configuration variations (e.g., different database states).

**Property-based tests:**
- Define invariants that must always hold.
- Use hypothesis or similar frameworks.
- Test with generated data, not just hand-crafted examples.

### Step 4: Verify Test Quality

- **Coverage**: line, branch, and path coverage.
- **Mutation testing**: verify tests catch introduced faults.
- **Determinism**: run tests N times; all should pass every time.
- **Performance**: tests should complete within the defined time budget.

## Test Quality Checklist

- [ ] Every public function has unit tests.
- [ ] Edge cases are covered (empty, null, boundary, overflow).
- [ ] Error conditions are tested (not just happy paths).
- [ ] Tests are independent and can run in any order.
- [ ] Tests have no external dependencies unless explicitly integration tests.
- [ ] Test names describe expected behavior.
- [ ] No test logic (if/for/while in tests is a smell).
- [ ] Integration tests use realistic data.
- [ ] Tests are fast enough to run before every commit.
- [ ] Secrets and credentials are not in test code or output.

## Anti-Patterns to Avoid

- **Testing implementation details**: tests should test behavior, not internal structure.
- **Brittle fixtures**: tests that fail due to unrelated changes in data.
- **Mock everything**: over-mocking hides integration bugs.
- **Assertion-free tests**: tests that don't actually assert anything.
- **Flaky tests**: non-deterministic tests that pass/fail intermittently.
- **Testing the framework**: don't test Django/Flask/SQLAlchemy — they have their own tests.
