# Engineering Principles

## Guiding Philosophy

These principles define *why* and *how* we build software. They inform every standard, pattern, and practice in this repository.

## 1. Correctness First

Software must be correct before it is fast, elegant, or extensible.

- A system that produces wrong answers has no value regardless of its other qualities.
- Prefer proven solutions over novel ones when correctness is critical.
- Formal reasoning, property-based testing, and exhaustive validation are investments in correctness.
- When in doubt, make the system refuse unclear inputs rather than guess.

## 2. Simplicity

Simplicity is the ultimate sophistication in engineering.

- Solve the problem at hand, not hypothetical future problems.
- A simpler system is easier to understand, verify, and change.
- Every abstraction, framework, or indirection must earn its complexity budget.
- Prefer flat over nested, explicit over implicit, and obvious over clever.

## 3. Reliability

Systems must work correctly and continuously under expected and unexpected conditions.

- Design for failure: assume networks partition, disks fill, services crash, and inputs are malicious.
- Graceful degradation is better than catastrophic failure.
- Observability (metrics, logs, traces) is not optional — without it you cannot know if the system is reliable.
- Automation must replace manual operations; toil is a design smell.

## 4. Scalability

Design systems that can grow without fundamental redesign.

- Identify and document scalability ceilings early.
- Separate read and write paths when their scaling characteristics differ.
- Prefer horizontal scaling unless operational complexity makes vertical scaling more economical.
- Load-test before going to production; benchmark before optimizing.

## 5. Maintainability

Code is read far more often than it is written.

- Code should be self-documenting: clear names, obvious structure, minimal comments explaining *why* not *what*.
- Every module, package, and service should have a single, well-defined responsibility.
- Reduce coupling: a change in one component should not cascade to unrelated components.
- Dependency injection, interfaces, and protocol boundaries are tools for maintainability.

## 6. Security by Design

Security is not a feature; it is a property of the entire system.

- Threat model early and often. Understand your attacker's capabilities and incentives.
- Principle of least privilege: every component should have only the permissions it needs.
- Defense in depth: no single security control is trusted in isolation.
- Treat secrets as vulnerabilities: rotate them, audit access, never log them.

## 7. Iterative Delivery

Deliver value continuously rather than attempting perfect delivery at the end.

- Favor small, reversible changes over large, irreversible ones.
- Each iteration should produce a working (if incomplete) system.
- Measure outcomes, not outputs — a delivered feature that isn't used is waste.

## 8. Explicit over Implicit

In distributed systems and concurrent code, implicit behavior is dangerous.

- Make state changes, error handling, and side effects explicit in the code.
- Configuration should be external and versioned, not hardcoded.
- Timeouts, retries, and error budgets should be tuned explicitly and documented.
- Prefer explicit interfaces over convention-based or reflection-based wiring.

## Priorities When They Conflict

When principles conflict, use this hierarchy:

1. **Correctness** — being wrong is worse than being slow or ugly
2. **Security** — a compromised system cannot be correct, simple, or reliable
3. **Reliability** — an unavailable system delivers no value
4. **Maintainability** — unmaintainable code becomes incorrect over time
5. **Simplicity** — complexity should justify itself against the above
6. **Scalability** — many systems never need to scale; premature scalability is complexity
7. **Iterative Delivery** — perfect architecture shipped too late is irrelevant
