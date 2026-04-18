# stage6_oop_order.py
# OOPTS Order System — Stage 6: Object-Oriented Programming
# Concepts: class, __init__, instance methods, self, encapsulation,
#           to_dict(), display(), JSON file persistence

import json
import os
import datetime

# ─────────────────────────────────────────────
# Base Record Class (encapsulation + timestamps)
# ─────────────────────────────────────────────

class Record:
    def __init__(self, record_id):
        self._record_id   = record_id
        self._created_at  = datetime.datetime.now()
        self._updated_at  = datetime.datetime.now()

    def _update_timestamp(self):
        """Refreshes the updated_at timestamp (call after any mutation)."""
        self._updated_at = datetime.datetime.now()

    def get_details(self):
        return (f"ID: {self._record_id} | "
                f"Created: {self._created_at.strftime('%Y-%m-%d %H:%M:%S')}")


# ─────────────────────────────────────────────
# Order Class
# ─────────────────────────────────────────────

class Order(Record):
    def __init__(self, order_id, customer, product, quantity, price):
        super().__init__(order_id)
        self.order_id = order_id
        self.customer = customer
        self.product  = product
        self.quantity = quantity
        self.price    = price
        self.status   = "Placed"

    # ── Core Methods ────────────────────────

    def calculate_total(self):
        """Returns the total cost of the order."""
        return self.quantity * self.price

    def update_status(self, new_status):
        """Updates the current status and refreshes the timestamp."""
        self.status = new_status
        self._update_timestamp()

    def to_dict(self):
        """Converts the Order object to a serialisable dictionary."""
        return {
            "order_id": self.order_id,
            "customer": self.customer,
            "product":  self.product,
            "quantity": self.quantity,
            "price":    self.price,
            "status":   self.status,
            "total":    self.calculate_total()
        }

    def display(self):
        """Prints order details in a readable receipt format."""
        print(f"--- Order ID: {self.order_id} ---")
        print(f"Customer : {self.customer}")
        print(f"Product  : {self.product}")
        print(f"Quantity : {self.quantity}")
        print(f"Price    : ${self.price:.2f}")
        print(f"Total    : ${self.calculate_total():.2f}")
        print(f"Status   : [{self.status}]")
        print("-" * 30)

    def __repr__(self):
        return f"Order(id={self.order_id}, customer='{self.customer}', total=${self.calculate_total():.2f})"


# ─────────────────────────────────────────────
# File Persistence (JSON)
# ─────────────────────────────────────────────

def save_orders(order_list, filename="orders.json"):
    """Saves a list of Order objects to a JSON file."""
    try:
        with open(filename, 'w') as f:
            json.dump([o.to_dict() for o in order_list], f, indent=4)
        print(f"[Saved] {len(order_list)} order(s) → '{filename}'")
    except IOError as e:
        print(f"[Error] Could not save: {e}")

def load_orders(filename="orders.json"):
    """Loads orders from a JSON file. Returns a list of Order objects."""
    if not os.path.exists(filename):
        print(f"[Info] '{filename}' not found. Starting fresh.")
        return []
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        orders = []
        for d in data:
            o = Order(d["order_id"], d["customer"], d["product"], d["quantity"], d["price"])
            o.status = d.get("status", "Placed")
            orders.append(o)
        print(f"[Loaded] {len(orders)} order(s) from '{filename}'")
        return orders
    except (json.JSONDecodeError, IOError, KeyError) as e:
        print(f"[Error] Could not load: {e}")
        return []


# ─────────────────────────────────────────────
# Example Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=== Stage 6 — OOP Demo ===\n")

    # Create orders
    o1 = Order(101, "Ravi",  "Laptop",   1, 1200.00)
    o2 = Order(102, "Priya", "Mouse",    2, 25.50)
    o3 = Order(103, "Arjun", "Keyboard", 1, 75.00)

    # Display
    for order in [o1, o2, o3]:
        order.display()

    # Update status
    o1.update_status("Shipped")
    print(f"\nAfter update: {o1}")
    print(f"Record details: {o1.get_details()}\n")

    # Save to JSON
    save_orders([o1, o2, o3])

    # Load back from JSON
    loaded = load_orders()
    print("\nLoaded back from file:")
    for order in loaded:
        print(f"  {order}")
