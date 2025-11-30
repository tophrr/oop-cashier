from datetime import date

class Product:
    def __init__(self, product_id, name, price, stock):
        self.product_id = product_id
        self.name = name
        self.stock = stock
        self.price = price
    
    def addstock(self, quantity):
        if quantity <= 0:
            print("Quantity has to be above 0.")
            return
        
        self.stock += quantity
        return
    
    def reducestock(self, quantity):
        if quantity <= 0:
            print("Quantity has to be above 0.")
            return
        if quantity > self.stock:
            print("Quantity has to be below stock.")
            return
        
        self.stock -= quantity
        return
    
    def info(self):
        return f"Product ID: {self.product_id} | Product Name: {self.name} Product Price: {self.price} | Product Stock: {self.stock}"

class LimitedLifeProduct(Product):
    def __init__(self, product_id, name, price, stock, expirydate):
        super().__init__(product_id, name, price, stock)
        self.expirydate = expirydate
    
    def info(self):
        return f"Product ID: {self.product_id} | Product Name: {self.name} Product Price: {self.price} | Product Stock: {self.stock} | Product Expiry Date: {self.expirydate}"

class UnlimitedLifeProduct(Product):
    def info(self):
        return f"Product ID: {self.product_id} | Product Name: {self.name} Product Price: {self.price} | Product Stock: {self.stock}"            
