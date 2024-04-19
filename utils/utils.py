from config import path_balance, path_authorization, path_usernames
from utils.decorateurs import check_last_message
import json
import os
from datetime import datetime

def get_percent(balance_1, balance_2):
    return round((balance_1 / (balance_1 + balance_2)) * 100)

def get_balance():
    with open(path_balance, "r", encoding="utf-8") as file:
        balance = json.load(file)
    return balance

def save_balance(balance):
    with open(path_balance, "w", encoding="utf-8") as file:
        json.dump(balance, file)
        
def update_balance(user_id, value):
    balance = get_balance()
    balance[user_id] += value
    save_balance(balance)
    
    update_hist(user_id, value)

def get_id():
    with open(path_authorization, "r", encoding="utf-8") as file:
        authorized_id = json.load(file)["auth"]
    return authorized_id

def get_str_id():
    with open(path_authorization, "r", encoding="utf-8") as file:
        authorized_id = json.load(file)["auth"]
    ids = [str(id) for id in authorized_id]
    return ids

def get_name_id():
    with open(path_usernames, "r", encoding="utf-8") as file:
        users = json.load(file)
    return users

def get_second_user(user_id):
    ids = get_str_id()
    ids.remove(user_id)
    return ids[0]

def get_hist(user_id):
    path_history = os.path.join("data", f"{user_id}.json")
    with open(path_history, "r", encoding="utf-8") as file:
        history = json.load(file)["hist"]
    
    return history

def save_hist(user_id, history):
    path_history = os.path.join("data", f"{user_id}.json")
    with open(path_history, "w", encoding="utf-8") as file:
        json.dump(history, file)
    

def update_hist(user_id, amount):
    
    history = get_hist(user_id)

    date = datetime.now()
    date = date.strftime("%Y/%m/%d")
    history = [{"date": date, "amount": amount}] + history
    history = {"hist": history}
    
    save_hist(user_id, history)


def get_message_hist(user_id, index_start):
    history = get_hist(user_id)
    users   = get_name_id()
    
    balance = get_balance()[user_id]
    
    name = users[user_id]
    
    index_end = index_start + 15
    if index_end > len(history):
        index_end = len(history)
    
    message = f"""----- {name}'s historic -----\n\nTotal balance: {balance} €\n\n"""
    for i in range(index_start, index_end):            
        message += f"""{history[i]['date']}                     {history[i]["amount"]} €\n"""
    
    return message

def get_len_hist(user_id):
    history = get_hist(user_id)
    return len(history)


@check_last_message
async def set_last_message(query, text, reply_markup=None):

    await query.edit_message_text(text=text,  reply_markup=reply_markup) 

    