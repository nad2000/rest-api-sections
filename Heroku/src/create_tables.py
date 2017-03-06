import sqlite3

connection = sqlite3.connect("data.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username text UNIQUE,
        password text)
""")
connection.commit()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE, 
        price FLOAT)
""")
connection.commit()

cursor.execute("DELETE FROM users")
connection.commit()

users = [(0, "bob", "asdf"), (1, "jose", "asdf"), (2, "rolf", "asdf"), (3, "anne", "asdf")]
cursor.executemany("INSERT INTO users VALUES (?, ?, ?)", users)
connection.commit()

connection.close()
