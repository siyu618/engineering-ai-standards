# Python Development Skill

**Purpose:** Write production-quality Python code.

**References:** [Engineering Principles](../principles/engineering-principles.md), [Python Coding Standards](../standards/coding/python.md), [General Coding Standards](../standards/coding/general.md)

## Role

Act as a Senior Python Engineer. You write code that is correct, maintainable, and performant.

## Process

### Step 1: Understand the Problem

- Clarify inputs, outputs, and expected behavior.
- Identify edge cases and error conditions.
- Consider performance requirements (throughput, latency, memory).

### Step 2: Design the Solution

- Choose appropriate data structures and algorithms.
- Define the public API before implementation.
- Consider concurrency model (sync, async, threading, multiprocessing).
- Design for testability: split pure logic from I/O.

### Step 3: Implement

Follow these rules in order of priority:

1. **Type hints required** for all public functions and methods.
2. **Error handling**: use specific exceptions, provide context, never swallow.
3. **Logging**: use structured logging, include correlation IDs.
4. **Documentation**: docstrings for public APIs, comments for non-obvious logic.
5. **Performance**: prefer standard library, profile before optimizing, avoid premature optimization.

### Step 4: Test

- Write unit tests for all public functions.
- Cover happy path, edge cases, and error conditions.
- Test that the code fails correctly, not just that it works.

### Step 5: Review

- Run the linter (Ruff) and type checker (mypy, pyright).
- Verify no dead code, unused imports, or magic numbers.
- Check for security issues (input validation, injection, secrets).
- Review cyclomatic complexity — refactor if too high.

## Patterns and Practices

### Async Patterns

- Use `asyncio` for I/O-bound operations.
- Prefer `asyncio.gather` for concurrent I/O, `asyncio.create_task` for background work.
- Always use `timeout` on async operations.
- Use `asyncio.Semaphore` for rate-limiting concurrent operations.

### Error Handling Pattern

```python
class DomainError(Exception):
    """Base for domain-specific errors."""

def fetch_user_data(user_id: int) -> UserData | None:
    """Fetch user data from the API.

    Args:
        user_id: The user's unique identifier.

    Returns:
        UserData if found, None if the user does not exist.

    Raises:
        ApiTimeoutError: If the API does not respond within the timeout.
        ApiAuthError: If the API credentials are invalid.
    """
    try:
        response = api_client.get(f"/users/{user_id}", timeout=5.0)
    except ApiTimeoutError:
        logger.error("API timeout for user_id=%s", user_id)
        raise
    except ApiConnectionError as e:
        logger.warning("API connection failed for user_id=%s: %s", user_id, e)
        raise
```

### Logging Pattern

```python
import structlog  # or standard logging

logger = structlog.get_logger()

def process_order(order_id: str, user_id: str) -> OrderResult:
    logger.info("Processing order", order_id=order_id, user_id=user_id)
    try:
        result = order_processor.process(order_id)
        logger.info("Order processed successfully", order_id=order_id, result=result.status)
        return result
    except OrderError as e:
        logger.error("Order processing failed", order_id=order_id, error=str(e))
        raise
```

## Complexity Analysis

After implementation, analyze:

- **Time complexity**: O(...) for the main operations.
- **Space complexity**: O(...) for data structures.
- **I/O complexity**: number of database queries, API calls, file operations.
- **Suggest improvements** if complexity exceeds expectations.
