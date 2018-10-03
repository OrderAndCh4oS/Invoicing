import os
import sqlite3
from abc import ABCMeta

from invoicing.settings import DB


class Sqlite3Database(metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    def __init__(self):
        if not os.path.isfile(DB):
            raise OSError("Template was not found: " + DB)
        self.connection = sqlite3.connect(DB)
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
