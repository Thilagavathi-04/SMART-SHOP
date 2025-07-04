from abc import ABC, abstractmethod
from db import cursor, conn
from utils import hash_password

class User(ABC):  # ✅ Abstraction
    def __init__(self, username):
        self._username = username

    @abstractmethod
    def menu(self):  # ✅ Polymorphism
        pass

class Admin(User):  # ✅ Inheritance
    def menu(self):
        while True:
            print(f"\nAdmin Menu ({self._username}):")
            print("1. Add Product")
            print("2. View Products")
            print("3. Delete Product")
            print("4. Logout")
            choice = input("Choose: ")

            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.view_products()
            elif choice == '3':
                self.delete_product()
            elif choice == '4':
                break

    def add_product(self):
        name = input("Product name: ")
        price = float(input("Price: "))
        stock = int(input("Stock: "))
        cursor.execute("INSERT INTO products (name, price, stock) VALUES (?, ?, ?)", (name, price, stock))
        conn.commit()
        print("Product added.")

    def view_products(self):
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            print(row)

    def delete_product(self):
        pid = input("Product ID to delete: ")
        cursor.execute("DELETE FROM products WHERE id = ?", (pid,))
        conn.commit()
        print("Product deleted.")

class Customer(User):  # ✅ Inheritance
    def __init__(self, username):
        super().__init__(username)
        self.__cart = []  # ✅ Encapsulation

    def menu(self):  # ✅ Polymorphism
        while True:
            print(f"\nCustomer Menu ({self._username}):")
            print("1. View Products")
            print("2. Add to Cart")
            print("3. View Cart")
            print("4. Checkout")
            print("5. Logout")
            choice = input("Choose: ")

            if choice == '1':
                self.view_products()
            elif choice == '2':
                self.add_to_cart()
            elif choice == '3':
                self.view_cart()
            elif choice == '4':
                self.checkout()
            elif choice == '5':
                break

    def view_products(self):
        cursor.execute("SELECT * FROM products")
        for row in cursor.fetchall():
            print(row)

    def add_to_cart(self):
        pid = int(input("Enter Product ID: "))
        qty = int(input("Quantity: "))
        self.__cart.append((pid, qty))
        print("Added to cart.")

    def view_cart(self):
        print("Your Cart:")
        for item in self.__cart:
            pid, qty = item
            cursor.execute("SELECT name, price FROM products WHERE id = ?", (pid,))
            prod = cursor.fetchone()
            if prod:
                print(f"{prod[0]} x{qty} = {prod[1]*qty:.2f}")

    def checkout(self):
        total = 0
        for item in self.__cart:
            pid, qty = item
            cursor.execute("SELECT price, stock FROM products WHERE id = ?", (pid,))
            data = cursor.fetchone()
            if data and data[1] >= qty:
                total += data[0] * qty
                cursor.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (qty, pid))
            else:
                print(f"Not enough stock for product ID {pid}")
                return
        cursor.execute("SELECT id FROM users WHERE username = ?", (self._username,))
        uid = cursor.fetchone()[0]
        cursor.execute("INSERT INTO orders (user_id, total_price) VALUES (?, ?)", (uid, total))
        conn.commit()
        self.__cart.clear()
        print(f"Order placed! Total: ₹{total:.2f}")