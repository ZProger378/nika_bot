import json
from random import choice
from fuzzywuzzy import fuzz


def ratio(text, identity):
    # Получаю результаты нечёткого сравнения числом от 1 до 100
    a = fuzz.WRatio(text, identity)
    b = fuzz.token_sort_ratio(text, identity)
    if text in identity:
        c = 100
    else:
        c = 0
    # Получаю среднее арифметическое с 2 результатов
    res = round((a + b + c) / 3)

    return res  # Возвращаю результат


def get_reply_text(text):
    model = json.load(open("model.json", "rb"))  # Загружаю модель диалога
    dialog = model['dialog'].keys()  # Получаю все пока изученные вопросы
    comparisons = []
    extra_chars = "!@#$%^&*()\"'/\\.,?_-=+`"  # "Лишние" символы, которые не стоит считать
    for char in extra_chars: text = text.replace(char, "")  # Очистка текста от "лишних" символов
    # Сравниваю текст, полученный от пользователя со всеми изученными вопросами
    for rep in dialog:
        reps = rep.split("/")
        for rp in reps:
            res = ratio(text.lower(), rp)
            comparisons.append([rep, res])
    # Нахожу наибольшее совпадение
    question = ["!notunderstandme", 100]
    for comparison in comparisons:
        if comparison[1] >= 50:
            if question == ["!notunderstandme", 100]:
                question = comparison
            else:
                if comparison[1] > question[1]:
                    question = comparison
    # Получаю все возможные ответы на вопрос
    reply = model['dialog'][question[0]]

    return choice(reply)  # Возвращаю случайный ответ


while True:
    print("[NEKO] " + get_reply_text(input("[ME] ")))
