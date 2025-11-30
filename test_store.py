import unittest
import os
from product import NonPerishableProduct
from inventory import Inventory
from transaction import Transaction


class TestStoreSystem(unittest.TestCase):
    """
    Unit Testing untuk memastikan logika program berjalan benar
    """

    def setUp(self):
        # Menggunakan file test agar database utama aman
        self.test_inv_file = "test_inventory.json"
        self.test_log_file = "test_trans.json"

        # Bersihkan file sisa test sebelumnya
        if os.path.exists(self.test_inv_file):
            os.remove(self.test_inv_file)
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)

        self.inv = Inventory(self.test_inv_file)
        self.p1 = NonPerishableProduct("T0001", "Test Item", 1000, 10)
        self.inv.add_product(self.p1)

    def test_add_stock(self):
        """Test penambahan stok"""
        self.inv.update_stock("T0001", 5)
        self.assertEqual(self.inv.get_product("T0001").stock, 15)

    def test_insufficient_stock(self):
        """Test error handling saat stok kurang"""
        trx = Transaction(self.test_log_file)
        with self.assertRaises(ValueError):
            trx.add_item(self.p1, 20)  # Stok cuma 10, minta 20 harus error

    def test_checkout_process(self):
        """Test alur transaksi penuh: Masuk keranjang -> Bayar -> Stok berkurang"""
        trx = Transaction(self.test_log_file)
        trx.add_item(self.inv.get_product("T0001"), 2)

        # Cek total harga
        self.assertEqual(trx.total, 2000)

        # Lakukan Checkout
        trx.checkout(self.inv)

        # Cek apakah stok berkurang di inventory
        updated_prod = self.inv.get_product("T0001")
        self.assertEqual(updated_prod.stock, 8)  # 10 - 2 = 8

    def tearDown(self):
        # Bersihkan file dummy setelah test selesai
        if os.path.exists(self.test_inv_file):
            os.remove(self.test_inv_file)
        if os.path.exists(self.test_log_file):
            os.remove(self.test_log_file)


if __name__ == "__main__":
    unittest.main()
