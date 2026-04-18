# stage4_modular_functions.py
# OOPTS Order System — Stage 4: Modular Functions
# Concepts: functions, parameters, return values, docstrings,
#           separation of concerns, list of dicts

orders = []

# ─────────────────────────────────────────────
# Validation
# ─────────────────────────────────────────────

def validate_quantity(quantity):
    """Returns True if quantity is a positive integer."""
    return isinstance(quantity, int) and quantity > 0

def validate_price(price):
    """Returns True if price is a positive number."""
    return isinstance(price, (int, float)) and price > 0

# ─────────────────────────────────────────────
# Core Functions
# ─────────────────────────────────────────────

def calculate_total(quantity, price):
    """Returns total cost."""
    return quantity * price

def add_order(order_id, item, quantity, price):
    """Creates and appends a new order dict. Validates inputs first."""
    if not validate_quantity(quantity):
        print(f"Error: Invalid quantity '{quantity}'.")
        return
    if not validate_price(price):
        print(f"Error: Invalid price '{price}'.")
        return

    total = calculate_total(quantity, price)
    order = {
        "id":       order_id,
        "item":     item,
        "quantity": quantity,
        "price":    price,
        "total":    total,
        "status":   "Pending"
    }
    orders.append(order)
    print(f"Order {order_id} added successfully. Total: ${total:.2f}")

def list_orders():
    """Prints all orders in a readable format."""
    if not orders:
        print("No orders found.")
        return
    print(f"\n{'ID':<6} {'Item':<15} {'Qty':<5} {'Price':>8} {'Total':>9} {'Status':<12}")
    print("-" * 60)
    for o in orders:
        print(f"{o['id']:<6} {o['item']:<15} {o['quantity']:<5} ${o['price']:>7.2f} ${o['total']:>8.2f} {o['status']:<12}")

def search_order(order_id):
    """Returns the order dict matching order_id, or None."""
    for o in orders:
        if o['id'] == order_id:
            return o
    return None

def update_status(order_id, new_status):
    """Updates the status field of a given order."""
    order = search_order(order_id)
    if order:
        order['status'] = new_status
        print(f"Order {order_id} updated to '{new_status}'.")
    else:
        print(f"Order {order_id} not found.")

def delete_order(order_id):
    """Removes an order from the list by ID."""
    order = search_order(order_id)
    if order:
        orders.remove(order)
        print(f"Order {order_id} deleted.")
    else:
        print(f"Order {order_id} not found.")

# ─────────────────────────────────────────────
# Example Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":
    add_order(101, "Laptop",   1,  1200.00)
    add_order(102, "Mouse",    2,    25.50)
    add_order(103, "Keyboard", 3,    45.00)
    add_order(104, "Monitor",  -1,  320.00)  # Invalid quantity demo
    add_order(105, "Webcam",   1,    0)       # Invalid price demo

    list_orders()

    print("\n--- Search ---")
    result = search_order(102)
    print(f"Found: {result}")

    print("\n--- Update Status ---")
    update_status(101, "Shipped")
    update_status(999, "Delivered")  # Not found

    print("\n--- Delete ---")
    delete_order(103)

    list_orders()
