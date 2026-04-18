# stage9_csv_export.py
# CSV Report Generation for the OOPTS Order System

import csv
import os
from datetime import datetime

# ─────────────────────────────────────────────
# 1. Sample Order Data (dict-based, reuses Stage 5 structure)
# ─────────────────────────────────────────────

orders = [
    {"id": 101, "customer": "Ravi Kumar",    "product": "Laptop",      "category": "Electronics", "quantity": 1,  "price": 1200.00, "status": "Shipped"},
    {"id": 102, "customer": "Priya Sharma",  "product": "Mouse",       "category": "Electronics", "quantity": 3,  "price": 25.50,   "status": "Placed"},
    {"id": 103, "customer": "Arjun Singh",   "product": "Desk Chair",  "category": "Furniture",   "quantity": 2,  "price": 450.00,  "status": "Processing"},
    {"id": 104, "customer": "Sneha Reddy",   "product": "Notebook",    "category": "Stationery",  "quantity": 10, "price": 5.99,    "status": "Delivered"},
    {"id": 105, "customer": "Kiran Patel",   "product": "Monitor",     "category": "Electronics", "quantity": 1,  "price": 320.00,  "status": "Shipped"},
    {"id": 106, "customer": "Ravi Kumar",    "product": "Keyboard",    "category": "Electronics", "quantity": 2,  "price": 75.00,   "status": "Placed"},
]

# Compute total for each order
for order in orders:
    order["total"] = order["quantity"] * order["price"]


# ─────────────────────────────────────────────
# 2. Export Orders to CSV
# ─────────────────────────────────────────────

FIELDNAMES = ["id", "customer", "product", "category", "quantity", "price", "total", "status"]

def export_orders_to_csv(order_list, filename="orders_report.csv"):
    """
    Writes all orders to a CSV file using csv.DictWriter.
    Creates or overwrites the file.
    """
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()           # Write column headers
            writer.writerows(order_list)   # Write all order rows
        print(f"[SUCCESS] Exported {len(order_list)} orders to '{filename}'.")
    except IOError as e:
        print(f"[ERROR] Could not write file: {e}")


# ─────────────────────────────────────────────
# 3. Read Orders Back from CSV
# ─────────────────────────────────────────────

def load_orders_from_csv(filename="orders_report.csv"):
    """
    Reads orders from a CSV file using csv.DictReader.
    Returns a list of dicts with correct data types.
    """
    if not os.path.exists(filename):
        print(f"[ERROR] File '{filename}' not found.")
        return []

    loaded = []
    try:
        with open(filename, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # CSV reads everything as strings — convert numeric fields back
                row["id"]       = int(row["id"])
                row["quantity"] = int(row["quantity"])
                row["price"]    = float(row["price"])
                row["total"]    = float(row["total"])
                loaded.append(row)
        print(f"[SUCCESS] Loaded {len(loaded)} orders from '{filename}'.")
    except (IOError, ValueError) as e:
        print(f"[ERROR] Could not read file: {e}")

    return loaded


# ─────────────────────────────────────────────
# 4. Export a Filtered Summary Report
# ─────────────────────────────────────────────

def export_summary_by_status(order_list, status_filter, filename=None):
    """
    Exports a filtered subset of orders (by status) to a separate CSV.
    Auto-generates filename if not provided.
    """
    filtered = [o for o in order_list if o["status"].lower() == status_filter.lower()]

    if not filtered:
        print(f"[INFO] No orders found with status '{status_filter}'. No file created.")
        return

    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"orders_{status_filter.lower()}_{timestamp}.csv"

    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(filtered)
        print(f"[SUCCESS] '{status_filter}' report → '{filename}' ({len(filtered)} orders).")
    except IOError as e:
        print(f"[ERROR] {e}")


# ─────────────────────────────────────────────
# 5. Display CSV Contents as a Table
# ─────────────────────────────────────────────

def display_orders_table(order_list, title="Order Report"):
    """Prints orders in a readable table format."""
    if not order_list:
        print("[INFO] No orders to display.\n")
        return

    print(f"\n{'─'*70}")
    print(f"  {title}")
    print(f"{'─'*70}")
    print(f"{'ID':<6} {'Customer':<16} {'Product':<14} {'Cat':<12} {'Qty':<5} {'Price':>8} {'Total':>9} {'Status':<12}")
    print(f"{'─'*70}")
    for o in order_list:
        print(f"{o['id']:<6} {o['customer']:<16} {o['product']:<14} {o['category']:<12} "
              f"{o['quantity']:<5} ${float(o['price']):>7.2f} ${float(o['total']):>8.2f} {o['status']:<12}")
    print(f"{'─'*70}")
    grand_total = sum(float(o["total"]) for o in order_list)
    print(f"{'TOTAL':>60}  ${grand_total:.2f}")
    print(f"{'─'*70}\n")


# ─────────────────────────────────────────────
# 6. Demo / Example Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  STAGE 9 — CSV Report Export Demo")
    print("=" * 50 + "\n")

    # Step 1: Show original data
    display_orders_table(orders, title="Original Orders (in memory)")

    # Step 2: Export all orders to CSV
    export_orders_to_csv(orders, "orders_report.csv")

    # Step 3: Export filtered reports
    print()
    export_summary_by_status(orders, "Shipped",    "orders_shipped.csv")
    export_summary_by_status(orders, "Placed",     "orders_placed.csv")
    export_summary_by_status(orders, "Cancelled")  # No match — shows info message

    # Step 4: Read back the main CSV
    print()
    loaded = load_orders_from_csv("orders_report.csv")
    display_orders_table(loaded, title="Re-loaded from orders_report.csv")

    # Step 5: List files created
    print("─── Files created ───")
    for fname in ["orders_report.csv", "orders_shipped.csv", "orders_placed.csv"]:
        if os.path.exists(fname):
            size = os.path.getsize(fname)
            print(f"  {fname}  ({size} bytes)")
