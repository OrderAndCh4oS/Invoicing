from repository.base_repository import BaseRepository


class StatusRepository(BaseRepository):
    def find_all(self):
        self.cursor.execute('select id, title, colour from status')
        return self.get_all()

    def find_by_id(self, id):
        self.cursor.execute('select id, title, colour from status where id = ?', (id,))
        return self.get_one()

    def insert_status(self, title, colour):
        self.cursor.execute(
            'insert into status (title, colour) values (?, ?)',
            (title, colour)
        )

    def update_status(self, id, title, colour):
        self.cursor.execute(
            'update status set title = ?, colour = ? where id = ?',
            (title, colour, id)
        )

    def remove_status(self, id):
        self.cursor.execute('delete from status where id = ?', (id,))
