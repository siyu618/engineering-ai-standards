# Rust Coding Standards

## Version

- Target Rust edition 2024 (or latest stable).
- Use the latest stable Rust toolchain via `rustup`.

## Style

- Follow the [Rust Style Guide](https://rust-lang.github.io/api-guidelines/).
- Use `rustfmt` with default settings for formatting. Format on save or in CI.
- Use `clippy` as the linter. Address all warnings before merging. Use `#[allow(...)]` only with a comment explaining why.
- Use `snake_case` for variables, functions, and modules.
- Use `PascalCase` for types, traits, and enums.
- Use `SCREAMING_SNAKE_CASE` for constants and statics.

## Ownership and Borrowing

- Follow Rust's ownership model strictly. Do not use `unsafe` to circumvent the borrow checker.
- Prefer references (`&T`, `&mut T`) over `Rc`/`Arc` unless shared ownership is explicitly required.
- Use `Cow<'_, T>` (clone-on-write) for functions that may or may not need to take ownership.
- Use interior mutability (`Cell`, `RefCell`, `Mutex`) only when necessary and document the reason.

```rust
// Good
fn process_user(user: &User) -> Result<ProcessedUser, Error> {
    let validated = validate(&user.email)?;
    Ok(ProcessedUser { id: user.id, email: validated })
}

// Avoid unless necessary
fn process_user_shared(user: Arc<User>) -> Result<ProcessedUser, Error> {
    // ...
}
```

## Error Handling

- Use `Result<T, E>` for recoverable errors and `Option<T>` for absent values.
- Define domain-specific error types using `thiserror` or custom enums.
- Use `anyhow::Error` for application-level error propagation (binaries), `thiserror` for library-level errors.
- Use `?` operator for error propagation. Avoid explicit `match` on `Result` in application code.
- Do not use `unwrap()` or `expect()` in production code except in tests or when the invariant is truly impossible (with a comment).

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum UserError {
    #[error("user not found: {0}")]
    NotFound(String),
    #[error("validation error: {0}")]
    Validation(#[from] ValidationError),
    #[error("database error: {0}")]
    Database(#[from] sqlx::Error),
}

pub fn find_user(id: &str) -> Result<User, UserError> {
    let user = db::query("SELECT * FROM users WHERE id = $1", id)
        .fetch_optional()
        .await?
        .ok_or_else(|| UserError::NotFound(id.to_string()))?;
    Ok(user)
}
```

## Async Patterns

- Use `tokio` as the default async runtime for networked services.
- Use `async fn` for async functions. The return type is the concrete type, not `impl Future`.
- Use `tokio::spawn` for fire-and-forget tasks, with error handling via `JoinHandle`.
- Use `tokio::sync::Semaphore` for rate-limiting concurrent operations.
- Use `tokio::time::timeout` for all async operations with external dependencies.

```rust
pub async fn fetch_user_data(user_id: &str) -> Result<UserData, Error> {
    let user = timeout(Duration::from_secs(5), api_client.get_user(user_id))
        .await
        .map_err(|_| Error::Timeout("user API"))??;

    let preferences = timeout(Duration::from_secs(3), db::get_preferences(user_id))
        .await
        .map_err(|_| Error::Timeout("preferences DB"))?;

    Ok(UserData { user, preferences })
}
```

## Testing

- Use Rust's built-in `#[cfg(test)]` and `#[test]` for unit tests.
- Place unit tests in a `tests` module within each source file.
- Use `#[cfg(test)] mod tests { use super::*; ... }`.
- Use `assert_eq!`, `assert_ne!`, and custom assertion helpers.
- Use `#[should_panic]` only when testing that a panic is intentional.
- Use property-based testing with `proptest` or `quickcheck` for critical logic.
- Use `#[tokio::test]` for async tests.

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_parse_user_id_valid() {
        let result = parse_user_id("a1b2c3d4e5f6");
        assert!(result.is_ok());
    }

    #[test]
    fn test_parse_user_id_empty() {
        let result = parse_user_id("");
        assert!(result.is_err());
    }

    #[tokio::test]
    async fn test_fetch_user_success() {
        let user = fetch_user_data("test-id").await;
        assert!(user.is_ok());
    }
}
```

## Documentation

- All public items (functions, types, traits, fields) must have doc comments (`///` or `//!`).
- Include at least one example in doc comments for public functions.
- Use `#![warn(missing_docs)]` at the crate level for library crates.
- Run `cargo doc --no-deps` to verify documentation builds without errors.

## Dependencies

- Minimize dependencies. Each dependency adds compile time, attack surface, and maintenance burden.
- Use `cargo audit` to check for known vulnerabilities in the dependency tree.
- Pin major versions in `Cargo.toml`; use `cargo update` intentionally.
- Prefer well-established, actively maintained crates. Check the number of dependents and maintenance status.
