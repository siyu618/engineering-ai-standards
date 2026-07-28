# Context Management

## Principle

Context window is finite. Every token in the prompt has an opportunity cost. Agents must
selectively load relevant content from this repository based on the current task.

## Strategy

### 1. Task Classification

Before loading any content, classify the task:

| Task Type | Load Order |
|-----------|------------|
| System design | principles → standards/architecture → patterns → skills/design |
| Implementation | standards/coding → skills/python-development → patterns |
| Code review | standards/coding → skills/code-review |
| Testing | standards/testing → skills/testing |
| Bug fix | skills/testing → skills/python-development → skills/code-review |
| Incident | skills/incident-response → patterns → standards |

### 2. Priority Loading

Load content in this priority order within the context window:

1. **Task context** — user's instructions, current state, relevant files
2. **Identity** — AGENTS.md or adapter instructions
3. **Principles** — engineering-principles.md (core philosophy, ~2KB)
4. **Relevant standards** — specific standards files based on task type
5. **Active skill** — the SKILL.md for the current task
6. **Registry lookup** — skills.yaml for available skills

### 3. Sliding Window

When the context window is full:

- Drop successfully completed tool results
- Drop `principles/` after task orientation (they've been read)
- Summarize prior turns into compressed context
- Keep user instructions and active skill at all times

### 4. Adapter Selection

- If running in Claude Code: use `adapters/claude/CLAUDE.md`
- If running in Cursor: use `adapters/cursor/.cursorrules`
- If running in Copilot: use `adapters/github-copilot/copilot-instructions.md`
- If unknown: use `AGENTS.md`

## Anti-Patterns

- Loading all standards at once — only load what's relevant
- Keeping irrelevant patterns in context after design phase
- Loading all skills when only one is needed
