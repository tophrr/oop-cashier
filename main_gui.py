import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
from inventory import Inventory
from transaction import Transaction
from product import NonPerishableProduct, PerishableProduct


class StoreApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Sistem Manajemen Toko MYC Mart - UAS OOP")
        self.root.geometry("800x600")

        # Inisialisasi logic backend
        self.inventory = Inventory()
        self.current_transaction = Transaction()

        # Setup tab menu navigasi
        self.tabs = ttk.Notebook(root)
        self.tab_inventory = ttk.Frame(self.tabs)
        self.tab_cashier = ttk.Frame(self.tabs)

        self.tabs.add(self.tab_inventory, text="Manajemen Stok (Inventory)")
        self.tabs.add(self.tab_cashier, text="Mesin Kasir (Transaksi)")
        self.tabs.pack(expand=1, fill="both")

        # Render UI
        self.setup_inventory_ui()
        self.setup_cashier_ui()

        # Daftar nama anggota kelompok
        self.lbl_footer = tk.Label(
            root,
            text=(
                "Ben M. A. Nesta - 01082240016\n"
                "Christopher M. M. Gijoh - 01082240011\n"
                "Daniel G. O. Latupeirissa - 01082240027\n"
                "Yoel Sungkono - 01082240021"
            ),
            fg="#aaaaaa",
            font=("Arial", 8, "italic"),
            justify="right",
            bg=root.cget("bg")
        )

        # Meletakkan footer di pojok kanan bawah
        self.lbl_footer.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-5)

    def setup_inventory_ui(self):
        # Bagian input (Form Tambah Produk)
        frame_input = ttk.LabelFrame(
            self.tab_inventory, text="Tambah / Update Produk")
        frame_input.pack(fill="x", padx=10, pady=5)

        # Baris 1: ID, Nama, Harga, Stok
        ttk.Label(frame_input, text="ID Produk:").grid(
            row=0, column=0, padx=5, pady=5)
        self.entry_id = ttk.Entry(frame_input, width=15)
        self.entry_id.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame_input, text="Nama:").grid(
            row=0, column=2, padx=5, pady=5)
        self.entry_name = ttk.Entry(frame_input, width=20)
        self.entry_name.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(frame_input, text="Harga:").grid(
            row=0, column=4, padx=5, pady=5)
        self.entry_price = ttk.Entry(frame_input, width=12)
        self.entry_price.grid(row=0, column=5, padx=5, pady=5)

        ttk.Label(frame_input, text="Stok:").grid(
            row=0, column=6, padx=5, pady=5)
        self.entry_stock = ttk.Entry(frame_input, width=8)
        self.entry_stock.grid(row=0, column=7, padx=5, pady=5)

        # Baris 2: Tipe Produk & Tanggal Exp
        ttk.Label(frame_input, text="Tipe Produk:").grid(
            row=1, column=0, padx=5, pady=5)

        # Dropdown pilihan tipe
        self.combo_type = ttk.Combobox(
            frame_input, values=["Tahan Lama", "Mudah Rusak"], state="readonly", width=13)
        self.combo_type.current(0)  # Default: Tahan Lama
        self.combo_type.grid(row=1, column=1, padx=5, pady=5)
        self.combo_type.bind("<<ComboboxSelected>>",
                             self.toggle_expiry_input)  # Event listener

        ttk.Label(frame_input, text="Tgl Exp (YYYY-MM-DD):").grid(row=1,
                                                                  column=2, padx=5, pady=5, columnspan=2, sticky="e")
        self.entry_exp = ttk.Entry(frame_input, width=15)
        self.entry_exp.grid(row=1, column=4, padx=5, pady=5)
        self.entry_exp.config(state="disabled")  # Default mati

        # Tombol Simpan (Lebar mencakup 2 kolom)
        btn_add = ttk.Button(frame_input, text="Simpan Produk",
                             command=self.add_product_action)
        btn_add.grid(row=1, column=6, columnspan=2,
                     padx=10, pady=5, sticky="ew")

        # Bagian Tabel Inventory
        # Menambah kolom 'Tipe' dan 'Exp' di tabel
        self.tree = ttk.Treeview(self.tab_inventory, columns=(
            "ID", "Nama", "Tipe", "Harga", "Stok", "Exp"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nama", text="Nama Produk")
        self.tree.heading("Tipe", text="Tipe")
        self.tree.heading("Harga", text="Harga (Rp)")
        self.tree.heading("Stok", text="Sisa Stok")
        self.tree.heading("Exp", text="Expired")

        # Mengatur lebar kolom agar rapi
        self.tree.column("ID", width=80)
        self.tree.column("Nama", width=150)
        self.tree.column("Tipe", width=100)
        self.tree.column("Harga", width=100)
        self.tree.column("Stok", width=80)
        self.tree.column("Exp", width=100)

        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        ttk.Button(self.tab_inventory, text="Refresh Data",
                   command=self.refresh_inventory_table).pack(pady=20)

        self.refresh_inventory_table()

    def setup_cashier_ui(self):
        # Input Transaksi
        frame_trans = ttk.Frame(self.tab_cashier)
        frame_trans.pack(fill="x", padx=10, pady=10)

        ttk.Label(frame_trans, text="ID Produk:").pack(side="left")
        self.trans_id = ttk.Entry(frame_trans)
        self.trans_id.pack(side="left", padx=5)

        ttk.Label(frame_trans, text="Jumlah Beli:").pack(side="left")
        self.trans_qty = ttk.Entry(frame_trans, width=5)
        self.trans_qty.pack(side="left", padx=5)

        ttk.Button(frame_trans, text="Tambah ke Keranjang",
                   command=self.add_to_cart_action).pack(side="left", padx=10)

        # Tabel Keranjang
        self.cart_tree = ttk.Treeview(self.tab_cashier, columns=(
            "Nama", "Qty", "Subtotal"), show="headings")
        self.cart_tree.heading("Nama", text="Nama Barang")
        self.cart_tree.heading("Qty", text="Jumlah")
        self.cart_tree.heading("Subtotal", text="Subtotal")
        self.cart_tree.pack(fill="both", expand=True, padx=10)

        # Total & Checkout
        self.lbl_total = ttk.Label(
            self.tab_cashier, text="Total: Rp 0", font=("Arial", 14, "bold"))
        self.lbl_total.pack(pady=10)

        ttk.Button(self.tab_cashier, text="BAYAR (CHECKOUT)",
                   command=self.checkout_action).pack(pady=10, ipadx=20)

    # LOGIC ACTIONS

    def toggle_expiry_input(self, event):
        """Mengaktifkan/mematikan input tanggal berdasarkan pilihan Combobox"""
        pilihan = self.combo_type.get()
        if pilihan == "Mudah Rusak":
            self.entry_exp.config(state="normal")
        else:
            self.entry_exp.delete(0, tk.END)  # Hapus isi jika ada
            self.entry_exp.config(state="disabled")

    def add_product_action(self):
        try:
            # Ambil data umum
            pid = self.entry_id.get()
            name = self.entry_name.get()
            price_str = self.entry_price.get()
            stock_str = self.entry_stock.get()

            # Validasi input kosong dasar
            if not pid or not name or not price_str or not stock_str:
                raise ValueError(
                    "Semua kolom (ID, Nama, Harga, Stok) wajib diisi")

            price = int(price_str)
            stock = int(stock_str)
            prod_type = self.combo_type.get()

            # Logika pembuatan objek (factory logic)
            if prod_type == "Tahan Lama":
                # Membuat objek NonPerishableProduct
                p = NonPerishableProduct(pid, name, price, stock)

            else:
                # Validasi tanggal untuk PerishableProduct
                date_str = self.entry_exp.get()
                if not date_str:
                    raise ValueError(
                        "Tanggal Exp wajib diisi untuk produk mudah rusak")

                try:
                    y, m, d = map(int, date_str.split('-'))
                    exp_date = date(y, m, d)
                except ValueError:
                    raise ValueError(
                        "Format tanggal salah! Gunakan YYYY-MM-DD")

                # Membuat objek PerishableProduct
                p = PerishableProduct(pid, name, price, stock, exp_date)

            # Simpan ke inventory
            self.inventory.add_product(p)

            messagebox.showinfo(
                "Sukses", f"Produk '{name}' berhasil disimpan!")
            self.refresh_inventory_table()

            # Reset Form
            self.entry_id.delete(0, tk.END)
            self.entry_name.delete(0, tk.END)
            self.entry_price.delete(0, tk.END)
            self.entry_stock.delete(0, tk.END)
            self.entry_exp.delete(0, tk.END)

        except ValueError as e:
            messagebox.showerror("Input Error", str(e))
        except Exception as e:
            messagebox.showerror("System Error", str(e))

    def refresh_inventory_table(self):
        # Hapus data lama
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Load data baru dari inventory
        for p in self.inventory.get_all_products():
            # Cek tipe objek menggunakan isinstance untuk display di tabel
            if isinstance(p, PerishableProduct):
                tipe_txt = "Mudah Rusak"
                exp_txt = p.expiry_date.isoformat()
            else:
                tipe_txt = "Tahan Lama"
                exp_txt = "-"

            self.tree.insert("", "end", values=(
                p.product_id, p.name, tipe_txt, p.price, p.stock, exp_txt))

    def add_to_cart_action(self):
        try:
            pid = self.trans_id.get()
            if not pid:
                return  # Abaikan jika kosong

            qty_str = self.trans_qty.get()
            qty = int(qty_str) if qty_str else 1

            prod = self.inventory.get_product(pid)
            self.current_transaction.add_item(prod, qty)

            # Update Tampilan Keranjang
            self.cart_tree.insert("", "end", values=(
                prod.name, qty, prod.price * qty))
            self.lbl_total.config(
                text=f"Total: Rp {self.current_transaction.total}")

        except Exception as e:
            messagebox.showerror("Gagal Tambah", str(e))

    def checkout_action(self):
        try:
            msg = self.current_transaction.checkout(self.inventory)
            messagebox.showinfo("Berhasil", msg)

            # Reset UI
            for item in self.cart_tree.get_children():
                self.cart_tree.delete(item)
            self.lbl_total.config(text="Total: Rp 0")

            # Refresh stok di tab inventory
            self.refresh_inventory_table()

        except Exception as e:
            messagebox.showerror("Gagal Checkout", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = StoreApp(root)
    root.mainloop()
