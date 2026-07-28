# AGENTS.md — AI Agent Instructions

This repository defines engineering standards and skills for AI coding agents. It is designed for use by Claude Code, Cursor, GitHub Copilot, and future AI coding agents.

## Architecture

```
Principles → Standards → Patterns → Skills → Adapters → Evaluations
```

Each layer builds on the one above it. Start at the top and follow the chain.

## Agent Requirements

1. **Follow the principles** in `principles/` as your engineering philosophy. They define why we build software the way we do.
2. **Obey the mandatory rules** in `standards/`. These are not suggestions.
3. **Use patterns** from `patterns/` as reusable solutions. Reference them when designing systems or writing code.
4. **Load the applicable skill** from `skills/` for the task at hand. Each skill module contains a SKILL.md with process instructions, a CHANGELOG.md, and evaluation cases.
5. **Read your tool-specific config** from `adapters/` — each AI tool has its own adapter file.
6. **Validate changes through evaluations** in `evaluations/` before concluding. Run `python evaluations/runner/run.py` to validate evaluation cases.

## Communication

- Be concise. Prefer code over explanation where code is self-documenting.
- Explain trade-offs when there is no single right answer.
- Ask clarifying questions rather than guessing.
- Admit mistakes openly and fix them promptly.
