# stage10_cli_app.py
# Full CLI Menu Application — OOPTS Order Management System
# Combines: OOP, inheritance, exception handling, file I/O (JSON + CSV)

import json
import csv
import os
from datetime import datetime


# ══════════════════════════════════════════════════════════════
# CUSTOM EXCEPTIONS (from Stage 7)
# ══════════════════════════════════════════════════════════════

class OOPTSError(Exception):
    pass

class InvalidQuantityError(OOPTSError):
    def __init__(self, v): super().__init__(f"Invalid quantity '{v}': must be a positive integer.")

class InvalidPriceError(OOPTSError):
    def __init__(self, v): super().__init__(f"Invalid price '{v}': must be a positive number.")

class OrderNotFoundError(OOPTSError):
    def __init__(self, oid): super().__init__(f"Order ID '{oid}' not found.")

class DuplicateOrderError(OOPTSError):
    def __init__(self, oid): super().__init__(f"Order ID '{oid}' already exists.")


# ══════════════════════════════════════════════════════════════
# ORDER CLASSES (from Stage 8)
# ══════════════════════════════════════════════════════════════

class Order:
    def __init__(self, order_id, customer, product, quantity, price):
        self.order_id  = int(order_id)
        self.customer  = str(customer).strip().title()
        self.product   = str(product).strip().capitalize()
        self.quantity  = int(quantity)
        self.price     = float(price)
        self.status    = "Placed"

    def calculate_total(self):
        return self.quantity * self.price

    def get_type(self):
        return "Standard"

    def update_status(self, s):
        self.status = s

    def to_dict(self):
        return {
            "type": self.get_type(),
            "order_id": self.order_id,
            "customer": self.customer,
            "product":  self.product,
            "quantity": self.quantity,
            "price":    self.price,
            "status":   self.status
        }

    def display(self):
        print(f"  ┌─ [{self.get_type()}] Order #{self.order_id}")
        print(f"  │  Customer : {self.customer}")
        print(f"  │  Product  : {self.product}")
        print(f"  │  Qty × Price : {self.quantity} × ${self.price:.2f}")
        print(f"  │  Total    : ${self.calculate_total():.2f}")
        print(f"  │  Status   : {self.status}")
        print(f"  └{'─'*38}")


class BulkOrder(Order):
    DISCOUNT_THRESHOLD = 10
    DISCOUNT_RATE      = 0.15

    def calculate_total(self):
        raw = self.quantity * self.price
        return raw * (1 - self.DISCOUNT_RATE) if self.quantity >= self.DISCOUNT_THRESHOLD else raw

    def get_type(self): return "Bulk"

    def display(self):
        raw      = self.quantity * self.price
        discount = raw * self.DISCOUNT_RATE if self.quantity >= self.DISCOUNT_THRESHOLD else 0
        print(f"  ┌─ [{self.get_type()}] Order #{self.order_id}")
        print(f"  │  Customer : {self.customer}")
        print(f"  │  Product  : {self.product}")
        print(f"  │  Qty × Price : {self.quantity} × ${self.price:.2f}  →  ${raw:.2f}")
        if discount:
            print(f"  │  Discount : -${discount:.2f} (15% bulk)")
        print(f"  │  Total    : ${self.calculate_total():.2f}")
        print(f"  │  Status   : {self.status}")
        print(f"  └{'─'*38}")

    def to_dict(self):
        d = super().to_dict()
        d["discount"] = round(self.quantity * self.price * self.DISCOUNT_RATE, 2) \
                        if self.quantity >= self.DISCOUNT_THRESHOLD else 0
        return d


class DigitalOrder(Order):
    def __init__(self, order_id, customer, product, price, download_link):
        super().__init__(order_id, customer, product, quantity=1, price=price)
        self.download_link = download_link

    def get_type(self): return "Digital"

    def display(self):
        print(f"  ┌─ [{self.get_type()}] Order #{self.order_id}")
        print(f"  │  Customer : {self.customer}")
        print(f"  │  Product  : {self.product}")
        print(f"  │  Price    : ${self.price:.2f}")
        print(f"  │  Download : {self.download_link}")
        print(f"  │  Status   : {self.status}")
        print(f"  └{'─'*38}")

    def to_dict(self):
        d = super().to_dict()
        d["download_link"] = self.download_link
        return d


# ══════════════════════════════════════════════════════════════
# ORDER MANAGER
# ══════════════════════════════════════════════════════════════

class OrderManager:
    DATA_FILE   = "oopts_orders.json"
    REPORT_FILE = "oopts_report.csv"

    def __init__(self):
        self.orders = {}   # {order_id (int): Order object}
        self._load()

    # ── CRUD ──────────────────────────────────────────────────

    def add(self, order: Order):
        if order.order_id in self.orders:
            raise DuplicateOrderError(order.order_id)
        if order.quantity <= 0:
            raise InvalidQuantityError(order.quantity)
        if order.price <= 0:
            raise InvalidPriceError(order.price)
        self.orders[order.order_id] = order

    def get(self, order_id: int) -> Order:
        if order_id not in self.orders:
            raise OrderNotFoundError(order_id)
        return self.orders[order_id]

    def update_status(self, order_id: int, new_status: str):
        order = self.get(order_id)
        order.update_status(new_status)

    def delete(self, order_id: int):
        self.get(order_id)          # raises if not found
        del self.orders[order_id]

    def all(self):
        return list(self.orders.values())

    def search(self, query: str):
        q = query.lower()
        return [o for o in self.orders.values()
                if q in str(o.order_id) or q in o.customer.lower() or q in o.product.lower()]

    # ── FILE I/O (JSON) ──────────────────────────────────────

    def _load(self):
        if not os.path.exists(self.DATA_FILE):
            return
        try:
            with open(self.DATA_FILE, 'r') as f:
                data = json.load(f)
            for d in data:
                t = d.get("type", "Standard")
                if t == "Bulk":
                    o = BulkOrder(d["order_id"], d["customer"], d["product"], d["quantity"], d["price"])
                elif t == "Digital":
                    o = DigitalOrder(d["order_id"], d["customer"], d["product"], d["price"], d.get("download_link",""))
                else:
                    o = Order(d["order_id"], d["customer"], d["product"], d["quantity"], d["price"])
                o.status = d.get("status", "Placed")
                self.orders[o.order_id] = o
            print(f"  [INFO] Loaded {len(self.orders)} order(s) from '{self.DATA_FILE}'.")
        except Exception as e:
            print(f"  [WARNING] Could not load data: {e}")

    def save(self):
        try:
            with open(self.DATA_FILE, 'w') as f:
                json.dump([o.to_dict() for o in self.orders.values()], f, indent=2)
            print(f"  [SAVED] {len(self.orders)} order(s) → '{self.DATA_FILE}'.")
        except IOError as e:
            print(f"  [ERROR] Save failed: {e}")

    # ── CSV EXPORT ────────────────────────────────────────────

    def export_csv(self):
        if not self.orders:
            print("  [INFO] No orders to export.")
            return
        fields = ["order_id","type","customer","product","quantity","price","total","status"]
        try:
            with open(self.REPORT_FILE, 'w', newline='', encoding='utf-8') as f:
                w = csv.DictWriter(f, fieldnames=fields, extrasaction='ignore')
                w.writeheader()
                for o in self.orders.values():
                    row = o.to_dict()
                    row["total"] = round(o.calculate_total(), 2)
                    w.writerow(row)
            print(f"  [EXPORTED] Report → '{self.REPORT_FILE}' ({len(self.orders)} rows).")
        except IOError as e:
            print(f"  [ERROR] Export failed: {e}")


# ══════════════════════════════════════════════════════════════
# UI HELPERS
# ══════════════════════════════════════════════════════════════

def header(title):
    print(f"\n{'═'*46}")
    print(f"  {title}")
    print(f"{'═'*46}")

def divider():
    print(f"  {'─'*44}")

def safe_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("  [!] Enter a whole number.")

def safe_float(prompt):
    while True:
        try:
            v = float(input(prompt))
            if v <= 0: raise ValueError
            return v
        except ValueError:
            print("  [!] Enter a positive number.")

def safe_pos_int(prompt):
    while True:
        v = safe_int(prompt)
        if v > 0: return v
        print("  [!] Must be > 0.")

STATUS_OPTIONS = ["Placed","Processing","Shipped","Delivered","Cancelled"]

def pick_status():
    print("  Statuses:")
    for i, s in enumerate(STATUS_OPTIONS, 1):
        print(f"    {i}. {s}")
    while True:
        choice = safe_int("  Choose (1-5): ")
        if 1 <= choice <= len(STATUS_OPTIONS):
            return STATUS_OPTIONS[choice - 1]
        print("  [!] Invalid choice.")


# ══════════════════════════════════════════════════════════════
# MENU ACTIONS
# ══════════════════════════════════════════════════════════════

def menu_place_order(mgr: OrderManager):
    header("Place New Order")
    print("  Type: 1=Standard  2=Bulk  3=Digital")
    t = safe_int("  Select type: ")

    oid = safe_int("  Order ID   : ")
    cust = input("  Customer   : ").strip()
    prod = input("  Product    : ").strip()

    try:
        if t == 3:
            price = safe_float("  Price ($)  : ")
            link  = input("  Download URL: ").strip()
            order = DigitalOrder(oid, cust, prod, price, link)
        else:
            qty  = safe_pos_int("  Quantity   : ")
            price = safe_float("  Unit Price : ")
            order = BulkOrder(oid, cust, prod, qty, price) if t == 2 else Order(oid, cust, prod, qty, price)

        mgr.add(order)
        print(f"\n  [✓] Order #{oid} placed! Total: ${order.calculate_total():.2f}")
    except (DuplicateOrderError, InvalidQuantityError, InvalidPriceError) as e:
        print(f"  [ERROR] {e}")


def menu_view_orders(mgr: OrderManager):
    header("All Orders")
    orders = mgr.all()
    if not orders:
        print("  No orders yet.")
        return
    for o in orders:
        o.display()
    divider()
    grand = sum(o.calculate_total() for o in orders)
    print(f"  Grand Total: ${grand:.2f}   ({len(orders)} order(s))")


def menu_search(mgr: OrderManager):
    header("Search Orders")
    q = input("  Search (ID / name / product): ").strip()
    results = mgr.search(q)
    if not results:
        print("  No matching orders.")
    else:
        print(f"  {len(results)} result(s):\n")
        for o in results:
            o.display()


def menu_update_status(mgr: OrderManager):
    header("Update Order Status")
    oid = safe_int("  Order ID: ")
    try:
        order = mgr.get(oid)
        print(f"  Current status: {order.status}")
        new_status = pick_status()
        mgr.update_status(oid, new_status)
        print(f"  [✓] Order #{oid} → {new_status}")
    except OrderNotFoundError as e:
        print(f"  [ERROR] {e}")


def menu_delete_order(mgr: OrderManager):
    header("Delete Order")
    oid = safe_int("  Order ID to delete: ")
    try:
        order = mgr.get(oid)
        confirm = input(f"  Delete order #{oid} ({order.product} for {order.customer})? [y/N]: ")
        if confirm.lower() == 'y':
            mgr.delete(oid)
            print(f"  [✓] Order #{oid} deleted.")
        else:
            print("  Cancelled.")
    except OrderNotFoundError as e:
        print(f"  [ERROR] {e}")


def menu_export(mgr: OrderManager):
    header("Export Report")
    print("  1. Export CSV report")
    print("  2. Save JSON (auto-done on exit)")
    choice = safe_int("  Choose: ")
    if choice == 1:
        mgr.export_csv()
    elif choice == 2:
        mgr.save()
    else:
        print("  Invalid choice.")


# ══════════════════════════════════════════════════════════════
# MAIN LOOP
# ══════════════════════════════════════════════════════════════

MENU = [
    ("Place new order",    menu_place_order),
    ("View all orders",    menu_view_orders),
    ("Search orders",      menu_search),
    ("Update order status",menu_update_status),
    ("Delete an order",    menu_delete_order),
    ("Export report",      menu_export),
]

def main():
    print("\n" + "█"*46)
    print("█  OOPTS — ORDER MANAGEMENT SYSTEM  v1.0  █")
    print("█  Stages 1–10 Capstone Application       █")
    print("█"*46)

    mgr = OrderManager()

    while True:
        print(f"\n{'─'*46}")
        for i, (label, _) in enumerate(MENU, 1):
            print(f"  {i}. {label}")
        print(f"  0. Save & Exit")
        print(f"{'─'*46}")

        choice = input("  Select option: ").strip()

        if choice == '0':
            mgr.save()
            print("\n  Goodbye! All orders saved.\n")
            break

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(MENU):
                MENU[idx][1](mgr)
            else:
                print("  [!] Invalid option. Choose 0–6.")
        except ValueError:
            print("  [!] Enter a number.")


if __name__ == "__main__":
    main()
