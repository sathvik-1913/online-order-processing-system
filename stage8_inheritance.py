# stage8_inheritance.py
# Demonstrates Inheritance & Polymorphism in the OOPTS Order System

# ─────────────────────────────────────────────
# 1. Base Class: Order
# ─────────────────────────────────────────────

class Order:
    """Base class representing a standard customer order."""

    def __init__(self, order_id, customer, product, quantity, price):
        self.order_id = order_id
        self.customer = customer
        self.product = product
        self.quantity = quantity
        self.price = price
        self.status = "Placed"

    def calculate_total(self):
        """Returns the total cost. Can be overridden by subclasses."""
        return self.quantity * self.price

    def update_status(self, new_status):
        self.status = new_status

    def get_type(self):
        return "Standard"

    def display(self):
        print(f"┌─ [{self.get_type()} Order] ID: {self.order_id} ─────────────")
        print(f"│  Customer : {self.customer}")
        print(f"│  Product  : {self.product}")
        print(f"│  Qty      : {self.quantity}  x  ${self.price:.2f}")
        print(f"│  Total    : ${self.calculate_total():.2f}")
        print(f"│  Status   : {self.status}")
        print(f"└────────────────────────────────────────\n")

    def to_dict(self):
        return {
            "id": self.order_id,
            "type": self.get_type(),
            "customer": self.customer,
            "product": self.product,
            "quantity": self.quantity,
            "price": self.price,
            "total": self.calculate_total(),
            "status": self.status
        }


# ─────────────────────────────────────────────
# 2. Subclass: BulkOrder (inherits Order)
# ─────────────────────────────────────────────

class BulkOrder(Order):
    """
    A bulk order that applies a discount when quantity >= threshold.
    Overrides: calculate_total(), get_type(), display()
    """
    DISCOUNT_THRESHOLD = 10   # Minimum qty to qualify
    DISCOUNT_RATE = 0.15      # 15% discount

    def __init__(self, order_id, customer, product, quantity, price):
        super().__init__(order_id, customer, product, quantity, price)

    def calculate_total(self):
        """Applies a 15% discount if quantity meets the threshold."""
        raw_total = self.quantity * self.price
        if self.quantity >= BulkOrder.DISCOUNT_THRESHOLD:
            discount = raw_total * BulkOrder.DISCOUNT_RATE
            return raw_total - discount
        return raw_total

    def get_discount_amount(self):
        """Returns the discount applied (0 if not eligible)."""
        raw_total = self.quantity * self.price
        if self.quantity >= BulkOrder.DISCOUNT_THRESHOLD:
            return raw_total * BulkOrder.DISCOUNT_RATE
        return 0.0

    def get_type(self):
        return "Bulk"

    def display(self):
        print(f"┌─ [{self.get_type()} Order] ID: {self.order_id} ─────────────")
        print(f"│  Customer  : {self.customer}")
        print(f"│  Product   : {self.product}")
        print(f"│  Qty       : {self.quantity}  x  ${self.price:.2f}")
        raw = self.quantity * self.price
        discount = self.get_discount_amount()
        if discount > 0:
            print(f"│  Subtotal  : ${raw:.2f}")
            print(f"│  Discount  : -${discount:.2f} ({int(BulkOrder.DISCOUNT_RATE*100)}% bulk)")
        print(f"│  Total     : ${self.calculate_total():.2f}")
        print(f"│  Status    : {self.status}")
        print(f"└────────────────────────────────────────\n")

    def to_dict(self):
        d = super().to_dict()
        d["discount"] = self.get_discount_amount()
        return d


# ─────────────────────────────────────────────
# 3. Subclass: DigitalOrder (inherits Order)
# ─────────────────────────────────────────────

class DigitalOrder(Order):
    """
    A digital/downloadable order.
    Has no physical quantity — always 1 license.
    Adds a download_link attribute.
    Overrides: get_type(), display(), to_dict()
    """

    def __init__(self, order_id, customer, product, price, download_link):
        super().__init__(order_id, customer, product, quantity=1, price=price)
        self.download_link = download_link

    def get_type(self):
        return "Digital"

    def display(self):
        print(f"┌─ [{self.get_type()} Order] ID: {self.order_id} ─────────────")
        print(f"│  Customer  : {self.customer}")
        print(f"│  Product   : {self.product}")
        print(f"│  License   : 1 (digital)")
        print(f"│  Price     : ${self.price:.2f}")
        print(f"│  Total     : ${self.calculate_total():.2f}")
        print(f"│  Download  : {self.download_link}")
        print(f"│  Status    : {self.status}")
        print(f"└────────────────────────────────────────\n")

    def to_dict(self):
        d = super().to_dict()
        d["download_link"] = self.download_link
        return d


# ─────────────────────────────────────────────
# 4. Polymorphic Function
# ─────────────────────────────────────────────

def print_order_summary(order):
    """
    Polymorphic: works with Order, BulkOrder, or DigitalOrder.
    Calls the correct display() and calculate_total() for each type.
    """
    order.display()

def get_grand_total(order_list):
    """Returns the sum of totals across any mix of order types."""
    return sum(o.calculate_total() for o in order_list)


# ─────────────────────────────────────────────
# 5. Demo / Example Usage
# ─────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 50)
    print("  STAGE 8 — Inheritance & Polymorphism Demo")
    print("=" * 50 + "\n")

    # Create a mixed list of order types
    orders = [
        Order(101, "Ravi", "Notebook", 2, 5.99),
        BulkOrder(102, "Priya Supplies Co.", "Pen", 50, 1.20),
        BulkOrder(103, "Arjun Stores", "Folder", 5, 3.00),   # below threshold, no discount
        DigitalOrder(104, "Sneha", "Python Course", 499.00, "https://oopts.edu/dl/py101"),
        DigitalOrder(105, "Kiran", "Logo Pack", 199.00, "https://oopts.edu/dl/logo-pack"),
    ]

    # Polymorphic display — same function call, different behaviour per type
    print("─── All Orders ───\n")
    for order in orders:
        print_order_summary(order)

    # Grand total across all types
    total = get_grand_total(orders)
    print(f"{'─'*42}")
    print(f"  GRAND TOTAL (all orders): ${total:.2f}")
    print(f"{'─'*42}\n")

    # isinstance checks
    print("─── Type Checking (isinstance) ───")
    for o in orders:
        print(f"  Order {o.order_id} — type: {o.get_type():<10} | is Order: {isinstance(o, Order)}")

    # Update status polymorphically
    print("\n─── Updating statuses ───")
    orders[0].update_status("Shipped")
    orders[3].update_status("Download Ready")
    for o in orders:
        print(f"  Order {o.order_id} ({o.get_type()}): {o.status}")
