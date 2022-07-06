#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
from peewee import Model
from datetime import datetime
from vkinder.interactions import searcher_id
from playhouse.sqlite_ext import SqliteExtDatabase
from peewee import AutoField, TextField, DateTimeField, IntegerField, CharField


path_db = os.path.join('vkinder', 'db', 'vkinder.db')
db = SqliteExtDatabase(path_db, pragmas={
    'journal_mode': 'wal',
    'cache_size': -64 * 1000,
    'synchronous': 0})
table = f'searcher_{searcher_id}'


class Vkinder(Model):
    class Meta:
        database = db


class Searcher(Vkinder):
    id = AutoField()
    user_id = IntegerField(null=False, unique=True)
    name = CharField(null=False)
    page_url = CharField(null=False)
    top_photo = TextField(null=False)
    date_search = DateTimeField(default=datetime.now())

    class Meta:
        table_name = table
        name = table