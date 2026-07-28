# Cache-Aside (Lazy Loading)

## Context

Applications frequently access data from slow data sources (databases, external APIs, file systems). Caching frequently accessed data in a fast data store (Redis, Memcached) can dramatically reduce latency and load.

## Problem

How to cache data while keeping the cache consistent with the source of truth, handling cache failures gracefully, and avoiding stale reads?

## Solution

### Cache-Aside Pattern

The application is responsible for loading data into the cache on demand. The cache is not automatically populated — it is populated by the application when a cache miss occurs.

```
Application                          Cache           Database
    │                                  │                │
    │── GET key ──────────────────────>│                │
    │<── MISS ─────────────────────────│                │
    │                                  │                │
    │── SELECT * FROM table WHERE ... ────────────────>│
    │<── result ───────────────────────────────────────│
    │                                  │                │
    │── SET key = result ─────────────>│                │
    │<── OK ───────────────────────────│                │
    │                                  │                │
    │── GET key ──────────────────────>│                │
    │<── result ───────────────────────│                │
```

### Read-Through Procedure

1. Check the cache for the requested key.
2. If found (cache hit), return the cached value.
3. If not found (cache miss), query the database.
4. Store the result in the cache with a TTL.
5. Return the result.

### Write-Through Procedure

When updating data:

1. Write the update to the database.
2. Delete (or update) the corresponding cache entry.
3. Do NOT write to cache first — write to the database as the source of truth.

## Implementation

### Basic Cache-Aside (Python)

```python
def get_user(user_id: str) -> User:
    cache_key = f"user:{user_id}"

    # Check cache
    cached = redis.get(cache_key)
    if cached is not None:
        return deserialize_user(cached)

    # Cache miss — query database
    user = database.query("SELECT * FROM users WHERE id = ?", user_id)
    if user is None:
        return None

    # Populate cache (with TTL)
    redis.setex(cache_key, 3600, serialize_user(user))
    return user

def update_user(user_id: str, data: dict) -> User:
    # Write to source of truth
    user = database.execute(
        "UPDATE users SET name = ? WHERE id = ? RETURNING *",
        data["name"], user_id
    )

    # Invalidate cache
    redis.delete(f"user:{user_id}")
    return user
```

## Cache Failure Handling

### Cache Breakdown

When a cache miss is followed by a database failure, the application should:
1. Return stale data if available (graceful degradation).
2. Return an error if no stale data exists.
3. Never return incorrect data.

### Cache Penetration

When a key is repeatedly requested but doesn't exist in the database:
- Cache the null result with a short TTL (e.g., 60 seconds).
- Use a Bloom filter to check key existence before hitting the cache.

### Cache Avalanche

When many cached entries expire simultaneously:
- Add jitter to TTL values: `ttl = base_ttl + random(-ttl_jitter, ttl_jitter)`.
- Use a warm-up process before enabling the cache for new deployments.
- Consider using a dedicated cache layer for hot keys that never expires.

### Hot Key

When a single key receives a disproportionate amount of traffic:
- Split the hot key across multiple cache nodes (e.g., `key:1`, `key:2`, ..., `key:N`).
- Use local in-process cache as an L1 cache with a very short TTL (seconds).
- Consider pre-computing the value and pushing updates to cache nodes.

## Monitoring

Essential metrics for cache performance:
- **Hit rate**: Cache hits / total requests. Alert if trending downward.
- **Miss rate**: Cache misses / total requests. High miss rate may indicate TTL too short.
- **Stale reads**: Data returned from cache that was outdated. Track via version comparison.
- **Latency**: Cache read/write latency. Should be orders of magnitude below database latency.

## Consequences

### Benefits
- Cache contains only what is actually requested (efficient space usage).
- Resilient to cache failure: application can fall back to database.
- Simple to implement and understand.

### Trade-offs
- Cold start: initial requests after deployment will experience cache misses and higher latency.
- Stale data: writes invalidate the cache, but concurrent reads may see stale data until invalidation completes.
- Cache stampede: multiple concurrent requests for the same missing key all hit the database.

## Related Patterns

- **Read-Through Cache**: Cache automatically loads data from the database on miss.
- **Write-Through Cache**: Cache is updated on every write, keeping it always current.
- **Write-Behind Cache**: Writes are batched and asynchronously written to the database.
