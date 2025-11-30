from product import Product

class Inventory:
    def __init__(self):
        self.products = {}
        
    def addproduct(self, product):
        if product.product_id in self.products:
            print("Product already existed.")
            return
        self.products[product.product_id] = product
        print("Product has been added.")

    def getproduct(self, product_id):
        if product_id not in self.products:
            print("Product not found.")
            return
        return self.products[product_id]

    def updatestock(self, product_id, qtychange):
        product = self.getproduct(product_id)
        if product is None:
            return

        if qtychange > 0:
            product.addstock(qtychange)
        else:
            product.reducestock(-qtychange)

    def listproducts(self):
        print("     PRODUCT LIST     ")
        if not self.products:
            print("No products available.")
            return

        for p in self.products.values():
            print(p.info())
