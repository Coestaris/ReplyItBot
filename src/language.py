# coding=utf8

lang = [
    {
        "lang" : "ru",
        "content" : 
        {
            "help" : 
u"""
Привет! Бот для настраиваемого авто-ответа на сообщения в паблике.
🤔Для взаемодействия юзай🤔:

/help - Данную помощь

/add - Вызывает мастер создания нового тригера

/list - Выводит список триггеров бота

/disable - Отключить работу бота

/enable - Возобновить работу бота

/settings - Меню настроек
""",
            "server_error" : u"error",
            "add_enter_regexp" : u"{}, а теперь введите сам тригер. Точное вхождение или регулярку для поиска (подробнее смотри в /help)",
            "add_enter_sendTrigger" : u"Отлично, а теперь скинь мне то, чем мне отвечать на данные сообщения (изображение, аудио, гифка, текст)",
            "add_ok" : u"Замечательно! Тригер был создан",

            "err_wrong_regex" : u"Введенная строка (\"_{}_\") не является валидной регуляркой. Процедура создания прервана. Если вы на 100% уверены, что она верная, обратитесь к @coestaris за помощью",
            
        }
    }
]

def getLang(l):
    global lang

    for a in lang:
        if(a["lang"] == l):
            return a["content"]

    raise ValueError("Unknown language")