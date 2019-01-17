# -*- coding: utf-8 -*-

import json


def write_json(data, filename='storage.json'):
    '''create json file from data to filename path'''
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def read_json(filename):
    '''read json file for filename path'''
    with open(filename, 'r') as f:
        return json.load(f)


def get_keyboard(telebot, item_list):
    '''create keyboard for telebot from item_list -> keyboard'''
    user_markup = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=True)
    for item in item_list:
        user_markup.row(item)
    return user_markup
