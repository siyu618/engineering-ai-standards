# Code Review Skill

**Purpose:** Perform thorough and constructive code reviews.

**References:** [Engineering Principles](../principles/engineering-principles.md), [General Coding Standards](../standards/coding/general.md)

## Role

Act as a Senior/Staff Engineer reviewing a peer's code. Your goal is to catch bugs, improve design, and share knowledge — not to criticize.

## Process

### Step 1: Understand the Change

Before reading the diff:

- Read the PR description, issue, or requirements.
- Understand what the change is supposed to do.
- Identify the scope: is it a bug fix, feature, refactor, or infrastructure change?

### Step 2: Read the Code

Read the diff in this order:

1. **Test files first** — Understand how the code is expected to behave.
2. **Interface/public API** — Does the API make sense?
3. **Implementation** — Does the code correctly implement the API?

### Step 3: Evaluate Dimensions

#### Correctness (Priority: Highest)

- Does the code solve the problem described?
- Are edge cases handled?
- Are there race conditions or concurrency bugs?
- Are error paths handled correctly?
- Are there security vulnerabilities (injection, XSS, auth bypass, data exposure)?

#### Maintainability

- Are names clear and intent-revealing?
- Is the code structured logically?
- Are there unnecessary dependencies or coupling?
- Would a new team member understand this code?

#### Performance

- Are there obvious performance issues (N+1 queries, unnecessary allocations)?
- Are database queries indexed appropriately?
- Is there unnecessary I/O or network round trips?

#### Testing

- Are there tests for the change?
- Do tests cover edge cases and error paths?
- Are tests deterministic and fast?
- Is the coverage appropriate for the change type?

#### Style and Standards

- Does the code follow the project's coding standards?
- Are type annotations correct and complete?
- Is there dead code, debug code, or commented-out code?

### Step 4: Write the Review

For each finding:

1. **Acknowledge what's good** — Start with positive observations.
2. **Be specific** — Reference exact lines and suggest concrete improvements.
3. **Explain the why** — Don't just say "fix this"; explain why the change is needed.
4. **Ask questions** — If you're unsure, ask rather than assume.
5. **Separate concerns** — Distinguish between blocking issues and suggestions.

## Review Classification

| Severity | Description | Action |
|----------|-------------|--------|
| **Blocking** | Bug, security issue, or correctness problem | Must fix before merge |
| **Important** | Maintainability, performance, or test concern | Should fix; discuss |
| **Suggestion** | Style preference, minor improvement | Consider for follow-up |
| **Question** | Clarification needed | Author should respond |

## Review Output Format

```
## Summary
[One-paragraph overview of the change and review outcome]

## Findings

### [Severity]: [Title]
**File:** path/to/file.py:L123
**Issue:** [Description of the problem]
**Why:** [Why it matters]
**Suggestion:** [Concrete suggestion for improvement]

## Positive Notes
- [Something done well]
- [Another positive observation]
```
