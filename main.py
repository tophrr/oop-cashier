from datetime import date
from inventory import Inventory
from product import LimitedLifeProduct, UnlimitedLifeProduct
from transaction import Transaction

def dictionaryinventory(inventory):
    inventory.addproduct(LimitedLifeProduct("P001", "Ice Cream", 15000, 10, date(2025, 12, 31)))
    inventory.addproduct(LimitedLifeProduct("P002", "Chocolate", 12000, 8, date(2025, 11, 20)))
    inventory.addproduct(UnlimitedLifeProduct("P003", "Spatula", 7000, 20))
    inventory.addproduct(UnlimitedLifeProduct("P004", "Spoon", 50000, 30))

def mainmenu():
    inventory = Inventory()
    dictionaryinventory(inventory)

    while True:
        print("\n    CASHIER    ")
        print("1. Show product list")
        print("2. Add stock to product")
        print("3. New transaction")
        print("4. Exit")

        choice = input("Choose command: ")

        if choice == "1":
            inventory.listproducts()

        elif choice == "2":
            product_id = input("Enter product ID: ")
            quantity_text = input("How many do you want to add? ")

            if not quantity_text.isdigit():
                print("Quantity must be a positive number.")
                continue

            quantity = int(quantity_text)
            inventory.updatestock(product_id, quantity)

        elif choice == "3":
            transaction = Transaction()

            while True:
                code = input("Enter product ID or 'done' to finish command: ")
                if code.lower() == "done":
                    break

                product = inventory.getproduct(code)
                if product is None:
                    continue

                quantity_text = input("Quantity: ")
                if not quantity_text.isdigit():
                    print("Quantity must be a positive number.")
                    continue

                quantity = int(quantity_text)
                transaction.additem(product, quantity) 

            transaction.printreceipt()

        elif choice == "4":
            print("Thank you.")
            break

        else:
            print("Please input our listed commands.")

if __name__ == "__main__":
    mainmenu()
