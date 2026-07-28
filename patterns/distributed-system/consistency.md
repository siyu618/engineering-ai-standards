# Consistency Models

## Context

Distributed systems involve multiple nodes maintaining copies or partitions of data. The CAP theorem states that a distributed data store can only provide two of three guarantees: Consistency, Availability, and Partition Tolerance. Understanding consistency models is essential to choosing the right trade-offs for each part of the system.

## Problem

How to manage data consistency across distributed nodes while meeting availability, latency, and partition tolerance requirements?

## Solutions

### Strong Consistency

All reads see the most recent write. This is the familiar single-node behavior.

**Mechanisms:**
- Single-leader replication with synchronous replication
- Consensus protocols (Raft, Paxos)
- Distributed transactions (2PC, 3PC)

**Suitable when:**
- Financial transactions and balance updates
- Inventory management (overselling prevention)
- Authentication and authorization state

**Cost:**
- Higher latency (coordination overhead)
- Reduced availability during partitions
- Lower throughput (serialization)

**Example:**
```sql
-- Strong consistency via single-leader with sync replication
BEGIN TRANSACTION ISOLATION LEVEL SERIALIZABLE;
UPDATE accounts SET balance = balance - 100 WHERE id = 1;
UPDATE accounts SET balance = balance + 100 WHERE id = 2;
COMMIT;
```

### Eventual Consistency

If no new updates are made to a data item, eventually all accesses will return the last updated value.

**Mechanisms:**
- Leaderless replication (Dynamo-style)
- Multi-leader replication
- Asynchronous replication with conflict resolution (CRDTs, last-write-wins)

**Suitable when:**
- User profile updates (slight staleness is acceptable)
- Social feed content
- Analytics and reporting data
- Content delivery networks

**Cost:**
- Stale reads possible
- Conflict resolution complexity
- Application-level reconciliation may be required

**Example:**
```python
# Eventual consistency via asynchronous replication
def update_user_profile(user_id, data):
    primary_db.update(user_id, data)           # immediate
    message_queue.publish("profile_updated", {  # async replication
        "user_id": user_id,
        "data": data,
        "version": timestamp()
    })
```

### Read-After-Write Consistency

After a write, the same client (or session) will always see the written value, but other clients may see stale data.

**Mechanisms:**
- Session stickiness (read-your-writes cookie)
- Version vector tracking per client
- Read-repair with timestamp comparison

**Suitable when:**
- User-facing applications where the user expects to see their own changes
- E-commerce order placement (user sees their order immediately)

**Cost:**
- Session affinity may complicate load balancing
- Additional metadata per write operation

**Example:**
```python
# Read-after-write via sticky sessions
response.set_cookie("data_version", latest_version)
# On read, check cookie and route to node with current data
```

### Monotonic Reads

After a read, subsequent reads never return a value older than the previous read.

**Mechanisms:**
- Consistent hashing with stable node assignment
- Version progression tracking
- Time-based routing

**Suitable when:**
- Dashboard displays showing time-series data
- Multi-step workflows where later steps depend on earlier reads

## Choosing a Consistency Model

| Data Type | Recommended Model | Rationale |
|-----------|-------------------|-----------|
| Financial transactions | Strong | Money must be accurate |
| User profiles | Eventual | Staleness is acceptable |
| Shopping cart | Read-after-write | User expects to see their additions |
| Product catalog | Eventual | CDN-delivered, local caches |
| Inventory count | Strong | Overselling costs money |
| Activity feed | Eventual | Ordering is approximate |
| Session tokens | Strong | Security-sensitive |
| Analytics | Eventual | Throughput over accuracy |

## Consistency and Idempotency

Idempotency keys require at least **read-after-write consistency** on the idempotency store. If a duplicate request reads a stale state where the key doesn't exist, the operation will be incorrectly re-executed.

## Related Patterns

- [Idempotency](idempotency.md): Requires consistent key lookup to prevent duplicate execution.
- [Retry](retry.md): Retry behavior must respect the chosen consistency model.
- **CQRS**: Separates read and write models to allow different consistency guarantees for each.
- **Saga**: Manages long-running transactions with eventual consistency.
