# -*- coding: utf-8 -*-

import logging
import telebot
import config
from flask import Flask
from flask import request
from helpers import read_json, get_keyboard


logging.basicConfig(filename="file.log", level=logging.INFO)
log = logging.getLogger("ex")


app = Flask(__name__)
API_TOKEN = config.TOKEN
bot = telebot.TeleBot(API_TOKEN)
storage = read_json('storage.json')


@app.route('/', methods=['POST', 'GET'])
def web_hook():
    if request.method == 'POST':
        if request.headers.get('content-type') == 'application/json':
            json_string = request.get_data().decode('utf-8')
            update = telebot.types.Update.de_json(json_string)
            bot.process_new_updates([update])
            return ''
        else:
            request.abort(403)
    return ''


# start process by step to choice country
@bot.message_handler(commands=['help', 'start'])
def process_choice_country(message):
    try:
        if message.text != '/start':
            msg = bot.reply_to(message, 'Выберите пожалуйста вариант из меню')
            bot.register_next_step_handler(msg, process_choice_country)
            return
        user_markup = get_keyboard(telebot=telebot, item_list=storage['country'])
        msg = bot.reply_to(message, 'Выберите страну для визита', reply_markup=user_markup)
        bot.register_next_step_handler(msg, process_choice_date)
    except Exception as e:
        log.exception(e)
        bot.reply_to(message, 'Введите команду /help')


# process by step to choice date
def process_choice_date(message):
    try:
        msg = bot.reply_to(message, 'Введите дату вылета в формате 01-01-2001')
        bot.register_next_step_handler(msg, process_choice_count)
    except Exception as e:
        log.exception(e)
        bot.reply_to(message, 'Введите команду /help')


# process by step to choice nights count
def process_choice_count(message):
    try:
        user_markup = get_keyboard(telebot=telebot, item_list=storage['nights_count'])
        msg = bot.reply_to(message, 'Выберите количество ночей', reply_markup=user_markup)
        bot.register_next_step_handler(msg, process_choice_budget)
    except Exception as e:
        log.exception(e)
        bot.reply_to(message, 'Введите команду /help')


# process by step to choice budget
def process_choice_budget(message):
    try:
        user_markup = get_keyboard(telebot=telebot, item_list=storage['budget'])
        msg = bot.reply_to(message, 'Выберите бюджет на человека', reply_markup=user_markup)
        bot.register_next_step_handler(msg, process_send_number)
    except Exception as e:
        log.exception(e)
        bot.reply_to(message, 'Введите команду /help')


# process by step to send number
def process_send_number(message):
    try:
        keyboard = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
        reg_button = telebot.types.KeyboardButton(text="Поделиться своим номером телефона", request_contact=True)
        keyboard.add(reg_button)
        msg = bot.reply_to(message, 'Поделитесь номером', reply_markup=keyboard)
        bot.register_next_step_handler(msg, process_choice_end)
    except Exception as e:
        log.exception(e)
        bot.reply_to(message, 'Введите команду /help')


# process by step to end all choices
def process_choice_end(message):
    try:
        user_markup = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
        user_markup.row('/start')
        bot.reply_to(message, 'Заявка принята! Оператор свяжется С Вами в ближайшее время')
        bot.reply_to(message, 'Для нового заказа введите команду /start', reply_markup=user_markup)
    except Exception as e:
        log.exception(e)
        bot.reply_to(message, 'Введите команду /help')


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()

if __name__ == '__main__':
    app.run()
