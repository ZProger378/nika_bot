from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_markup(player_one, player_two, map_list):
    markup = InlineKeyboardMarkup(row_width=3)
    btns = []
    if map_list == {}:
        map_list = {
            "1_1": "empty", "2_1": "empty", "3_1": "empty",
            "1_2": "empty", "2_2": "empty", "3_2": "empty",
            "1_3": "empty", "2_3": "empty", "3_3": "empty"
        }
    for i in range(3):
        for x in range(3):
            symbol = "⬜️"
            if map_list[f"{x}_{i}"] == "tic":
                symbol = "❌"
            elif map_list[f"{x}_{i}"] == "tac":
                symbol = "⭕️"
            btns.append(InlineKeyboardButton(
                symbol, callback_data=f"tictactoe_{x}_{i}_{map_list[f'{x}_{i}']}_{player_one}_{player_two}"
            ))
    markup.add(btns[0], btns[1], btns[2],
               btns[3], btns[4], btns[5],
               btns[6], btns[7], btns[8])

    return markup
