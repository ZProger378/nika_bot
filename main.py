###################################
# Импортирование ебучих библиотек #
###################################

import json
import wiki
import config
import fuzz_methods
from config import bot
from random import randint
from database import User, TTToe
from fuzz_methods import is_message_to_bot
from TicTacToe.markups import main_markup as tttoe_markup


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    # Сокращение названий переменных для удобства
    message = call.message
    data = call.data
    if data.startswith("tictactoe_"):  # При нажатии на поле игры
        # Получение ID игры и нажатого поля
        game_id = int(data.split("_")[1])
        btn_id = int(data.split("_")[-1])
        game = TTToe(game_id)  # Получение данных об игре
        if not int(game.map[btn_id - 1]):
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

                # Получение позиций занятых определённым игроком
                player_one_pos = []
                player_two_pos = []
                for btn_id, i in enumerate(game.map):
                    if i == "1":
                        player_one_pos.append(btn_id + 1)
                    elif i == "2":
                        player_two_pos.append(btn_id + 1)

                # Все возможные позиция для выйгрыша
                winner_positions = [
                    [1, 4, 7], [2, 5, 8],
                    [3, 6, 9], [1, 2, 3],
                    [4, 5, 6], [7, 8, 9],
                    [1, 5, 9], [3, 5, 7]
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


# Обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}")


@bot.message_handler(chat_types=["group", "supergroup"])
def main_handler(message):
    #######################
    # Основной обработчик #
    #######################

    text = message.text.lower()  # Преобразуем текст в lowercase
    user = User(message.from_user.id)  # Получаю объект "пользователь"
    if not user.is_exist():  # Если пользователь не существует
        user.create(username=message.from_user.username.lower())  # Добавление пользователя в базу данных

    if message.reply_to_message and message.reply_to_message.from_user.id not in [message.from_user.id,
                                                                                  bot.get_me().id]:
        answers = fuzz_methods.get_reply_text(text)
        if "!rep" in answers or text.startswith("+"):  # Если выявлено повышение репутации члену группы
            user_id = message.reply_to_message.from_user.id  # Получение ID члена группы
            username = bot.get_chat_member(chat_id=message.chat.id, user_id=user_id).user.username  # Получение username
            user = User(user_id)
            if not user.is_exist():
                user.create(username)
            user.addrep()  # Добавление к репутации
            bot.reply_to(message, f"Уважение оказано @{username} (+1 к репутации)")
        elif "!new_alias" in answers:
            user_id = message.reply_to_message.from_user.id  # Получение ID члена группы
            username = bot.get_chat_member(chat_id=message.chat.id, user_id=user_id).user.username  # Получение username
            user = User(user_id)
            alias = ""
            alias_start = text.find('"')
            alias_end = text.find('"', alias_start + 1)
            if alias_start != -1:
                for i in range(alias_start + 1, alias_end):
                    alias += text[i]
                user.new_alias(alias)
                bot.reply_to(message, f"<b>Новая кличка</b> \"<i>{alias}</i>\" для @{username}")
            else:
                bot.reply_to(message, f"Если хочешь дать кличку человеку, "
                                      f"ты должен ответить на его сообщение "
                                      f"\"Кличка\" и в ковычках указать кличку\n\n"
                                      f"<code><i>Кличка \"новая кличка\"</i></code>")

    # Если обращаются к боту
    if is_message_to_bot(text) or message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id:
        if is_message_to_bot(text):
            text_list = text.split(" ")
            text_list[0] = ""
            text = " ".join(text_list)
        text = text.strip()
        answers = fuzz_methods.get_reply_text(text)  # Получаю ответ на команды
        # Отправка сообщений
        for i, answer in enumerate(answers):
            if not answer.startswith("!"):  # Если сообщение - не команда
                if not i:
                    if i in ["Я не знаю, что на это ответить(", "Я не совсем тебя понимаю",
                             "Я не поняла, что вы хотели сказать \uD83D\uDE44", "?"]:
                        pass
                    bot.reply_to(message, answer)
                else:
                    bot.send_message(message.chat.id, answer)
            else:
                #####################
                # Обработчик команд #
                #####################

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
                elif answer == "!userinfo":  # Получение информации о себе
                    user = User(message.from_user.id)
                    bot.reply_to(message, f"<b>Информация о тебе</b>\n\n"
                                          f"👤 USERNAME: @{user.username}\n"
                                          f"🤖 ID: <code>{user.id}</code>\n"
                                          f"😎 Репутация: <b>{user.rep}</b>\n"
                                          f"✏️ Кличка: <i>{str(user.alias).replace('None', 'Нет')}</>"
                                 .replace("@None", "Нет"))
                elif answer == "!wikisearch":  # Поиск по WikiPedia
                    # Нахожу ключевые слова
                    key_words = [text.find("когда"), text.find("что"), text.find("кто")]

                    prompt = ""  # Запрос
                    result = []  # Результат

                    # Составляю запрос на основе ключевых слов
                    if sum(key_words) != -3:
                        for question in key_words:
                            if question != -1:  # Если ключевое слово найдено
                                # Составляю запрос
                                for x in range(question, len(text)):
                                    prompt += text[x]
                                # Делаю запрос в википедию
                                result = wiki.search(prompt)
                                if result is not None:  # Если страница найдена
                                    # Вывожу результат поиска в чат
                                    bot.reply_to(message, f"По запросу \"<i>{prompt}</i>\":")
                                    # Перебор и вывод результата
                                    for x, message_text in enumerate(result):
                                        bot.send_message(message.chat.id, f"<b>{message_text}</b>")
                                    bot.send_message(message.chat.id, f"<i>Источник: <b>WikiPedia</b></i>")

                                    # Выход из цикла
                                    break
                                prompt = ""  # Очистка запроса

                    # Если не получилось составить запрос
                    if not result or sum(key_words) == -3:
                        prompt = text  # Запросом будет являться всё сообщение
                        result = wiki.search(prompt)  # Запрос в википедию
                        if result is not None:  # Если результат не равен None
                            # Вывожу результат поиска в чат
                            bot.reply_to(message, f"По запросу \"<i>{prompt}</i>\":")
                            # Перебор и вывод результата
                            for x, message_text in enumerate(result):
                                bot.send_message(message.chat.id, f"<b>{message_text}</b>")
                            bot.send_message(message.chat.id, f"<i>Источник: <b>WikiPedia</b></i>")
                            break  # Выход из цикла
                    if not result:  # Если ничего не нашёл
                        bot.reply_to(message, f"По запросу \"<i>{prompt}</i>\" я ничего не нашла(")


if __name__ == "__main__":
    # Запуск бота методом .polling()
    print("[i] Bot is started...")
    bot.polling(none_stop=True, interval=0)
