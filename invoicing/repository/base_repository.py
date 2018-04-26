import sqlite3
from abc import ABCMeta, abstractmethod

from database import Database


class BaseRepository(metaclass=ABCMeta):
    __metaclass__ = ABCMeta

    # Todo: Not great, initialises a connection for every instance of crud classes
    # Todo: DB may not be found after pip install
    def __init__(self):
        self.connection = Database('../Invoicing.db').getDB()
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

    def check_rows_updated(self, message):
        if self.has_updated_rows() > 0:
            print(message + '\n')
        else:
            print('Error performing update, please try again')

    def get_description(self):
        return self.cursor.description

    @abstractmethod
    def find_all(self):
        pass

    @abstractmethod
    def find_by_id(self, id):
        pass
