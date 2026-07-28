# Idempotency

## Context

In distributed systems, network failures, timeouts, and retries can cause the same operation to be delivered more than once. Without idempotency guarantees, duplicate operations can lead to incorrect state: double charges, duplicate orders, or inconsistent data.

## Problem

How to ensure that an operation can be safely applied multiple times without changing the result beyond the first application?

## Solution

### Idempotency Key Pattern

The caller generates a unique idempotency key for each operation and sends it with the request. The server tracks used keys and returns the stored result for duplicate requests instead of re-executing the operation.

```
Client                              Server
  │                                   │
  │── Request(idempotency_key=abc) ──>│
  │                                   ├── Check key "abc"
  │                                   ├── Not found → execute operation
  │                                   ├── Store result for key "abc"
  │<── Response(result) ──────────────│
  │                                   │
  │── Request(idempotency_key=abc) ──>│  (retry)
  │                                   ├── Check key "abc"
  │                                   ├── Found → return stored result
  │<── Response(result) ──────────────│
```

### Key Generation

- Keys should be client-generated to allow safe retry from the client side.
- UUID v4 or v7 is the recommended key format.
- The key must be unique across the entire scope of the operation (e.g., per user, per resource).

### Key Storage

- Keys must be stored durably before executing the operation (at-least-once semantics).
- Set a TTL on the key based on the retry window (typical: 24 hours).
- Use a highly available data store (Redis with replication, DynamoDB, PostgreSQL).
- Index the key for fast lookup; a primary key lookup is ideal.

### Key Lifecycle

1. Client generates a unique idempotency key.
2. Server receives request and checks the key in the idempotency store.
3. If key not found: execute the operation and store the result.
4. If key found: return the stored result (do not re-execute).
5. If key found but operation is still in-flight: return 409 Conflict or 429 Too Many Requests.
6. Keys expire after TTL; expired keys can be safely purged.

## Implementation

### HTTP API Pattern

```
POST /api/orders
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000
```

- Accept the idempotency key via a request header.
- Return 201 Created for initial request, 200 OK for retries.
- Include the idempotency key in the response for debugging.

### Database Pattern (Transactional)

```sql
-- Attempt to insert the idempotency key
INSERT INTO idempotency_keys (key, handler, created_at)
VALUES ('abc', 'create_order', NOW())
ON CONFLICT (key) DO NOTHING
RETURNING *;

-- If row inserted: execute business logic
-- If row exists: return previous result
```

## Consequences

### Benefits
- Safe retry: clients can retry without fear of duplicate side effects.
- Exactly-once processing semantics at the application level.
- Simplified client error handling.

### Trade-offs
- Storage overhead for tracking idempotency keys.
- TTL management: keys must live long enough for retries but not forever.
- Cache invalidation: if the operation result changes (rare), stored results may be stale.

## Related Patterns

- [Retry](retry.md): Use idempotency to enable safe retry.
- [Consistency](consistency.md): Idempotency keys work best with strong consistency on the key store.
- **Optimistic Locking**: Alternative approach for preventing duplicate writes using version numbers.
