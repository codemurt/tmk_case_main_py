from util import *
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
from os import getenv
import logging

load_dotenv()

bot_token = getenv('BOT_TOKEN')
bot = TeleBot(bot_token)
val_manager = ValManager(4 * 60 * 60)
metal_manger = MetalManager(4 * 60 * 60)

logging.basicConfig(filemode='a', level=logging.INFO)

@bot.message_handler(commands = ["start"])
def start(message):
    markup = InlineKeyboardMarkup()
    btn1 = InlineKeyboardButton('Курс валюты', callback_data='currency')
    btn2 = InlineKeyboardButton('Курс металла', callback_data='metal')
    markup.add(btn1, btn2)
    logging.info(f'Start: {time.asctime()}. Message: {message}')
    bot.send_message(message.from_user.id, "Выберите что вы хотите узнать?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "currency":
        markup_val = InlineKeyboardMarkup()
        cny_button = InlineKeyboardButton('🇨🇳 к 🇷🇺', callback_data='yuan')
        dollar_button = InlineKeyboardButton('🇺🇸 к 🇷🇺', callback_data='dollar')
        markup_val.add(cny_button, dollar_button)
        bot.send_message(call.message.chat.id, "Выберите валюты", reply_markup=markup_val)
    elif call.data == "metal":
        markup_metal = InlineKeyboardMarkup()
        steel_button = InlineKeyboardButton('Стоимость стали', callback_data='steel')
        cast_iron_button = InlineKeyboardButton('Стоимость чугуна', callback_data='cast_iron')
        markup_metal.add(steel_button, cast_iron_button)
        bot.send_message(call.message.chat.id, "Выберите металл", reply_markup=markup_metal)
    elif call.data == "yuan":
        valute = val_manager.get_data('CNY')
        if valute is not None:
            bot.send_message(call.message.chat.id, f"Текущий курс Юаня к Рублю:\n1 юань = {valute} руб.")
        else:
            bot.send_message(call.message.chat.id, "Данные не найдены. Извините")
    elif call.data == "dollar":
        valute = val_manager.get_data('USD')
        if valute is not None:
            bot.send_message(call.message.chat.id, f"Текущий курс Доллара к Рублю:\n1 доллар = {valute} руб.")
        else:
            bot.send_message(call.message.chat.id, "Данные не найдены. Извините")
    elif call.data == "steel":
        valute = metal_manger.get_data('STL')
        if valute is not None:
            bot.send_message(call.message.chat.id, f"Текущий курс стали: {valute}, $/т")
        else:
            bot.send_message(call.message.chat.id, "Данные не найдены. Извините")

    elif call.data == "cast_iron":
        valute = metal_manger.get_data('IRN')
        if valute is not None:
            bot.send_message(call.message.chat.id, f"Текущий курс чугуна: {valute} $/т., exw, внутр. цены России, без НДС")
        else:
            bot.send_message(call.message.chat.id, "Данные не найдены. Извините")

    logging.info(f'Callback_query: {time.asctime()}. Callback: {call.data}')

if __name__ == "__main__":
    bot.infinity_polling()