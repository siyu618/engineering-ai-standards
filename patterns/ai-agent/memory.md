# AI Agent Memory

## Context

LLMs have a fixed context window and no built-in persistence between conversations. For an AI agent to maintain coherent long-running interactions, learn from past experience, and reference prior knowledge, an explicit memory system is required.

## Problem

How to provide an AI agent with persistent, retrievable, and manageable memory across turns and sessions?

## Solution

### Memory Architecture

```
┌─────────────────────────────────────────┐
│            Memory System                 │
│                                         │
│  ┌─────────────┐  ┌──────────────────┐  │
│  │ Working     │  │ Episodic Memory  │  │
│  │ Memory      │  │ (Past Turns)     │  │
│  │ (Context)   │  │                  │  │
│  └─────────────┘  └──────────────────┘  │
│  ┌────────────────────────────────────┐ │
│  │        Semantic Memory              │ │
│  │  (Facts, Knowledge, Patterns)      │ │
│  └────────────────────────────────────┘ │
└─────────────────────────────────────────┘
```

### 1. Working Memory

The current context window. Contains the system prompt, conversation history, and immediate task state.

**Characteristics:**
- Volatile: lost when the session ends.
- Fixed capacity: bounded by the model's context window.
- Fast access: no retrieval latency.

**Management strategies:**
- **Sliding window**: keep the most recent N turns.
- **Summary compression**: summarize older turns when the window fills.
- **Priority eviction**: drop low-priority messages (e.g., successful tool results) before high-priority ones (e.g., user instructions).

### 2. Episodic Memory

A record of past interactions, stored and retrievable across sessions.

**Characteristics:**
- Persistent: survives session boundaries.
- Retrievable: can be searched by content, time, or metadata.
- Append-only: episodes are never modified, only added.

**Storage strategies:**
- **Conversation logs**: full transcripts stored in a database.
- **Episode summaries**: synthesized summaries of each session.
- **Vector embeddings**: semantic search over past episodes.

**Retrieval triggers:**
- Explicit user request ("remember when we discussed X").
- Semantic similarity to current query.
- Periodic consolidation (agent reviewing its own history).

### 3. Semantic Memory

Structured knowledge extracted from interactions and external sources.

**Characteristics:**
- Fact-oriented: stores individual facts, preferences, and patterns.
- Structured: key-value pairs, knowledge graph entries, or document chunks.
- Mutable: facts can be updated or corrected.

**Common implementations:**
- **Key-value store**: simple preferences and facts.
- **Vector database**: semantic search over knowledge chunks.
- **Knowledge graph**: relationships between entities and concepts.
- **File-based (e.g., memory files)**: structured markdown files for long-term recall.

### Memory File Pattern

Structured files with frontmatter metadata are an effective pattern for semantic memory.

```markdown
---
name: project-config
description: Project configuration and preferences
metadata:
  type: project
---

The project uses FastAPI with SQLAlchemy async.
- Database: PostgreSQL 16
- Cache: Redis 7
- Queue: Celery with Redis broker

**Key decisions:**
- API versioning via URL prefix (/v1/)
- Authentication via JWT with 15-minute access tokens
```

## Memory Retrieval Flow

```
User Input
    │
    ▼
Working Memory ── Is information in current context?
    │                        │
    │ Yes                    │ No
    ▼                        ▼
Continue Processing    Semantic Memory ── Search facts / knowledge
                              │                        │
                              │ Found                  │ Not Found
                              ▼                        ▼
                       Load into Working         Episodic Memory
                       Memory                    Search past turns
                                                    │
                                                    ▼
                                              Semantic consolidation
                                              (if pattern detected)
```

## Memory Consolidation

Periodically, the agent should consolidate episodic memories into semantic knowledge:

- **Batch processing**: at fixed intervals (every N sessions), analyze episode summaries for recurring patterns.
- **Event-triggered**: when a pattern repeats (e.g., same issue reported twice), consolidate into semantic memory.
- **User-directed**: on explicit request ("save this as a fact").

## Consequences

### Benefits
- Continuity: the agent can maintain context across long sessions and multiple sessions.
- Learning: recurring patterns are captured as semantic knowledge.
- Efficiency: the working memory is reserved for immediate context.

### Trade-offs
- Retrieval latency: accessing persistent memory is slower than working memory.
- Storage costs: storing full episode histories requires durable storage.
- Consolidation complexity: extracting knowledge from episodes requires careful prompt design.

## Related Patterns

- [Architecture](architecture.md): The agent architecture that hosts this memory system.
- [Tool Use](tool-use.md): Tools that interact with the memory system.
- [Evaluation](evaluation.md): Evaluating memory retrieval accuracy and relevance.
