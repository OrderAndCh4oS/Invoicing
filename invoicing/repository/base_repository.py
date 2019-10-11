from abc import ABCMeta

from invoicing.database.sqlite3 import Sqlite3Database
from invoicing.query_builder.query_builder import QueryBuilder


class BaseRepository(Sqlite3Database, metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    def __init__(self, table):
        super().__init__()
        self.table = table

    def find_all(self, select='*'):
        query = QueryBuilder(self.table) \
            .select(select) \
            .from_()
        self.execute(**query.build())
        return self.get_all()

    def find_paginated(self, select='*', limit=10, page=1):
        query = QueryBuilder(self.table) \
            .select(select) \
            .from_() \
            .limit(limit) \
            .offset(page * limit - limit)
        self.execute(**query.build())
        return self.get_all()

    def find_by_id(self, id, select='*'):
        query = QueryBuilder(self.table) \
            .select(select) \
            .from_() \
            .where('id = ?', id)
        self.execute(**query.build())
        return self.get_one()

    def get_count(self):
        query = QueryBuilder(self.table) \
            .count() \
            .from_()
        self.execute(**query.build())
        return self.get_one()

    def find_last_inserted(self, select='*'):
        query = QueryBuilder(self.table) \
            .select(select) \
            .from_() \
            .where_id_is_last_inserted()
        self.execute(**query.build())
        return self.get_one()

    def insert(self, values):
        query = QueryBuilder(self.table) \
            .insert(values)
        self.execute(**query.build())

    def update_parent_foreign_keys(self, related_keys):
        """
        :param related_keys:  {"related_table": ("related_name", [1, 2, 3])}
        :return: []
        """
        last_id = self.cursor.lastrowid
        for related_table, relations in related_keys.items():
            for id in relations[1]:
                query = QueryBuilder(related_table) \
                    .update({relations[0]: last_id}) \
                    .where('id = ?', id)
                self.execute(**query.build())

    def update(self, id, set):
        query = QueryBuilder(self.table) \
            .update(set) \
            .where('id = ?', id)
        self.execute(**query.build())

    def remove(self, id):
        query = QueryBuilder(self.table) \
            .delete() \
            .where('id = ?', id)
        self.execute(**query.build())
