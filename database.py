import sqlite3
import time


# функция для получения экземпляров connect и cursor
def connect_db():
    con = sqlite3.connect("main_db.db")
    cur = con.cursor()

    return con, cur


# Инициализация класса "пользователь"
class User:
    def __init__(self, user_id=None, username=None):  # Получение пользователя с базы данных
        con, cur = connect_db()
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
        con, cur = connect_db()
        cur.execute("INSERT INTO users (user_id, username, rep) "
                    "VALUES (?, ?, ?)", (self.id, username, 0))
        con.commit()

        # Инициализация полей объекта
        self.username = username
        self.rep = 0
        self.alias = None

    # Метод для добавления репутации
    def addrep(self):
        con, cur = connect_db()
        cur.execute("UPDATE users SET rep = rep + 1 WHERE user_id = ?", (self.id,))
        con.commit()

    # Метод для получения клички
    def new_alias(self, alias):
        con, cur = connect_db()
        cur.execute("UPDATE users SET alias = ? WHERE user_id = ?", (alias, self.id))
        con.commit()

    # Метод для внесения правок в бд
    def edit(self, column, new_value):
        con, cur = connect_db()
        cur.execute(f"UPDATE users SET {column} = ? WHERE user_id = ?", (new_value, self.id))
        con.commit()

    # Метод для проверки на существование пользователя в бд
    # Возвращает 2 значения (True или False)
    def is_exist(self):
        con, cur = connect_db()
        cur.execute("SELECT user_id FROM users WHERE user_id = ?", (self.id,))
        if cur.fetchone() is not None:
            return True
        else:
            return False


# Класс "Сообщение"
class Message:
    # Инициализация полей объекта класса
    def __init__(self, message=None, message_id=None, user_id=None, text=None, date=None):
        if message is None:  # Если объект сообщения не был передан в конструктор класса
            self.id = message_id
            self.user_id = user_id
            self.text = text
            self.date = date
        else:  # Иначе
            self.id = message.message_id
            self.user_id = message.from_user.id
            self.text = message.text
            self.date = message.date

    # Сохранение сообщения в бд
    def write_db(self):
        con, cur = connect_db()
        cur.execute("INSERT INTO messages (id, user_id, text) VALUES (?, ?, ?)",
                    (self.id, self.user_id, self.text))
        con.commit()


class Messages:
    # Получение всех сообшений
    def __init__(self):
        con, cur = connect_db()
        cur.execute("SELECT * FROM messages")
        unsorted = cur.fetchall()
        # Инициализация полей
        self.count = len(unsorted)
        self.messages = []
        # Получение сообщений
        for i in unsorted:
            self.messages.append(Message(message_id=i[0], user_id=i[1], text=i[2], date=i[3]))

    # Фильтр по ID пользователя
    def filter_by_id(self, user_id):
        result = []  # Список результатов
        # Перебор сообщений и проверка на ID
        for message in self.messages:
            if message.user_id == user_id:
                result.append(message)
        self.count = len(result)  # Количество сообщений

        return result  # Возвращение результата


# Инициализация класса с данными о партии в крестики-нолики
class TTToe:
    def __init__(self, game_id):  # Получение игры с базы данных
        con, cur = connect_db()
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
        con, cur = connect_db()
        cur.execute("INSERT INTO tttoe (id, player_one, player_two, map, winner, step) "
                    "VALUES (?, ?, ?, ?, ?, ?)", (self.id, player_one, player_two, "000000000", 0, 1))
        con.commit()

        self.player_one = player_one
        self.player_two = player_two
        self.step = 1
        self.map = "000000000"
        self.winner = 0

    def edit_map(self, new_map):
        con, cur = connect_db()
        cur.execute("UPDATE tttoe SET map = ? WHERE id = ?", (new_map, self.id))
        con.commit()

        self.map = new_map

    def edit_step(self, new_step):
        con, cur = connect_db()
        cur.execute("UPDATE tttoe SET step = ? WHERE id = ?", (new_step, self.id))
        con.commit()

        self.step = new_step

    def edit_winner(self, winner):
        con, cur = connect_db()
        cur.execute("UPDATE tttoe SET winner = ? WHERE id = ?", (winner, self.id))
        con.commit()

        self.winner = winner

    def is_exist(self):
        con, cur = connect_db()
        cur.execute("SELECT * FROM tttoe WHERE id = ?", (self.id,))

        if cur.fetchone():
            return True
        else:
            return False
