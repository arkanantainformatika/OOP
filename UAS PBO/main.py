"""
Tema: Hewan Peliharaan
Judul: Pet Shop

Penyimpanan eksternal: TSV (Tab Separated Values)
Mirip dengan CSV, tapi menggunakan tab sebagai pemisah. Memudahkan karena nama produk mungkin ada yang punya koma.
"""

import os
from typing import List


class User:
    def __init__(self, name, username, password, role):
        self.name = name
        self.username = username
        self.password = password
        self.role = role
        self._shopping_cart = []

    def get_shopping_cart_total(self):
        total = 0
        for product, amount in self._shopping_cart:
            total += product.price * amount

        return total

    # Lihat isi keranjang belanja.
    def get_shopping_cart_items(self, interactive=False):
        if len(self._shopping_cart) == 0:
            if interactive:
                print("Keranjang belanja kosong.")
                Utils.enter_and_continue()

            return

        print("Keranjang Belanja: ")
        for product, amount in self._shopping_cart:
            print(
                f"* {product.name} - {product.get_price_formatted()} - Jumlah: {amount}"
            )

        print()
        print(f"Total: {Utils.format_rupiah(self.get_shopping_cart_total())}")

        print()

        if interactive:
            Utils.enter_and_continue()

    def add_to_shopping_cart(self, product, amount):
        # Cek apakah produk sudah ada di keranjang.
        for i, (p, a) in enumerate(self._shopping_cart):
            if p is product:
                self._shopping_cart[i] = (p, amount)
                print("Jumlah produk berhasil diubah.")
                break
        else:
            self._shopping_cart.append((product, amount))
            print("Produk berhasil ditambahkan ke keranjang.")

    def remove_from_shopping_cart(self):
        if len(self._shopping_cart) == 0:
            print("Keranjang belanja kosong.")
            Utils.enter_and_continue()
            return

        print("[0] Kembali")
        for i, (p, a) in enumerate(self._shopping_cart):
            print(f"[{i + 1}] {p.name} - {p.get_price_formatted()} - Jumlah: {a}")

        choice = input("Pilihan: ")

        if choice == "0":
            return

        try:
            index = int(choice) - 1
            self._shopping_cart.pop(index)
            print("Produk berhasil dihapus dari keranjang.")
        except (ValueError, IndexError):
            print("Pilihan tidak valid.")

        Utils.enter_and_continue()

    def checkout(self):
        for product, amount in self._shopping_cart:
            product.decrease_stock(amount)

        Product.save_to_file()
        self._shopping_cart = []

    # Buat user. Hanya input-input beserta validasinya.
    @staticmethod
    def input_user(admin=False):
        while True:
            nama = input("Nama: ")
            # Validasi nama ga boleh kosong.
            if nama == "":
                print("Nama tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            username = input("Username: ")
            # Validasi username ga boleh kosong.
            if username == "":
                print("Username tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            # Validasi username harus unik.
            if any(user.username == username for user in user_list):
                print("Username sudah ada.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            password = input("Password: ")
            # Validasi password ga boleh kosong.
            if password == "":
                print("Password tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        # Default role adalah user.
        role = "user"

        # Jika admin, maka bisa pilih role.
        if admin:
            while True:
                role_dict = {"1": "user", "2": "admin", "3": "doctor"}
                print("Role: ")
                print("[1] User")
                print("[2] Admin")
                print("[3] Doctor")
                role = input("Role: ")

                # Validasi role ga boleh kosong.
                if role == "":
                    print("Role tidak boleh kosong.")
                    Utils.enter_and_continue()
                    continue

                if role not in role_dict.keys():
                    print("Role tidak valid.")
                    Utils.enter_and_continue()
                    continue

                role = role_dict[role]

                break

        return User(nama, username, password, role)

    @staticmethod
    def create_user():
        user = User.input_user()
        user_list.append(user)

        print("User berhasil ditambahkan.")

        User.save_to_file()
        Utils.enter_and_continue()

    @staticmethod
    def list_user():
        print("Daftar User: ")
        for i, user in enumerate(user_list):
            print(f"{i + 1}. {user.name} - {user.username} - {user.role}")

        Utils.enter_and_continue()

    # Simpan user ke tsv.
    @staticmethod
    def save_to_file():
        with open("users.tsv", "w") as file:
            file.write("nama\tusername\tpassword\trole\n")
            for user in user_list:
                file.write(
                    f"{user.name}\t{user.username}\t{user.password}\t{user.role}\n"
                )

    # Ambil user dari tsv.
    @staticmethod
    def load_from_file():
        with open("users.tsv", "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                name, username, password, role = line.strip().split("\t")
                user = User(name, username, password, role)
                user_list.append(user)

    @staticmethod
    def login():
        username = input("Username: ")
        password = input("Password: ")

        # Cek apakah username dan password ada di user_list.
        user = next((user for user in user_list if user.username == username), None)

        if user is not None and user.password == password:
            print("Login berhasil.")
            Utils.enter_and_continue()

            return user

        print("Username atau password salah.")
        Utils.enter_and_continue()

        return None

    @staticmethod
    def menu(current_user):
        while True:
            Utils.clear()
            print("Menu User")
            print("[0] Kembali")
            print("[1] Toko / Belanja")
            print("[2] Layanan")

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice == "1":
                Shop.menu(current_user)
            elif choice == "2":
                Service.menu(current_user)
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def forgot_password():
        username = input("Username: ")
        name = input("Nama: ")
        # Cari user berdasarkan username dan name.
        user = next(
            (
                user
                for user in user_list
                if user.username == username and user.name == name
            ),
            None,
        )

        if user is None:
            print("Username atau nama salah.")
            Utils.enter_and_continue()
            return

        if user.role == "admin":
            print("Tidak bisa reset password admin.")
            Utils.enter_and_continue()
            return

        while True:
            new_password = input("Password baru: ")
            if new_password == "":
                print("Password tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            break

        user.password = new_password

        print("Password berhasil diubah.")
        Utils.enter_and_continue()

        User.save_to_file()


current_user: User | None = None


class Admin(User):
    def __init__(self, name, username, password, role):
        super().__init__(name, username, password, role)

    @staticmethod
    def menu(current_user):
        while True:
            Utils.clear()
            print("Menu Admin")
            print("[0] Kembali")
            print("[1] Tambah User")
            print("[2] Lihat User")
            print("[3] Tambah Produk")
            print("[4] Lihat Produk")

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice == "1":
                User.create_user()
            elif choice == "2":
                User.list_user()
            elif choice == "3":
                Product.create_product()
            elif choice == "4":
                Product.list_product()


class Doctor(User):
    def __init__(self, name, username, password, role):
        super().__init__(name, username, password, role)

    @staticmethod
    def menu(current_user):
        while True:
            Utils.clear()
            print("Menu Dokter")
            print("[0] Kembali")
            print("[1] Lihat User")
            print("[2] Lihat Produk")

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice == "1":
                User.list_user()
            elif choice == "2":
                Product.list_product()


# Utility class.
# Isinya method-method kayak clear screen, press enter to continue.
class Utils:
    @staticmethod
    def clear():
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    @staticmethod
    def enter_and_continue():
        input("Press Enter to continue...")
        Utils.clear()

    # Ubah format angka jadi format rupiah.
    @staticmethod
    def format_rupiah(amount):
        formatted_amount = f"{amount:,.2f}"
        formatted_amount = (
            formatted_amount.replace(",", "X").replace(".", ",").replace("X", ".")
        )

        return f"Rp. {formatted_amount}"


class Product:
    def __init__(self, name, price, stock, category):
        self.name = name
        self.price = price
        self._stock = stock
        self.category = category

    def get_price_formatted(self):
        return Utils.format_rupiah(self.price)

    # Enkapsulasi pada stock
    def get_stock(self):
        return self._stock

    def decrease_stock(self, amount):
        if self._stock < amount:
            print("Stok tidak cukup.")
            Utils.enter_and_continue()
            return False

        self._stock -= amount

    def increase_stock(self, amount):
        self._stock += amount

    def set_stock(self, amount):
        if amount < 0:
            print("Stok tidak boleh negatif.")
            Utils.enter_and_continue()
            return False

        self._stock = amount

    # Buat produknya. Hanya input-input beserta validasinya.
    @staticmethod
    def input_product():
        while True:
            name = input("Nama produk: ")
            # Validasi nama produk ga boleh kosong.
            if name == "":
                print("Nama produk tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            # Validasi nama produk harus unik.
            if any(product.name == name for product in product_list):
                print("Nama produk sudah ada.")
                Utils.enter_and_continue()
                continue

            break

        while True:
            price = input("Harga produk: ")
            # Validasi harga produk harus angka valid.
            if not price.isdigit():
                print("Harga produk harus angka yang valid.")
                Utils.enter_and_continue()
                continue

            price = int(price)

            break

        while True:
            stock = input("Stok produk: ")
            # Validasi stok produk harus angka.
            if not stock.isdigit():
                print("Stok produk harus angka yang valid.")
                Utils.enter_and_continue()
                continue

            stock = int(stock)

            break

        while True:
            category_dict = {
                "1": "hewan",
                "2": "makanan",
                "3": "mainan",
                "4": "aksesoris",
                "5": "lainnya",
            }
            print("Kategori Produk: ")
            print("[1] Hewan")
            print("[2] Makanan")
            print("[3] Mainan")
            print("[4] Aksesoris (Kalung, Pakaian, dll.)")
            print("[5] Lainnya")
            category = input("Kategori produk: ")
            # Validasi kategori produk ga boleh kosong.
            if category == "":
                print("Kategori produk tidak boleh kosong.")
                Utils.enter_and_continue()
                continue

            if category not in category_dict.keys():
                print("Kategori produk tidak valid.")
                Utils.enter_and_continue()
                continue

            category = category_dict[category]

            break

        return Product(name, price, stock, category)

    @staticmethod
    def create_product():
        product = Product.input_product()
        product_list.append(product)

        print("Produk berhasil ditambahkan.")

        Product.save_to_file()
        Utils.enter_and_continue()

    @staticmethod
    def list_product():
        print("Daftar Produk: ")
        for i, product in enumerate(product_list):
            print(
                f"{i + 1}. {product.name} - {product.get_price_formatted()} - {product.get_stock()} - {product.category}"
            )

        Utils.enter_and_continue()

    # Simpan produk dari tsv.
    @staticmethod
    def save_to_file():
        with open("products.tsv", "w") as file:
            file.write("nama\tharga\tstok\tkategori\n")
            for product in product_list:
                file.write(
                    f"{product.name}\t{product.price}\t{product.get_stock()}\t{product.category}\n"
                )

    # Ambil produk dari tsv.
    @staticmethod
    def load_from_file():
        with open("products.tsv", "r") as file:
            lines = file.readlines()
            for line in lines[1:]:
                name, price, stock, category = line.strip().split("\t")
                product_list.append(
                    Product(name, int(price), int(stock), category.title())
                )


class Shop:
    categories = ["Hewan", "Makanan", "Mainan", "Aksesoris", "Lainnya"]

    @staticmethod
    def print_categories():
        print("[0] Kembali")
        for i, category in enumerate(Shop.categories):
            print(f"[{i + 1}] {category}")

        return Shop.categories

    @staticmethod
    def list_product_by_category(category):
        Utils.clear()
        print("[0] Kembali")

        # Print produk sesuai kategori.
        result = [product for product in product_list if product.category == category]

        for i, product in enumerate(result):
            print(
                f"[{i + 1}] {product.name} - {product.get_price_formatted()} - Stok: {product.get_stock()}"
            )

        return result

    @staticmethod
    def catalogue(current_user):
        while True:
            try:
                Utils.clear()
                current_user.get_shopping_cart_items()
                categories = Shop.print_categories()
                choice = input("Pilihan: ")

                if choice == "0":
                    break

                category = categories[int(choice) - 1]
            except (ValueError, IndexError):
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()
                continue

            while True:
                Utils.clear()
                products = Shop.list_product_by_category(category)

                choice = input("Pilihan: ")

                if choice == "0":
                    break

                Utils.clear()
                try:
                    product = products[int(choice) - 1]
                    while True:
                        print("Produk yang dipilih: ")
                        print(f"Nama: {product.name}")
                        print(f"Harga: {product.get_price_formatted()}")
                        print(f"Stok: {product.get_stock()}")
                        print()

                        amount = input("Jumlah: ")

                        if not amount.isdigit():
                            print("Jumlah harus angka.")
                            Utils.enter_and_continue()
                            continue

                        if product.get_stock() < int(amount):
                            print("Stok tidak cukup.")
                            Utils.enter_and_continue()
                            continue

                        if int(amount) <= 0:
                            print("Jumlah harus lebih dari 0.")
                            Utils.enter_and_continue()
                            continue

                        amount = int(amount)
                        break

                    current_user.add_to_shopping_cart(product, amount)

                    Utils.enter_and_continue()

                except (ValueError, IndexError):
                    print("Pilihan tidak valid.")
                    Utils.enter_and_continue()
                    continue

    @staticmethod
    def menu(current_user: User):
        while True:
            Utils.clear()
            print("Menu Toko")
            print("[0] Kembali")
            print("[1] Lihat Keranjang Belanja")
            print("[2] Hapus Item dari Keranjang Belanja")
            print("[3] Katalog Toko")
            if current_user.get_shopping_cart_total() > 0:
                print("[4] Checkout")

            choice = input("Pilihan: ")
            Utils.clear()

            if choice == "0":
                break
            elif choice == "1":
                current_user.get_shopping_cart_items(interactive=True)
            elif choice == "2":
                current_user.remove_from_shopping_cart()
            elif choice == "3":
                Shop.catalogue(current_user)
            elif choice == "4":
                # Validasi belanjaan harus lebih dari 0.
                if current_user.get_shopping_cart_total() == 0:
                    print("Keranjang belanja kosong.")
                    Utils.enter_and_continue()
                    continue

                current_user.checkout()
                print("Terima kasih telah berbelanja!")
                Utils.enter_and_continue()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()


# Antrean layanan yang menunggu.
class ServiceQueue:
    def __init__(self, user, service_type, pet_type=None, package=None, price=0):
        self.user = user
        self.service_type = service_type
        self.pet_type = pet_type
        self.package = package
        self.status = "Waiting"
        self.result = None
        self.price = price


queue = []


class Service:
    @staticmethod
    def check_health(current_user):
        item = ServiceQueue(current_user, "Check Health")
        queue.append(item)
        print("Anda telah ditambahkan ke antrean untuk pengecekan kesehatan.")
        print(f"Nomor antrean: {len(queue) + 1}")
        Utils.enter_and_continue()

    @staticmethod
    def pet_care(current_user):
        while True:
            Utils.clear()
            print("Menu Perawatan")
            print("[0] Kembali")
            print("[1] Anjing")
            print("[2] Kucing")

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice == "1":
                Service.care_package(
                    current_user,
                    "Anjing",
                )
            elif choice == "2":
                Service.care_package(current_user, "Kucing")
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def care_package(current_user, pet_type):
        price_dict = {
            "Anjing": {
                "Paket A (Lengkap)": 500000,
                "Paket B (Treatment)": 300000,
                "Paket C (Mandi)": 150000,
            },
            "Kucing": {
                "Paket A (Lengkap)": 400000,
                "Paket B (Treatment)": 250000,
                "Paket C (Mandi)": 100000,
            },
        }

        while True:
            Utils.clear()
            print(f"Paket Perawatan untuk {pet_type}")
            print("[0] Kembali")

            # Daftar harga berdasarkan jenis hewan
            for package, price in price_dict[pet_type].items():
                print(
                    f"[{list(price_dict[pet_type].keys()).index(package) + 1}] {package} - {Utils.format_rupiah(price)}"
                )

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice in [str(i) for i in range(1, len(price_dict[pet_type]) + 1)]:
                package = list(price_dict[pet_type].keys())[int(choice) - 1]
                price = price_dict[pet_type][package]

                item = ServiceQueue(current_user, "Pet Care", pet_type, package, price)
                queue.append(item)
                print(
                    f"Anda telah ditambahkan ke antrean untuk {package} perawatan {pet_type} dengan harga {Utils.format_rupiah(price)}."
                )
                Utils.enter_and_continue()
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()

    @staticmethod
    def view_service_status(current_user):
        user_queue_items = [item for item in queue if item.user == current_user]

        if not user_queue_items:
            print("Anda tidak memiliki layanan yang sedang diproses.")
            Utils.enter_and_continue()
            return

        print("Status Layanan Anda:")
        for item in user_queue_items:
            print(str(item))

        Utils.enter_and_continue()

    @staticmethod
    def menu(current_user):
        while True:
            Utils.clear()
            print("Menu Layanan")
            print("[0] Kembali")
            print("[1] Kesehatan")
            print("[2] Perawatan")
            print("[3] Lihat Status Layanan Anda")

            choice = input("Pilihan: ")

            if choice == "0":
                break
            elif choice == "1":
                Service.check_health(current_user)
            elif choice == "2":
                Service.pet_care(current_user)
            elif choice == "3":
                Service.view_service_status(current_user)
            else:
                print("Pilihan tidak valid.")
                Utils.enter_and_continue()


user_list: List[User] = []
# TODO: pisah product sama hewan.
product_list: List[Product] = []

Product.load_from_file()
User.load_from_file()

while True:
    print("Selamat datang di Pet Shop!")
    print("[0] Keluar dari aplikasi")
    print("[1] Login")
    print("[2] Daftar")
    print("[3] Lupa Password")

    choice = input("Pilihan: ")
    Utils.clear()

    if choice == "0":
        break
    elif choice == "1":
        current_user = User.login()
        if current_user is None:
            continue

        if current_user.role == "admin":
            Admin.menu(current_user)
        elif current_user.role == "doctor":
            Doctor.menu(current_user)
        else:
            User.menu(current_user)

    elif choice == "2":
        User.create_user()

    elif choice == "3":
        User.forgot_password()
    else:
        print()
        print("Pilihan tidak valid.")
        Utils.enter_and_continue()
    Utils.clear()
