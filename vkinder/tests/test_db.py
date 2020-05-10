#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import unittest
from unittest.mock import patch


ids_from_db = []
result_search = []
searcher_id = ''
fixtures = os.path.join('vkinder', 'tests', 'fixtures.json')

with open(fixtures, encoding='utf8') as file:
    data_ = json.load(file)
    ids_from_db.extend(data_['ids_from_db'])
    result_search.extend(data_['result_search'])
    searcher_id += data_['searcher_id']


class DBTestCase(unittest.TestCase):
    @classmethod
    @patch('vkinder.interactions.searcher_id', searcher_id, create=True)
    def setUpClass(cls) -> None:
        import vkinder.db.methods as methods
        import vkinder.db.objects as objects
        cls.methods = methods
        cls.objects = objects
        cls.methods.create_table()

    def test_01_clear_db(self):
        self.assertEqual(bool(self.methods.list_ids()), False)

    def test_02_type(self):
        self.assertIsInstance(self.methods.list_ids(), list)

    def test_03_add_to_table(self):
        self.assertEqual(self.methods.add_rows(result_search), 'OK')

    def test_04_exists_row(self):
        self.assertSetEqual(set(self.methods.list_ids()), set(ids_from_db))

    def test_05_delete_table(self):
        self.methods.delete_rows()

    def test_06_clear_db(self):
        self.assertEqual(bool(self.methods.list_ids()), False)

    @classmethod
    def tearDownClass(cls) -> None:
        cls.methods.close_connect()


if __name__ == '__main__':
    unittest.main()
