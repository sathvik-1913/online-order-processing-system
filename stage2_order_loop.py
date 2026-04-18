# stage2_order_loop.py
# OOPTS Order System — Stage 2: Loops & Menu-Driven Input
# Concepts: while loop, if/elif/else, list.append(), basic menu system

orders = []

def main():
    while True:
        print("\n--- ORDER MANAGEMENT SYSTEM ---")
        print("1. Place Order")
        print("2. View Orders")
        print("3. Exit")

        choice = input("Select an option (1-3): ")

        if choice == '1':
            item_name = input("Enter item name: ")
            try:
                quantity = int(input("Enter quantity: "))
                if quantity > 0:
                    order_details = f"Item: {item_name} | Quantity: {quantity}"
                    orders.append(order_details)
                    print("Order added successfully!")
                else:
                    print("Invalid quantity. Must be greater than 0.")
            except ValueError:
                print("Invalid input. Please enter a number for quantity.")

        elif choice == '2':
            print("\n--- Current Orders ---")
            if not orders:
                print("No orders placed yet.")
            else:
                for i, order in enumerate(orders, 1):
                    print(f"{i}. {order}")

        elif choice == '3':
            print("Exiting system. Goodbye!")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
