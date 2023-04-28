from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from database import TTToe


def main_markup(game_id):
    markup = InlineKeyboardMarkup(row_width=3)
    btns = []
    game = TTToe(game_id)
    btn_id = 0
    for i in range(3):
        for x in range(3):
            symbol = "⬜️"
            btn_id += 1
            if game.map[btn_id-1] == "1":
                symbol = "❌"
            elif game.map[btn_id-1] == "2":
                symbol = "⭕️"
            btns.append(InlineKeyboardButton(
                symbol, callback_data=f"tictactoe_{game.id}_{btn_id}"
            ))
    markup.add(btns[0], btns[1], btns[2],
               btns[3], btns[4], btns[5],
               btns[6], btns[7], btns[8])

    return markup
