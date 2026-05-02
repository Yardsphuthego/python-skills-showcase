from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


COMPLETED_STATUSES = {"paid", "processing", "on_the_way", "arrived", "delivered"}


def _round(amount: Decimal) -> Decimal:
    return amount.quantize(Decimal("0.01"))


def _mask_phone(value: str) -> str:
    if not value:
        return ""
    if len(value) <= 4:
        return value
    return f"{'*' * (len(value) - 4)}{value[-4:]}"


@dataclass(slots=True)
class Product:
    product_id: str
    name: str
    sku: str = ""
    active: bool = True
    stock: int = 0


@dataclass(slots=True)
class Order:
    order_id: str
    order_number: str
    created_at: datetime
    status: str
    total_amount: Decimal
    customer_phone: str = ""


@dataclass(slots=True)
class OrderItem:
    order_id: str
    product_id: str
    quantity: int
    unit_price: Decimal


def generate_financial_report(
    *,
    year: int,
    month: int,
    vendor_name: str,
    vendor_city: str,
    vendor_phone: str,
    orders: list[Order],
    order_items: list[OrderItem],
    products: list[Product],
) -> dict:
    month_orders = [
        order
        for order in orders
        if order.created_at.year == year and order.created_at.month == month
    ]
    order_ids = {order.order_id for order in month_orders}
    filtered_items = [item for item in order_items if item.order_id in order_ids]
    product_map = {product.product_id: product for product in products}

    order_units: dict[str, int] = defaultdict(int)
    product_stats: dict[str, dict] = {}
    units_sold = 0
    for item in filtered_items:
        order_units[item.order_id] += item.quantity
        matching_order = next(order for order in month_orders if order.order_id == item.order_id)
        if matching_order.status not in COMPLETED_STATUSES:
            continue

        units_sold += item.quantity
        product = product_map.get(item.product_id)
        row = product_stats.setdefault(
            item.product_id,
            {
                "product_id": item.product_id,
                "product_name": product.name if product else "Unknown product",
                "sku": product.sku if product else "",
                "units_sold": 0,
                "revenue": Decimal("0.00"),
            },
        )
        row["units_sold"] += item.quantity
        row["revenue"] += item.unit_price * item.quantity

    gross_sales = Decimal("0.00")
    refunds_total = Decimal("0.00")
    cancelled_total = Decimal("0.00")
    completed_orders = 0
    cancelled_orders = 0
    refunded_orders = 0
    unique_customers = {
        order.customer_phone
        for order in month_orders
        if order.status in COMPLETED_STATUSES and order.customer_phone
    }

    daily: dict[str, dict] = {}
    transactions = []
    for order in month_orders:
        amount = order.total_amount
        day_key = order.created_at.strftime("%Y-%m-%d")
        row = daily.setdefault(
            day_key,
            {
                "date": day_key,
                "orders": 0,
                "completed_orders": 0,
                "cancelled_orders": 0,
                "refunded_orders": 0,
                "gross_sales": Decimal("0.00"),
                "refunds_total": Decimal("0.00"),
                "cancelled_total": Decimal("0.00"),
                "net_sales": Decimal("0.00"),
                "units_sold": 0,
            },
        )
        row["orders"] += 1

        if order.status in COMPLETED_STATUSES:
            completed_orders += 1
            gross_sales += amount
            row["completed_orders"] += 1
            row["gross_sales"] += amount
            row["net_sales"] += amount
            row["units_sold"] += order_units[order.order_id]
        elif order.status == "refunded":
            refunded_orders += 1
            refunds_total += amount
            row["refunded_orders"] += 1
            row["refunds_total"] += amount
            row["net_sales"] -= amount
        elif order.status == "cancelled":
            cancelled_orders += 1
            cancelled_total += amount
            row["cancelled_orders"] += 1
            row["cancelled_total"] += amount

        transactions.append(
            {
                "order_number": order.order_number,
                "date": order.created_at.isoformat(),
                "status": order.status,
                "amount": str(_round(amount)),
                "item_count": order_units[order.order_id],
                "customer_phone_masked": _mask_phone(order.customer_phone),
            }
        )

    average_ticket = _round(gross_sales / completed_orders) if completed_orders else Decimal("0.00")
    daily_rows = [
        {
            "date": row["date"],
            "orders": row["orders"],
            "completed_orders": row["completed_orders"],
            "cancelled_orders": row["cancelled_orders"],
            "refunded_orders": row["refunded_orders"],
            "gross_sales": str(_round(row["gross_sales"])),
            "refunds_total": str(_round(row["refunds_total"])),
            "cancelled_total": str(_round(row["cancelled_total"])),
            "net_sales": str(_round(row["net_sales"])),
            "units_sold": row["units_sold"],
        }
        for _, row in sorted(daily.items())
    ]

    top_products = sorted(
        (
            {
                **stats,
                "revenue": str(_round(stats["revenue"])),
            }
            for stats in product_stats.values()
        ),
        key=lambda item: (item["units_sold"], Decimal(item["revenue"])),
        reverse=True,
    )[:10]

    active_products = sum(1 for product in products if product.active)
    total_stock_units = sum(product.stock for product in products if product.active)
    low_stock_products = sum(1 for product in products if product.active and product.stock <= 5)
    days_with_sales = sum(1 for row in daily_rows if Decimal(row["gross_sales"]) > Decimal("0.00"))

    return {
        "source": "portfolio_demo",
        "vendor": {
            "business_name": vendor_name,
            "city": vendor_city,
            "phone_number": vendor_phone,
        },
        "period": {"year": year, "month": month},
        "summary": {
            "total_orders": len(month_orders),
            "completed_orders": completed_orders,
            "cancelled_orders": cancelled_orders,
            "refunded_orders": refunded_orders,
            "gross_sales": str(_round(gross_sales)),
            "refunds_total": str(_round(refunds_total)),
            "cancelled_total": str(_round(cancelled_total)),
            "net_sales": str(_round(gross_sales - refunds_total)),
            "average_ticket": str(average_ticket),
            "unique_customers": len(unique_customers),
            "units_sold": units_sold,
            "days_with_sales": days_with_sales,
            "active_products": active_products,
            "total_products": len(products),
            "low_stock_products": low_stock_products,
            "inventory_units_on_hand": total_stock_units,
        },
        "daily_operations": daily_rows,
        "top_products": top_products,
        "transactions": transactions,
    }
