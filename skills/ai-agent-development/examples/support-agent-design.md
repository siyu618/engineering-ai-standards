# Example: Customer Support Agent Design

This example walks through using the [AI Agent Development Skill](../SKILL.md) to design a support agent.

## Step 1: Define Purpose

- **Problem**: Reduce tier-1 support ticket resolution time
- **Users**: Customers submitting support tickets via web chat
- **Success criteria**: 80% automated resolution rate, CSAT above 4.5/5
- **Scope boundary**: Do NOT handle refunds over $100 or account security breaches

## Step 2: Agent Architecture

Chosen variant: **ReAct Agent** — support tickets require multi-step reasoning (read KB, check order, decide action).

```
[User Input] → [Classifier: intent detection]
                    │
    ┌───────────────┼───────────────┐
    ▼               ▼               ▼
[Password Reset] [Order Status] [Refund Request]
    │               │               │
    ▼               ▼               ▼
[Tool: reset]   [Tool: get_order] [Tool: process_refund]
```

## Step 3: Tools

| Tool | Description | Safety Control |
|------|-------------|----------------|
| search_kb(query) | Search knowledge base articles | Read-only |
| get_order(order_id) | Fetch order details | Read-only |
| process_refund(order_id, amount) | Process refund | Requires confirmation if > $100 |
| reset_password(user_id) | Send password reset email | Requires user verification |
| escalate_to_human(ticket_id) | Transfer to human agent | Logs reason for escalation |

## Step 4: System Prompt

```
You are a customer support agent for an e-commerce platform.
You have access to the knowledge base and order system.
Always verify identity before performing account changes.
If unsure about a request, escalate to a human agent.
```

## Step 5: Evaluation Cases

| Case | Scenario | Expected |
|------|----------|----------|
| Happy path | Password reset request | Successfully reset, confirmation message |
| Edge case | Refund over $100 | Correctly escalate to human |
| Safety | User asks to change another user's password | Refuse, escalate |
