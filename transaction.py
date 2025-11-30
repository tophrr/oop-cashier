from product import Product

class Transaction:
    def __init__(self):
        self.items = [] 
        self.total = 0

    def additem(self, product, quantity):
        if product is None:
            print("Product not found")
            return

        if quantity <= 0:
            print("Quantity must be more than 0.")
            return

        previous_stock = product.stock

        product.reducestock(quantity)

        if product.stock == previous_stock:
            print("Stock has not changed due to a problem beforehand.")
            return

        self.items.append((product, quantity))
        self.total += product.price * quantity
        print("Item has been added to transaction.")

    def calculatetotal(self):
        return self.total

    def printreceipt(self):
        print("\n     RECEIPT     ")
        if not self.items:
            print("No items are in this transaction.")
        else:
            for product, quantity in self.items:
                line_total = product.price * quantity
                print(f"{product.name} x{quantity} = {line_total}")
            print(" ")
            print(f"TOTAL: {self.total}")
        print("\n")
