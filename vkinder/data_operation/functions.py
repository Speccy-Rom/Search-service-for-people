#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from vkinder.common_functions import translate_auto


def delete_exist_id(list_dicts, list_id):
    data = []
    for dict_ in list_dicts:
        if dict_['id'] not in list_id:
            data.append(dict_)
    return data


def delete_stop(list_):
    list_result = []
    stop_list = ['него', 'а', 'ж', 'нее', 'со', 'без', 'же', 'ней', 'так', 'за', 'такой', 'будет',  'ни', 'там',
                 'будто', 'здесь', 'нибудь', 'бы', 'и', 'тем', 'из', 'ним', 'из-за', 'них', 'то', 'были',
                 'или', 'ничего', 'тогда', 'им', 'но', 'но', 'того', 'ну', 'тоже', 'в', 'их', 'о', 'вам', 'к', 'об',
                 'вас', 'тот', 'он', 'три', 'ведь', 'какая', 'тут', 'во', 'какой', 'вот', 'у', 'впрочем',
                 'от', 'уж', 'которого', 'перед', 'уже', 'которые', 'по', 'кто', 'под', 'хоть', 'куда', 'после',
                 'чего', 'всю', 'ли', 'потому', 'чем', 'г', 'между', 'почти', 'через', 'где', 'при', 'что', 'мне',
                 'про', 'чтоб', 'да', 'чтобы', 'даже', 'чуть', 'два', 'можно', 'с', 'для', 'мой', 'до', 'другой',
                 'этом', 'его', 'на', 'этот', 'ее', 'над', 'эту', 'ей', 'надо', 'ему', 'если', 'том', 'не']
    for word in list_:
       if word.lower() not in stop_list:
           list_result.append(word)
    return list_result


def delete_space(list_set):
    list_result = []
    for i in list_set:
        if (len(i) > 0) & (i not in ['-', '—', '!', '"', "'", '`']):
            list_result.append(i)
    return list_result


def delete_end_of_word(list_):
    list_result = []
    for word in list_:
        if len(word) in [4, 5,]:
            list_result.append(word[:-1])
        elif len(word) >= 6:
            list_result.append(word[:-2])
    return list_result


def str_to_list(string):
    if string:
        pattern_cirill = r'[а-я]{4,}'
        if re.findall(pattern_cirill, string, re.I):
            str_ = string
        else:
            str_ = translate_auto(string)
        pattern = r'\s|[^\w^-]|_'
        list_ = re.split(pattern, str_.lower())
        list_ = delete_end_of_word(list_)
        set_ = set(list_)
        list_ = delete_space(set_)
        list_ = delete_stop(list_)
        return list_
    else:
        return []
