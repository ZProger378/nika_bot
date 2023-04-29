import json
import fuzz_methods
from config import bot
from random import randint
from database import User, TTToe
from TicTacToe.markups import main_markup as tttoe_markup
from fuzz_methods import is_message_to_bot


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    message = call.message
    data = call.data
    if data.startswith("tictactoe_"):  # При нажатии на поле игры
        # Получение ID игры и нажатого поля
        game_id = int(data.split("_")[1])
        btn_id = int(data.split("_")[-1])
        game = TTToe(game_id)  # Получение данных об игре
        # Если игрок ходит своей очередью
        if (game.player_one == call.from_user.id and game.step == 1) or (
                game.player_two == call.from_user.id and game.step == 2) and game.winner == 0:
            _map = game.map
            new_map = ""
            # Обновление очереди
            if game.step == 1:
                new_step = 2
            else:
                new_step = 1
            # Обновление карты
            for i, char in enumerate(_map):
                if i == btn_id - 1:
                    if char == "0":
                        if game.player_one == call.from_user.id:
                            new_map += "1"
                        elif game.player_two == call.from_user.id:
                            new_map += "2"
                    else:
                        new_map += char
                else:
                    new_map += char

            # Применение изменений
            game.edit_map(new_map)
            game.edit_step(new_step)

            # Перезапись полей в формат {X;Y}
            map_dic = {}
            btn_id = 0
            for y in range(3):
                for x in range(3):
                    map_dic[f"{x+1}{y+1}"] = game.map[btn_id]
                    btn_id += 1
            # Получение позиций занятых определённым игроком
            player_one_pos = []
            player_two_pos = []
            for xy in map_dic.keys():
                if map_dic[xy] == "1":
                    player_one_pos.append(xy)
                elif map_dic[xy] == "2":
                    player_two_pos.append(xy)
            # Все возможные позиция для выйгрыша
            winner_positions = [
                ["11", "12", "13"],
                ["21", "22", "23"],
                ["31", "32", "33"],
                ["11", "21", "31"],
                ["12", "22", "32"],
                ["13", "23", "33"],
                ["11", "22", "33"],
                ["31", "22", "13"]
            ]
            winner = 0
            for pos in winner_positions:  # Перебор выйгрышных позиций и проверка на их присутствие
                if pos[0] in player_one_pos and pos[1] in player_one_pos and pos[2] in player_one_pos:
                    winner = 1  # Побеждает 1 игрок
                    break
                elif pos[0] in player_two_pos and pos[1] in player_two_pos and pos[2] in player_two_pos:
                    winner = 2  # Побеждает 2 игрок
                    break

            if winner == 0:  # Если никто не победил = игра продолжнается
                user = User([game.player_one, game.player_two][new_step - 1])
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                      text=f"Ход @{user.username}",
                                      reply_markup=tttoe_markup(game.id))
            else:  # Иначе = конец игры
                game.edit_winner(winner)
                user = User([game.player_one, game.player_two][winner - 1])
                bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                                      text=f"@{user.username} - победил!",
                                      reply_markup=tttoe_markup(game.id))
        elif game.winner != 0:  # Если игра окончена = удаление сообщения
            bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}")


@bot.message_handler(chat_types=["group", "supergroup"])
def main_handler(message):
    text = message.text.lower()  # Преобразуем текст в lowercase
    user = User(message.from_user.id)  # Получаю объект "пользователь"
    if not user.is_exist():  # Если пользователь не существует
        user.create(username=message.from_user.username.lower())  # Добавление пользователя в базу данных

    # Если обращаются к боту
    if is_message_to_bot(text) or message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id:
        answers = fuzz_methods.get_reply_text(text)  # Получаю ответ на команды
        # Отправка сообщений
        for i, answer in enumerate(answers):
            if not answer.startswith("!"):  # Если сообщение - не команда
                if not i:
                    bot.reply_to(message, answer)
                else:
                    bot.send_message(message.chat.id, answer)
            else:
                if answer == "!tictactoe":  # Запуск игры в крестики-нолики
                    # Получение имени 2-го игрока
                    username = None
                    for word in text.split(" "):
                        if word.startswith("@"):
                            username = word.split("@")[-1]
                    if username is not None:  # Если имя 2-го игрока найдено = запуск игры
                        user = User(username=username)
                        # Запуск игры и вывод пустого поля
                        game = TTToe(randint(100000, 9999999))
                        game.create(message.from_user.id, user.id)
                        bot.send_message(message.chat.id, f"Ход @{message.from_user.username}",
                                         reply_markup=tttoe_markup(game.id))
                    else:  # Если имя пользователя не получено
                        bot.reply_to(message, f"Напиши ник, с кем хочешь играть (Типо: @Name)")
                    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


if __name__ == "__main__":
    # Запуск бота методом .polling()
    print("[i] Bot is started...")
    bot.polling(none_stop=True, interval=0)
