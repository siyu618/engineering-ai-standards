# Example: Code Review Output

This example demonstrates the [Code Review Skill](../SKILL.md) output format for a real code review.

## Summary

Reviewed a Flask checkout endpoint with security-sensitive operations. Found 2 blocking issues (insecure deserialization, SQL injection), 1 important issue (silent error handling), and 2 suggestions.

## Findings

### 🔴 Blocking: Insecure Deserialization via Pickle

**File:** checkout.py:L6
**Issue:** Using `pickle.load()` on user-controlled filenames. This allows arbitrary code execution.
**Why:** Pickle deserialization can execute arbitrary Python code during unpickling.
**Suggestion:** Use a safe serialization format like JSON.

```python
# Instead of:
with open(f"user_data_{user_id}.pkl", "rb") as f:
    return pickle.load(f)

# Use:
with open(f"user_data_{user_id}.json", "r") as f:
    return json.load(f)
```

### 🔴 Blocking: SQL Injection

**File:** checkout.py:L49
**Issue:** String interpolation in SQL query with user-supplied discount code.
**Suggestion:** Use parameterized queries.

```python
cursor.execute("SELECT * FROM discounts WHERE code = ?", (discount_code,))
```

### 🟡 Important: Silent Exception Handling

**File:** checkout.py:L43
**Issue:** Bare `except: pass` silently swallows all errors including `KeyError` and `TypeError`.
**Suggestion:** Catch specific exceptions and log context.

## Positive Notes

- Clean route structure with clear separation of concerns
- Good use of JSON response formatting
- Timeout set on external HTTP call
