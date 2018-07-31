from abc import ABCMeta

from database.sqlite3 import Sqlite3Database
from query_builder.query_builder import QueryBuilder


class BaseRepository(Sqlite3Database, metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    def __init__(self, table):
        super().__init__()
        self.table = table

    def find_all(self, select=('*')):
        query = QueryBuilder(self.table) \
            .select(select) \
            .from_()
        self.execute(**query.build())
        return self.get_all()

    def find_by_id(self, id, select=('*')):
        query = QueryBuilder(self.table) \
            .select(select) \
            .from_() \
            .where('id = ?', id)
        self.execute(**query.build())
        return self.get_one()

    def insert(self, values):
        query = QueryBuilder(self.table) \
            .insert(values)
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
