# Write-Through Cache

## Context

In Cache-Aside and Read-Through patterns, cache entries become stale when the underlying data is updated. The application must explicitly invalidate or update the cache after writes. Write-Through ensures the cache is always consistent with the database by writing to both on every update.

## Problem

How to ensure the cache is always consistent with the database without relying on explicit invalidation or TTL expiry?

## Solution

### Write-Through Pattern

On every write operation, the application writes data to both the database (source of truth) and the cache. The cache is updated synchronously as part of the write transaction, ensuring reads immediately see the updated value.

```
Application                     Cache                  Database
    │                             │                       │
    │── UPDATE data ─────────────>│                       │
    │                             │── UPDATE data ───────>│
    │                             │<── OK ─────────────────│
    │<── OK ──────────────────────│                       │
    │                             │                       │
    │── GET data ────────────────>│                       │
    │<── updated data (cached) ───│                       │
```

### Write Sequence

1. Application sends write request.
2. **Cache is updated first** (or both in a coordinated transaction).
3. **Database is updated** (source of truth).
4. Only after both succeed, the write is considered complete.
5. If the database write fails, the cache update must be rolled back.

## Implementation

```python
class WriteThroughCache:
    def __init__(self, redis_client, db_client, ttl=3600):
        self.redis = redis_client
        self.db = db_client
        self.ttl = ttl

    def set(self, key: str, data: dict) -> None:
        # Write to cache first
        self.redis.setex(key, self.ttl, serialize(data))

        # Write to database (source of truth)
        try:
            self.db.update(key, data)
        except Exception:
            # Rollback cache on database failure
            self.redis.delete(key)
            raise

    def get(self, key: str) -> dict | None:
        cached = self.redis.get(key)
        if cached is not None:
            return deserialize(cached)
        return None  # Cache miss — caller should handle
```

## Cache Update vs. Cache Invalidation

Write-Through uses **cache update** (set the new value in cache). The alternative is **cache invalidation** (delete the cache entry, let the next read populate it via Cache-Aside/Read-Through).

| Approach | Pros | Cons |
|----------|------|------|
| **Cache Update** | No cache miss on next read | Wasted writes if data is rarely read after update |
| **Cache Invalidation** | Cache only contains hot data | Cache miss penalty on next read |

**Recommendation:** Use cache update for frequently-read data, cache invalidation for rarely-read data.

## When to Use

- **Read-after-write consistency required**: the user should immediately see their own changes.
- **Write frequency is moderate**: if data is written every second but read once a week, update is wasteful.
- **Data is shared across multiple readers**: all readers should see updates promptly.

## When to Avoid

- **Write-heavy workloads**: every write updates the cache, even if the data is never read again.
- **Cache space is constrained**: unnecessary cache entries evict more valuable data.
- **Database latency is high**: synchronous writes slow down both cache and database.

## Consequences

### Benefits
- Cache is always up-to-date with the database.
- No stale reads after write operations.
- No cache miss penalty after writes.

### Trade-offs
- Write latency increases (both cache and database must be updated).
- Write amplification: cache is updated even for data that is rarely read.
- Rollback complexity: if the database write fails, the cache must be reverted.

## Related Patterns

- [Cache-Aside](cache-aside.md): Lazy cache population, requires explicit invalidation.
- [Read-Through](read-through.md): Cache-miss-driven population.
- [Write-Behind](write-behind.md): Async write optimization of this pattern.
