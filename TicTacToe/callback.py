from database import TTToe, User
from TicTacToe.markups import main_markup as tttoe_markup


# Основной обработчик
def tttoe_callback(call, bot):
    data = call.data
    message = call.message
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
