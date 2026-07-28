---
name: ai-agent-development
version: 1.0.0
category:
  - ai
  - agent
dependencies:
  - principles/engineering-principles.md
  - patterns/ai-agent/architecture.md
  - patterns/ai-agent/memory.md
  - patterns/ai-agent/tool-use.md
  - patterns/ai-agent/evaluation.md
evaluation:
  enabled: true
  cases:
    - ai-agent-eval-design
---

# AI Agent Development Skill

**Purpose:** Design and implement reliable AI agent systems.

**References:** [Engineering Principles](../../principles/engineering-principles.md), [AI Agent Architecture](../../patterns/ai-agent/architecture.md), [AI Agent Memory](../../patterns/ai-agent/memory.md), [AI Agent Tool Use](../../patterns/ai-agent/tool-use.md), [AI Agent Evaluation](../../patterns/ai-agent/evaluation.md)

## Role

Act as an AI Engineer specializing in building production-grade LLM-powered agent systems.

## Process

### Step 1: Define the Agent's Purpose

- What specific problem does this agent solve?
- Who are the users? What are their expectations?
- What is the success criteria for the agent?
- What is the scope boundary — what should the agent NOT do?

### Step 2: Design the Agent Architecture

Choose the agent variant based on requirements:

| If the task requires... | Use... |
|-------------------------|--------|
| Complex multi-step reasoning | ReAct Agent |
| Simple tool execution | Tool-Use Agent |
| Multiple expertise domains | Orchestrated Agent |

Define:
- **System prompt**: instructions, persona, constraints, output format.
- **Tools**: what tools are needed, their schemas, and access controls.
- **Memory**: working memory size, episodic storage, semantic memory structure.
- **Error handling**: what happens on tool failure, LLM error, timeout.

### Step 3: Implement Tools

For each tool, follow the [Tool Use patterns](../../patterns/ai-agent/tool-use.md):

- One tool = one responsibility.
- Structured inputs and outputs.
- Clear error messages for recoverable and non-recoverable failures.
- Instrumentation: log every call, timing, and result.

### Step 4: Design the Prompt

System prompt structure:

```
You are [ROLE].

## Instructions
[Core behavior instructions]

## Constraints
[What you must NOT do]

## Process
[Step-by-step process to follow]

## Tools
[Tool descriptions — automatically populated from tool registry]

## Output Format
[Expected output format]
```

### Step 5: Implement Evaluation

Before deploying, create evaluation cases:

- **Happy path**: the agent handles a typical request correctly.
- **Edge cases**: the agent handles unusual inputs gracefully.
- **Failure recovery**: the agent recovers from tool failures.
- **Safety**: the agent refuses harmful requests.
- **Efficiency**: the agent completes tasks within expected turn count.

### Step 6: Implement Observability

- Log every LLM call: prompt, response, tokens, latency.
- Log every tool call: input, output, duration, error.
- Trace requests across agent turns.
- Track aggregate metrics: success rate, average turns, average latency.

## Patterns for Reliable Agents

### Guardrails

- Validate all user inputs before passing to the LLM.
- Validate all tool outputs before returning to the LLM.
- Set maximum turn limits to prevent infinite loops.
- Set maximum token limits per turn and per session.

### Human-in-the-Loop

- Require human confirmation for destructive or irreversible actions.
- Allow human override at any point in the agent's execution.
- Provide clear visibility into the agent's reasoning and planned actions.

### Graceful Degradation

- When the LLM is unavailable, return a clear error with retry timing.
- When a tool fails, the agent should try alternatives or ask for input.
- When context is full, summarize and continue rather than crashing.

## Anti-Patterns

- **Overly permissive prompts**: giving the agent too much freedom leads to unpredictable behavior.
- **Hidden tool side effects**: tools that silently modify state cause confusion.
- **Ignoring token limits**: not monitoring token usage leads to mid-task failures.
- **No timeout on tools**: a hung tool blocks the entire agent.
- **Testing without evaluation**: deploying without evaluation is flying blind.
- **Prompting without versioning**: prompts change silently and regressions go undetected.
