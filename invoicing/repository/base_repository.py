import os
import sqlite3
from abc import ABCMeta

from database import Database
from query_builder.query_builder import QueryBuilder


class BaseRepository(metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    # Todo: Not great, initialises a connection for every instance of crud classes
    # Todo: DB may not be found after a pip install (maybe will now using os.path)
    # Todo: Write a Dependency Injection/Services class
    def __init__(self, table):
        self.table = table
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(BASE_DIR, "../../Invoicing.db")
        self.connection = Database(db_path).getDB()
        self.connection.row_factory = sqlite3.Row
        self.cursor = self.connection.cursor()

    def __exit__(self):
        self.connection.close()

    def has_updated_rows(self):
        return self.connection.total_changes > 0

    def save(self):
        self.connection.commit()

    def get_all(self):
        self.connection.commit()
        return self.cursor.fetchall()

    def get_one(self):
        self.connection.commit()
        return self.cursor.fetchone()

    def get_headers(self):
        return list(map(lambda x: x[0], self.cursor.description))

    def check_rows_updated(self, message):
        if self.has_updated_rows() > 0:
            print('\n' + message)
        else:
            print('\nError performing update, please try again')

    def get_description(self):
        return self.cursor.description

    def execute(self, sql='', parameters=()):
        self.cursor.execute(sql, parameters)

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
