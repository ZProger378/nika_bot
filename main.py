from config import bot


# обработчик команды /start
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.first_name}")


if __name__ == "__main__":
    # запуск бота методом .polling()
    bot.polling(none_stop=True, interval=0)
