import wikipedia

wikipedia.set_lang("ru")  # Настройка языка


# Код функции скопирован с форума, и я в душе не ебу, что он делает
def grouper(iterable, n):
    args = [iter(iterable)] * n
    return zip(*args)


def search(prompt, sentences=0):
    try:
        # Запрос в википедию
        res = wikipedia.summary(prompt, sentences=sentences)
    except wikipedia.exceptions.PageError:  # Если страница не найдена
        # Возвращаю Нон
        return None
    else:  # Иначе = возвращаю результат поиска
        # Ограничиваю объём сообщения 4096 символами, чтобы api телеграмма мне по шапке не надавало
        result = [res[x:x + 4096] for x in range(0, len(res), 4096)]
        return result
