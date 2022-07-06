#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import getpass
import requests
from vkinder.vk.api import vk_login


YES = ['yes', 'y', 'да', 'д', 1, '1', 'lf', 'l', 'нуы']
NO = ['no', 'not', 'n', 'нет', 'н', 0, '0', 'ytn', 'тщ', 'тще']
URL = 'https://translate.yandex.net/api/v1.5/tr.json/translate'
KEY_API = 'trnsl.1.1.20190704T182934Z.17f33d8db55385c6.e6d41260c9ccabfba9197455fd6d6679fec9bf38'


def init_variable():
    two_factor = input('\nВы используете двухфакторную авторизацию? (да/нет) - ')
    login = str(input('Пожалуйста, введите логин (желательно номер телефона): '))
    password = getpass.getpass('Введите Ваш пароль и нажмите "Enter" (символы не отображаются): ')
    return (
        vk_login(login, password, True)
        if two_factor in YES
        else vk_login(login, password)
    )


def translate(text, from_='en', to='ru'):
    ''' translation text '''
    params = {
        'key': KEY_API,
        'text': text,
        'lang': f'{from_}-{to}',
    }
    response = requests.get(URL, params=params)
    return ''.join(response.json()['text'])


def translate_auto(text, to='ru'):
    ''' auto translation text '''
    params = {
        'key': KEY_API,
        'text': text,
        'lang': f'{to}',
        'options': 1,
    }
    response = requests.get(URL, params=params)
    return ''.join(response.json()['text'])


def max_value_of_keys(dict_):
    index = 0
    key_ = None
    for key in dict_.keys():
        if index < dict_[key]:
            index = dict_[key]
            key_ = key
            continue
    return key_


def get_top_ids(dict_):
    list_top_ids = []
    index = 0
    if len(dict_) < 10:
        for k in dict_.copy():
            key_ = max_value_of_keys(dict_)
            list_top_ids.append(key_)
            dict_.pop(key_)
            index += 1
    else:
        while index < 10:
            key_ = max_value_of_keys(dict_)
            list_top_ids.append(key_)
            dict_.pop(key_)
            index += 1
    return list_top_ids


def write_json(text, filename, path='', mode='wt'):
    if path:
        make_dir(path)
    out_file = os.path.join(path, f'{filename}')
    txt = json.dumps(text, sort_keys=True, indent=4, ensure_ascii=False)
    with open(out_file, mode=mode, encoding='utf8') as file:
        file.write(txt)
        
def make_dir(path):
    pwd = os.getcwd()
    if '\\' in path:
        lst = path.split('\\')
        for i in lst:
            if i not in os.listdir():
                os.mkdir(i)
            os.chdir(i)
    elif '/' in path:
        lst = path.split('/')
        for i in lst:
            if i not in os.listdir():
                os.mkdir(i)
            os.chdir(i)
    elif path not in os.listdir():
        os.mkdir(path)
    os.chdir(pwd)


