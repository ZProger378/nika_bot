import json
import fuzz_methods
from config import bot
from database import User
from fuzz_methods import is_message_to_bot


# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}")


@bot.message_handler(chat_types=["group", "supergroup"])
def main_handler(message):
    text = message.text.lower()  # Преобразуем текст в lowercase
    user = User(message.chat.id)  # Получаю объект "пользователь"
    if not user.is_exist():  # Если пользователь не существует
        user.create(username=message.from_user.username)  # Добавление пользователя в базу данных

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
                        from TicTacToe.markups import main_markup
                        user = User(username=message.from_user.username)
                        # Запуск игры и вывод пустого поля
                        bot.send_message(message.chat.id, f"Запускаю игру...",
                                         reply_markup=main_markup(message.chat.id, user.id, map_list={}))
                    else:  # Если имя пользователя не получено
                        bot.reply_to(message, f"Напиши ник, с кем хочешь играть (Типо: @Name)")


if __name__ == "__main__":
    # Запуск бота методом .polling()
    print("[i] Bot is started...")
    bot.polling(none_stop=True, interval=0)
