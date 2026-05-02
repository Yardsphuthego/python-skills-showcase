from datetime import datetime
from decimal import Decimal

from showcase.reporting import Order, OrderItem, Product, generate_financial_report


def test_generate_financial_report_summarizes_orders_products_and_daily_sales():
    orders = [
        Order(
            order_id="1",
            order_number="ORD-001",
            created_at=datetime(2026, 5, 1, 10, 30),
            status="paid",
            total_amount=Decimal("120.00"),
            customer_phone="+26771234567",
        ),
        Order(
            order_id="2",
            order_number="ORD-002",
            created_at=datetime(2026, 5, 1, 15, 45),
            status="refunded",
            total_amount=Decimal("20.00"),
            customer_phone="+26772345678",
        ),
    ]
    order_items = [
        OrderItem(order_id="1", product_id="p1", quantity=2, unit_price=Decimal("30.00")),
        OrderItem(order_id="1", product_id="p2", quantity=1, unit_price=Decimal("60.00")),
    ]
    products = [
        Product(product_id="p1", name="Notebook", sku="NB-01", stock=20),
        Product(product_id="p2", name="Backpack", sku="BP-99", stock=4),
    ]

    report = generate_financial_report(
        year=2026,
        month=5,
        vendor_name="Skills Demo Shop",
        vendor_city="Gaborone",
        vendor_phone="+26770000000",
        orders=orders,
        order_items=order_items,
        products=products,
    )

    assert report["summary"]["gross_sales"] == "120.00"
    assert report["summary"]["refunds_total"] == "20.00"
    assert report["summary"]["units_sold"] == 3
    assert report["summary"]["low_stock_products"] == 1
    assert report["top_products"][0]["product_name"] == "Notebook"
