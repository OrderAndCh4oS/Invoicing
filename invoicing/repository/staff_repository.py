from repository.base_repository import BaseRepository


class StaffRepository(BaseRepository):
    def find_all(self):
        self.cursor.execute('select id, first_name, last_name, job_title, rate from staff')
        return self.get_all()

    def find_by_id(self, id):
        self.cursor.execute('select id, first_name, last_name, job_title, rate from staff where id = ?', (id,))
        return self.get_one()

    def insert_staff(self, first_name, last_name, job_title, rate):
        self.cursor.execute(
            'insert into staff (first_name, last_name, job_title, rate) values (?, ?, ?, ?)',
            (first_name, last_name, job_title, rate)
        )

    def update_staff(self, id, first_name, last_name, job_title, rate):
        self.cursor.execute(
            'update staff set first_name = ?, last_name = ?, job_title = ?, rate = ? where id = ?',
            (first_name, last_name, job_title, rate, id)
        )

    def remove_staff(self, id):
        self.cursor.execute('delete from staff where id = ?', (id,))
