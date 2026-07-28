# Write-Behind Cache (Write-Back)

## Context

Write-Through cache ensures consistency by writing to both cache and database synchronously, but it adds write latency. For write-heavy workloads or when the database is a bottleneck, you may want to acknowledge writes quickly and propagate them to the database asynchronously.

## Problem

How to provide low-latency write acknowledgment while ensuring data is eventually persisted to the database?

## Solution

### Write-Behind Pattern

Data is written to the cache immediately, and the database is updated asynchronously. The cache acts as a buffer, accumulating writes and persisting them in batches or after a delay.

```
Application                     Cache                  Database
    │                             │                       │
    │── UPDATE data ─────────────>│                       │
    │<── OK ──────────────────────│                       │
    │                             │  (async)              │
    │                             │── BATCH UPDATE ──────>│
    │                             │<── OK ─────────────────│
    │                             │                       │
    │── GET data ────────────────>│                       │
    │<── latest data (cached) ────│                       │
```

### Write Flow

1. Application writes data to the cache.
2. Cache acknowledges immediately (low latency).
3. Cache queues the write for database persistence.
4. Database is updated asynchronously (batch or individual, with retry).
5. If database write fails, the cache retains the data for retry.

## Implementation

```python
import asyncio
from collections.abc import Awaitable, Callable

class WriteBehindCache:
    def __init__(self, redis_client, db_client, ttl=3600, flush_interval=5.0):
        self.redis = redis_client
        self.db = db_client
        self.ttl = ttl
        self.flush_interval = flush_interval
        self._queue: list[tuple[str, dict]] = []
        self._lock = asyncio.Lock()

    async def set(self, key: str, data: dict) -> None:
        """Acknowledge write immediately, queue for async persistence."""
        # Write to cache immediately
        self.redis.setex(key, self.ttl, serialize(data))

        # Queue for database persistence
        async with self._lock:
            self._queue.append((key, data))

    async def _flush(self) -> None:
        """Flush queued writes to the database."""
        while True:
            await asyncio.sleep(self.flush_interval)
            async with self._lock:
                batch = self._queue.copy()
                self._queue.clear()

            if not batch:
                continue

            try:
                # Batch write to database
                await self.db.batch_update(batch)
            except Exception as e:
                logger.error("Write-behind flush failed: %s", e)
                # Re-queue failed writes for retry
                async with self._lock:
                    self._queue.extend(batch)

    async def get(self, key: str) -> dict | None:
        cached = self.redis.get(key)
        if cached is not None:
            return deserialize(cached)
        return None

    async def start(self) -> None:
        """Start the background flush loop."""
        asyncio.create_task(self._flush())
```

## Durability Considerations

Write-behind trades durability for latency:

| Strategy | Risk | Mitigation |
|----------|------|------------|
| **In-memory queue** | Lost if cache restarts | Use persistent cache (Redis AOF/RDB) |
| **Single cache node** | Lost if node fails | Use replication, failover |
| **Async batch flush** | Partial batch loss | Write-ahead log for queued operations |
| **Database failure** | Unbounded queue growth | Circuit breaker, dead letter queue |

## When to Use

- **Write-heavy workloads** where write throughput is limited by database capacity.
- **Bursty write patterns** where the database cannot handle peak load.
- **Non-critical writes** where temporary data loss (seconds to minutes) is acceptable.
- **Analytics and metrics** where throughput is more important than individual write accuracy.

## When to Avoid

- **Financial transactions** or any operation requiring strong durability guarantees.
- **Compliance-sensitive data** that must be immediately persisted.
- **Real-time consistency requirements** where the database must reflect the latest state immediately.

## Consequences

### Benefits
- Low write latency: cache acknowledges immediately.
- High write throughput: batches database writes efficiently.
- Peak smoothing: absorbs write bursts without database overload.

### Trade-offs
- Data loss risk: writes acknowledged but not yet persisted can be lost on cache failure.
- Consistency window: database lags behind cache (eventual consistency).
- Complexity: requires retry logic, dead letter queues, and monitoring of the flush process.
- Recovery time: on cache failure, unflushed writes are lost or require replay.

## Related Patterns

- [Cache-Aside](cache-aside.md): Reads use lazy loading, writes go directly to the database.
- [Write-Through](write-through.md): Synchronous write to both cache and database.
- [Cache-Avalanche](cache-aside.md#cache-avalanche): TTL management to prevent cascading failures.
