import telegram
import traceback

import dbUser
import db
import utils
import cfg
import language

send_typing_action = utils.send_action(telegram.ChatAction.TYPING)
send_upload_video_action = utils.send_action(telegram.ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = utils.send_action(telegram.ChatAction.UPLOAD_PHOTO)

bot = None

def notify_admin(ex):
    print("Error: {}\nAdmin has been notifyed".format(ex))
    for admin in cfg.globalCfg.admins:
        bot.send_message(
            chat_id=admin,
            text="*Bot error!*\n\n_{}_\n\n{}".format(
                utils.escape_string(ex.__str__()), 
                utils.escape_string(traceback.format_exc())), 
            parse_mode = telegram.ParseMode.MARKDOWN)
    pass

def errorHandler(bot, update, error):
    print(error)
    try:
        user = db.get_user(update.message.chat_id)
        update.message.reply_text(language.getLang(user.lang)["server_error"], reply_markup = { "remove_keyboard" : True })
    
    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def start(bot, update):
    try:
        if(update.message.chat.type == telegram.chat.Chat.PRIVATE):
            #todo
            pass
        else:
        
            if(not db.has_user(update.message.chat_id)):
                db.store_user(dbUser.dbUser(teleid=update.message.chat_id, debugName=update.message.chat.title))

            user = db.get_user(update.message.chat_id)
            update.message.reply_text(language.getLang(user.lang)["help"], reply_markup = { "remove_keyboard" : True })
    
    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def help(bot, update):
    
    try:
        user = db.get_user(update.message.chat_id)
        update.message.reply_text(language.getLang(user.lang)["help"], reply_markup = { "remove_keyboard" : True })

    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def add(bot, update):
      
    try:
        group = db.get_user(update.message.chat_id)
        user = update.message.from_user

        bot.send_message(chat_id=update.message.chat_id, 
            text=language.getLang(group.lang)["add_enter_regexp"].format(user.first_name),
            reply_markup = { "remove_keyboard" : True })
        pass    

    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def list(bot, update):
      
    try:
        user = db.get_user(update.message.chat_id)
        pass    

    except Exception as ex:
        notify_admin(ex)
