# -*- coding: utf-8 -*-
import sqlite3
import time

import telebot
from telebot import TeleBot, types
import config
from config import cover
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
    bot.send_photo(chat_id=message.chat.id, photo=functions.get_img(),
                   caption=f"Привет, рад тебя видеть {message_sender}\nНажимай на 🤍 и давай познакомимся",
                   reply_markup=keyboards.first_step)


@bot.message_handler(commands=['admin'])
def handler_admin(message):
    chat_id = message.chat.id
    if chat_id == config.admin:
        bot.send_message(chat_id, 'Вы перешли в меню админа', reply_markup=keyboards.admin_menu)


@bot.callback_query_handler(func=lambda call: call.data == 'admin_sending_messages' or call.data == 'exit_admin_menu'
                                              or call.data == 'admin_info' or call.data == 'edit_text'
                                              or call.data == 'green' or call.data == 'red' or call.data == 'edit_img'
                                              or call.data == 'add_case' or call.data == 'delete_case')
def but0_pressed(call: types.CallbackQuery):
    if call.data == 'admin_sending_messages':
        msg = bot.send_message(call.message.chat.id,
                               text='Введите текст рассылки')
        bot.register_next_step_handler(msg, admin_sending_messages)

    if call.data == 'exit_admin_menu':
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id - 1)

    if call.data == 'admin_info':
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=functions.admin_info(),
            reply_markup=keyboards.admin_menu
        )
    if call.data == 'edit_text':
        msg = bot.send_message(call.message.chat.id,
                               text='Введите новый текст БИО')
        bot.register_next_step_handler(msg, admin_edit_bio)

    if call.data == 'edit_img':
        msg = bot.send_message(call.message.chat.id,
                               text='пришлите новое фото')
        bot.register_next_step_handler(msg, admin_edit_img)


    if call.data == 'green':
        conn = sqlite3.connect('auternous_bot.sqlite')
        cursor = conn.cursor()

        cursor.execute(f'UPDATE messages SET status = ? where rowid = 1', [config.status_1])

        conn.commit()
        conn.close()

    if call.data == 'red':
        conn = sqlite3.connect('auternous_bot.sqlite')
        cursor = conn.cursor()

        cursor.execute(f'UPDATE messages SET status = ? where rowid = 1', [config.status_0])

        conn.commit()
        conn.close()

    if call.data == 'add_case':
        msg = bot.send_message(call.message.chat.id,
                               text='Введите название кейса в формате "название|ссылка"')
        bot.register_next_step_handler(msg, admin_add_case)

    if call.data == 'delete_case':
        msg = bot.send_message(call.message.chat.id,
                               text='Введите точное название кейса, который хотите удалить')
        bot.register_next_step_handler(msg, admin_delete_case)




@bot.callback_query_handler(func=lambda call: call.data == "go")
def but1_pressed(call: types.CallbackQuery):
    # if call.message.chat.id == config.thank_you:


    #bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=config.start.format(functions.get_status()),
                            # reply_markup=keyboards.main_keys)

    bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=functions.get_img(), caption=config.start.format(functions.get_status())), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=keyboards.main_keys)


@bot.callback_query_handler(func=lambda call: call.data == "cases")
def but1_pressed(call: types.CallbackQuery):
    # if call.message.chat.id == config.thank_you:
    name = functions.get_cases()
    link = functions.get_links()


    cases_keyboard = types.InlineKeyboardMarkup(row_width=1)
    for x in range(len(name)):
        button = types.InlineKeyboardButton(
            text=name[x],
            url=link[x]
        )
        cases_keyboard.add(button)
    cases_keyboard.add(InlineKeyboardButton("⬅️", callback_data="go"))




    bot.edit_message_media(media=telebot.types.InputMedia(type='photo', media=functions.get_img(), caption=config.cases), chat_id=call.message.chat.id, message_id=call.message.message_id, reply_markup=cases_keyboard)


@bot.callback_query_handler(func=lambda call: call.data == "WhoAmI")
def but2_pressed(call: types.CallbackQuery):
    #bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                             #caption=functions.get_bio(),
                             #reply_markup=keyboards.go_back)

    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,media=telebot.types.InputMedia(type='photo', media=functions.get_img(),
                                                          caption=functions.get_bio()), reply_markup=keyboards.go_back)

@bot.callback_query_handler(func=lambda call: call.data == "Dialog")
def but3_pressed(call: types.CallbackQuery):
    #bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                             #caption=config.go_to_dialog, reply_markup=keyboards.go_back)

    bot.edit_message_media(chat_id=call.message.chat.id, message_id=call.message.message_id,media=telebot.types.InputMedia(type='photo', media=functions.get_img(),
                                                          caption=config.go_to_dialog), reply_markup=keyboards.go_back)


@bot.message_handler()
def send_poslanie(message: Message):
    if not message.chat.id == admin_id:
        message_worked = message.text
        message_sender = message.from_user.username
        bot.send_message(admin_id, f"Новое сообщение от @{message_sender}!\n\n{message_worked}",
                         reply_markup=keyboards.delete)
        bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        bot.send_message(chat_id=message.chat.id, text='Cпасибо за вопрос. Напишу сразу же, как освобожусь',
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
        bot.delete_message(message.chat.id, message.message_id - 1)
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


def admin_edit_bio(message):
    new_bio = message.text
    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE messages SET bio = ? where rowid = 1', [new_bio])

    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, text='Биография отредактирована', reply_markup=keyboards.delete)
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)

@bot.message_handler(content_types=["photo"])
def admin_edit_img(message):
    photo_id = message.photo[-1].file_id
    # Достаём картинку
    photo_file = bot.get_file(photo_id)  # <class 'telebot.types.File'>
    photo_bytes = bot.download_file(photo_file.file_path)  # <class 'bytes'>
    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()

    cursor.execute(f'UPDATE messages SET img = ? where rowid = 1', [photo_bytes])

    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, text='Фото отредактировано', reply_markup=keyboards.delete)
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)


def admin_add_case(message):
    case = message.text
    label, link = case.split('|')
    print(label)
    print(link)
    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT * FROM cases WHERE label = "{label}"').fetchall()

    if len(row) == 0:
        cursor.execute(
            f'INSERT INTO cases VALUES ("{label}", "{link}")')
        conn.commit()
    bot.send_message(message.chat.id, text='Кейс добавлен', reply_markup=keyboards.delete)
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)

def admin_delete_case(message):
    case = message.text
    conn = sqlite3.connect('auternous_bot.sqlite')
    cursor = conn.cursor()
    cursor.execute(f'DELETE FROM cases WHERE label = "{case}"')
    conn.commit()
    conn.close()
    bot.send_message(message.chat.id, text='Кейс удалён', reply_markup=keyboards.delete)
    bot.delete_message(message.chat.id, message.message_id)
    bot.delete_message(message.chat.id, message.message_id - 1)




if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
