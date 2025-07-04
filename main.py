from db import init_db
from user import Admin, Customer
from utils import hash_password, get_secure_password
from db import cursor

init_db()

def register():
    username = input("New Username: ").lower()
    password = get_secure_password()
    role = input("Role (admin/user): ").lower()
    try:
        cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                       (username, hash_password(password), role))
        from db import conn
        conn.commit()
        print("Registered successfully.")
    except:
        print("Username already exists!")

def login():
    username = input("Username: ").lower()
    password = get_secure_password()
    cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", 
                   (username, hash_password(password)))
    result = cursor.fetchone()
    if result:
        role = result[0]
        if role == "admin":
            Admin(username).menu()
        else:
            Customer(username).menu()
    else:
        print("Login failed.")

def main():
    while True:
        print("\n--- SmartShop Console ---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == '1':
            register()
        elif choice == '2':
            login()
        elif choice == '3':
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()