from repository.base_repository import BaseRepository


class ClientRepository(BaseRepository):
    def find_all(self):
        query = 'select clients.id, fullname, email, telephone, companies.name as company_name ' \
                'from clients ' \
                'join companies on company_id = companies.id'
        self.cursor.execute(query)
        return self.get_all()

    def find_by_id(self, id):
        query = 'select clients.id, fullname, email, telephone, companies.name as company_name, companies.address as company_address ' \
                'from clients ' \
                'join companies on company_id = companies.id ' \
                'where clients.id = ?'
        self.cursor.execute(query, (id,))
        return self.get_one()

    def find_clients_by_company_id(self, company_id):
        self.cursor.execute(
            'select id, fullname, email, telephone, company_id from clients where company_id = ?',
            (company_id,)
        )
        return self.get_all()

    def find_client_and_company_by_id(self, id):
        query = 'select id, fullname, email, telephone, name, address ' \
                'from clients ' \
                'join company on client.company_id = company.id where client.id = ?'
        self.cursor.execute(query, (id,))
        return self.get_one()

    def insert_client(self, fullname, email, telephone, company_id):
        self.cursor.execute('insert into clients (fullname, email, telephone, company_id) values (?, ?, ?, ?)',
                            (fullname, email, telephone, company_id))

    def update_client(self, id, fullname, email, telephone):
        self.cursor.execute('update clients set fullname = ?, email = ?, telephone = ? where id = ?',
                            (fullname, email, telephone, id))

    def remove_client(self, id):
        self.cursor.execute('delete from clients where id = ?', (id,))

    def remove_clients_by_company_id(self, company_id):
        self.cursor.execute('delete from clients where company_id = ?', (company_id,))
