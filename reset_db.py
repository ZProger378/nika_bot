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
cur.execute("CREATE TABLE tttoe ("
            "id INT, player_one INT, player_two INT, step INT, map VARCHAR(9), winner INT"
            ")"
)
cur.execute("CREATE TABLE messages ("
            "id INT, user_id INT, text VARCHAR(4096), "
            "date DATETIME DEFAULT CURRENT_TIMESTAMP"
            ")"
)
