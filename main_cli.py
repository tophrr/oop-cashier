from inventory import Inventory
from product import NonPerishableProduct, PerishableProduct
from transaction import Transaction
from datetime import date


def main():
    inventory = Inventory()  # Load data dari inventory.json

    print((
        "Proyek UAS OOP - Sistem Manajemen Toko MYC Mart\n"
        "Ben M. A. Nesta - 01082240016\n"
        "Christopher M. M. Gijoh - 01082240011\n"
        "Daniel G. O. Latupeirissa - 01082240027\n"
        "Yoel Sungkono - 01082240021"
    ))

    while True:
        print("\n===== SISTEM KASIR TOKO MYC Mart =====")
        print("1. Lihat Semua Produk")
        print("2. Tambah Produk Baru (Admin)")
        print("3. Tambah Stok (Restock)")
        print("4. Transaksi Kasir")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            print("\n --- DAFTAR PRODUK ---")
            products = inventory.get_all_products()
            if not products:
                print("Inventory kosong")
            for p in products:
                # Menggunakan polymorphism pada p.to_dict()
                info = p.to_dict()
                print(
                    f"[{info['id']}] {info['name']} | Stok: {info['stock']} | Rp {info['price']}")

        elif pilihan == "2":
            try:
                tipe = input("Tipe (1: Tahan Lama, 2: Mudah Rusak): ")
                pid = input("ID Produk: ")
                nama = input("Nama Produk: ")
                harga = int(input("Harga: "))
                stok = int(input("Stok Awal: "))

                if tipe == "1":
                    p = NonPerishableProduct(pid, nama, harga, stok)
                else:
                    tgl_str = input("Tanggal Exp (YYYY-MM-DD): ")
                    y, m, d = map(int, tgl_str.split('-'))
                    p = PerishableProduct(
                        pid, nama, harga, stok, date(y, m, d))

                inventory.add_product(p)
                print("Produk berhasil disimpan ke database")
            except Exception as e:
                print(f"ERROR: {e}")

        elif pilihan == "3":
            try:
                pid = input("ID Produk: ")
                qty = int(input("Jumlah penambahan: "))
                inventory.update_stock(pid, qty)
                print("Stok berhasil diupdate")
            except Exception as e:
                print(f"ERROR: {e}")

        elif pilihan == "4":
            trx = Transaction()
            print("\n--- MENU TRANSAKSI ---")
            while True:
                pid = input(
                    "Masukkan ID Produk (atau ketik \"bayar\" jika selesai): ")
                if pid.lower() == 'bayar':
                    break

                try:
                    prod = inventory.get_product(pid)
                    qty = int(input(f"Beli {prod.name}, jumlah: "))
                    trx.add_item(prod, qty)
                    print(
                        f"Masuk keranjang. Subtotal saat ini: Rp {trx.total}")
                except Exception as e:
                    print(f"GAGAL: {e}")

            # Proses Checkout
            if trx.total > 0:
                print(f"Total Tagihan: Rp {trx.total}")
                konfirm = input("Konfirmasi bayar? (y/n): ")
                if konfirm.lower() == 'y':
                    try:
                        inventory.update_stock  # Agar inventory ter-load
                        trx.checkout(inventory)
                        print("Transaksi berhasil dan tersimpan")
                    except Exception as e:
                        print(f"Checkout Gagal: {e}")
            else:
                print("Transaksi dibatalkan")

        elif pilihan == "5":
            print("Terima kasih telah menggunakan sistem MYC Mart!")
            break
        else:
            print("Pilihan tidak valid")


if __name__ == "__main__":
    main()
