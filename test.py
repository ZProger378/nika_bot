import sqlite3
from database import User


user = User(123)
if not user.is_exist():
    user = user.create(123, "ZProger")
print(user.username)

con = sqlite3.connect("main_db.db")
cur = con.cursor()
cur.execute("SELECT * FROM users")

print(cur.fetchall())

user = User(123)

print(user.username)
