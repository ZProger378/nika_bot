import json
import time
from datetime import datetime

from telebot import TeleBot
import wikipedia

# BOT SETTINGS
setting = json.load(open("settings.json", "rb"))
print("[i] Settings has been loaded!")
bot_token = setting['token']
creater = setting['creater']
bot = TeleBot(bot_token, parse_mode="html")
bot_name = bot.get_me().username


# DATETIME FUNCTIONS
def tconv(date):
    date_str = time.strftime("%H:%M:%S %d.%m.%Y", time.localtime(date))
    dt = datetime.strptime(date_str, "%H:%M:%S %d.%m.%Y")

    return dt
