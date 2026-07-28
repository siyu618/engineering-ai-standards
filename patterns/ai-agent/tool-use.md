# AI Agent Tool Use

## Context

LLMs can invoke external tools (functions, APIs, databases) to extend their capabilities beyond text generation. However, naive tool calling leads to issues: hallucinated arguments, cascading errors, unintended side effects, and lack of observability.

## Problem

How to design a tool-use system that is reliable, safe, and observable?

## Solution

### Tool Definition

Every tool must have a clear definition following this schema:

| Field | Description | Required |
|-------|-------------|----------|
| `name` | Unique identifier | Yes |
| `description` | When and how to use this tool | Yes |
| `parameters` | JSON Schema of input parameters | Yes |
| `returns` | Description of return value | Yes |
| `side_effects` | What the tool changes in the world | Recommended |
| `errors` | What errors can occur | Recommended |
| `rate_limit` | Max calls per time window | Optional |

### Tool Design Principles

1. **Each tool does one thing.** If a tool has multiple modes, split it.
2. **Fail loudly.** Tools should raise descriptive errors, not silently return empty results.
3. **Validate inputs.** Every tool must validate its inputs against its schema.
4. **Set timeouts.** Every tool execution must have a timeout. Long-running tools should report progress.
5. **Log everything.** Every tool call, its inputs, outputs, duration, and errors must be logged.

### Tool Categories

```
┌─────────────────────────────────────────────┐
│               Tool Registry                  │
│                                             │
│  Read Tools      Write Tools    Meta Tools  │
│  ┌─────────┐    ┌─────────┐    ┌─────────┐  │
│  │ Search  │    │ Create  │    │ Ask     │  │
│  │ Read    │    │ Update  │    │ Confirm │  │
│  │ List    │    │ Delete  │    │ Plan    │  │
│  │ Query   │    │ Execute │    │ Reflect │  │
│  └─────────┘    └─────────┘    └─────────┘  │
└─────────────────────────────────────────────┘
```

#### Read Tools (Harmless, Fast)
- Search knowledge bases, query databases, read files, fetch URLs.
- No side effects — safe to retry and call speculatively.
- Should complete within seconds.

#### Write Tools (State-Changing, Require Care)
- Create or modify resources, send messages, trigger workflows.
- Must be idempotent where possible.
- Should prompt for confirmation before destructive actions.
- Require explicit user approval for irreversible operations.

#### Meta Tools (Agent Self-Management)
- Request clarification from the user.
- Confirm before executing a destructive action.
- Ask for permission when uncertain.
- Decompose complex tasks into sub-steps.

### Tool Calling Flow

```
LLM decides to call tool
    │
    ▼
Validate arguments against schema
    │
    ├── Invalid → Return error to LLM (with validation details)
    │
    ▼ Valid
Execute tool
    │
    ├── Success → Return result to LLM
    │
    ├── Transient error → Retry with backoff (if applicable)
    │
    └── Permanent error → Return error to LLM (with context)
```

### Error Handling Pattern

```python
class ToolError(Exception):
    def __init__(self, message: str, recoverable: bool = False, context: dict = None):
        self.message = message
        self.recoverable = recoverable
        self.context = context or {}
        super().__init__(message)

def safe_tool_call(tool_func, **kwargs):
    """Execute a tool with structured error handling."""
    try:
        logger.info("Calling tool: %s with args: %s", tool_func.__name__, kwargs)
        start = time.monotonic()
        result = tool_func(**kwargs)
        duration = time.monotonic() - start
        logger.info("Tool %s completed in %.2fs", tool_func.__name__, duration)
        return {"success": True, "result": result, "duration": duration}
    except ToolError as e:
        logger.warning("Tool %s error: %s", tool_func.__name__, e.message)
        return {
            "success": False,
            "error": e.message,
            "recoverable": e.recoverable,
            "context": e.context,
        }
    except Exception as e:
        logger.error("Tool %s unexpected error: %s", tool_func.__name__, str(e))
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "recoverable": False,
        }
```

## Consequences

### Benefits
- Extensibility: agents can use any tool without modifying the agent.
- Safety: structured error handling prevents cascading failures.
- Observability: every tool call is logged and traceable.

### Trade-offs
- Latency: each tool call adds at least one round trip.
- Schema maintenance: tool schemas must be kept in sync with implementations.
- Tool selection: too many tools can overwhelm the LLM's tool selection accuracy.

## Related Patterns

- [Architecture](architecture.md): The agent architecture that hosts the tool system.
- [Memory](memory.md): Tools that read/write agent memory.
- [Evaluation](evaluation.md): Evaluating tool selection accuracy and execution reliability.
