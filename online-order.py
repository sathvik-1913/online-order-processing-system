"""
Simple Online Order Processing System
"""

import json
import uuid
from datetime import datetime

# ── In-memory "database" ──────────────────────────────────────────────────────

PRODUCTS = {
    "P001": {"name": "Laptop",     "price": 799.99, "stock": 10},
    "P002": {"name": "Mouse",      "price":  25.99, "stock": 50},
    "P003": {"name": "Keyboard",   "price":  49.99, "stock": 30},
    "P004": {"name": "Monitor",    "price": 299.99, "stock": 15},
    "P005": {"name": "Headphones", "price":  89.99, "stock": 20},
}

ORDERS = {}          # order_id → order dict
CUSTOMERS = {}       # email → customer dict

# ── Helpers ───────────────────────────────────────────────────────────────────

def separator(char="─", width=55):
    print(char * width)

def header(title):
    separator("═")
    print(f"  {title}")
    separator("═")

def show_products():
    header("📦  Product Catalogue")
    print(f"{'ID':<8}{'Name':<15}{'Price':>10}{'Stock':>8}")
    separator()
    for pid, p in PRODUCTS.items():
        stock_flag = " ⚠ Low" if p["stock"] < 5 else ""
        print(f"{pid:<8}{p['name']:<15}${p['price']:>9.2f}{p['stock']:>8}{stock_flag}")
    separator()

# ── Core operations ───────────────────────────────────────────────────────────

def register_customer():
    header("👤  Register Customer")
    name  = input("  Full name  : ").strip()
    email = input("  Email      : ").strip().lower()
    phone = input("  Phone      : ").strip()

    if email in CUSTOMERS:
        print("  ✓ Customer already exists.")
        return CUSTOMERS[email]

    customer = {"name": name, "email": email, "phone": phone,
                "joined": datetime.now().strftime("%Y-%m-%d %H:%M")}
    CUSTOMERS[email] = customer
    print(f"\n  ✓ Customer '{name}' registered successfully!")
    return customer


def place_order():
    header("🛒  Place New Order")
    email = input("  Customer email : ").strip().lower()

    if email not in CUSTOMERS:
        print("  ✗ Customer not found. Please register first.")
        return

    cart = {}
    show_products()

    while True:
        pid = input("  Enter Product ID (or 'done' to finish): ").strip().upper()
        if pid == "DONE":
            break
        if pid not in PRODUCTS:
            print("  ✗ Invalid product ID.")
            continue

        try:
            qty = int(input(f"  Quantity for {PRODUCTS[pid]['name']}: "))
            if qty <= 0:
                raise ValueError
        except ValueError:
            print("  ✗ Enter a positive integer.")
            continue

        if PRODUCTS[pid]["stock"] < qty:
            print(f"  ✗ Only {PRODUCTS[pid]['stock']} in stock.")
            continue

        cart[pid] = cart.get(pid, 0) + qty
        print(f"  ✓ Added {qty}× {PRODUCTS[pid]['name']}")

    if not cart:
        print("  ✗ No items in cart. Order cancelled.")
        return

    # Calculate totals
    subtotal = sum(PRODUCTS[p]["price"] * q for p, q in cart.items())
    tax      = round(subtotal * 0.10, 2)
    total    = round(subtotal + tax, 2)

    # Show order summary
    separator()
    print("  ORDER SUMMARY")
    separator()
    for pid, qty in cart.items():
        line = PRODUCTS[pid]["price"] * qty
        print(f"  {PRODUCTS[pid]['name']:<18} {qty:>2} × ${PRODUCTS[pid]['price']:.2f} = ${line:.2f}")
    separator()
    print(f"  {'Subtotal':<28} ${subtotal:.2f}")
    print(f"  {'Tax (10%)':<28} ${tax:.2f}")
    print(f"  {'TOTAL':<28} ${total:.2f}")
    separator()

    confirm = input("  Confirm order? (yes/no): ").strip().lower()
    if confirm != "yes":
        print("  Order cancelled.")
        return

    # Deduct stock & save order
    for pid, qty in cart.items():
        PRODUCTS[pid]["stock"] -= qty

    order_id = "ORD-" + str(uuid.uuid4())[:8].upper()
    ORDERS[order_id] = {
        "order_id":  order_id,
        "customer":  email,
        "items":     cart,
        "subtotal":  subtotal,
        "tax":       tax,
        "total":     total,
        "status":    "Processing",
        "placed_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
    }

    print(f"\n  ✓ Order placed! Your Order ID: {order_id}")
    return order_id


def view_order():
    header("🔍  View Order")
    order_id = input("  Enter Order ID: ").strip().upper()

    if order_id not in ORDERS:
        print("  ✗ Order not found.")
        return

    o = ORDERS[order_id]
    c = CUSTOMERS.get(o["customer"], {})
    separator()
    print(f"  Order ID   : {o['order_id']}")
    print(f"  Customer   : {c.get('name','N/A')}  ({o['customer']})")
    print(f"  Date       : {o['placed_at']}")
    print(f"  Status     : {o['status']}")
    separator()
    for pid, qty in o["items"].items():
        print(f"  {PRODUCTS[pid]['name']:<18} × {qty}")
    separator()
    print(f"  Total      : ${o['total']:.2f}  (incl. 10% tax)")
    separator()


def update_order_status():
    header("🔄  Update Order Status")
    order_id = input("  Enter Order ID: ").strip().upper()

    if order_id not in ORDERS:
        print("  ✗ Order not found.")
        return

    statuses = ["Processing", "Confirmed", "Shipped", "Delivered", "Cancelled"]
    print("  Available statuses:")
    for i, s in enumerate(statuses, 1):
        print(f"    {i}. {s}")

    try:
        choice = int(input("  Select status number: "))
        new_status = statuses[choice - 1]
    except (ValueError, IndexError):
        print("  ✗ Invalid choice.")
        return

    # Restore stock if cancelling
    if new_status == "Cancelled" and ORDERS[order_id]["status"] != "Cancelled":
        for pid, qty in ORDERS[order_id]["items"].items():
            PRODUCTS[pid]["stock"] += qty

    ORDERS[order_id]["status"] = new_status
    print(f"  ✓ Order {order_id} updated to '{new_status}'.")


def list_all_orders():
    header("📋  All Orders")
    if not ORDERS:
        print("  No orders yet.")
        return

    print(f"{'Order ID':<14}{'Customer':<22}{'Total':>9}  {'Status':<12}  {'Date'}")
    separator()
    for o in ORDERS.values():
        c = CUSTOMERS.get(o["customer"], {})
        print(f"{o['order_id']:<14}{c.get('name','N/A'):<22}"
              f"${o['total']:>8.2f}  {o['status']:<12}  {o['placed_at']}")
    separator()


def view_customers():
    header("👥  Registered Customers")
    if not CUSTOMERS:
        print("  No customers yet.")
        return

    for c in CUSTOMERS.values():
        orders = [o for o in ORDERS.values() if o["customer"] == c["email"]]
        spent  = sum(o["total"] for o in orders)
        print(f"  {c['name']:<20}  {c['email']:<25}  "
              f"Orders: {len(orders):>2}   Spent: ${spent:.2f}")
    separator()


def generate_report():
    header("📊  Sales Report")
    if not ORDERS:
        print("  No orders to report.")
        return

    total_revenue = sum(o["total"] for o in ORDERS.values()
                        if o["status"] != "Cancelled")
    total_orders  = len(ORDERS)
    cancelled     = sum(1 for o in ORDERS.values() if o["status"] == "Cancelled")
    delivered     = sum(1 for o in ORDERS.values() if o["status"] == "Delivered")

    # Top products
    sales = {}
    for o in ORDERS.values():
        if o["status"] != "Cancelled":
            for pid, qty in o["items"].items():
                sales[pid] = sales.get(pid, 0) + qty

    print(f"  Total Orders     : {total_orders}")
    print(f"  Delivered        : {delivered}")
    print(f"  Cancelled        : {cancelled}")
    print(f"  Total Revenue    : ${total_revenue:.2f}")
    separator()
    if sales:
        print("  Top Selling Products:")
        for pid, qty in sorted(sales.items(), key=lambda x: -x[1]):
            print(f"    {PRODUCTS[pid]['name']:<18} — {qty} units sold")
    separator()

# ── Main menu ─────────────────────────────────────────────────────────────────

def main():
    menu = {
        "1": ("Register Customer",   register_customer),
        "2": ("Place Order",         place_order),
        "3": ("View Order",          view_order),
        "4": ("Update Order Status", update_order_status),
        "5": ("List All Orders",     list_all_orders),
        "6": ("View Customers",      view_customers),
        "7": ("View Products",       show_products),
        "8": ("Sales Report",        generate_report),
        "0": ("Exit",                None),
    }

    print("\n" + "═" * 55)
    print("   🛍️   ONLINE ORDER PROCESSING SYSTEM")
    print("═" * 55)

    while True:
        print()
        for key, (label, _) in menu.items():
            print(f"   {key}.  {label}")
        print()
        choice = input("  Select option: ").strip()

        if choice == "0":
            print("\n  👋  Goodbye!\n")
            break
        elif choice in menu:
            print()
            menu[choice][1]()
        else:
            print("  ✗ Invalid option. Try again.")

if __name__ == "__main__":
    main()