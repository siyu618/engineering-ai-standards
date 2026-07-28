# Python Coding Standards

## Version

- Target Python 3.11+.
- All new code must be compatible with Python 3.11 minimum.

## Style

- Follow [PEP 8](https://peps.python.org/pep-0008/) with a line length of 100 characters.
- Use [Ruff](https://docs.astral.sh/ruff/) for linting and formatting.
- Use `snake_case` for variables, functions, and methods.
- Use `PascalCase` for classes.
- Use `UPPER_CASE` for constants.
- Use `_` prefix for internal/private methods and attributes.

## Type Hints

- All function signatures must include type annotations for parameters and return values.
- Use `from __future__ import annotations` to enable deferred evaluation.
- Prefer `list[X]` over `List[X]`, `dict[K, V]` over `Dict[K, V]` (Python 3.9+ syntax).
- Use `Optional[X]` or `X | None` consistently within a project.
- Use `TypedDict` for structured dictionaries and `dataclass` or `pydantic` for data objects.
- Avoid `Any` unless interfacing with untyped third-party code.

## Error Handling

- Use specific exception types, not bare `except:` or `except Exception:`.
- Create custom exception classes for domain-level errors.
- Use `try` blocks only for the code that is expected to raise.
- Prefer `contextlib.suppress` for deliberately ignored expected exceptions.

```python
# Good
try:
    result = api_client.fetch(user_id)
except ApiTimeoutError:
    logger.warning("API timed out for user %s", user_id)
    result = fallback_data
except ApiAuthError:
    raise

# Avoid
try:
    result = api_client.fetch(user_id)
except Exception:
    pass
```

## Logging

- Use the `logging` module. Never use `print()` for production logging.
- Use lazy formatting: `logger.info("User %s logged in", user.id)` not f-strings.
- Configure structured (JSON) logging in production services.
- Include correlation IDs in log records for distributed tracing.

## Testing

- Use `pytest` as the test runner.
- Aim for 90%+ coverage on business logic; infrastructure code may have lower targets.
- Use `pytest.fixture` for test dependencies, not `setUp` methods.
- Property-based testing with `hypothesis` is encouraged for critical business logic.
- Tests must be deterministic — no dependencies on network access or time of day without mocking.

## Dependency Management

- Use `uv` or `pip-tools` for dependency pinning.
- Separate production and development dependencies.
- Pin exact versions for production deployments; use ranges only for libraries.
- Regularly audit dependencies for vulnerabilities.
