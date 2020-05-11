#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tqdm._main import tqdm
from vkinder.vk.objects import UserVK
from vkinder.data_operation.functions import delete_exist_id, str_to_list


class Analise:
    weights = {
        'activities': 14,
        'about': 12,
        'interests': 16,
        'music': 12,
        'movies': 5,
        'tv': 1,
        'books': 11,
        'games': 4,
        'quotes': 6,
        'status': 5,
        'groups': 10,
        'common_count': 4,
    }
    vote = {}

    def __init__(self, list_dicts, ids_from_db, reference, cursor):
        self.tqdm = tqdm(desc='Magic', total=1, unit=' lucks', leave=False)
        self.data = delete_exist_id(list_dicts, ids_from_db)
        self.reference = reference
        self.cursor = cursor

    def vote_put(self):
        for key_ in self.weights.keys():
            if key_ in ['common_count', 'groups']:
                continue
            else:
                list_searcher = str_to_list(self.reference[key_])
                for dict_ in self.data:
                    self.tqdm.update(3)
                    try:
                        list_found = str_to_list(dict_[key_])
                    except Exception as err:
                        continue
                    else:
                        for word in list_searcher:
                            if word in list_found:
                                self.tqdm.update(5)
                                try:
                                    tmp = self.vote[dict_['id']]
                                except KeyError as err:
                                    self.vote[dict_['id']] = self.weights[key_]
                                else:
                                    self.vote[dict_['id']] += self.weights[key_]

    def vote_friends_mutual(self):
        self.vote_put()
        for dict_ in self.data:
            self.tqdm.update(2)
            try:
                friends = dict_['common_count']
            except Exception as err:
                continue
            else:
                if friends:
                    self.tqdm.update(6)
                    try:
                        tmp = self.vote[dict_['id']]
                    except KeyError as err:
                        self.vote[dict_['id']] = (self.weights['common_count'] * friends)
                    else:
                        self.vote[dict_['id']] += (self.weights['common_count'] * friends)

    def vote_groups(self):
        self.vote_friends_mutual()
        set_searcher = set(self.reference['groups'])
        for dict_ in self.data:
            self.tqdm.update(11)
            if dict_['is_closed'] & (not dict_['can_access_closed']):
                self.tqdm.update(1)
                continue
            else:
                self.tqdm.update(7)
                set_found = set(UserVK(self.cursor, dict_['id']).groups)
                count_groups = len(set_searcher.intersection(set_found))
                if count_groups:
                    self.tqdm.update(16)
                    try:
                        tmp = self.vote[dict_['id']]
                    except KeyError as err:
                        self.vote[dict_['id']] = (self.weights['groups'] * count_groups)
                    else:
                        self.vote[dict_['id']] += (self.weights['groups'] * count_groups)
      
    def result(self):
      self.tqdm.close()
      return self.vote

