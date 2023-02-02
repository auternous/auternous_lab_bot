from telebot import TeleBot, types
import config
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from telebot.types import Message


first_step = InlineKeyboardMarkup()
first_step.add(InlineKeyboardButton("🤍", callback_data="go"))

main_keys = InlineKeyboardMarkup()
main_keys.add(InlineKeyboardButton(text=config.button_bio, callback_data="WhoAmI"))
main_keys.add(InlineKeyboardButton(text=config.button_go_to_dialog, callback_data="Dialog"))
main_keys.add(InlineKeyboardButton(text=config.button_link, url=config.link))

go_back = InlineKeyboardMarkup()
go_back.add(InlineKeyboardButton("⬅️", callback_data="go"))

delete = InlineKeyboardMarkup()
delete.add(InlineKeyboardButton("❌", callback_data="close"))