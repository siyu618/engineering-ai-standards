# TypeScript Coding Standards

## Version

- Target TypeScript 5.x with strict mode enabled.
- Target Node.js 20 LTS or latest stable.

## Style

- Follow the [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) or project-configured formatter (Prettier).
- Use 2-space indentation, 100-character line length.
- Use `camelCase` for variables, functions, and methods.
- Use `PascalCase` for classes, interfaces, types, and enums.
- Use `UPPER_CASE` for global constants.
- Use `kebab-case` for file names.

## Type System

- Enable `strict: true` in `tsconfig.json`. This enables `noImplicitAny`, `strictNullChecks`, `strictFunctionTypes`, and others.
- Prefer `interface` over `type` for object shapes that may be extended.
- Use `type` for unions, intersections, and mapped types.
- Avoid `any`. Use `unknown` when the type is truly not known, and narrow with type guards.
- Use `as const` for literal types and readonly arrays.
- Use branded types for domain primitives (e.g., `UserId` instead of `string`).

```typescript
// Good
type UserId = string & { readonly __brand: "UserId" };
function createUserId(id: string): UserId {
  return id as UserId;
}

interface User {
  readonly id: UserId;
  readonly email: string;
  readonly createdAt: Date;
}

// Avoid
function process(data: any): any {
  return data;
}
```

## Error Handling

- Use typed errors — either custom `Error` subclasses or discriminated union result types.
- Avoid throwing non-Error values.
- Use the Result pattern for expected failures:

```typescript
type Result<T, E = Error> = { ok: true; value: T } | { ok: false; error: E };

function parseUserId(input: string): Result<UserId, ValidationError> {
  if (!input.match(/^[a-f0-9]{24}$/)) {
    return { ok: false, error: new ValidationError("Invalid user ID format") };
  }
  return { ok: true, value: input as UserId };
}
```

## Async Patterns

- Use `async/await` over raw promises. Avoid callback-based APIs.
- All async functions must have explicit return types: `Promise<T>`.
- Use `Promise.all` for independent concurrent operations, `Promise.allSettled` when partial success is acceptable.
- Always handle promise rejections — no floating promises.
- Use `AbortController` for cancellable async operations.

## Testing

- Use `vitest` or `jest` as the test runner.
- Aim for 90%+ coverage on business logic.
- Use `describe`/`it` blocks with descriptive names.
- Prefer `toBe`, `toEqual` over `toBeTruthy` for explicit assertions.
- Use `test.each` for data-driven tests.

## Linting and Formatting

- Use `eslint` with `@typescript-eslint` plugin.
- Use `prettier` for consistent formatting.
- Enforce import order via `eslint-plugin-import`.

## Dependency Management

- Use `pnpm` as the package manager (or `npm` if locked by project).
- Pin exact versions in production dependencies; use ranges for dev dependencies.
- Regularly run `npm audit` or `pnpm audit` for vulnerability scanning.
- Keep `node_modules` out of version control.
