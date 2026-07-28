# Agent Runtime Concepts

This directory defines how AI coding agents should operate when using this repository.
These are not code — they are conceptual documents that define the agent operating model.

## Contents

| Document | Purpose |
|----------|---------|
| [Context Management](context-management.md) | How agents select relevant standards and skills |
| [Memory Policy](memory-policy.md) | How to store and retrieve reusable engineering knowledge |
| [Tool Policy](tool-policy.md) | When to use which tool |
| [Verification Loop](verification-loop.md) | Self-verification cycle: Generate → Verify → Test → Review → Improve |

## Usage

Agents should load the applicable runtime document based on their task phase:

1. **Start**: Read context-management.md to understand how to load relevant skills
2. **During**: Follow tool-policy.md for tool selection and access
3. **Memory**: Use memory-policy.md for persisting learnings
4. **End**: Run verification-loop.md before concluding
