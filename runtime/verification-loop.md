# Verification Loop

## Principle

Before concluding any task, the agent should run a self-verification loop.
This catches errors, omissions, and misunderstandings before they reach the user.

## Loop

```
   ┌───────────────────────────────────────────┐
   │              TASK COMPLETE?                │
   └───────────────────────────────────────────┘
                       │
                       ▼
   ┌───────────────────────────────────────────┐
   │        1. GENERATE                         │
   │   Was the output produced?                 │
   │   Are all required artifacts created?      │
   └───────────────────────────────────────────┘
                       │
                       ▼
   ┌───────────────────────────────────────────┐
   │        2. VERIFY                           │
   │   Does the output solve the problem?       │
   │   Are edge cases handled?                  │
   │   Is the solution safe?                    │
   └───────────────────────────────────────────┘
                       │
                       ▼
   ┌───────────────────────────────────────────┐
   │        3. TEST                             │
   │   Does the code compile/run?              │
   │   Do the tests pass?                       │
   │   Are new tests written for the change?    │
   └───────────────────────────────────────────┘
                       │
                       ▼
   ┌───────────────────────────────────────────┐
   │        4. REVIEW                           │
   │   Is the code maintainable?               │
   │   Are there security concerns?             │
   │   Does it follow repository standards?     │
   └───────────────────────────────────────────┘
                       │
                       ▼
   ┌───────────────────────────────────────────┐
   │        5. IMPROVE                          │
   │   What could be better?                    │
   │   Are there simpler alternatives?          │
   │   Is there unused code or complexity?      │
   └───────────────────────────────────────────┘
                       │
                       ▼
                  ┌─────────┐
                  │  DONE   │
                  └─────────┘
```

## Verification Checklist

### For Code Changes

- [ ] Code produces correct output for all inputs
- [ ] Edge cases handled (empty, null, boundary, error)
- [ ] No security vulnerabilities (injection, XSS, auth)
- [ ] Error handling is explicit and informative
- [ ] Logging is appropriate (no sensitive data)
- [ ] Tests exist and pass
- [ ] No dead code or commented-out code

### For Design Changes

- [ ] Design addresses all requirements
- [ ] Trade-offs documented
- [ ] Failure modes identified
- [ ] Scalability considered
- [ ] Consistency model appropriate

### For Documentation Changes

- [ ] Technically accurate
- [ ] Clear and unambiguous
- [ ] Follows repository structure
- [ ] Cross-references valid
- [ ] No duplication of existing content

## When to Loop

If any check in the verification loop fails, the agent should:

1. Identify the specific gap
2. Return to the GENERATE or IMPROVE phase
3. Re-verify after the fix
4. Continue until all checks pass

## Anti-Patterns

- **Skipping verification** for "simple" changes — most bugs come from simple changes
- **Only testing the happy path** — edge cases are where failures live
- **Accepting the first working solution** — always check for improvement opportunities
- **Ignoring test results** — if tests fail, the change is not complete
