import logging
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

storage_path = ""

def choose_path():
    global storage_path
    root = tk.Tk()
    root.withdraw()
    storage_path = filedialog.askdirectory()
    root.destroy()

def save_group_chat(update: Update, context: CallbackContext):
    message = update.message
    chat_id = message.chat.id
    chat_text = message.text

    if message.chat.type != 'group':
        return

    current_date = datetime.now().strftime("%Y-%m-%d")

    sender_name = message.from_user.full_name or message.from_user.username

    formatted_message = f"[{datetime.now().strftime('%H:%M:%S')}] {sender_name}: {chat_text}"

    print(f"Received message from '{sender_name}' in group '{message.chat.title}' ({chat_id}) on {current_date}: {chat_text}")

    filename = f'{storage_path}/group_chat_{current_date}.txt'
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{formatted_message}\n")

def log_deleted_message(update: Update, context: CallbackContext):
    deleted_message = update.effective_message
    chat_id = update.effective_chat.id
    chat_title = update.effective_chat.title

    sender_name = deleted_message.from_user.full_name or deleted_message.from_user.username
    message_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    log_entry = f"[{message_time}] [{chat_title}] [{chat_id}] {sender_name}: Message deleted - {deleted_message.text}"

    with open('deleted_message_logs.txt', 'a', encoding='utf-8') as log_file:
        log_file.write(log_entry + '\n')

def main():

    choose_path()

    updater = Updater('6340227723:AAGesLETr8EeZEqFSxTuymtFogsC2aHkICY', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.group, save_group_chat))

    updater.start_polling()

    updater.idle()

if __name__ == '__main__':
    main()


""" web-based code wihtout gui
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

storage_path = "/home/lucareinholz123456789"

def save_group_chat(update: Update, context: CallbackContext):
    message = update.message
    chat_id = message.chat.id
    chat_text = message.text

    if message.chat.type != 'group':
        return

    current_date = datetime.now().strftime("%Y-%m-%d")

    sender_name = message.from_user.full_name
    if not sender_name:
        # If the user's full name is not available, use their username
        sender_name = message.from_user.username

    formatted_message = f"[{datetime.now().strftime('%H:%M:%S')}] {sender_name}: {chat_text}"

    print(f"Received message from '{sender_name}' in group '{message.chat.title}' ({chat_id}) on {current_date}: {chat_text}")

    filename = f'{storage_path}/group_chat_{current_date}.txt'
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(f"{formatted_message}\n")

def main():

    updater = Updater('6340227723:AAGesLETr8EeZEqFSxTuymtFogsC2aHkICY', use_context=True)

    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.group, save_group_chat))

    updater.start_polling()

    updater.idle()

updater = None

if __name__ == '__main__':
    main()
"""
