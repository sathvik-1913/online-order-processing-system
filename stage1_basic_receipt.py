# stage1_basic_receipt.py
# OOPTS Order System — Stage 1: Basic Input/Output & Receipt Printing
# Concepts: input(), print(), variables, f-strings, try/except, basic arithmetic

def main():
    print("--- Welcome to the OOPTS Order System ---")

    customer_name = input("Enter Customer Name: ")
    product_name  = input("Enter Product Name: ")

    try:
        quantity      = int(input("Enter Quantity: "))
        price_per_unit = float(input("Enter Price per Unit: "))

        if quantity <= 0:
            print("Error: Quantity must be greater than 0.")
        else:
            total_amount = quantity * price_per_unit

            print("\n" + "=" * 30)
            print("       ORDER RECEIPT")
            print("=" * 30)
            print(f"Customer:     {customer_name}")
            print(f"Product:      {product_name}")
            print(f"Quantity:     {quantity}")
            print(f"Unit Price:   ${price_per_unit:.2f}")
            print("-" * 30)
            print(f"TOTAL AMOUNT: ${total_amount:.2f}")
            print("=" * 30)

    except ValueError:
        print("Invalid input. Please enter numeric values for quantity and price.")


if __name__ == "__main__":
    main()
