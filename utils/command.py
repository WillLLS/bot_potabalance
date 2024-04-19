
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, constants
from utils.decorateurs import *
from utils.utils import get_str_id, get_balance, update_balance, get_percent, get_name_id, get_message_hist, get_second_user, get_len_hist, set_last_message


@auth
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hello!")

@auth
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    
    user_id = str(update.effective_user.id)
    
    balance     = get_balance()
    second_id   = get_second_user(user_id)
    
    if balance[user_id] == 0 and balance[second_id] == 0:
        percent = 50
    
    else:
        percent = get_percent(balance[user_id], balance[second_id])
    
    with open(f"load_imgs/{percent}.png", "rb") as file:
        await context.bot.send_photo(chat_id=update.effective_chat.id, photo=file)

@auth
@check_args
@chek_args_int
async def spent(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    
    value = int(context.args[0])
    user_id = str(update.effective_user.id)
    
    update_balance(user_id, value)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Balance updated")

@auth
@check_args
@chek_args_int
async def sent(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    user_id = str(update.effective_user.id)
    
    value = int(context.args[0])
    
    # Update the user_id balance
    update_balance(user_id, value)
    
    # Choose a user to send money to    
    ids = get_str_id()
    users = get_name_id()
    
    keyboard = []
    for id in ids:
        if id != user_id:
            data = {"sent": {"to_id": id, "amount": value}}
            keyboard.append([InlineKeyboardButton(users[id], callback_data=json.dumps(data))])
                
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Choose a user on the one you sent money", reply_markup=reply_markup)

@auth
async def hist(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    
    ids     = get_str_id()
    users   = get_name_id()
    
    keyboard = []
    for id in ids:
        data = {"hist": {"user_id": id, "index_start": 0}}
        keyboard.append([InlineKeyboardButton(users[id], callback_data=json.dumps(data))])
        
    reply_markup = InlineKeyboardMarkup(keyboard)
    print(query==None)
    if query == None:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Which user's historic do you want to see ?", reply_markup=reply_markup)
    else:
        await set_last_message(query=query, text="Which user's historic do you want to see ?", reply_markup=reply_markup)


@auth
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None) -> None:
    query = update.callback_query
    
    await query.answer()

    # Chargement des données
    data = json.loads(query.data)
    command = list(data.keys())[0]
        
    if command == "sent":
        update_balance(data["sent"]["to_id"], -data["sent"]["amount"])
        
        await set_last_message(query=query, text="Balance updated")
    
    elif command == "hist":
        user_selected = data["hist"]["user_id"]
        index_start = data["hist"]["index_start"]
        message = get_message_hist(user_selected, index_start)
        
        history_length = get_len_hist(user_selected)
        
        keyboard = []
        
        previous    = "◀"
        next        = "▶"
        
        data_previous   = {"hist": {"user_id": user_selected, "index_start": index_start - 15 if index_start - 15 >= 0 else 0}}
        data_next       = {"hist": {"user_id": user_selected, "index_start": index_start + 15 if index_start + 15 < history_length else index_start}}
        
        keyboard = [
            [
                InlineKeyboardButton(previous, callback_data=json.dumps(data_previous)), 
                InlineKeyboardButton(next, callback_data=json.dumps(data_next))
            ],
            [
                InlineKeyboardButton("←", callback_data=json.dumps({"back": "hist"}))
            ],
            [
                InlineKeyboardButton("Quit", callback_data=json.dumps({"quit": "hist"}))
            ]
        ]
            
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await set_last_message(query=query, text=message, reply_markup=reply_markup)
        
    elif command == "back":
        if data["back"] == "hist":
            await hist(update, context, query)
        
    elif command == "quit":
        await set_last_message(query=query, text="End of history")

@auth
async def help(update: Update, context: ContextTypes.DEFAULT_TYPE, query=None):
    import time
    
    help_start      = "/start: Say hello :)"
    help_balance    = "/balance: Show the current balance"
    help_spent      = "/spent: Update the balance - Argument needed: amount"
    example_spent   = "► Example: '/spent 10'"
    help_sent       = "/sent: Sent money - Argument needed: amount"
    example_sent    = "► Example: '/sent 10' - Then choose the user"
    help_hist       = "/hist: Show the historic - Then choose the user"
    help_help       = "/help: Show the help"
    
    help_list = [help_start, help_balance, help_spent, example_spent, help_sent, example_sent, help_hist, help_help]   
    
    for help_ in help_list:   
        await context.bot.send_message(chat_id=update.effective_chat.id, text=help_)
        time.sleep(0.5)