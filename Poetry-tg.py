from telebot import TeleBot, types
from Poetry import Stik
from config import TOKEN
import time
import threading

bot = TeleBot(TOKEN)

stik = Stik()

# Словарь для хранения информации о пользователях
users = {}

chat = {}

newstih = None
stih = None
password = None
stih = {}

def broadcast_message(message_text):
    for chat_id in users:
        try:
            bot.send_message(chat_id, message_text)
        except Exception as e:
            print(f"{chat_id}: {e}")


@bot.message_handler(commands=["start"])
def start(message):
    chat_id = message.chat.id
    username = message.from_user.username if message.from_user.username else message.from_user.first_name
    user_id = message.from_user.id
    
    # Сохраняем информацию о пользователе в словаре
    users[chat_id] = {"username": username, "user_id": user_id}
    
    bot.send_message(chat_id, "Приветствую вас, дорогие друзья!")

@bot.message_handler(commands=['Рассылка'])
def broadcast_command(message):
    if message.from_user.id == 292824554:
        msg = bot.reply_to(message, "Введите текст для рассылки:")
        bot.register_next_step_handler(msg, process_broadcast_text)
    else:
        bot.reply_to(message, "У вас нет прав на эту команду.")
    
def process_broadcast_text(message):
    broadcast_message(message.text)
    bot.reply_to(message, "Рассылка запущена!")

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

user_messages = {}
dima_messages = {}


@bot.message_handler(commands=["Задать_вопрос"])
def dima(message):
    bot.send_message(message.chat.id, "Напиши сообщение Дмитрию")
    # Сохраняем chat_id пользователя
    user_messages[message.chat.id] = {"user_id": message.from_user.id, "username": message.from_user.username if message.from_user.username else message.from_user.first_name}
    bot.register_next_step_handler(message, dima_k)

def dima_k(message):
    chat_id = message.chat.id
    dima_message = message.text
    
    # Получаем информацию об отправителе
    if chat_id in user_messages:
        user_info = user_messages[chat_id]
        username = user_info['username']
        user_id = user_info['user_id']

        # Создаем инлайн кнопку ответа
        markup = types.InlineKeyboardMarkup(row_width=1)
        item = types.InlineKeyboardButton("Ответить", callback_data=f"reply_{chat_id}")
        markup.add(item)
        
        sent_message = bot.send_message(292824554, f"Сообщение от пользователя @{username} (ID: {user_id}): {dima_message}", reply_markup=markup)
        
        # Сохраняем id сообщения, которое отправили Диме
        dima_messages[sent_message.message_id] = chat_id
        
        bot.send_message(chat_id, "Сообщение отправлено Дмитрию!")
    else:
         bot.send_message(chat_id, "Ошибка: не удалось сохранить информацию об отправителе.")
    
    # Очищаем данные об отправителе
    if chat_id in user_messages:
        del user_messages[chat_id]

@bot.callback_query_handler(func=lambda call: call.data.startswith("reply_"))
def callback_inline(call):
    chat_id_reply = int(call.data.split("_")[1])
    msg = bot.send_message(call.message.chat.id, "Напишите ответ пользователю", reply_to_message_id=call.message.message_id)
    
    bot.register_next_step_handler(msg, reply_handler, chat_id_reply)
    
def reply_handler(message, chat_id_reply):
    reply_text = message.text
    bot.send_message(chat_id_reply, f"Ответ от Димы: {reply_text}")
    bot.send_message(message.chat.id, "Ответ отправлен пользователю.")
    
    if message.reply_to_message.message_id in dima_messages:
      del dima_messages[message.reply_to_message.message_id]


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
    if password == "20092007":
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
