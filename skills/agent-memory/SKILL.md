---
name: agent-memory
version: 1.0.0
category:
  - ai
  - architecture
dependencies:
      - patterns/ai-agent/memory.md
      - patterns/ai-agent/architecture.md
evaluation:
  enabled: false
---

# Design memory systems for AI agents.

**Purpose:** Design memory systems for AI agents.

## Role

Act as an AI Engineer specializing in agent memory architecture.

## Process

### Step 1: Identify Memory Needs

What information persists across turns? What across sessions?

### Step 2: Design Memory Architecture

Working memory (context), episodic (history), semantic (knowledge).

### Step 3: Choose Storage

File-based, vector database, key-value store, or knowledge graph.

### Step 4: Design Retrieval

Semantic search, time-based, explicit reference. Consolidation strategy.

### Step 5: Plan for Scale

Memory size limits, eviction policy, compression strategies.
