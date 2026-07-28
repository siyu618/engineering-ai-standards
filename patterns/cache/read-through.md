# Read-Through Cache

## Context

Applications frequently read the same data from a slow data source. When a cache miss occurs, the application must query the database and populate the cache manually (as in Cache-Aside). Read-Through automates this by making the cache itself responsible for loading data from the database on a miss.

## Problem

How to reduce application complexity by delegating cache population to the cache layer, while maintaining consistency between cache and database?

## Solution

### Read-Through Pattern

The cache provider (e.g., Redis with server-side logic, or a caching library) intercepts read requests. On a cache miss, the cache layer loads the data from the database, stores it, and returns it to the application.

```
Application                     Cache                  Database
    │                             │                       │
    │── GET key ─────────────────>│                       │
    │                             │── (cache miss) ──────>│
    │                             │<── result ─────────────│
    │                             │── SET key: TTL ───────│
    │<── result ──────────────────│                       │
    │                             │                       │
    │── GET key ─────────────────>│                       │
    │<── result (cached) ─────────│                       │
```

### Key Difference from Cache-Aside

In **Cache-Aside**, the application is responsible for:
1. Checking the cache.
2. Querying the database on miss.
3. Populating the cache.

In **Read-Through**, the application:
1. Requests data from the cache (as if it were the primary data store).
2. The cache handles miss loading transparently.

## Implementation

### Using a Cache Library (Python)

```python
from cachetools import cached, TTLCache

# Read-through via caching decorator
cache = TTLCache(maxsize=10000, ttl=3600)

@cached(cache)
def get_user(user_id: str) -> User:
    # Only called on cache miss — cachetools handles read-through
    return database.query("SELECT * FROM users WHERE id = ?", user_id)
```

### Using Redis with Server-Side Logic

```python
import redis

class ReadThroughCache:
    def __init__(self, redis_client, db_client, ttl=3600):
        self.redis = redis_client
        self.db = db_client
        self.ttl = ttl

    def get(self, key: str, loader: callable) -> dict:
        # Check cache
        cached = self.redis.get(key)
        if cached is not None:
            return deserialize(cached)

        # Cache miss — load from database via the loader function
        data = loader()
        if data is None:
            return None

        # Populate cache
        self.redis.setex(key, self.ttl, serialize(data))
        return data
```

## When to Use

- **Data is read frequently** but written infrequently.
- **Read workload dominates** (e.g., 95%+ reads).
- **Cache miss penalty is acceptable** — the first read after a TTL expiry will be slow.

## When to Avoid

- **Write-heavy workloads**: the cache will constantly miss due to frequent invalidations.
- **Data changes frequently**: TTL management becomes complex and stale reads are common.
- **Low read volume**: the overhead of maintaining the cache layer isn't justified.

## Consequences

### Benefits
- Simplified application logic: no explicit cache check/populate code.
- Centralized cache strategy: all cache loading logic is in one place.
- Consistent behavior: all reads go through the same path.

### Trade-offs
- Cache provider lock-in: requires a cache that supports read-through (or a library that provides it).
- Cold start: all data starts cold (population on first access).
- Cache stampede: multiple concurrent misses for the same key all trigger database queries.

## Related Patterns

- [Cache-Aside](cache-aside.md): Application-managed cache loading (simpler, more control).
- [Write-Through](write-through.md): Keeps cache in sync on writes.
- [Write-Behind](write-behind.md): Async write optimization.
