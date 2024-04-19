import logging
import json
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

import time

from utils.command import start, balance, spent, sent, hist, button, help

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
    

if __name__ == '__main__':
    
    token = ""
    
    application = ApplicationBuilder().token(token).build()
    application.base_url = "https://api.telegram.org/bot" + token
    
    application.add_handler(CallbackQueryHandler(button))
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('balance', balance))
    application.add_handler(CommandHandler('spent', spent))
    application.add_handler(CommandHandler('sent', sent))
    application.add_handler(CommandHandler('hist', hist))
    application.add_handler(CommandHandler('help', help))

    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)