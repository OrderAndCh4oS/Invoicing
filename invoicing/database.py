import sqlite3


class Database:
    def __init__(self, database):
        self.db = sqlite3.connect(database)

    def getDB(self):
        return self.db