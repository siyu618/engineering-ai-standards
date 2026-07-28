# ADR-007: Agent Runtime Model

**Status:** Accepted
**Date:** 2026-07-28

## Context

Skills define *what* to do (process instructions). Workflows define *when* to do it
(orchestration). But neither defines *how the agent should operate* at a meta level —
how to manage context, what to remember, when to use which tool, and how to verify its
own output.

This gap became apparent when agents produced incomplete work because they:
- Loaded irrelevant standards into their context window
- Didn't persist project knowledge between sessions
- Used the wrong tool for the task
- Skipped verification on "simple" changes

## Decision

Create a `runtime/` directory with four concept documents, separate from skills and workflows.
These documents define the agent operating model — the "runtime" that governs how the agent
executes skills and workflows.

### Runtime Documents

| Document | Purpose | Why Separate |
|----------|---------|-------------|
| context-management.md | How to select relevant content | Applies to ALL tasks, not skill-specific |
| memory-policy.md | What to remember and forget | Cross-session concern |
| tool-policy.md | When to use which tool | Agent-level, not task-level |
| verification-loop.md | Self-verification cycle | Meta-process, not domain process |

### Why Not Part of Skills

- Runtime concepts are agent-agnostic (they apply regardless of which AI tool is used)
- Skills are domain-specific; runtime is domain-agnostic
- Mixing runtime into skills would duplicate the same instructions across every skill
- Runtime evolves with agent capabilities, not with domain knowledge

### Why Not Part of Workflows

- Workflows compose skills into processes; runtime defines how the agent executes any step
- Verification loop applies to every step of every workflow
- Context management is a prerequisite for even loading a workflow

## Consequences

### Positive
- Clear separation: skills (domain), workflows (process), runtime (operating model)
- Runtime documents are loaded once per session, not once per skill
- New agents can learn operating model from runtime/ without reading every skill

### Negative
- Four more files for agents to potentially load (mitigated by priority loading)
- Runtime documents could grow stale if agent capabilities change rapidly

## Related

- [ADR-001: Three-Layer Architecture](001-three-layer-architecture.md)
- [ADR-003: Evaluation Framework](003-evaluation-framework.md)
