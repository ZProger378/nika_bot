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

    # Метод для добавления репутации
    def addrep(self):
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        cur.execute("UPDATE users SET rep = rep + 1 WHERE user_id = ?", (self.id,))
        con.commit()

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


# Инициализация класса с данными о партии в крестики-нолики
class TTToe:
    def __init__(self, game_id):  # Получение игры с базы данных
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM tttoe WHERE id = ?", (game_id,))
        unsorted = cur.fetchone()
        self.id = game_id
        if unsorted is not None:
            self.player_one = unsorted[1]
            self.player_two = unsorted[2]
            self.step = unsorted[3]
            self.map = unsorted[4]
            self.winner = unsorted[5]

    def create(self, player_one, player_two):
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        cur.execute("INSERT INTO tttoe (id, player_one, player_two, map, winner, step) "
                    "VALUES (?, ?, ?, ?, ?, ?)", (self.id, player_one, player_two, "000000000", 0, 1))
        con.commit()

        self.player_one = player_one
        self.player_two = player_two
        self.step = 1
        self.map = "000000000"
        self.winner = 0

    def edit_map(self, new_map):
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        cur.execute("UPDATE tttoe SET map = ? WHERE id = ?", (new_map, self.id))
        con.commit()

        self.map = new_map

    def edit_step(self, new_step):
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        cur.execute("UPDATE tttoe SET step = ? WHERE id = ?", (new_step, self.id))
        con.commit()

        self.step = new_step

    def edit_winner(self, winner):
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        cur.execute("UPDATE tttoe SET winner = ? WHERE id = ?", (winner, self.id))
        con.commit()

        self.winner = winner

    def is_exist(self):
        con = sqlite3.connect("main_db.db")
        cur = con.cursor()
        cur.execute("SELECT * FROM tttoe WHERE id = ?", (self.id,))

        if cur.fetchone():
            return True
        else:
            return False
