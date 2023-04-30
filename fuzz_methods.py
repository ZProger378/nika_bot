import json
from random import choice
from fuzzywuzzy import fuzz
from fuzzywuzzy.process import extractOne, dedupe


# Функция для проверки на то, обращается ли пользователь к боту
def is_message_to_bot(message_text):
    # Загрузка всех возможных кличек бота
    model = json.load(open("model.json", "rb"))
    names = model['name']
    # Перебор кличек и проверка
    for name in names:
        if message_text.startswith(name):  # Пользователь обращается к боту
            return True
    else:
        return False  # Пользователь не обращается к боту


def ratio(text, identity):
    # Получаю результаты нечёткого сравнения числом от 1 до 100
    a = extractOne(identity, text)[1]
    b = fuzz.WRatio(text, identity)
    c = fuzz.token_set_ratio(text, identity)
    # Получаю среднее арифметическое с3 2 результатов
    res = round((2 * a + b + c) / 4)

    return res  # Возвращаю результат


def get_reply_text(text):
    ######################
    # Загрузка настрокек #
    ######################

    model = json.load(open("model.json", "rb"))  # Загружаю модель диалога
    var = model['var']  # Загрузка локальных переменных
    names = model['name']  # Загрузка кличек бота
    dialog = model['dialog'].keys()  # Получаю все пока изученные вопросы
    comparisons = []  # Инициализация списка сходств
    extra_chars = "!@#$%^&*()\"'/\\.,?_=`"  # "Лишние" символы, которые не стоит считать

    #####################
    # Очистка сообщения #
    #####################
    text = text.strip()  # Очистка от "лишних" пробелов
    for char in extra_chars: text = text.replace(char, "")  # Очистка текста от "лишних" символов

    ####################################################
    # Нечёткое сравнение текста с изученными вопросами #
    ####################################################

    # Сравниваю текст, полученный от пользователя со всеми изученными вопросами
    for rep in dialog:
        reps = rep.split("/")
        for rp in reps:
            res = ratio(text.lower(), rp)
            comparisons.append([rep, res])
    # Нахожу наибольшее совпадение
    if text in names:  # Если сообщение представляет собой просто обращение к боту
        questions = [["!call_bot", 100]]
    else:  # Иначе
        questions = [["!notunderstandme", 100]]
        for comparison in comparisons:
            if comparison[1] >= 70:  # Если совпадение более 70%
                # Добавляем распознанную команду в список
                if questions[0][0] == "!notunderstandme":
                    questions = [comparison]
                else:
                    questions.append(comparison)

    ####################################
    # Подведение результатов сравнения #
    ####################################

    # Получаю все возможные ответы на вопрос
    replys = []
    results = []
    # Получение вопросов
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

    return list(dedupe(results))  # Возвращаю ответы в виде списка


print("[i] FUZZ_METHODS is loaded!")
