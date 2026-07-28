# Memory Policy

## Principle

Agents should persist reusable engineering knowledge across sessions. Not everything
needs to be remembered — only patterns, decisions, and conventions that would be useful
to recall in future interactions.

## Memory Architecture

```
┌──────────────────────────────────────────┐
│            Agent Memory System            │
│                                          │
│  Working Memory (current context)        │
│    ↕ eviction / summarization            │
│  Episodic Memory (past turns)            │
│    ↕ consolidation                       │
│  Semantic Memory (facts, knowledge)      │
└──────────────────────────────────────────┘
```

## What to Remember

### Store in Semantic Memory

- **Architecture decisions**: why a particular pattern was chosen
- **Project conventions**: naming, structure, code style
- **Recurring issues**: bugs that appear repeatedly, with their fixes
- **Domain knowledge**: business rules, constraints, terminology

### Store in Episodic Memory

- Full conversation logs (if storage permits)
- Session summaries with key outcomes
- Decision points with alternatives considered

### Do NOT Store

- Transient debugging output
- Successful tool results from standard operations
- Large code blocks that exist in version control

## Memory File Format

When persisting to files, use structured markdown with frontmatter:

```markdown
---
name: descriptive-name
description: one-line summary
metadata:
  type: project | pattern | decision
---

The fact or knowledge to persist.
- Key point 1
- Key point 2

**Related:** link to other memory entries
```

## Retrieval

- On session start, load the most relevant semantic memories based on task context
- On encountering a problem, search episodic memory for similar past issues
- Consolidation: periodically summarize episodic patterns into semantic knowledge

## Consolidation Triggers

| Trigger | Action |
|---------|--------|
| Same issue appears twice | Store as semantic pattern |
| New convention established | Store as project fact |
| Architecture decision made | Store as decision record |
| Session ends | Generate episodic summary |
