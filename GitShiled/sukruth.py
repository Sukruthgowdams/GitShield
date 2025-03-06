import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

username = input("Enter username: ")
query = f"SELECT * FROM users WHERE username = '{username}'"  # 🚨 Vulnerable to SQL Injection
cursor.execute(query)
