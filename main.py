# -*- coding: utf-8 -*-
import sqlite3
import time

from telebot import TeleBot, types
import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message
import keyboards
import functions

admin_id = config.admin
bot = TeleBot(config.TOKEN)
admin_sending_messages_dict = {}


@bot.message_handler(commands=['start'])
def send_welcome(message):
    message_sender = message.from_user.username
    functions.first_join(user_id=message.chat.id, name=message.from_user.username)
    bot.send_photo(chat_id=message.chat.id, photo=open(config.cover, 'rb'),
                   caption=f"Привет, рад тебя видеть {message_sender}\nНажимай на 🤍 и давай познакомимся",
                   reply_markup=keyboards.first_step)


@bot.message_handler(commands=['admin'])
def handler_admin(message):
    chat_id = message.chat.id
    print(chat_id)
    if chat_id == config.admin:
        bot.send_message(chat_id, 'Вы перешли в меню админа', reply_markup=keyboards.admin_menu)

@bot.callback_query_handler(func=lambda call: call.data =='admin_sending_messages' or call.data =='exit_admin_menu' or call.data =='admin_info')
def but0_pressed(call: types.CallbackQuery):
    if call.data == 'admin_sending_messages':
        msg = bot.send_message(call.message.chat.id,
                               text='Введите текст рассылки')
        bot.register_next_step_handler(msg, admin_sending_messages)

    if call.data == 'exit_admin_menu':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id-1)


    if call.data == 'admin_info':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=functions.admin_info(),
            reply_markup=keyboards.admin_menu
        )


@bot.callback_query_handler(func=lambda call: call.data == "go")
def but1_pressed(call: types.CallbackQuery):
    # if call.message.chat.id == config.thank_you:

    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=config.start,
                             reply_markup=keyboards.main_keys)


@bot.callback_query_handler(func=lambda call: call.data == "WhoAmI")
def but2_pressed(call: types.CallbackQuery):
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=config.bio,
                             reply_markup=keyboards.go_back)


@bot.callback_query_handler(func=lambda call: call.data == "Dialog")
def but3_pressed(call: types.CallbackQuery):
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                             caption=config.go_to_dialog, reply_markup=keyboards.go_back)


@bot.message_handler()
def send_poslanie(message: Message):
    if message.chat.id !=admin_id:
        message_worked = message.text
        message_sender = message.from_user.username
        bot.send_message(admin_id, f"Новое сообщение от @{message_sender}!\n\n{message_worked}",
                         reply_markup=keyboards.delete)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(chat_id=message.chat.id, text = 'Cпасибо за вопрос. Напишу сразу же, как освобожусь',
                         reply_markup=keyboards.delete)

    elif message.chat.id == admin_id:
        bot.send_message(chat_id=message.chat.id, text='АДМИН, ты серьёзно?',
                         reply_markup=keyboards.delete)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


@bot.callback_query_handler(func=lambda call: call.data == "close")
def but4_pressed(call: types.CallbackQuery):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


def admin_sending_messages(message):
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.delete_message(message.chat.id, message.message_id)
    dict = functions.Admin_sending_messages(message.chat.id)
    admin_sending_messages_dict[message.chat.id] = dict

    dict = admin_sending_messages_dict[message.chat.id]
    dict.text = message.text

    msg = bot.send_message(message.chat.id,
                           text='Отправьте "ПОДТВЕРДИТЬ" для подтверждения')
    bot.register_next_step_handler(msg, admin_sending_messages_2)

def admin_sending_messages_2(message):
    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()
    dict = admin_sending_messages_dict[message.chat.id]
    if message.text == 'ПОДТВЕРДИТЬ':
        bot.delete_message(message.chat.id, message.message_id-1)
        bot.delete_message(message.chat.id, message.message_id)
        cursor.execute(f'SELECT * FROM users')
        row = cursor.fetchall()

        for i in range(len(row)):
            try:
                time.sleep(1)
                bot.send_message(row[i][0], dict.text, reply_markup=keyboards.delete)

            except:
                pass
    else:
        bot.send_message(message.chat.id, text='Рассылка отменена', reply_markup=keyboards.delete)

        bot.delete_message(message.chat.id, message.message_id)
        bot.delete_message(message.chat.id, message.message_id - 1)




if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
