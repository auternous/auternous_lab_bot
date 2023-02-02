# -*- coding: utf-8 -*-
from telebot import TeleBot, types
import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message

admin_id = config.admin
bot = TeleBot(config.TOKEN)
photo_me = open(config.cover, 'rb')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    message_sender = message.from_user.username

    bot.send_photo(chat_id=message.chat.id, photo=photo_me,
                   caption=f"Привет, рад тебя видеть {message_sender}\nНажимай на 🤍 и давай познакомимся",
                   reply_markup=markup_1)



@bot.callback_query_handler(func=lambda call: call.data == "go")
def but1_pressed(call: types.CallbackQuery):
    # if call.message.chat.id == config.thank_you:

    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=config.start,
                             reply_markup=markup_main)


@bot.callback_query_handler(func=lambda call: call.data == "WhoAmI")
def but2_pressed(call: types.CallbackQuery):
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption=config.bio,
                             reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "Dialog")
def but3_pressed(call: types.CallbackQuery):
    bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id,
                             caption=config.go_to_dialog, reply_markup=markup)


@bot.message_handler()
def send_poslanie(message: Message):
    message_worked = message.text
    message_sender = message.from_user.username
    print(message.message_id - 1)
    bot.send_message(admin_id, f"Новое сообщение от @{message_sender}!\n\n{message_worked}")
    bot.delete_message(message.chat.id, message.message_id)
    bot.edit_message_caption(chat_id=message.chat.id, caption=config.thank_you,
                             reply_markup=markup)


markup_1 = InlineKeyboardMarkup()
markup_1.add(InlineKeyboardButton("🤍", callback_data="go"))

markup_main = InlineKeyboardMarkup()
markup_main.add(InlineKeyboardButton(text=config.button_bio, callback_data="WhoAmI"))

markup_main.add(InlineKeyboardButton(text=config.button_go_to_dialog, callback_data="Dialog"))
markup_main.add(InlineKeyboardButton(text=config.button_link, url=config.link))

markup = InlineKeyboardMarkup()
markup.add(InlineKeyboardButton("⬅️", callback_data="go"))

if __name__ == '__main__':
    bot.infinity_polling(skip_pending=True)
