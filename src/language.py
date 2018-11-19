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
            "add_enter_regexp" : u"{}, а теперь введите сам тригер. Точное вхождение или регулярку для поиска (подробнее смотри в /help)"
        }
    }
]

def getLang(l):
    global lang

    for a in lang:
        if(a["lang"] == l):
            return a["content"]

    raise ValueError("Unknown language")