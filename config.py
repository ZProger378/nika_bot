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
