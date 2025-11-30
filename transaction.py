import json
from datetime import datetime


class Transaction:
    """
    Class untuk menangani keranjang belanja dan checkout.
    Menggunakan konsep AGGREGATION (Transaction punya daftar items).
    """

    def __init__(self, log_filename="transactions.json"):
        self.items = []  # List tuple (Product Object, quantity)
        self.total = 0
        self.log_filename = log_filename

    def add_item(self, product, quantity):
        """Menambah barang ke keranjang (Belum mengurangi stok database)"""
        if quantity <= 0:
            raise ValueError("Jumlah beli harus positif")

        # Validasi stok sementara
        if quantity > product.stock:
            raise ValueError(f"Stok tidak cukup. Sisa: {product.stock}")

        self.items.append({"product": product, "qty": quantity})
        self.total += product.price * quantity

    def checkout(self, inventory_system):
        """
        Finalisasi transaksi:
        1. Kurangi stok real di inventory.
        2. Simpan log transaksi ke JSON.
        """
        if not self.items:
            raise ValueError("Keranjang kosong")

        # 1. Kurangi Stok
        for item in self.items:
            prod = item["product"]
            qty = item["qty"]
            # Memanggil fungsi update_stock di inventory (yang akan save ke JSON)
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
            with open(self.log_filename, 'r') as f:
                existing_logs = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        existing_logs.append(log_entry)

        with open(self.log_filename, 'w') as f:
            json.dump(existing_logs, f, indent=4)
