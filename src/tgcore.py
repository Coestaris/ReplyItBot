import telegram
import traceback
import re
import time
import os
import psutil
import json

import dbUser
import db
import utils
import cfg
import language

send_typing_action = utils.send_action(telegram.ChatAction.TYPING)
send_upload_video_action = utils.send_action(telegram.ChatAction.UPLOAD_VIDEO)
send_upload_photo_action = utils.send_action(telegram.ChatAction.UPLOAD_PHOTO)

WAITING_FOR_REGEX = 1
WAITING_FOR_TRIGGER = 2
WAITING_FOR_EX_TRIGGER = 3

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

@send_typing_action
@utils.restricted
def adm_stat(bot, update):

    try:
        pid = os.getpid()
        py = psutil.Process(pid)
        mem = psutil.virtual_memory()

        bot.send_message(
            chat_id = update.message.chat_id, 
            text = u"*CPU*: {}_%_\n\n*Mem*:\n_Total_: {}\n_Available_: {}\n_Free_: {}\n_Used_: {} ({}%)\n\n*Server uptime*: {}\n\n*Bot uptime*: {}"
                .format(psutil.cpu_percent(), 
                    utils.sizeof_fmt(mem.total), 
                    utils.sizeof_fmt(mem.available), 
                    utils.sizeof_fmt(mem.free), 
                    utils.sizeof_fmt(mem.used), 
                    mem.percent, 
                    utils.display_time(time.time() - psutil.boot_time(), 5), 
                    utils.display_time(time.time() - py.create_time(), 5)),
            parse_mode = telegram.ParseMode.MARKDOWN,
            reply_markup = { "remove_keyboard" : True })
    
    except Exception as ex:
        notify_admin(ex)

@send_typing_action
@utils.restricted
def adm_dump(bot, update):

    try:
        with open(db.dbFileName) as f:
            data = json.load(f)

            bot.send_message(
                chat_id = update.message.chat_id, 
                text = u"```json{{\n{}```".format(json.dumps(data, sort_keys=True, indent=2)),
                parse_mode = telegram.ParseMode.MARKDOWN,
                reply_markup = { "remove_keyboard" : True })
        
    except Exception as ex:
        notify_admin(ex)

@send_typing_action
@utils.restricted
def adm_drop(bot, update):

    try:
        os.remove(db.dbFileName)
        db.reassign_db()
        db.store_user(dbUser.dbUser(update.message.chat_id))

        bot.send_message(
            chat_id = update.message.chat_id, 
            text = "Database dropped",
            reply_markup = { "remove_keyboard" : True })

    except Exception as ex:
        notify_admin(ex)

def errorHandler(bot, update, error):
    print(error)
    try:
        if(update == None):
            raise TypeError("Update was error. Error is: " + str(error))
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
def remove(bot, update):
    
    try:
        group = db.get_user(update.message.chat_id)
        user = update.message.from_user
        
        if(len(group.triggers) == 0):
            bot.send_message(chat_id=update.message.chat_id, 
                text=language.getLang(group.lang)["list_is_empty"],
                reply_markup = { "remove_keyboard" : True },
                reply_to_message_id=update.message.message_id)
            return

        custom_keyboard = []
        i = 1
        for x in group.triggers:
            custom_keyboard.append([telegram.KeyboardButton(text=u"{} - \"{}\"".format(i, x["text"]))])
            i += 1

        bot.send_message(chat_id=update.message.chat_id, 
            text=language.getLang(group.lang)["remove_trigger"],
            reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard, resize_keyboard=True),
            reply_to_message_id=update.message.message_id)

        group.userActions[user.id] = {}
        group.userActions[user.id]["i"] = WAITING_FOR_EX_TRIGGER
        db.store_user(group)   
        pass

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

        group.userActions[user.id] = {}
        group.userActions[user.id]["i"] = WAITING_FOR_REGEX
        db.store_user(group)   
        pass    

    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def enable(bot, update):
    try:
        group = db.get_user(update.message.chat_id)
        if(group.enabled):
            bot.send_message(chat_id=update.message.chat_id, 
                text=language.getLang(group.lang)["err_bot_is_enabled"],
                reply_markup = { "remove_keyboard" : True },
                reply_to_message_id=update.message.message_id)
            return
        
        group.enabled = True
        db.store_user(group)   

        bot.send_message(chat_id=update.message.chat_id, 
            text=language.getLang(group.lang)["bot_enabled"],
            reply_markup = { "remove_keyboard" : True },
            reply_to_message_id=update.message.message_id)
        return

    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def disable(bot, update):
    try:
        group = db.get_user(update.message.chat_id)
        if(not group.enabled):
            bot.send_message(chat_id=update.message.chat_id, 
                text=language.getLang(group.lang)["err_bot_is_disabled"],
                reply_markup = { "remove_keyboard" : True },
                reply_to_message_id=update.message.message_id)
            return

        group.enabled = False
        db.store_user(group)

        bot.send_message(chat_id=update.message.chat_id, 
            text=language.getLang(group.lang)["bot_disabled"],
            reply_markup = { "remove_keyboard" : True },
            reply_to_message_id=update.message.message_id)
        return

    except Exception as ex:
        notify_admin(ex)

@send_typing_action
def list(bot, update):
      
    try:
        user = db.get_user(update.message.chat_id)
        if(len(user.triggers) == 0):
            bot.send_message(chat_id=update.message.chat_id, 
                text=language.getLang(user.lang)["list_is_empty"],
                reply_markup = { "remove_keyboard" : True },
                reply_to_message_id=update.message.message_id)
            return
        
        text = language.getLang(user.lang)["list"]
        for x in user.triggers:
            text += utils.escape_string(language.getLang(user.lang)["list_item"].format(
                x["text"],  
                language.getLang(user.lang)["list_item_has_caption"] if x["caption"] != None else "", 
                language.getLang(user.lang)["list_item_has_attachment"].format(x["attachment"]["type"]) if x["attachment"] != None else ""))


        bot.send_message(chat_id=update.message.chat_id, 
            text=text,
            reply_markup = { "remove_keyboard" : True },
            parse_mode = telegram.ParseMode.MARKDOWN,
            reply_to_message_id=update.message.message_id)
        
    except Exception as ex:
        notify_admin(ex)

def allInputHandler(bot, update):
      
    try:
        group = db.get_user(update.message.chat_id)
        user = update.message.from_user
        textMessage = update.message.text

        if(str(user.id) in group.userActions):
            
            if(group.userActions[str(user.id)]["i"] == WAITING_FOR_REGEX):
                
                if(textMessage != '' and utils.isReValid(textMessage)):

                    if(textMessage in [ x["text"] for x in group.triggers]):
                        bot.send_message(chat_id=update.message.chat_id, 
                            text=utils.escape_string(language.getLang(group.lang)["err_same_regex_exists"].format(textMessage)),
                            reply_markup = { "remove_keyboard" : True },
                            parse_mode = telegram.ParseMode.MARKDOWN,
                            reply_to_message_id=update.message.message_id)

                        del group.userActions[str(user.id)]
                        db.store_user(group)
                        return

                    group.userActions[str(user.id)]["r"] = textMessage
                    group.userActions[str(user.id)]["i"] = WAITING_FOR_TRIGGER
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

            elif(group.userActions[str(user.id)]["i"] == WAITING_FOR_TRIGGER):
                
                if(update.message.caption != None):
                    textMessage = update.message.caption

                attachment = None
                if(update.message.photo != None and len(update.message.photo) != 0):
                    attachment = {
                        "file_id" : update.message.photo[-1].file_id,
                        "type" : "photo"
                    }
                if(update.message.sticker != None):
                    attachment = {
                        "file_id" : update.message.sticker.file_id,
                        "type" : "sticker"
                    }
                if(update.message.video != None):
                    attachment = {
                        "file_id" : update.message.video.file_id,
                        "type" : "video"
                    }
                if(update.message.voice != None):
                    attachment = {
                        "file_id" : update.message.voice.file_id,
                        "type" : "voice"
                    }
                if(update.message.video_note != None):
                    attachment = {
                        "file_id" : update.message.video_note.file_id,
                        "type" : "video_note"
                    }
                if(update.message.document != None):
                    attachment = {
                        "file_id" : update.message.document.file_id,
                        "type" : "document"
                    }
                if(update.message.audio != None):
                    attachment = {
                        "file_id" : update.message.audio.fild_id,
                        "type" : "audio"
                    }
                if(update.message.animation != None):
                    attachment = {
                        "file_id" : update.message.animation.fild_id,
                        "type" : "animation"
                    }

                group.triggers.append( { "text" : group.userActions[str(user.id)]["r"], "attachment" : attachment, "caption" : textMessage } )
                bot.send_message(chat_id=update.message.chat_id, 
                        text=utils.escape_string(language.getLang(group.lang)["add_ok"]),
                        reply_markup = { "remove_keyboard" : True },
                        parse_mode = telegram.ParseMode.MARKDOWN,
                        reply_to_message_id=update.message.message_id)

                del group.userActions[str(user.id)]
                db.store_user(group)
                return

            elif(group.userActions[str(user.id)]["i"] == WAITING_FOR_EX_TRIGGER):

                try:
                    parts = textMessage.split('-')[0]
                    index = int(parts) - 1

                    if(index < 0 or index >= len(group.triggers)):
                        bot.send_message(chat_id=update.message.chat_id, 
                            text=utils.escape_string(language.getLang(group.lang)["err_cant_find_item"]),
                            reply_markup = { "remove_keyboard" : True },
                            reply_to_message_id=update.message.message_id)

                        del group.userActions[str(user.id)]
                        db.store_user(group)
                        return

                    bot.send_message(chat_id=update.message.chat_id, 
                            text=utils.escape_string(language.getLang(group.lang)["delete_ok"]),
                            reply_markup = { "remove_keyboard" : True },
                            reply_to_message_id=update.message.message_id)

                    del group.triggers[index]
                    del group.userActions[str(user.id)]
                    db.store_user(group)

                except IndexError:
                    
                    bot.send_message(chat_id=update.message.chat_id, 
                            text=utils.escape_string(language.getLang(group.lang)["err_cant_find_item"]),
                            reply_markup = { "remove_keyboard" : True },
                            reply_to_message_id=update.message.message_id)

                    del group.userActions[str(user.id)]
                    db.store_user(group)
                    return

                pass

        else:
            
            if(not group.enabled):
                return
            
            if(update.message.caption != None):
                textMessage = update.message.caption

            if(textMessage != None):

                for trigger in group.triggers:
                    if(re.search(re.compile(trigger["text"]), textMessage)):

                        if(trigger["attachment"] != None):
                            if(trigger["attachment"]["type"] == "photo"):
                                bot.send_photo(
                                    chat_id=update.message.chat_id,
                                    photo=trigger["attachment"]["file_id"],
                                    reply_to_message_id=update.message.message_id,
                                    caption=trigger["caption"])

                            elif(trigger["attachment"]["type"] == "sticker"):
                                 bot.send_sticker(
                                    chat_id=update.message.chat_id,
                                    sticker=trigger["attachment"]["file_id"],
                                    reply_to_message_id=update.message.message_id)

                            elif(trigger["attachment"]["type"] == "video"):
                                bot.send_video(
                                    chat_id=update.message.chat_id,
                                    video=trigger["attachment"]["file_id"],
                                    reply_to_message_id=update.message.message_id,
                                    caption=trigger["caption"])
                            
                            elif(trigger["attachment"]["type"] == "voice"):
                                bot.send_voice(
                                    chat_id=update.message.chat_id,
                                    voice=trigger["attachment"]["file_id"],
                                    reply_to_message_id=update.message.message_id)

                            elif(trigger["attachment"]["type"] == "document"):
                                bot.send_document(
                                    chat_id=update.message.chat_id,
                                    document=trigger["attachment"]["file_id"],
                                    reply_to_message_id=update.message.message_id,
                                    caption=trigger["caption"])
                            
                            elif(trigger["attachment"]["type"] == "video_note"):
                                bot.send_video_note(
                                    chat_id=update.message.chat_id,
                                    video_note=trigger["attachment"]["file_id"],
                                    reply_to_message_id=update.message.message_id)
                            
                            elif(trigger["attachment"]["type"] == "audio"):
                                bot.send_audio(
                                    chat_id=update.message.chat_id,
                                    audio=trigger["attachment"]["file_id"],
                                    reply_to_message_id=update.message.message_id,
                                    caption=trigger["caption"])
                            
                            elif(trigger["attachment"]["type"] == "animation"):
                                bot.send_animation(
                                    chat_id=update.message.chat_id,
                                    animation=trigger["attachment"]["file_id"],
                                    reply_to_message_id=update.message.message_id,
                                    caption=trigger["caption"])

                        else:
                            bot.send_message(chat_id=update.message.chat_id, 
                                text=trigger["caption"],
                                reply_markup = { "remove_keyboard" : True },
                                reply_to_message_id=update.message.message_id)

    except Exception as ex:
        notify_admin(ex)