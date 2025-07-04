import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

cursor.execute("SELECT username FROM users")
users = cursor.fetchall()

print("📋 Registered users:")
for user in users:
    print(f" - {user[0]}")

conn.close()