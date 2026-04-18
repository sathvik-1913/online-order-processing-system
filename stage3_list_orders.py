# stage3_list_orders.py
# OOPTS Order System — Stage 3: Lists, String Methods & Search
# Concepts: list of lists, str.strip(), str.title(), str.capitalize(),
#           case-insensitive search, formatted table output

# ─────────────────────────────────────────────
# 1. List of orders (list of lists)
#    Format: [Order ID, Customer Name, Product Name]
# ─────────────────────────────────────────────
orders = [
    ["101", "  alice smith  ", "LAPTOP"],
    ["102", "Bob Jones",       "mouse"],
    ["103", "alice smith",     "Keyboard"],
    ["104", "Carol White",     "MONITOR"],
    ["105", "bob jones",       "USB HUB"],
]

# ─────────────────────────────────────────────
# 2. Clean customer/product names
# ─────────────────────────────────────────────
for order in orders:
    order[1] = order[1].strip().title()    # " Alice Smith " -> "Alice Smith"
    order[2] = order[2].capitalize()       # "LAPTOP"        -> "Laptop"

# ─────────────────────────────────────────────
# 3. Search function (case-insensitive on ID or Customer Name)
# ─────────────────────────────────────────────
def search_orders(query):
    """Returns all orders where query matches Order ID or Customer Name."""
    query = query.lower()
    results = []
    for order in orders:
        if query in order[0].lower() or query in order[1].lower():
            results.append(order)
    return results

# ─────────────────────────────────────────────
# 4. Display orders as a formatted table
# ─────────────────────────────────────────────
def display_orders(order_list, title="Orders"):
    print(f"\n--- {title} ---")
    if not order_list:
        print("  (no results)")
        return
    print(f"{'ID':<10} {'Customer':<20} {'Product':<15}")
    print("-" * 45)
    for order in order_list:
        print(f"{order[0]:<10} {order[1]:<20} {order[2]:<15}")

# ─────────────────────────────────────────────
# Execution
# ─────────────────────────────────────────────
if __name__ == "__main__":
    display_orders(orders, title="All Orders")

    search_term = input("\nSearch by Name or ID: ")
    found = search_orders(search_term)

    display_orders(found, title=f"Search Results for '{search_term}'")
