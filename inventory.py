import json
import os
from product import Product, PerishableProduct, NonPerishableProduct


class Inventory:
    """
    Class untuk mengelola daftar produk dan I/O file JSON sebagai database sederhana
    """

    def __init__(self, filename="inventory.json"):
        self.products = {}  # Dictionary untuk menyimpan objek Product
        self.filename = filename
        self.load_data()  # Otomatis muat data saat aplikasi mulai

    def add_product(self, product):
        """Menambahkan produk baru ke sistem"""
        if product.product_id in self.products:
            raise ValueError(
                f"Produk dengan ID {product.product_id} sudah ada")

        self.products[product.product_id] = product
        self.save_data()  # Simpan perubahan ke file JSON

    def get_product(self, product_id):
        """Mencari produk berdasarkan ID"""
        if product_id not in self.products:
            raise KeyError("Produk tidak ditemukan")
        return self.products[product_id]

    def update_stock(self, product_id, quantity):
        """Update stok produk (bisa tambah atau kurang)"""
        product = self.get_product(product_id)
        if quantity > 0:
            product.add_stock(quantity)
        else:
            product.reduce_stock(abs(quantity))

        self.save_data()  # Simpan perubahan stok ke JSON

    def get_all_products(self):
        """Mengembalikan daftar semua produk dalam inventaris"""
        self.load_data()  # Pastikan data terbaru dimuat dari file JSON
        return self.products.values()

    def save_data(self):
        """Menyimpan seluruh data produk ke file JSON"""
        data_list = [p.to_dict() for p in self.products.values()]
        try:
            with open(self.filename, 'w') as f:
                json.dump(data_list, f, indent=4)
        except IOError as e:
            print(f"Gagal menyimpan database: {e}")

    def load_data(self):
        """Membaca file JSON dan mengubahnya kembali menjadi Objek Python"""
        if not os.path.exists(self.filename):
            return  # Jika file belum ada, biarkan kosong

        try:
            with open(self.filename, 'r') as f:
                data_list = json.load(f)
                for item in data_list:
                    # Menggunakan factory method dari class Product
                    prod_obj = Product.from_dict(item)
                    self.products[prod_obj.product_id] = prod_obj
        except (json.JSONDecodeError, IOError):
            self.products = {}  # Reset inventory jika file rusak atau tidak bisa dibaca
            print("Database rusak atau kosong, membuat inventory baru")
