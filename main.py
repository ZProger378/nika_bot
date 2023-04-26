import json
from config import bot
import fuzz_methods
from fuzz_methods import is_message_to_bot


# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}")


@bot.message_handler(chat_types=["group", "supergroup"])
def main_handler(message):
    text = message.text.lower()  # Преобразуем текст в lowercase
    if is_message_to_bot(text):  # Если обращаются к боту
        answers = fuzz_methods.get_reply_text(text)  # Получаю ответ на команды
        # Отправка сообщений
        for i, answer in enumerate(answers):
            if not i:
                bot.reply_to(message, answer)
            else:
                bot.send_message(message.chat.id, answer)


if __name__ == "__main__":
    # Запуск бота методом .polling()
    print("[i] Bot is started...")
    bot.polling(none_stop=True, interval=0)
