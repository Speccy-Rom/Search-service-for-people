#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from peewee import InternalError, IntegrityError
from vkinder.db.objects import db, Searcher, path_db


def create_file_db():
    if not os.path.exists(path_db):
        open(path_db, "w").close()


def create_table():
    '''check exist table'''
    create_file_db()
    try:
        db.connect()
        Searcher.create_table()
    except InternalError as err:
        return err
    else:
        return 'ok'


def add_rows(list_dicts):
    '''write result to db'''
    error = ''
    for dict_ in list_dicts:
        row = Searcher(
            user_id=dict_['user_id'],
            name=dict_['name'],
            page_url=dict_['page_url'],
            top_photo=' | '.join(dict_['top_photo'])
        )
        try:
            row.save()
        except IntegrityError as err:
            error += f'{err}\n'
            continue
    return f'Was detected warnings.\n{error}' if error else 'OK'


def list_ids():
    '''list ids for check exist id'''
    column = Searcher.select(Searcher.user_id)
    return [data.user_id for data in column]


def delete_rows():
    execute = Searcher.delete().where(Searcher.user_id in list_ids())
    return execute.execute()


def close_connect():
    return db.close()
