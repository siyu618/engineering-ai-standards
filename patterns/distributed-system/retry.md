# Retry

## Context

In distributed systems, transient failures are inevitable: network timeouts, database connection drops, service restarts, and resource contention. A well-designed retry mechanism can turn transient failures into successful operations without human intervention.

## Problem

How to recover from transient failures without overwhelming the system, causing cascading failures, or violating idempotency guarantees?

## Solution

### Exponential Backoff with Jitter

The standard retry strategy: increase the delay between retries exponentially and add random jitter to prevent thundering herd.

```
delay = min(base_delay * 2^attempt, max_delay)
actual_delay = random_between(0, delay)  // full jitter
```

### Retry Configuration

```
max_retries:       3
base_delay:        100ms
max_delay:         10s
backoff_multiplier: 2
jitter_type:       full     // none | equal | full | decorrelated
```

### When to Retry

- Retry only on **transient failures** (timeout, connection reset, 503 Service Unavailable).
- Do NOT retry on **client errors** (400, 401, 403, 404, 422) — the client must fix the request.
- Do NOT retry on **rate limiting** (429) without respecting the Retry-After header.
- Do NOT retry on **server errors that indicate permanent state** (e.g., "payment declined").

### Circuit Breaker

Combine retry with a circuit breaker to prevent retrying into a failing system:

```
States: CLOSED → OPEN → HALF_OPEN → CLOSED

CLOSED:   Normal operation, requests pass through.
OPEN:     Failures exceed threshold, requests fail fast without attempting.
HALF_OPEN: After timeout, allow probe request to test recovery.
```

### Retry Budget

Define a retry budget to limit the total retry load on the system:

- Track the ratio of retries to total requests per endpoint.
- If the ratio exceeds the budget (e.g., 20%), stop retrying and fail fast.
- Reset the budget window periodically (e.g., every 60 seconds).

## Implementation

### Idiomatic Retry (Python)

```python
import random
import time
from functools import wraps

def retry(max_retries=3, base_delay=0.1, max_delay=10.0):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except TransientError as e:
                    last_exception = e
                    if attempt == max_retries:
                        raise
                    delay = min(base_delay * (2 ** attempt), max_delay)
                    actual_delay = random.uniform(0, delay)  # full jitter
                    time.sleep(actual_delay)
            raise last_exception
        return wrapper
    return decorator
```

## Consequences

### Benefits
- Resilience: systems recover automatically from transient failures.
- Availability: reduces false negatives and improves perceived uptime.
- Self-healing: operators are not required for short-lived failure scenarios.

### Trade-offs
- Amplification: retries can amplify load on an already stressed system.
- Distributed coordination: without circuit breakers, retries can cascade.
- Latency: retries increase tail latency (p99 may become p99 * retries).

## Related Patterns

- [Idempotency](idempotency.md): Required for safe retry of non-read operations.
- [Consistency](consistency.md): Retry mechanisms must respect consistency boundaries.
- **Circuit Breaker**: Prevents retries when the system is known to be failing.
- **Bulkhead**: Isolates retry pools to prevent cascading failures.
