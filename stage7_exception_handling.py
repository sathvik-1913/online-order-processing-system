# stage7_exception_handling.py
# Custom exception classes for the OOPTS Order System

# ─────────────────────────────────────────────
# 1. Custom Exception Classes
# ─────────────────────────────────────────────

class OOPTSError(Exception):
    """Base exception for all OOPTS Order System errors."""
    pass

class InvalidQuantityError(OOPTSError):
    """Raised when quantity is not a positive integer."""
    def __init__(self, value):
        self.value = value
        super().__init__(f"Invalid quantity: '{value}'. Quantity must be a positive integer.")

class InvalidPriceError(OOPTSError):
    """Raised when price is not a positive number."""
    def __init__(self, value):
        self.value = value
        super().__init__(f"Invalid price: '{value}'. Price must be a positive number.")

class OrderNotFoundError(OOPTSError):
    """Raised when an order ID does not exist."""
    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"Order with ID '{order_id}' was not found.")

class DuplicateOrderError(OOPTSError):
    """Raised when an order ID already exists."""
    def __init__(self, order_id):
        self.order_id = order_id
        super().__init__(f"Order ID '{order_id}' already exists. Use a unique ID.")


# ─────────────────────────────────────────────
# 2. Validation Functions (raise custom errors)
# ─────────────────────────────────────────────

def validate_quantity(quantity):
    """Validates that quantity is a positive integer. Raises InvalidQuantityError if not."""
    if not isinstance(quantity, int) or quantity <= 0:
        raise InvalidQuantityError(quantity)
    return True

def validate_price(price):
    """Validates that price is a positive number. Raises InvalidPriceError if not."""
    if not isinstance(price, (int, float)) or price <= 0:
        raise InvalidPriceError(price)
    return True


# ─────────────────────────────────────────────
# 3. Order Management with Exception Handling
# ─────────────────────────────────────────────

orders = {}

def add_order(order_id, customer, product, quantity, price):
    """
    Adds a new order with full validation.
    Raises DuplicateOrderError, InvalidQuantityError, or InvalidPriceError.
    """
    try:
        if order_id in orders:
            raise DuplicateOrderError(order_id)
        validate_quantity(quantity)
        validate_price(price)

        orders[order_id] = {
            "id": order_id,
            "customer": customer,
            "product": product,
            "quantity": quantity,
            "price": price,
            "total": quantity * price,
            "status": "Placed"
        }
        print(f"[SUCCESS] Order {order_id} added for {customer}.")

    except DuplicateOrderError as e:
        print(f"[ERROR] {e}")
    except InvalidQuantityError as e:
        print(f"[ERROR] {e}")
    except InvalidPriceError as e:
        print(f"[ERROR] {e}")
    except OOPTSError as e:
        print(f"[SYSTEM ERROR] Unexpected OOPTS error: {e}")
    finally:
        print(f"  >> add_order({order_id}) attempt complete.\n")


def get_order(order_id):
    """
    Retrieves an order by ID.
    Raises OrderNotFoundError if not found.
    """
    try:
        if order_id not in orders:
            raise OrderNotFoundError(order_id)
        return orders[order_id]
    except OrderNotFoundError as e:
        print(f"[ERROR] {e}")
        return None


def update_order_status(order_id, new_status):
    """
    Updates the status of an existing order.
    Uses get_order() which handles OrderNotFoundError internally.
    """
    order = get_order(order_id)
    if order:
        old_status = order["status"]
        order["status"] = new_status
        print(f"[UPDATED] Order {order_id}: '{old_status}' → '{new_status}'")


def display_all_orders():
    """Displays all orders in a formatted table."""
    if not orders:
        print("[INFO] No orders currently in the system.\n")
        return
    print(f"\n{'ID':<8} {'Customer':<15} {'Product':<12} {'Qty':<5} {'Total':>8} {'Status':<12}")
    print("-" * 65)
    for o in orders.values():
        print(f"{o['id']:<8} {o['customer']:<15} {o['product']:<12} {o['quantity']:<5} ${o['total']:>7.2f} {o['status']:<12}")
    print()


# ─────────────────────────────────────────────
# 4. Safe Input Helper (wraps user input with error handling)
# ─────────────────────────────────────────────

def safe_int_input(prompt):
    """Prompts user for an integer, handles ValueError gracefully."""
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("[ERROR] Please enter a valid whole number.")

def safe_float_input(prompt):
    """Prompts user for a float, handles ValueError gracefully."""
    while True:
        try:
            value = float(input(prompt))
            return value
        except ValueError:
            print("[ERROR] Please enter a valid numeric value.")


# ─────────────────────────────────────────────
# 5. Demo / Example Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  STAGE 7 — Exception Handling Demo")
    print("=" * 50 + "\n")

    # Valid orders
    add_order(101, "Ravi", "Laptop", 1, 1200.00)
    add_order(102, "Priya", "Mouse", 3, 25.50)

    # Duplicate ID
    add_order(101, "Arjun", "Keyboard", 2, 45.00)

    # Invalid quantity
    add_order(103, "Sneha", "Monitor", -2, 300.00)

    # Invalid price
    add_order(104, "Kiran", "Headphones", 1, 0)

    # Search existing and missing orders
    print("--- Searching Orders ---")
    order = get_order(102)
    if order:
        print(f"Found: {order}\n")

    get_order(999)  # Should trigger OrderNotFoundError

    # Update status
    print("--- Updating Status ---")
    update_order_status(102, "Shipped")
    update_order_status(999, "Delivered")  # Should fail gracefully

    # Display all
    display_all_orders()
