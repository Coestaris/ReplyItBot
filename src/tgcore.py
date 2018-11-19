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
        if(isinstance(update, NoneType)):
            raise TypeError("Update was error. Error is: " + error)
        else:
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
            reply_markup = { "remove_keyboard" : True },
            reply_to_message_id=update.message.message_id)

        group.userActions[user.id] = WAITING_FOR_REGEX
        db.store_user(group);    
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

WAITING_FOR_REGEX = 1
WAITING_FOR_TRIGGER = 2

def textInputHandler(bot, update):
      
    try:
        group = db.get_user(update.message.chat_id)
        user = update.message.from_user
        textMessage = update.message.text

        if(str(user.id) in group.userActions):
            
            if(group.userActions[str(user.id)] == WAITING_FOR_REGEX):
                
                if(textMessage != '' and utils.isReValid(textMessage)):

                    if(textMessage in [x["text"] for x in group.triggers]):
                        bot.send_message(chat_id=update.message.chat_id, 
                            text=utils.escape_string(language.getLang(group.lang)["err_same_regex_exists"].format(textMessage)),
                            reply_markup = { "remove_keyboard" : True },
                            parse_mode = telegram.ParseMode.MARKDOWN,
                            reply_to_message_id=update.message.message_id)

                        del group.userActions[str(user.id)]
                        db.store_user(group)
                        return

                    group.userActions[str(user.id)] = WAITING_FOR_TRIGGER
                    bot.send_message(chat_id=update.message.chat_id, 
                        text=language.getLang(group.lang)["add_enter_sendTrigger"],
                        reply_markup = { "remove_keyboard" : True },
                        reply_to_message_id=update.message.message_id)
                    
                    db.store_user(group)
                    return
                else:
                    bot.send_message(chat_id=update.message.chat_id, 
                        text=utils.escape_string(language.getLang(group.lang)["err_wrong_regex"].format(textMessage)),
                        reply_markup = { "remove_keyboard" : True },
                        parse_mode = telegram.ParseMode.MARKDOWN,
                        reply_to_message_id=update.message.message_id)
                    
                    del group.userActions[str(user.id)]
                    db.store_user(group)
                    return

            elif(group.userActions[str(user.id)] == WAITING_FOR_TRIGGER):
                
                if(update.message.caption != None):
                    textMessage += update.message.caption

                if(update.message.photo != None):
                    #todo
                    print update.message.photo
                group.triggers.append( { "text" : textMessage, "attachments" : None } )

                bot.send_message(chat_id=update.message.chat_id, 
                        text=utils.escape_string(language.getLang(group.lang)["add_ok"]),
                        reply_markup = { "remove_keyboard" : True },
                        parse_mode = telegram.ParseMode.MARKDOWN,
                        reply_to_message_id=update.message.message_id)

                del group.userActions[str(user.id)]
                db.store_user(group)
                return

            else:
                pass

        else:
            pass    

    except Exception as ex:
        notify_admin(ex)
