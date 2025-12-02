import json
import os
from datetime import datetime


class Transaction:
    """
    Class untuk menangani keranjang belanja dan checkout.
    Menggunakan konsep Aggregation (Transaction punya daftar items).
    """

    def __init__(self, log_filename="transactions.json"):
        self.items = []  # List tuple (Product Object, quantity)
        self.total = 0
        self.log_filename = log_filename

    def add_item(self, product, quantity):
        """Menambah barang ke keranjang (Belum mengurangi stok database)"""
        if quantity <= 0:
            raise ValueError("Jumlah beli harus positif")

        # Validasi stok sementara dari inventory sebelum ditambahkan ke keranjang
        if quantity > product.stock:
            raise ValueError(f"Stok tidak cukup. Stok tersedia: {product.stock}")

        # Validasi stok dari item yang sudah ada di keranjang   
        for item in self.items:
            if item["product"].product_id == product.product_id:
                if item["qty"] + quantity > product.stock:
                    raise ValueError(f"Stok tidak cukup. Stok tersedia: {product.stock}")
                item["qty"] += quantity
                self.total += product.price * quantity
                return

        # Jika produk belum ada di keranjang, tambahkan sebagai item baru
        self.items.append({"product": product, "qty": quantity})
        self.total += product.price * quantity

    def checkout(self, inventory_system):
        """Proses checkout: kurangi stok dan simpan log transaksi"""
        if not self.items:
            raise ValueError("Keranjang kosong")

        # 1. Kurangi Stok
        for item in self.items:
            prod = item["product"]
            qty = item["qty"]
            inventory_system.update_stock(prod.product_id, -qty)

        # 2. Simpan Log Transaksi
        self.save_transaction_log()

        # Reset keranjang
        self.items = []
        self.total = 0
        return "Transaksi Berhasil!"

    def save_transaction_log(self):
        """Menyimpan riwayat transaksi ke file JSON"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "total_amount": self.total,
            "items": [
                {
                    "product_id": item["product"].product_id,
                    "product_name": item["product"].name,
                    "quantity": item["qty"],
                    "subtotal": item["product"].price * item["qty"]
                }
                for item in self.items
            ]
        }

        # Baca log lama, tambah log baru, simpan ulang
        existing_logs = []
        try:
            if os.path.exists(self.log_filename):
                with open(self.log_filename, 'r') as f:
                    existing_logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        existing_logs.append(log_entry)

        with open(self.log_filename, 'w') as f:
            json.dump(existing_logs, f, indent=4)

    @staticmethod
    def get_history_log(filename="transactions.json"):
        """Membaca seluruh log transaksi dari JSON"""
        if not os.path.exists(filename):
            return []

        try:
            with open(filename, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
