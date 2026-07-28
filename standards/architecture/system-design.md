# System Design Standards

## API Design

### REST

- Use resource-oriented URLs: `/users/{id}/orders/{order_id}`
- Use HTTP methods correctly: GET (read), POST (create), PUT (replace), PATCH (partial update), DELETE (remove).
- Use standard HTTP status codes: 200 (OK), 201 (Created), 204 (No Content), 400 (Bad Request), 401 (Unauthorized), 403 (Forbidden), 404 (Not Found), 409 (Conflict), 422 (Unprocessable Entity), 429 (Too Many Requests), 500 (Internal Server Error).
- Paginate list endpoints with cursor-based pagination. Offset-based pagination is acceptable only for small, stable datasets.
- Version APIs via URL prefix (`/v1/`) or content negotiation. Never expose unversioned APIs.

### gRPC

- Use Protocol Buffers v3 for service definitions.
- Define service, RPC, message, and enum in a single `.proto` file per bounded context.
- Prefer unary RPCs unless streaming semantics are explicitly required.
- Handle gRPC status codes correctly: translate internal errors to appropriate gRPC codes.

### GraphQL

- Follow the schema-first approach: design the schema before implementing resolvers.
- Use connections (cursor-based pagination) for list fields per Relay specification.
- Implement DataLoader or equivalent for batching and deduplication.
- Guard against deep query nesting with maximum depth and complexity limits.

## Database Design

- Define clear ownership: each service owns its data store. Do not share databases across services.
- Use migrations for schema changes. Every migration must be reversible.
- Index with intention: add indexes based on query patterns, not speculation.
- Use read replicas for read-heavy workloads; route writes to the primary.
- Document the consistency model (strong vs. eventual) for each data store.

## Distributed Systems Fundamentals

- All inter-service communication must assume network failure. Use timeouts, retries with backoff, and circuit breakers.
- Prefer asynchronous communication (message queues, event streams) over synchronous calls for non-critical paths.
- Every service must expose health check and metrics endpoints.
- Distributed tracing must be implemented across all services using a shared trace context.

## Observability

- **Logging**: Structured, centralized, with correlation IDs across service boundaries.
- **Metrics**: RED (Rate, Errors, Duration) metrics for every service endpoint. USE (Utilization, Saturation, Errors) for every resource.
- **Tracing**: End-to-end trace for every request crossing service boundaries. Sample 100% of errors, 1-10% of successful requests.
- **Alerting**: Alert on symptoms (high latency, error rate) not causes (high CPU). Define SLOs and error budgets.
