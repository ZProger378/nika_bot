import sqlite3


# Инициализация класса "пользователь"
class User:
    def __init__(self, user_id=None, username=None):  # Получение пользователя с базы данных
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        # Получаю "сырые" данные...
        if username is None:
            cur.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        else:
            cur.execute("SELECT * FROM users WHERE username = ?", (username,))
        unsorted = cur.fetchone()
        self.id = user_id

        if unsorted:  # Если пользователь есть в базе
            self.id = unsorted[0]
            self.username = unsorted[1]
            self.rep = unsorted[2]
            self.alias = unsorted[3]

    def create(self, username):  # Сохранение пользователя в бд
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        cur.execute("INSERT INTO users (user_id, username, rep) "
                    "VALUES (?, ?, ?)", (self.id, username, 0))
        con.commit()

        # Инициализация полей объекта
        self.username = username
        self.rep = 0
        self.alias = None

    # Метод для внесения правок в бд
    def edit(self, column, new_value):
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        cur.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (new_value, self.id))
        con.commit()

    # Метод для проверки на существование пользователя в бд
    # Возвращает 2 значения (True или False)
    def is_exist(self):
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        cur.execute("SELECT user_id FROM users WHERE user_id = ?", (self.id,))
        if cur.fetchone() is not None:
            return True
        else:
            return False
