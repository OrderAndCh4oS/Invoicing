from database import Database


class BaseRepository:
    def __init__(self):
        self.connection = Database('../Invoicing.db').getDB()
        self.cursor = self.connection.cursor()

    def has_updated_rows(self):
        return self.connection.total_changes > 0

    def close_connection(self):
        self.connection.close()

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