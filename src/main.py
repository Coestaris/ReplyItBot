import logging

from telegram.ext import CommandHandler, Filters, MessageHandler, Updater, CallbackQueryHandler

import cfg
import language
import tgcore
import utils

def main():
    
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    logger.log(logging.INFO, "Loading configs...")
    cfg.globalCfg = cfg.cfg.parse_cfg()
    
    logger.log(logging.INFO, "Init tgcore...")
    updater = Updater(cfg.globalCfg.tg_token)
    tgcore.bot = updater.bot
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", tgcore.start))
    dp.add_handler(CommandHandler("help", tgcore.help))
    dp.add_handler(CommandHandler("add", tgcore.add))
    dp.add_handler(CommandHandler("list", tgcore.list))

    dp.add_handler(CommandHandler("disable", tgcore.disable))
    dp.add_handler(CommandHandler("enable", tgcore.enable))
    dp.add_handler(CommandHandler("settings", tgcore.settings))
    dp.add_handler(CommandHandler("remove", tgcore.remove))

    dp.add_handler(CommandHandler("adm_dump", tgcore.adm_dump))    
    dp.add_handler(CommandHandler("adm_drop", tgcore.adm_drop))    
    dp.add_handler(CommandHandler("adm_stat", tgcore.adm_stat))

    dp.add_handler(MessageHandler(Filters.all, tgcore.allInputHandler))
    dp.add_handler(CallbackQueryHandler(tgcore.callback_inline))

    dp.add_error_handler(tgcore.errorHandler)

    logger.log(logging.INFO, "Starting polling...")
    updater.start_polling()

    logger.log(logging.INFO, "Going to loop...")
    updater.idle()


if __name__ == '__main__':
    main()
    