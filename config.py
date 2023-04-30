import json
from telebot import TeleBot
import wikipedia

# BOT SETTINGS
setting = json.load(open("settings.json", "rb"))
print("[i] Settings has been loaded!")
bot_token = setting['token']
creater = setting['creater']
bot = TeleBot(bot_token, parse_mode="html")
bot_name = bot.get_me().username

# WIKIPEDIA SETTINGS
wikipedia.set_lang("ru")


def search(prompt, sentences):
    try:
        result = wikipedia.summary(prompt, sentences=sentences)
    except wikipedia.exceptions.PageError:
        return None
    else:
        return result
