import json
from random import choice
from fuzzywuzzy import fuzz
from fuzzywuzzy.process import extractOne, dedupe


def ratio(text, identity):
    # Получаю результаты нечёткого сравнения числом от 1 до 100
    # a = fuzz.WRatio(text, identity)
    # b = fuzz.token_sort_ratio(text, identity)
    # if text in identity:
    #     c = 100
    # else:
    #     c = 0
    # Получаю среднее арифметическое с 2 результатов
    # res = round((a + b + c) / 3)
    a = extractOne(identity, text)[1]
    b = fuzz.WRatio(text, identity)
    с = fuzz.token_set_ratio(text, identity)
    res = round((a + b + с) / 3)

    return res  # Возвращаю результат


def get_reply_text(text):
    model = json.load(open("model.json", "rb"))  # Загружаю модель диалога
    var = model['var']  # Загрузка локальных переменных
    dialog = model['dialog'].keys()  # Получаю все пока изученные вопросы
    comparisons = []  # Инициализация списка сходств
    extra_chars = "!@#$%^&*()\"'/\\.,?_-=+`"  # "Лишние" символы, которые не стоит считать
    for char in extra_chars: text = text.replace(char, "")  # Очистка текста от "лишних" символов
    # Сравниваю текст, полученный от пользователя со всеми изученными вопросами
    for rep in dialog:
        reps = rep.split("/")
        for rp in reps:
            res = ratio(text.lower(), rp)
            comparisons.append([rep, res])
    # Нахожу наибольшее совпадение
    questions = [["!notunderstandme", 100]]
    for comparison in comparisons:
        if comparison[1] >= 70:  # Если совпадение более 70%
            if questions[0][0] == "!notunderstandme":
                questions = [comparison]
            else:
                questions.append(comparison)
    # Получаю все возможные ответы на вопрос
    replys = []
    results = []
    # Получение текста вопросов
    qs = []
    for question in questions:
        if question[0] not in qs:
            qs.append(question[0])
    # Получение ответов
    for question in qs:
        replys.append(model['dialog'][question])
    # Сборка всех ответов
    for reply in replys:
        reply = choice(reply)  # Получение случайного ответа на вопрос
        # Замена имен переменных на их значение из словаря var{}
        # Пример: "{name}" -> "Неко"
        for key in var.keys():
            reply = reply.replace("{" + key + "}", var[key])
        # Добавление в список ответов
        results.append(reply)

    return list(dedupe(results))  # Возвращаю ответы


while True:
    replys = get_reply_text(input("[ME] "))
    for reply in replys:
        print("[NEKO] " + reply)
