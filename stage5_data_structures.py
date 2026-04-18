# stage5_data_structures.py
# OOPTS Order System — Stage 5: Dictionaries, Sets & Tuples
# Concepts: dict, set comprehension, tuple, list comprehension,
#           immutability, category filtering, invoice summaries

# ─────────────────────────────────────────────
# 1. Dictionary-based order records
# ─────────────────────────────────────────────
orders = [
    {"order_id": 101, "customer": "Rahul",   "product": "Mobile Case",  "category": "Electronics", "quantity": 2,  "price": 299,  "status": "Placed"},
    {"order_id": 102, "customer": "Priya",   "product": "Laptop Stand", "category": "Electronics", "quantity": 1,  "price": 899,  "status": "Shipped"},
    {"order_id": 103, "customer": "Anita",   "product": "Notebook",     "category": "Stationery",  "quantity": 5,  "price": 49,   "status": "Delivered"},
    {"order_id": 104, "customer": "Rahul",   "product": "Pen Set",      "category": "Stationery",  "quantity": 3,  "price": 120,  "status": "Placed"},
    {"order_id": 105, "customer": "Kiran",   "product": "Office Chair", "category": "Furniture",   "quantity": 1,  "price": 4500, "status": "Processing"},
    {"order_id": 106, "customer": "Priya",   "product": "USB Hub",      "category": "Electronics", "quantity": 2,  "price": 350,  "status": "Shipped"},
]

# ─────────────────────────────────────────────
# 2. Sets — unique product categories
# ─────────────────────────────────────────────
unique_categories = {order["category"] for order in orders}

# ─────────────────────────────────────────────
# 3. Tuples — immutable invoice summaries
#    Format: (Order ID, Customer, Total Amount)
# ─────────────────────────────────────────────
invoice_summaries = tuple(
    (order["order_id"], order["customer"], order["quantity"] * order["price"])
    for order in orders
)

# ─────────────────────────────────────────────
# 4. Category-based filtering function
# ─────────────────────────────────────────────
def filter_by_category(category_name):
    """Returns a list of orders matching the given category (case-insensitive)."""
    return [order for order in orders if order["category"].lower() == category_name.lower()]

# ─────────────────────────────────────────────
# 5. Customer order summary using a dict
# ─────────────────────────────────────────────
def customer_summary():
    """Groups total spend per customer using a dictionary."""
    summary = {}
    for order in orders:
        name  = order["customer"]
        total = order["quantity"] * order["price"]
        summary[name] = summary.get(name, 0) + total
    return summary

# ─────────────────────────────────────────────
# Output
# ─────────────────────────────────────────────
if __name__ == "__main__":
    print("=== Unique Categories (set) ===")
    print(unique_categories)

    print("\n=== Invoice Summaries (tuple of tuples) ===")
    for inv in invoice_summaries:
        print(f"  Order #{inv[0]} | {inv[1]:<10} | ${inv[2]:,.2f}")

    print("\n=== Filter: Electronics ===")
    for order in filter_by_category("Electronics"):
        print(f"  {order['product']} — Qty: {order['quantity']} — Status: {order['status']}")

    print("\n=== Filter: Stationery ===")
    for order in filter_by_category("Stationery"):
        print(f"  {order['product']} — Qty: {order['quantity']} — Status: {order['status']}")

    print("\n=== Customer Spend Summary (dict) ===")
    for customer, total in customer_summary().items():
        print(f"  {customer:<10}: ${total:,.2f}")
