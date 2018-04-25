from repository.base_repository import BaseRepository

class CompanyRepository(BaseRepository):
    def find_all(self):
        self.cursor.execute('select id, name, address from companies')
        return self.get_all()

    def find_by_id(self, id):
        self.cursor.execute('select id, name, address from companies where id = ?', (id,))
        return self.get_one()

    def insert_company(self, address, name):
        self.cursor.execute('insert into companies (name, address) values (?, ?)', (name, address))

    def update_company(self, id, name, address):
        self.cursor.execute('update companies set name = ?, address = ? where id = ?', (name, address, id))

    def remove_company(self, id):
        self.cursor.execute('delete from companies where id = ?', (id,))
        self.cursor.execute('delete from clients where company_id = ?', (id,))
