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

/help - Выводит данную помощь
/add - Вызывает мастер создания нового тригера
/list - Выводит список триггеров бота
/disable - Отключить работу бота
/enable - Возобновить работу бота
/settings - Меню настроек

Отличный гайд по регулярным выражениям:
https://habr.com/post/115825/

Сайт для проверки и дебага регулярок:
https://regex101.com/
""",
            "server_error" : u"Произошла серверная ошибка😢😢",
            "add_enter_regexp" : u"{}, а теперь введите сам тригер. Точное вхождение или регулярку для поиска (подробнее смотри в /help)",
            "add_enter_sendTrigger" : u"Отлично, а теперь скинь мне то, чем мне отвечать на данные сообщения (изображение, аудио, гифка, текст)",
            "add_ok" : u"✅ Замечательно! Тригер был создан",
            "delete_ok" : u"✅ Тригер был удален",

            "list_is_empty" : u"Список триггеров пуст",
            "list" : u"Список активных триггеров:\n",
            "list_item" : u"- \"*{}*\" {}{} \n",
            "list_item_has_caption" : u"\\[текст]",
            "list_item_has_attachment" : u"\\[вложение: {}]",
            
            "bot_enabled" : u"️✅ Бот снова активен",
            "bot_disabled" : u"️✅ Бот отключен",

            "remove_trigger" : "Укажите какой тригер вы хотите удалить",

            "err_cant_find_item" : u"⛔️ Данного тригера не найдено",
            "err_wrong_regex" : u"️⛔️ Введенная строка (\"_{}_\") не является валидной регуляркой. Процедура создания прервана. Если вы на 100% уверены, что она верная, обратитесь к @coestaris за помощью",
            "err_same_regex_exists" : u"️⛔️ Точно такой же тригер уже в списке. Процедура создания прервана.",
            
            "err_bot_is_disabled" : u"️⛔️ Бот уже вырублен",
            "err_bot_is_enabled" : u"️⛔️ Бот уже работает",

            "err_not_allowed" : u"⛔️Вас (UserID: {}) нету в списке тех, кому разрешено юзать эту функцию.",

            "menu" : u"Выберите кнопку из списка",
            "menu_lang" : u"Выбрать язык",
            "menu_ignoreCase" : u"{} Игнорировать регистр",
            "menu_admMode" : u"{} Защищенный режим",
            "menu_close" : u"Закрыть",

            "menu_ru" : u"{} Русский🇷🇺",
            "menu_en" : u"{} English🇺🇸"

        }
    }
]

def getLang(l):
    global lang

    for a in lang:
        if(a["lang"] == l):
            return a["content"]

    raise ValueError("Unknown language")