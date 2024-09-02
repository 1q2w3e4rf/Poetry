from telebot import TeleBot, types
from Poetry import Stik
from config import TOKEN
import time
import threading

bot = TeleBot(TOKEN)

stik = Stik()

chat = {}

newstih = None
stih = None
password = None
stih = {}

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Я телеграмм бот в котором можно прочитать стихи")

@bot.message_handler(commands=["stih"])
def stih2(message):
    if message.chat.id not in chat:
        chat[message.chat.id] = {}
    chat[message.chat.id]["chat_id"] = message.chat.id
    newstih_list = stik.get_newstih()
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for newstih in newstih_list:
        keyboard.add(newstih[0])
    bot.send_message(message.chat.id, "Выберите стих", reply_markup=keyboard)

def stih1(message):
    newstih_list = stik.get_newstih()
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    for newstih in newstih_list:
        keyboard.add(newstih[0])
    bot.send_message(message.chat.id, "Стих добавлен", reply_markup=keyboard)

@bot.message_handler(commands=["new"])
def new(message):
    bot.send_message(message.chat.id, "Введите пароль")
    bot.register_next_step_handler(message, new_password)

def new_stih(message):
    chat_id = message.chat.id
    if chat_id not in stih:
        stih[chat_id] = {}
    stih[chat_id]["newstih"] = message.text
    bot.send_message(message.chat.id, "Напишите стих")
    bot.register_next_step_handler(message, stih_text)

def stih_text(message):
    chat_id = message.chat.id
    stih[chat_id]["stih"] = message.text
    bot.send_message(chat_id, "Готово!")
    stik.new_stih(stih[chat_id]["newstih"], stih[chat_id]["stih"])
    result = stih1(message)
    if result is not None:
        bot.send_message(chat_id, result)

def new_password(message):
    password = message.text
    if password == "12345":
        bot.send_message(message.chat.id, "Напишите название стиха")
        bot.register_next_step_handler(message, new_stih)


@bot.message_handler(content_types=["text"])
def stih_choice(message):
    if message.text:
        newstih_list = stik.get_newstih()
        for newstih in newstih_list:
            if message.text.lower() == newstih[0].lower():
                stih = stik.get_stih(newstih[0])
                if stih:
                    bot.send_message(message.chat.id, stih)
                    return
        bot.send_message(message.chat.id, "Стих не найден")

def send_message_periodically():
    while True:
        for chat_id in chat:
            bot.send_message(chat_id, "Не забывайте обновлять список стихов на команду /stih!")
        time.sleep(3600)

thread = threading.Thread(target=send_message_periodically)
thread.start()

bot.infinity_polling()