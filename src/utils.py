import json
import re
from functools import wraps

import language

LIST_OF_ADMINS = []

def sizeof_fmt(num, suffix='B'):
    for unit in ['','K','M','G','T','P','E','Z']:
        if abs(num) < 1024.0:
            return "%3.2f %s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f %s%s" % (num, 'Y', suffix)

def escape_string(input):
    return input.replace("_", "\\_").replace("*", "\\*").replace("[", "\\[").replace("`", "\\`")

def display_time(seconds, granularity=2):
    
    intervals = (
        ('weeks', 604800),  # 60 * 60 * 24 * 7
        ('days', 86400),    # 60 * 60 * 24
        ('hours', 3600),    # 60 * 60
        ('minutes', 60),
        ('seconds', 1),
    )
    result = []
    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{0:.0f} {1}".format(value, name))
    return ', '.join(result[:granularity])

def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            update.message.reply_text(language.getLang("ru")["err_not_allowed"].format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped

def send_action(action):
    def decorator(func):
        @wraps(func)
        def command_func(*args, **kwargs):
            bot, update = args
            bot.send_chat_action(chat_id=update.message.chat_id, action=action)
            func(bot, update, **kwargs)
        return command_func
    
    return decorator

def isReValid(regex):
    try:
        re.compile(regex)
        return True
    except re.error:
        return False