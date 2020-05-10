#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
from datetime import datetime
from vkinder.common_functions import YES, translate


def bdate_to_age(bdate):
    '''превращаем дату рождения в возраст полных лет'''
    date_list = bdate.split('.')
    birth_date = datetime(year=int(date_list[2]), month=int(date_list[1]), day=int(date_list[0]))
    age = (datetime.now() - birth_date).days // 365
    return age


def find_country():
    '''ищем страну для определения города'''
    list_country = []
    path = os.path.join('vkinder', 'vk', 'countries.json')
    with open(path) as file:
        list_country.extend(json.load(file))
    your_country = input('\nПожалуйста, введите страну (на английском): ').lower()
    for country in list_country:
        if your_country in country['Name'].lower():
            find_country_ = country['Code']
            print(f'Выбрана: {country["Name"]}.')
            return find_country_
        else:
            print('По-умолчанию выбрана: Russian Federation.')
            return 'RU'


def find_city(cursor):
    '''определяем город для поиска'''
    try:
        id_country = cursor.database.getCountries(code=find_country())['items'][0]['id']
    except Exception as err:
        print(translate('Error in input. Detailed: '), translate(str(err)), '\n',
              translate('Set to default city Moscow.'))
        return 1
    else:
        your_city = input('Введите город: ').lower()
        try:
            id_city = cursor.database.getCities(country_id=id_country, q=your_city)['items'][0]
        except Exception as err:
            print(translate('Error in input. Detailed: '), translate(str(err)), '\n',
                  translate('Set to default city Moscow.'))
            return 1
        else:
            answer = input(f'Ваш выбор {id_city["title"]}? (да/нет) - ').lower()
            if answer in YES:
                return id_city['id']
            else:
                print('Поздравляю! По-умолчанию выбран город Москва! ))))')
                return 1


def age_determination(age=None):
    if age:
        start, stop = [(age - 2), (age + 2)]
        answer = input(f'\nИщем партнера с {start} до {stop} лет/года? (да/нет) - ').lower()
        if answer in YES:
            print('Отлично.')
            return [start, stop]
        else:
            age_from = int(input('Начиная с какого возраста ищем партнера? (целое число) - '))
            age_to = int(input('До какого возраста ищем партнера? (целое число) - '))
            return [age_from, age_to]
    else:
        age_from = int(input('Начиная с какого возраста ищем партнера? (целое число) - '))
        age_to = int(input('До какого возраста ищем партнера? (целое число) - '))
        return [age_from, age_to]


def gender_determination(integer):
    '''определяем пол кого будем искать'''
    alert = 'Начинаем поиск...'
    list = [0, 'девушку/женщину', 'парня/мужчину']
    sex_inverse = {1: 2, 2: 1}
    value = sex_inverse.pop(integer)
    answer = input(f'\nВы ищете {list.pop(value)}? (да/нет) - ').lower()
    if answer in YES:
        print(alert)
        return value
    else:
        answer2 = input(f'Вы ищете {list.pop(1)}??.. (да/нет) - ').lower()
        if answer2 in YES:
            print(alert)
            return sex_inverse.values().__iter__().__next__()
        else:
            print(alert)
            return list[0]



def select_getinfo():
    while True:
        select = input('\nВыберем как будем искать.\n'
                       '   1 - ищем партнера исходя из информации о Вас (при отсутствии дополним)\n'
                       '   2 - ищем по описанным Вами параметрам (ключевым словам)\nВыбор: ').strip()
        if int(select) in [1, 2]:
            return int(select)
        else:
            continue


def metadata_found(cursor):
    print('\n   В качестве ответов на открытые вопросы можете вводить ключевые слова.\n'
          '   При отсутствии ответа вводите пробел.\n'
          '   НО ПОМНИТЕ: чем больше ключевых слов - тем интереснее результат ))')
    meta = {
        'age_from': int(input('Начиная с какого возраста ищем партнера? (целое число) - ')),
        'age_to': int(input('До какого возраста ищем партнера? (целое число) - ')),
        'city': find_city(cursor),
        'activities': input('Какова деятельность искомого партнера? - '),
        'interests': input('Каковы интересы искомого партнера? - '),
        'about': input('Что интересно в поле "О себе" у искомого партнера? - '),
        'books': input('Какие книги интересны искомому партнеру? - '),
        'movies': input('Какие фильмы интересны искомому партнеру? - '),
        'music': input('Какая музыка/исполнители интересны искомому партнеру? - '),
        'games': input('Какие игры интересны искомому партнеру? - '),
        'tv': input('Какие ТВ-шоу интересны искомому партнеру? - '),
        'quotes': input('Какие цитаты могут понравиться искомому партнеру? - '),
        'status': input('Что интересного может указать партнер в статусе? - '),
    }
    return meta


def max_value_likes_photo(list_):
    index = 0
    photo_id = None
    for dict_ in list_:
        count = dict_['likes']['count']
        if index < count:
            index = count
            photo_id = dict_['id']
            continue
    return photo_id


def get_top_urls(list_):
    list_photos = []
    index = 0
    while index < 3:
        photo_id = max_value_likes_photo(list_)
        for photo in list_:
            if photo['id'] == photo_id:
                for sizes in photo['sizes']:
                    if sizes['type'] == 'x':
                        list_photos.append(sizes['url'])
                        list_.remove(photo)
        index += 1
    return list_photos
