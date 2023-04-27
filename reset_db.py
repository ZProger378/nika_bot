import sqlite3


with open("main_db.db", "w") as f:
    f.write("")

con = sqlite3.connect("main_db.db")
cur = con.cursor()
cur.execute("CREATE TABLE users ("
            "user_id INT, username VARCHAR(64), "
            "rep INT, alias VARCHAR(64)"
            ")"
)
