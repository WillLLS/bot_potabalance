from telegram import Update
from telegram.ext import ContextTypes
from config import path_authorization, path_balance
import json
import os


def auth(function):
    async def foo(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
        user_id = update.effective_user.id
        
        with open(path_authorization, "r", encoding="utf-8") as file:
            authorized_id = json.load(file)
        
        if user_id in authorized_id["auth"]:
            await function(update, context, query)
        
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Not allowed!")
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Your id is: {user_id}")
    return foo

def check_args(function):
    async def foo(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
        if len(context.args) == 0:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Argument needed!")
        else:
            await function(update, context)
    return foo

def chek_args_int(function):
    async def foo(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
        try:
            int(context.args[0])
        except:
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Argument must be an integer")
        else:
            await function(update, context)
    return foo

def msg_checker(function):
    async def foo(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
        if update.message.text == "Hello":
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")
        else:
            await function(update, context)
    return foo

def check_last_message(function):
    
    def clean_message(message):
        message = message.replace("\n", "")
        message = message.replace(" ", "")
        return message
    
    async def foo(query, text, reply_markup=None):
        
        last_message    = query.message.text
        last_message    = clean_message(last_message)
        new_message     = clean_message(text)
                
        if new_message == last_message:
            pass
        else:
            await function(query, text, reply_markup)
            
    return foo