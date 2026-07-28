# Go Coding Standards

## Version

- Target Go 1.22+.
- Use Go modules (`go.mod`) for dependency management.

## Style

- Follow [Effective Go](https://go.dev/doc/effective_go) and [Go Code Review Comments](https://go.dev/wiki/CodeReviewComments).
- Use `gofmt` or `go fmt` for automatic formatting. No exceptions — formatting is non-negotiable in Go.
- Use `go vet` as the minimum static analysis. Add `staticcheck` for deeper linting.
- Use `MixedCaps` or `mixedCaps` (exported vs. unexported) rather than underscores.
- File names are `snake_case.go`.

## Conventions

- **Exported identifiers**: Capitalize the first letter of exported names. This is how Go controls visibility.
- **Interfaces**: Name with `-er` suffix where possible (`Reader`, `Writer`, `Processor`). Keep interfaces small (1-3 methods).
- **Errors**: Error values start with lowercase (unless they begin with a proper noun) and should not end with punctuation.
- **Packages**: Use short, lowercase, single-word package names. Avoid `util`, `common`, `misc`.

```go
// Good
package user

type Service struct { /* ... */ }

func (s *Service) Create(ctx context.Context, req *CreateRequest) (*User, error) {
    return s.store.Create(ctx, req)
}

// Avoid
package user_management

type UserManagementService struct { /* ... */ }
```

## Error Handling

- Handle errors explicitly. There is no `try-catch` in Go by design.
- Use `errors.Is` and `errors.As` for error inspection. Use `fmt.Errorf` with `%w` for error wrapping.
- Sentinel errors should be defined as `var ErrNotFound = errors.New("user not found")`.
- Do not use `_` to discard errors. If a function returns an error, handle it or explicitly ignore with a comment explaining why.

```go
// Good
user, err := s.store.FindByID(ctx, id)
if err != nil {
    if errors.Is(err, ErrNotFound) {
        return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
    }
    return nil, fmt.Errorf("finding user %s: %w", id, err)
}

// Never
user, _ := s.store.FindByID(ctx, id)
```

## Concurrency

- Use `sync.WaitGroup` for waiting on a collection of goroutines.
- Use `errgroup` from `golang.org/x/sync/errgroup` for goroutines that return errors.
- Use `context.Context` as the first parameter of any blocking or cancellable function.
- Use channels for communication, `sync.Mutex` or `sync.RWMutex` for mutual exclusion.
- Avoid `sync.Once` for anything other than one-time initialization.

```go
func (s *Service) ProcessBatch(ctx context.Context, ids []string) error {
    g, ctx := errgroup.WithContext(ctx)
    for _, id := range ids {
        id := id // capture
        g.Go(func() error {
            return s.processOne(ctx, id)
        })
    }
    return g.Wait()
}
```

## Testing

- Use Go's built-in `testing` package as the primary test framework.
- Use `testify/assert` or `testify/require` for assertions.
- Use table-driven tests for testing multiple scenarios.

```go
func TestParseUserID(t *testing.T) {
    tests := []struct {
        name    string
        input   string
        want    UserID
        wantErr bool
    }{
        {"valid hex string", "a1b2c3d4e5f6", "a1b2c3d4e5f6", false},
        {"empty string", "", "", true},
        {"invalid characters", "zzzzzzzzzzzz", "", true},
    }
    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := ParseUserID(tt.input)
            if tt.wantErr {
                require.Error(t, err)
                return
            }
            require.NoError(t, err)
            assert.Equal(t, tt.want, got)
        })
    }
}
```

## Documentation

- Every exported identifier must have a doc comment.
- Use `// Package ...` comments at the top of package files.
- Use `go doc` or `pkgsite` to verify documentation renders correctly.
- Include example code in `_test.go` files or `example_test.go` for runnable examples.

## Performance

- Prefer `make` with capacity hints for slices and maps when size is known or bounded.
- Use `sync.Pool` for frequently allocated temporary objects.
- Profile before optimizing. Use `pprof` and `benchstat` to measure and compare.
- Avoid reflection in hot paths. Use code generation (`go generate`) as an alternative.
