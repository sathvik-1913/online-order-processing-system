# stage11_analytics_graphs.py
# OOPTS Order System — Stage 11: Analytics & Data Visualization
# Concepts: matplotlib, bar chart, pie chart, line chart, horizontal bar,
#           subplots, data aggregation, saving figures to PNG

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from collections import defaultdict

# ══════════════════════════════════════════════════════════════
# SAMPLE ORDER DATA
# ══════════════════════════════════════════════════════════════

orders = [
    {"order_id": 101, "customer": "Ravi Kumar",   "product": "Laptop",      "category": "Electronics", "quantity": 1,  "price": 1200.00, "status": "Shipped",    "date": "2024-01-05"},
    {"order_id": 102, "customer": "Priya Sharma",  "product": "Mouse",       "category": "Electronics", "quantity": 3,  "price": 25.50,   "status": "Delivered",  "date": "2024-01-08"},
    {"order_id": 103, "customer": "Arjun Singh",   "product": "Desk Chair",  "category": "Furniture",   "quantity": 2,  "price": 450.00,  "status": "Processing", "date": "2024-01-12"},
    {"order_id": 104, "customer": "Sneha Reddy",   "product": "Notebook",    "category": "Stationery",  "quantity": 10, "price": 5.99,    "status": "Delivered",  "date": "2024-01-15"},
    {"order_id": 105, "customer": "Kiran Patel",   "product": "Monitor",     "category": "Electronics", "quantity": 1,  "price": 320.00,  "status": "Shipped",    "date": "2024-01-18"},
    {"order_id": 106, "customer": "Ravi Kumar",    "product": "Keyboard",    "category": "Electronics", "quantity": 2,  "price": 75.00,   "status": "Placed",     "date": "2024-02-02"},
    {"order_id": 107, "customer": "Meera Nair",    "product": "Bookshelf",   "category": "Furniture",   "quantity": 1,  "price": 1800.00, "status": "Delivered",  "date": "2024-02-05"},
    {"order_id": 108, "customer": "Priya Sharma",  "product": "Pen Set",     "category": "Stationery",  "quantity": 5,  "price": 120.00,  "status": "Shipped",    "date": "2024-02-10"},
    {"order_id": 109, "customer": "Rohan Das",     "product": "Webcam",      "category": "Electronics", "quantity": 1,  "price": 850.00,  "status": "Cancelled",  "date": "2024-02-14"},
    {"order_id": 110, "customer": "Sneha Reddy",   "product": "Lamp",        "category": "Furniture",   "quantity": 2,  "price": 299.00,  "status": "Placed",     "date": "2024-02-20"},
    {"order_id": 111, "customer": "Kiran Patel",   "product": "USB Hub",     "category": "Electronics", "quantity": 4,  "price": 350.00,  "status": "Delivered",  "date": "2024-03-01"},
    {"order_id": 112, "customer": "Meera Nair",    "product": "Highlighter", "category": "Stationery",  "quantity": 8,  "price": 15.00,   "status": "Delivered",  "date": "2024-03-05"},
    {"order_id": 113, "customer": "Rohan Das",     "product": "Headphones",  "category": "Electronics", "quantity": 1,  "price": 2200.00, "status": "Shipped",    "date": "2024-03-10"},
    {"order_id": 114, "customer": "Arjun Singh",   "product": "File Cabinet","category": "Furniture",   "quantity": 1,  "price": 3200.00, "status": "Processing", "date": "2024-03-15"},
    {"order_id": 115, "customer": "Ravi Kumar",    "product": "Mousepad",    "category": "Electronics", "quantity": 3,  "price": 45.00,   "status": "Delivered",  "date": "2024-03-20"},
]

# Add computed total to each order
for o in orders:
    o["total"] = o["quantity"] * o["price"]


# ══════════════════════════════════════════════════════════════
# DATA AGGREGATION HELPERS
# ══════════════════════════════════════════════════════════════

def sales_by_product():
    """Returns {product: total_revenue} sorted descending."""
    data = defaultdict(float)
    for o in orders:
        data[o["product"]] += o["total"]
    return dict(sorted(data.items(), key=lambda x: x[1], reverse=True))

def orders_by_category():
    """Returns {category: order_count}."""
    data = defaultdict(int)
    for o in orders:
        data[o["category"]] += 1
    return dict(data)

def revenue_by_category():
    """Returns {category: total_revenue}."""
    data = defaultdict(float)
    for o in orders:
        data[o["category"]] += o["total"]
    return dict(data)

def orders_by_status():
    """Returns {status: count}."""
    data = defaultdict(int)
    for o in orders:
        data[o["status"]] += 1
    return dict(data)

def revenue_by_month():
    """Returns {month_label: total_revenue} in chronological order."""
    data = defaultdict(float)
    for o in orders:
        month = o["date"][:7]   # "YYYY-MM"
        data[month] += o["total"]
    return dict(sorted(data.items()))

def top_customers():
    """Returns {customer: total_spend} for top 5 customers."""
    data = defaultdict(float)
    for o in orders:
        data[o["customer"]] += o["total"]
    sorted_data = dict(sorted(data.items(), key=lambda x: x[1], reverse=True)[:5])
    return sorted_data


# ══════════════════════════════════════════════════════════════
# COLOUR PALETTE
# ══════════════════════════════════════════════════════════════

PALETTE   = ["#4C6EF5", "#37B24D", "#F59F00", "#F03E3E", "#7950F2", "#1C7ED6", "#0CA678"]
CAT_COLORS = {
    "Electronics": "#4C6EF5",
    "Furniture":   "#F59F00",
    "Stationery":  "#37B24D",
}
STATUS_COLORS = {
    "Delivered":  "#37B24D",
    "Shipped":    "#4C6EF5",
    "Processing": "#F59F00",
    "Placed":     "#74C0FC",
    "Cancelled":  "#F03E3E",
}


# ══════════════════════════════════════════════════════════════
# CHART 1 — Horizontal Bar: Revenue by Product
# ══════════════════════════════════════════════════════════════

def chart_revenue_by_product(ax):
    data    = sales_by_product()
    products = list(data.keys())
    revenues = list(data.values())
    colors   = [PALETTE[i % len(PALETTE)] for i in range(len(products))]

    bars = ax.barh(products, revenues, color=colors, height=0.6, edgecolor="none")

    for bar, val in zip(bars, revenues):
        ax.text(val + 50, bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}", va="center", ha="left", fontsize=8, color="#444")

    ax.set_title("Revenue by Product", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Total Revenue (₹)", fontsize=9)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}k"))
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_facecolor("#FAFAFA")
    ax.grid(axis="x", linestyle="--", alpha=0.4)


# ══════════════════════════════════════════════════════════════
# CHART 2 — Pie: Orders by Category
# ══════════════════════════════════════════════════════════════

def chart_orders_by_category(ax):
    data   = orders_by_category()
    labels = list(data.keys())
    sizes  = list(data.values())
    colors = [CAT_COLORS.get(l, "#aaa") for l in labels]

    wedges, texts, autotexts = ax.pie(
        sizes,
        labels=None,
        colors=colors,
        autopct="%1.0f%%",
        startangle=140,
        pctdistance=0.75,
        wedgeprops={"edgecolor": "white", "linewidth": 2},
    )
    for at in autotexts:
        at.set_fontsize(10)
        at.set_fontweight("bold")
        at.set_color("white")

    ax.legend(wedges, [f"{l} ({s})" for l, s in zip(labels, sizes)],
              loc="lower center", bbox_to_anchor=(0.5, -0.12),
              fontsize=9, frameon=False, ncol=3)
    ax.set_title("Orders by Category", fontsize=13, fontweight="bold", pad=12)


# ══════════════════════════════════════════════════════════════
# CHART 3 — Line: Monthly Revenue Trend
# ══════════════════════════════════════════════════════════════

def chart_monthly_revenue(ax):
    data    = revenue_by_month()
    months  = [m.replace("2024-", "Month ") for m in data.keys()]
    values  = list(data.values())

    ax.plot(months, values, color="#4C6EF5", linewidth=2.5,
            marker="o", markersize=8, markerfacecolor="white",
            markeredgewidth=2.5, markeredgecolor="#4C6EF5")
    ax.fill_between(months, values, alpha=0.1, color="#4C6EF5")

    for x, y in zip(months, values):
        ax.text(x, y + 200, f"₹{y:,.0f}", ha="center", fontsize=8, color="#4C6EF5", fontweight="bold")

    ax.set_title("Monthly Revenue Trend", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Revenue (₹)", fontsize=9)
    ax.set_xlabel("Month", fontsize=9)
    ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}k"))
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("#FAFAFA")
    ax.grid(axis="y", linestyle="--", alpha=0.4)


# ══════════════════════════════════════════════════════════════
# CHART 4 — Bar: Order Status Distribution
# ══════════════════════════════════════════════════════════════

def chart_order_status(ax):
    data    = orders_by_status()
    statuses = list(data.keys())
    counts   = list(data.values())
    colors   = [STATUS_COLORS.get(s, "#aaa") for s in statuses]

    bars = ax.bar(statuses, counts, color=colors, width=0.55, edgecolor="none")

    for bar, val in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.1,
                str(val), ha="center", va="bottom", fontsize=11, fontweight="bold")

    ax.set_title("Order Status Distribution", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Number of Orders", fontsize=9)
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.set_facecolor("#FAFAFA")
    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.set_ylim(0, max(counts) + 2)
    ax.tick_params(axis="x", labelsize=9)


# ══════════════════════════════════════════════════════════════
# CHART 5 — Grouped Bar: Revenue vs Orders by Category
# ══════════════════════════════════════════════════════════════

def chart_category_comparison(ax):
    import numpy as np
    cats     = list(CAT_COLORS.keys())
    rev_data = revenue_by_category()
    ord_data = orders_by_category()

    revenues = [rev_data.get(c, 0) / 1000 for c in cats]   # in thousands
    counts   = [ord_data.get(c, 0) * 500 for c in cats]     # scaled for visibility

    x     = np.arange(len(cats))
    width = 0.35

    b1 = ax.bar(x - width/2, revenues, width, label="Revenue (₹000s)",
                color=["#4C6EF5","#F59F00","#37B24D"], edgecolor="none")
    b2 = ax.bar(x + width/2, counts,   width, label="Orders × 500",
                color=["#91A7FF","#FFD43B","#8CE99A"], edgecolor="none")

    ax.set_xticks(x)
    ax.set_xticklabels(cats, fontsize=9)
    ax.set_title("Revenue vs Order Volume by Category", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylabel("Value", fontsize=9)
    ax.legend(fontsize=8, frameon=False)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_facecolor("#FAFAFA")
    ax.grid(axis="y", linestyle="--", alpha=0.4)


# ══════════════════════════════════════════════════════════════
# CHART 6 — Horizontal Bar: Top 5 Customers by Spend
# ══════════════════════════════════════════════════════════════

def chart_top_customers(ax):
    data      = top_customers()
    customers = list(data.keys())
    spends    = list(data.values())
    colors    = PALETTE[:len(customers)]

    bars = ax.barh(customers, spends, color=colors, height=0.5, edgecolor="none")

    for bar, val in zip(bars, spends):
        ax.text(val + 30, bar.get_y() + bar.get_height() / 2,
                f"₹{val:,.0f}", va="center", ha="left", fontsize=8, color="#444")

    ax.set_title("Top 5 Customers by Spend", fontsize=13, fontweight="bold", pad=12)
    ax.set_xlabel("Total Spend (₹)", fontsize=9)
    ax.invert_yaxis()
    ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"₹{x/1000:.0f}k"))
    ax.spines[["top", "right", "left"]].set_visible(False)
    ax.set_facecolor("#FAFAFA")
    ax.grid(axis="x", linestyle="--", alpha=0.4)
    ax.tick_params(axis="y", labelsize=9)


# ══════════════════════════════════════════════════════════════
# MAIN — Build the Dashboard
# ══════════════════════════════════════════════════════════════

def build_dashboard(save_path="oopts_dashboard.png"):
    fig = plt.figure(figsize=(18, 14))
    fig.patch.set_facecolor("#F0F2F5")

    # Title banner
    fig.text(0.5, 0.97, "OOPTS Order Management System — Analytics Dashboard",
             ha="center", va="top", fontsize=18, fontweight="bold", color="#1A1A2E")
    fig.text(0.5, 0.945, f"Total Orders: {len(orders)}  |  "
             f"Total Revenue: ₹{sum(o['total'] for o in orders):,.2f}  |  "
             f"Categories: {len(set(o['category'] for o in orders))}  |  "
             f"Customers: {len(set(o['customer'] for o in orders))}",
             ha="center", va="top", fontsize=11, color="#555")

    # Grid layout: 3 rows × 2 cols
    gs = fig.add_gridspec(3, 2, hspace=0.45, wspace=0.35,
                          top=0.90, bottom=0.06, left=0.07, right=0.97)

    ax1 = fig.add_subplot(gs[0, 0])
    ax2 = fig.add_subplot(gs[0, 1])
    ax3 = fig.add_subplot(gs[1, 0])
    ax4 = fig.add_subplot(gs[1, 1])
    ax5 = fig.add_subplot(gs[2, 0])
    ax6 = fig.add_subplot(gs[2, 1])

    chart_revenue_by_product(ax1)
    chart_orders_by_category(ax2)
    chart_monthly_revenue(ax3)
    chart_order_status(ax4)
    chart_category_comparison(ax5)
    chart_top_customers(ax6)

    # Style all axes backgrounds
    for ax in [ax1, ax3, ax4, ax5, ax6]:
        ax.set_facecolor("#FAFAFA")
        for spine in ax.spines.values():
            spine.set_color("#E0E0E0")

    plt.savefig(save_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"[✓] Dashboard saved → '{save_path}'")
    plt.show()


def print_summary():
    """Prints a text summary of key analytics."""
    print("\n" + "=" * 52)
    print("  OOPTS ANALYTICS SUMMARY")
    print("=" * 52)
    print(f"  Total Orders   : {len(orders)}")
    print(f"  Total Revenue  : ₹{sum(o['total'] for o in orders):,.2f}")
    print(f"  Avg Order Value: ₹{sum(o['total'] for o in orders)/len(orders):,.2f}")

    print("\n  --- Revenue by Category ---")
    for cat, rev in revenue_by_category().items():
        print(f"  {cat:<15}: ₹{rev:,.2f}")

    print("\n  --- Orders by Status ---")
    for status, count in orders_by_status().items():
        print(f"  {status:<12}: {count} order(s)")

    print("\n  --- Top 3 Products by Revenue ---")
    for i, (prod, rev) in enumerate(list(sales_by_product().items())[:3], 1):
        print(f"  {i}. {prod:<15}: ₹{rev:,.2f}")

    print("\n  --- Monthly Revenue ---")
    for month, rev in revenue_by_month().items():
        print(f"  {month}: ₹{rev:,.2f}")
    print("=" * 52)


if __name__ == "__main__":
    print_summary()
    build_dashboard("oopts_dashboard.png")
