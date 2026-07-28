# Tool Policy

## Principle

Tools are the agent's interface to the system. Each tool should be used with intent.
The wrong tool for the job wastes tokens, adds latency, and can cause unintended side effects.

## Tool Categories

### Read Tools (safe to use freely)

| Tool | When to Use |
|------|-------------|
| Read | Read any file. Use before modifying. |
| Glob/Find | Locate files by pattern. Use when path is uncertain. |
| Grep | Search for symbols, patterns, or text across files. |
| Bash (read-only) | `ls`, `cat` for quick file inspection. |
| WebFetch | Fetch documentation or reference content. |

### Write Tools (require intent)

| Tool | When to Use |
|------|-------------|
| Write | Create new files. Always read the directory structure first. |
| Edit | Modify existing files. Always read the target first. |
| Bash (git) | Stage, commit, push. Use with user approval. |

### Execution Tools (require caution)

| Tool | When to Use |
|------|-------------|
| Bash (build/test) | Run tests, build, lint. Use after implementation. |
| Bash (install) | Add dependencies. Confirm with user before modifying lock files. |

## Access Control Guidelines

| Action | Approval Required |
|--------|-------------------|
| Read any file | No |
| Create new file | No (but verify path first) |
| Modify existing file | No (but read first) |
| Install dependencies | Yes (user confirm) |
| Delete files or directories | Yes (user confirm) |
| Run tests | No |
| Deploy or release | Yes (user confirm) |
| Modify CI/CD config | Yes (user confirm) |

## Anti-Patterns

- **Read before edit**: never edit a file you haven't read in the same turn
- **Grep before glob**: use grep for content search, glob for path search
- **No speculative execution**: don't run commands just to see what happens
- **Prefer batch operations**: combine related changes into single commits
