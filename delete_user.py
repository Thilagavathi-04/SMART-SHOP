import sqlite3

conn = sqlite3.connect("shop.db")
cursor = conn.cursor()

username = input("Enter the username to delete: ").strip()

cursor.execute("DELETE FROM users WHERE username = ?", (username,))
conn.commit()

if cursor.rowcount > 0:
    print(f"✅ User '{username}' deleted successfully.")
else:
    print(f"❌ User '{username}' not found.")

conn.close()