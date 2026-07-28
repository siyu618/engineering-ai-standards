# Example: Python Refactoring

This example walks through using the [Python Development Skill](../SKILL.md) to refactor a legacy function.

## Before

```python
def process_orders(data):
    results = []
    for item in data:
        if item['status'] == 'pending':
            total = 0
            for product in item['products']:
                price = get_price(product['id'])
                if product['quantity'] > 0:
                    total += price * product['quantity']
            if total > 0:
                item['total'] = total
                item['status'] = 'processed'
                save(item)
                results.append({'id': item['id'], 'total': total, 'status': 'ok'})
            else:
                results.append({'id': item['id'], 'error': 'zero total'})
        elif item['status'] == 'cancelled':
            results.append({'id': item['id'], 'status': 'skipped'})
    return results
```

## After

```python
from dataclasses import dataclass
from typing import Optional
import structlog

logger = structlog.get_logger()

@dataclass
class OrderItem:
    product_id: str
    quantity: int

@dataclass
class Order:
    id: str
    status: str
    products: list[OrderItem]

@dataclass
class ProcessResult:
    id: str
    total: Optional[float] = None
    status: str = "ok"
    error: Optional[str] = None

def calculate_order_total(products: list[OrderItem]) -> float:
    total = 0.0
    for item in products:
        try:
            price = get_price(item.product_id)
            total += price * item.quantity
        except ApiTimeoutError:
            logger.error("Price fetch timeout", product_id=item.product_id)
            raise
    return total

def process_single_order(order: Order) -> ProcessResult:
    if order.status == "cancelled":
        return ProcessResult(id=order.id, status="skipped")

    if order.status != "pending":
        logger.warning("Unknown order status", status=order.status, order_id=order.id)
        return ProcessResult(id=order.id, status="unknown")

    total = calculate_order_total(order.products)
    if total <= 0:
        return ProcessResult(id=order.id, error="zero total")

    save(order.id, total)
    logger.info("Order processed", order_id=order.id, total=total)
    return ProcessResult(id=order.id, total=total)
```

## Key Improvements

- Type hints on all functions and data structures
- Specific exception handling instead of bare `except:`
- Structured logging with correlation IDs
- Single-responsibility functions
- Testable: pure logic separated from I/O
