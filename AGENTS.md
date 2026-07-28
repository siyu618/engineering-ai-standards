# AGENTS.md — AI Agent Instructions

This repository defines engineering standards and skills for AI coding agents. It is designed for use by Claude Code, Cursor, GitHub Copilot, and future AI coding agents.

## Architecture

```
Principles → Standards → Patterns → Skills → Workflows → Evaluations → Adapters → Governance
```

Each layer builds on the one above it. Start at the top and follow the chain.

## Agent Requirements

1. **Follow the principles** in `principles/` as your engineering philosophy. They define why we build software the way we do.
2. **Obey the mandatory rules** in `standards/`. These are not suggestions.
3. **Use patterns** from `patterns/` as reusable solutions. Reference them when designing systems or writing code.
4. **Load the applicable skill** from `skills/` for the task at hand. Each skill module contains SKILL.md, CHANGELOG.md, examples/, and evaluation cases.
5. **Check the registry** in `registry/skills.yaml` for an overview of all available skills, their versions, and owners.
6. **Follow workflows** in `workflows/` for multi-step engineering processes that compose multiple skills.
7. **Read your tool-specific config** from `adapters/` — each AI tool has its own adapter file.
8. **Validate changes through evaluations** in `evaluations/` before concluding. Run `python evaluations/runner/run.py --registry` to validate both evaluation cases and registry consistency.

## Communication

- Be concise. Prefer code over explanation where code is self-documenting.
- Explain trade-offs when there is no single right answer.
- Ask clarifying questions rather than guessing.
- Admit mistakes openly and fix them promptly.
