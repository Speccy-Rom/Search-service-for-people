#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from pprint import pprint
from datetime import datetime
from vkinder.vk.objects import UserFound, UserSearcher
from vkinder.common_functions import init_variable, YES, get_top_ids, write_json


def print_n_write(list_dicts):
    from vkinder.db.methods import add_rows
    print('\n   <<< ТОП ПО ВЕРСИИ VKINDER >>>\n')
    pprint(list_dicts)
    filename = f'top_for_searcher_{searcher_id}_{datetime.now().strftime("%Y.%m.%d_%H-%M-%S")}.json'
    path = os.path.join('vkinder', 'db', 'result')
    write_json(list_dicts, filename, path)
    add_rows(list_dicts)
    print('\n   -= Результаты поиска записаны в БД =-\n')


def show_top(dict_):
    result = dict_
    while True:
        if len(result) > 10:
            top_ids = get_top_ids(result)
            for key in result:
                if key in top_ids:
                    result.pop(key)
            top_list = [UserFound(vk_cursor, user_id).__dict__() for user_id in top_ids]
            print_n_write(top_list)
            answer = input('Показать остальных найденных? (да/нет) - ')
            if answer in YES:
                continue
            else:
                break
        else:
            top_list = [UserFound(vk_cursor, user_id).__dict__() for user_id in get_top_ids(result)]
            print_n_write(top_list)
            break


def run():
    global vk_cursor, searcher_id
    while True:
        try:
            vk_ = init_variable()
            vk_cursor = vk_.get_api()
            searcher_id = vk_cursor.users.get()[0]['id']
        except Exception as err:
            continue
        else:
            break
    iam = UserSearcher(vk_cursor, searcher_id)
    data_ = iam.search()
    reference = iam.__dict__()
    print('\nАнализ совпадения по группам даст более релевантный результат.'
          '\nНО это займет больше времени (до 50 минут).')
    answer = input('Используем для анализа совпадение по группам? (да/нет) - ')
    print('Анализируем...')
    from vkinder.data_operation.analise import Analise
    from vkinder.db.methods import create_table, list_ids, close_connect
    create_table()
    analise = Analise(data_, list_ids(), reference, vk_cursor)
    if answer in YES:
        analise.vote_groups()
    else:
        analise.vote_friends_mutual()
    result = analise.result()
    if result:
        show_top(result)
        close_connect()
        print('Поиск окончен.')
    else:
        close_connect()
        print('Поиск не дал результатов.')


def hello():
    '''
    1. Поиск партнера в vk.com
    9. Вывод справки.
    0. Выйти из программы.
    '''
    good_bye = '\n\n   Надеемся Вам очень понравилась наша программа!' \
               '\n   Вопросы и предложения присылайте по адресу: web-cpv.ru' \
               '\n   ДОСВИДАНИЯ!\n'
    print('\n\nДобро пожаловать в "Vkinder"'.upper())
    print('\n   Вам необходимо ввести цифру ниже, чтобы программа выполнила действие: '
          '\n   (для справки введите 9)')
    try:
        while True:
            prog = str(input(f'\n{"=" * 80}'
                             '\n\n  номер действия:  '.upper()))
            if prog == '1':
                run()
            elif prog == '9':
                print(hello.__doc__)
            elif prog == '0':
                print(good_bye)
                break
            else:
                print('\nТакой функционал программы пока не подвезли)))'
                      '\nЕсть предложения? Пишите по адресу: web-cpv.ru')
    except KeyboardInterrupt:
        print(good_bye)
