# General Coding Standards

## Code Quality

- All code must pass linting and static analysis before merging.
- No dead code, commented-out code, or unused imports in production code.
- Functions should do one thing and do it well. If a function cannot be described in a single sentence, it is doing too much.
- Maximum function complexity should be enforced via cyclomatic complexity checks (threshold: 10).
- All public APIs must have type signatures or type annotations.
- Magic numbers and strings must be named constants.

## Naming Conventions

- Names must reveal intent. Avoid single-letter names (except loop indices and mathematical functions where the domain is well-known).
- Boolean variables and functions should read as predicates: `is_active`, `has_permission`, `should_retry`.
- Consistency within a codebase takes precedence over personal preference.
- Avoid abbreviations unless they are universal (e.g., `ID`, `URL`, `HTTP`).

## Error Handling

- Do not silently swallow exceptions. Every error handler must either handle, re-raise, or log with context.
- Fail fast: validate inputs at system boundaries (API, file read, user input).
- Use structured error types that carry context, not bare strings.
- Do not use exceptions for control flow.

## Logging

- Log levels must be used consistently:
  - **ERROR**: Something is broken and needs human intervention.
  - **WARN**: Something unexpected happened but the system recovered.
  - **INFO**: Significant lifecycle events (startup, shutdown, configuration change).
  - **DEBUG**: Detailed information for diagnosing issues.
- Every log line must include enough context to understand what happened without needing to read the source code.
- Sensitive data (passwords, tokens, PII) must never be logged.

## Documentation

- Complex logic must have inline comments explaining *why*, not *what*.
- Every public module, class, and function must have a docstring or documentation comment.
- Documentation is part of the codebase: update it alongside code changes.
- Prefer self-documenting code over excessive comments.

## Version Control

- Commit messages should follow conventional commits format: `type(scope): description`.
- Each commit should represent a single logical change.
- Do not commit secrets, credentials, or configuration files containing sensitive data.
- Large binary files should use Git LFS or be excluded entirely.
