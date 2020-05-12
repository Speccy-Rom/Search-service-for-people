#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from tqdm._main import tqdm
from vkinder.vk.functions import gender_determination, age_determination, bdate_to_age
from vkinder.vk.functions import select_getinfo, find_city, metadata_found, get_top_urls


fields_searcher = 'domain,sex,bdate,activities,interests,books,about,status,music,movies,quotes,city'
fields_found = 'domain,activities,interests,games,books,about,status,music,movies,tv,quotes,common_count'


class UserVK:
    def __init__(self, cursor, id_):
        self.cursor = cursor
        self.resp = self.cursor.users.get(user_ids=id_, fields=fields_searcher)[0]
        if 'deactivated' in self.resp.keys():
            self.delete = True
            self.close = True
            self.can_access_closed = False
        elif self.resp['is_closed'] & (not self.resp['can_access_closed']):
            self.close = True
            self.can_access_closed = False
            self.delete = False
        elif self.resp['is_closed'] & self.resp['can_access_closed']:
            self.close = True
            self.can_access_closed = True
            self.delete = False
        else:
            self.can_access_closed = True
            self.close = False
            self.delete = False
        self.user_id = self.resp['id']
        self.family = self.resp['last_name']
        self.name = self.resp['first_name']
        self.domain = self.resp['domain']
        self.fio = self.name + ' ' + self.family
        self.url = f'https://vk.com/{self.domain}'
        self.sex = self.resp['sex']
        if self.delete or (self.close & (not self.can_access_closed)):
            self.groups = []
        else:
            self.groups = self.cursor.groups.get(user_id=id_, count=1000)['items']


class UserSearcher(UserVK):
    def about_searcher(self):
        ''' semi-automatic filling '''
        keys_ = self.resp.keys()
        if 'bdate' in keys_:
            self.bdate = self.resp['bdate']
            self.age = bdate_to_age(self.bdate)
        else:
            self.age = int(input('Сколько Вам полных лет? - '))
        self.age_start, self.age_stop = age_determination(self.age)
        if 'city' in keys_:
            self.city = self.resp['city']['id']
        else:
            self.city = find_city(self.cursor)
        print()
        if 'activities' in keys_:
            self.activities = self.resp['activities']
        else:
            self.activities = input('Какова Ваша деятельность? - ')
        if 'interests' in keys_:
            self.interests = self.resp['interests']
        else:
            self.interests = input('Каковы Ваши интересы? - ')
        if 'about' in keys_:
            self.about = self.resp['about']
        else:
            self.about = input('Что Вы бы указали в поле "О себе"? - ')
        if 'books' in keys_:
            self.books = self.resp['books']
        else:
            self.books = input('Какие книги Вам интересны? - ')
        if 'movies' in keys_:
            self.movies = self.resp['movies']
        else:
            self.movies = input('Какие фильмы Вам интересны? - ')
        if 'music' in keys_:
            self.music = self.resp['music']
        else:
            self.music = input('Какая музыка/исполнители интересны Вам? - ')
        if 'games' in keys_:
            self.games = self.resp['games']
        else:
            self.games = input('В какие игры Вы играете? - ')
        if 'tv' in keys_:
            self.tv = self.resp['tv']
        else:
            self.tv = input('Какие ТВ-шоу Вы смотрите? - ')
        if 'quotes' in keys_:
            self.quotes = self.resp['quotes']
        else:
            self.quotes = input('Какие цитаты Вам нравятся? - ')
        if 'status' in keys_:
            self.status = self.resp['status']
        else:
            self.status = input('Какой статус Вы установили бы? - ')

    def about_found(self):
        ''' manual filling '''
        meta = metadata_found(self.cursor)
        self.city = meta['city']
        self.interests = meta['interests']
        self.movies = meta['movies']
        self.books = meta['books']
        self.music = meta['music']
        self.games = meta['games']
        self.quotes = meta['quotes']
        self.age_start = meta['age_from']
        self.age_stop = meta['age_to']
        self.activities = meta['activities']
        self.about = meta['about']
        self.tv = meta['tv']
        self.status = meta['status']

    def search(self):
        ''' sum the most important criteria return up to 4800 unique people (not friend):
            sort: 0 - populate, 1 - registered
            status: 6 - active search, 1 - not married
        '''
        select = select_getinfo()
        if select == 1:
            self.about_searcher()
        elif select == 2:
            self.about_found()
        sex_target = gender_determination(self.sex)
        self.tqdm = tqdm(desc='Magic', total=1, unit=' lucks', leave=False)
        response = []
        resp1 = self.cursor.users.search(
            count=1000,
            age_from=self.age_start,
            age_to=self.age_stop,
            sex=sex_target,
            city=self.city,
            has_photo=1,
            fields=fields_found,
            is_friend=0,
            sort=1,
            status=6,
        )
        response.extend(resp1['items'])
        self.tqdm.update(13)
        resp2 = self.cursor.users.search(
            count=1000,
            age_from=self.age_start,
            age_to=self.age_stop,
            sex=sex_target,
            city=self.city,
            has_photo=1,
            fields=fields_found,
            is_friend=0,
            sort=0,
            status=6,
        )
        response.extend(resp2['items'])
        self.tqdm.update(13)
        resp3 = self.cursor.users.search(
            count=1000,
            age_from=self.age_start,
            age_to=self.age_stop,
            sex=sex_target,
            city=self.city,
            has_photo=1,
            fields=fields_found,
            is_friend=0,
            sort=1,
            status=1,
        )
        response.extend(resp3['items'])
        self.tqdm.update(13)
        resp4 = self.cursor.users.search(
            count=1000,
            age_from=self.age_start,
            age_to=self.age_stop,
            sex=sex_target,
            city=self.city,
            has_photo=1,
            fields=fields_found,
            is_friend=0,
            sort=0,
            status=1,
        )
        response.extend(resp4['items'])
        self.tqdm.update(13)
        resp5 = self.cursor.users.search(
            count=1000,
            age_from=self.age_start,
            age_to=self.age_stop,
            sex=sex_target,
            city=self.city,
            has_photo=1,
            fields=fields_found,
            is_friend=0,
            sort=1,
            status=6,
        )
        response.extend(resp5['items'])
        self.tqdm.update(13)
        resp6 = self.cursor.users.search(
            count=1000,
            age_from=self.age_start,
            age_to=self.age_stop,
            sex=sex_target,
            city=self.city,
            has_photo=1,
            fields=fields_found,
            is_friend=0,
            sort=0,
            status=6,
        )
        response.extend(resp6['items'])
        self.tqdm.close()
        return response

    def __dict__(self):
        return {
            'about': self.about,
            'activities': self.activities,
            'books': self.books,
            'interests': self.interests,
            'movies': self.movies,
            'music': self.music,
            'quotes': self.quotes,
            'games': self.games,
            'tv': self.tv,
            'groups': self.groups,
            'status': self.status,
        }


class UserFound(UserVK):
    def top_photo(self):
        self.photos = self.cursor.photos.get(user_id=self.user_id, album_id='profile',
                                             extended=1, photo_sizes=1, rev=1)
        list_photos = []
        if self.photos['count'] > 3:
            list_photos.extend(get_top_urls(self.photos['items']))
        else:
            for photo in self.photos['items']:
                for sizes in photo['sizes']:
                    if sizes['type'] == 'x':
                        list_photos.append(sizes['url'])
        return list_photos

    def __dict__(self):
        return {
            'user_id': self.user_id,
            'name': self.fio,
            'page_url': self.url,
            'top_photo': self.top_photo(),
        }
