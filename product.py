import json
from abc import ABC, abstractmethod
from datetime import date


class Product(ABC):
    """
    Parent Class (Abstract).
    Menerapkan ENCAPSULATION: Atribut dibuat private (__).
    """

    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    # Getter & Setter (Encapsulation)
    @property
    def product_id(self):
        return self.__product_id

    @property
    def name(self):
        return self.__name

    @property
    def price(self):
        return self.__price

    @property
    def stock(self):
        return self.__stock

    def add_stock(self, quantity):
        """Menambah stok dengan validasi"""
        if quantity <= 0:
            raise ValueError("Jumlah penambahan stok harus positif")
        self.__stock += quantity

    def reduce_stock(self, quantity):
        """Mengurangi stok dengan validasi (Exception Handling)"""
        if quantity <= 0:
            raise ValueError("Jumlah pengurangan harus positif")
        if quantity > self.__stock:
            raise ValueError(
                f"Stok tidak cukup! Stok saat ini: {self.__stock}")
        self.__stock -= quantity

    @abstractmethod
    def to_dict(self):
        """Method abstrak untuk konversi ke dictionary (persiapan JSON)"""
        pass

    @staticmethod
    def from_dict(data):
        """Factory Method untuk membuat objek dari data JSON"""
        if data['type'] == 'Perishable':
            # Konversi string tanggal kembali ke objek date
            y, m, d = map(int, data['expiry_date'].split('-'))
            return PerishableProduct(data['id'], data['name'], data['price'], data['stock'], date(y, m, d))
        else:
            return NonPerishableProduct(data['id'], data['name'], data['price'], data['stock'])


class PerishableProduct(Product):
    """
    Child Class untuk barang mudah rusak (Inheritance).
    """

    def __init__(self, product_id, name, price, stock, expiry_date):
        super().__init__(product_id, name, price, stock)
        self.expiry_date = expiry_date

    def to_dict(self):
        # Polymorphism: Output menyertakan expiry_date
        return {
            "type": "Perishable",
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "expiry_date": self.expiry_date.isoformat()
        }


class NonPerishableProduct(Product):
    """
    Child Class untuk barang tahan lama (Inheritance).
    """

    def to_dict(self):
        return {
            "type": "NonPerishable",
            "id": self.product_id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock
        }
