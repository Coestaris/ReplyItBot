# coding=utf8

import telegram
import db

import language

def get_main_menu(user, bot):
    return telegram.InlineKeyboardMarkup([
        [telegram.InlineKeyboardButton(text=language.getLang(user.lang)["menu_lang"], callback_data="btn_lang")],
        [telegram.InlineKeyboardButton(text=language.getLang(user.lang)["menu_ignoreCase"]
            .format(u"✅" if user.ignoreCase else u"⛔️"), callback_data="btn_ign")],
        [telegram.InlineKeyboardButton(text=language.getLang(user.lang)["menu_admMode"]
            .format(u"✅" if user.adminMode else u"⛔️") , callback_data="btn_adm")],
        [telegram.InlineKeyboardButton(text=language.getLang(user.lang)["menu_close"], callback_data="btn_close")]
    ])

def get_menu(act, user, bot):
    
    if(act == "btn_tomain" or act == "btn_ign" or act == "btn_adm"):

        if(act == "btn_ign"):
            user.ignoreCase = not user.ignoreCase

        if(act == "btn_adm"):
            user.adminMode = not user.adminMode

        db.store_user(user)
        return get_main_menu(user, bot) 
    
    elif(act == "btn_lang" or act == "btn_ru" or act == "btn_en"):

        if(act == "btn_ru"): 
            user.lang = "ru"
            db.store_user(user)
        
        if(act == "btn_en"): 
            user.lang = "en"
            db.store_user(user)

        return telegram.InlineKeyboardMarkup([
            [telegram.InlineKeyboardButton(text=language.getLang(user.lang)["menu_ru"]
                .format(u'✅' if user.lang == "ru" else u' '), callback_data="btn_ru")],
            #[telegram.InlineKeyboardButton(text=language.getLang(user.lang)["menu_en"]
            #    .format(u'✅' if user.lang == "en" else u' '), callback_data="btn_en")],
            [telegram.InlineKeyboardButton(text="Назад", callback_data="btn_tomain")]
        ])

    if(act == "btn_close"):
        return {}